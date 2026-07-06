import re
import time
import threading
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

import config
import listing_matcher
import seen_listings
import telegram_notifier


HIGH_TIER_MODELS = [
    "iphone 16",
    "iphone 16 pro",
    "iphone 16 pro max",
    "iphone 17",
    "iphone 17 pro",
    "iphone 17 pro max",
]

CARRIER_PATTERNS = [
    r"\bt-?mobile\b",
    r"\bat&t\b",
    r"\bat and t\b",
    r"\bverizon\b",
    r"\bcricket\b",
    r"\bboost\b",
    r"\bmetro\b",
    r"\bstraight talk\b",
]


def parse_ebay_time(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def is_scam(title):
    t = title.lower()
    return any(kw in t for kw in config.SCAM_KEYWORDS)


def is_unlocked_only_violation(title, model):
    if model not in HIGH_TIER_MODELS:
        return False

    t = title.lower()

    if "unlocked" in t:
        return False

    return any(re.search(pattern, t) for pattern in CARRIER_PATTERNS)


class EbayMonitor:
    def __init__(self):
        self.app_id = config.EBAY_APP_ID
        self.cert_id = config.EBAY_CERT_ID
        self.token = None
        self.token_exp = 0
        self.token_lock = threading.Lock()
        self.session = requests.Session()

    def close(self):
        try:
            self.session.close()
        except Exception:
            pass

    def get_token(self):
        now = datetime.now().timestamp()

        if self.token and now < self.token_exp:
            return self.token

        with self.token_lock:
            now = datetime.now().timestamp()
            if self.token and now < self.token_exp:
                return self.token

            try:
                r = self.session.post(
                    "https://api.ebay.com/identity/v1/oauth2/token",
                    auth=(self.app_id, self.cert_id),
                    data={
                        "grant_type": "client_credentials",
                        "scope": "https://api.ebay.com/oauth/api_scope",
                    },
                    timeout=config.REQUEST_TIMEOUT_SECONDS,
                )

                if r.status_code == 200:
                    data = r.json()
                    self.token = data["access_token"]
                    self.token_exp = now + data["expires_in"] - 90
                    print("[eBay] Token refreshed")
                    return self.token

                print(f"[eBay] Token failed: {r.status_code} {r.text[:200]}")

            except Exception as e:
                print(f"[eBay] Token error: {e}")

        return None

    def search(self, query):
        token = self.get_token()
        if not token:
            return []

        try:
            r = self.session.get(
                "https://api.ebay.com/buy/browse/v1/item_summary/search",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "q": query,
                    "limit": 100,
                    "sort": "newlyListed",
                    "filter": "priceCurrency:USD",
                },
                timeout=config.REQUEST_TIMEOUT_SECONDS,
            )

            if r.status_code == 200:
                return r.json().get("itemSummaries", [])

            if r.status_code == 429:
                print("[eBay] Rate limited. Backing off 10s.")
                time.sleep(10)
                return []

            print(f"[eBay] Search failed for {query}: {r.status_code} {r.text[:200]}")

        except Exception as e:
            print(f"[eBay] Search error for {query}: {e}")

        return []

    def scan_one_model(self, query, seen_dict, tier_label):
        alerts = []
        now = datetime.now(timezone.utc)
        results = self.search(query)

        for item in results:
            try:
                listing_id = item.get("itemId", "")
                title = item.get("title", "")
                price = float(item.get("price", {}).get("value", 0))
                url = item.get("itemWebUrl", "")
                is_auction = "AUCTION" in item.get("buyingOptions", [])

                if not listing_id:
                    continue

                if seen_listings.is_seen(listing_id, seen_dict):
                    continue

                if price < config.MIN_PRICE:
                    seen_listings.mark_seen(listing_id, seen_dict)
                    continue

                # Freshness filter: avoids pinging old listings eBay returns late.
                max_age = getattr(config, "MAX_LISTING_AGE_SECONDS", 0)
                item_creation_date = item.get("itemCreationDate")
                created_time = parse_ebay_time(item_creation_date)
                if max_age and created_time:
                    age_seconds = (now - created_time).total_seconds()
                    if age_seconds > max_age:
                        seen_listings.mark_seen(listing_id, seen_dict)
                        continue

                auction_mins_left = None
                if is_auction:
                    end_time = parse_ebay_time(item.get("itemEndDate") or item.get("auctionEndTime"))
                    if not end_time:
                        continue

                    mins_left = (end_time - now).total_seconds() / 60
                    if mins_left > config.AUCTION_ENDING_ALERT_MINUTES or mins_left < 0:
                        continue

                    auction_mins_left = int(mins_left)

                should_alert, model, threshold = listing_matcher.should_alert(title, price)

                if not should_alert:
                    seen_listings.mark_seen(listing_id, seen_dict)
                    continue

                model_min = config.MODEL_MIN_PRICE.get(model, config.MIN_PRICE)
                if price < model_min:
                    seen_listings.mark_seen(listing_id, seen_dict)
                    continue

                if is_scam(title):
                    seen_listings.mark_seen(listing_id, seen_dict)
                    continue

                if is_unlocked_only_violation(title, model):
                    seen_listings.mark_seen(listing_id, seen_dict)
                    continue

                extra = None
                if is_auction and auction_mins_left is not None:
                    extra = f"🔥 Ending Auction · {auction_mins_left} min left"

                # Alert immediately before extra logging/saving.
                telegram_notifier.send_alert(
                    title=title,
                    price=price,
                    threshold=threshold,
                    source="eBay",
                    url=url,
                    extra_info=extra,
                )

                seen_listings.mark_seen(listing_id, seen_dict)
                alerts.append({"title": title, "price": price, "model": model})

            except Exception as e:
                print(f"[Scan] Item error: {e}")

        print(f"[{tier_label}] Searched {query}: {len(results)} results | {len(alerts)} alerts")
        return alerts

    def scan_models_parallel(self, models, seen_dict, tier_label):
        all_alerts = []
        max_workers = min(len(models), config.MAX_WORKERS)

        if not models:
            return all_alerts

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.scan_one_model, model, seen_dict, f"{tier_label} {model}"): model
                for model in models
            }

            for future in as_completed(futures):
                model = futures[future]
                try:
                    alerts = future.result()
                    all_alerts.extend(alerts)
                except Exception as e:
                    print(f"[Parallel] {model} failed: {e}")

        return all_alerts
