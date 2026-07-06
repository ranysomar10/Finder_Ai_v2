import requests
import re
import config

cycle_alerts = []


def send_alert(title, price, threshold, source, url, condition=None, extra_info=None):
    sell_estimate = (threshold + 72) / 0.9065
    est_profit = round(sell_estimate * (1 - 0.0935) - price)

    if est_profit >= 150:
        tier = "🔥  E L I T E"
    elif est_profit >= 100:
        tier = "⚡  G R E A T"
    elif est_profit >= 65:
        tier = "✅  G O O D"
    else:
        tier = "📌  F O U N D"

    t_lower = title.lower()
    models = [
        "iphone 17 pro max", "iphone 17 pro", "iphone 17",
        "iphone 16 pro max", "iphone 16 pro", "iphone 16",
        "iphone 15 pro max", "iphone 15 pro", "iphone 14 pro max"
    ]

    detected_model = "iPhone"
    for m in models:
        if m in t_lower:
            detected_model = m.title()
            break

    storage_match = re.search(r"(\d+\s*gb|\d+\s*tb)", t_lower)
    storage = storage_match.group(0).upper().replace(" ", "") if storage_match else ""
    model_line = f"{detected_model}{' ' + storage if storage else ''}"

    if "unlocked" in t_lower:
        carrier_tag = "Unlocked"
    elif "cricket" in t_lower and "locked" in t_lower:
        carrier_tag = "Cricket Locked"
    elif ("t-mobile" in t_lower or "tmobile" in t_lower) and "locked" in t_lower:
        carrier_tag = "T-Mobile Locked"
    elif "at&t" in t_lower and "locked" in t_lower:
        carrier_tag = "AT&T Locked"
    elif "verizon" in t_lower and "locked" in t_lower:
        carrier_tag = "Verizon Locked"
    else:
        carrier_tag = "Carrier Unknown"

    is_priority = "unlocked" in t_lower and est_profit >= 80
    is_ending_auction = extra_info and "Ending Auction" in extra_info

    if is_ending_auction:
        header = "🔥 Ending Auction  ✦  A V U E X A I  ✦"
    elif is_priority:
        header = "⭐ PRIORITY  ✦  A V U E X A I  ✦"
    elif est_profit >= 150:
        header = "🔥 ELITE  ✦  A V U E X A I  ✦"
    elif est_profit >= 100:
        header = "⚡ GREAT  ✦  A V U E X A I  ✦"
    else:
        header = "✦  A V U E X A I  ✦"

    urgency = f"\n⏳  <b>{extra_info}</b>" if extra_info else ""

    message = (
        f"<b>{header}</b>\n"
        f"<b>{model_line}  ·  {carrier_tag}</b>\n"
        f"─────────────────\n\n"
        f"{tier}\n\n"
        f"<b>$ {price:.0f}</b>\n\n"
        f"─────────────────\n"
        f"Max Buy   <code>${threshold:.0f}</code>\n"
        f"Est. Profit   <code>~${est_profit}</code>"
        f"{urgency}\n"
        f"─────────────────\n\n"
        f"<a href=\"{url}\">View on {source}  →</a>"
    )

    cycle_alerts.append({
        "model": model_line,
        "price": price,
        "profit": est_profit,
        "priority": is_priority
    })

    return _send_telegram_message(message)


def send_daily_summary():
    if not cycle_alerts:
        send_status_message("📊 <b>Daily Summary</b>\n\nNo deals found this session.")
        cycle_alerts.clear()
        return

    total = len(cycle_alerts)
    priority_count = sum(1 for a in cycle_alerts if a["priority"])
    best = max(cycle_alerts, key=lambda x: x["profit"])
    avg_profit = round(sum(a["profit"] for a in cycle_alerts) / total)

    message = (
        f"<b>✦  A V U E X A I  ✦</b>\n"
        f"─────────────────\n"
        f"📊  <b>D A I L Y  S U M M A R Y</b>\n\n"
        f"Deals Found   <code>{total}</code>\n"
        f"⭐ Priority    <code>{priority_count}</code>\n"
        f"Avg Profit    <code>~${avg_profit}</code>\n\n"
        f"─────────────────\n"
        f"🏆 Best Deal\n"
        f"<b>{best['model']}</b>\n"
        f"Est. Profit   <code>~${best['profit']}</code>\n"
        f"─────────────────"
    )

    _send_telegram_message(message)
    cycle_alerts.clear()


def send_status_message(text):
    styled = f"<b>✦  A V U E X A I  ✦</b>\n─────────────────\n{text}"
    return _send_telegram_message(styled)


def _send_telegram_message(message):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return True

        print(f"[Telegram] Error: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        print(f"[Telegram] Exception: {e}")
        return False
