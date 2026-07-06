import time
import traceback
import datetime
from datetime import timezone, timedelta

import config
import seen_listings
import telegram_notifier
from ebay_monitor import EbayMonitor

QUIET_START = config.PAUSE_START_HOUR
QUIET_END = config.PAUSE_END_HOUR
TIMEZONE = timezone(timedelta(hours=-4))

last_reset_date = None


def is_quiet_hours():
    now = datetime.datetime.now(TIMEZONE)
    return QUIET_START <= now.hour < QUIET_END


def reset_seen_if_new_day(seen_dict):
    global last_reset_date
    today = datetime.datetime.now(TIMEZONE).date()

    if last_reset_date is None:
        last_reset_date = today

    if today != last_reset_date:
        seen_dict.clear()
        seen_listings.save_seen(seen_dict)
        last_reset_date = today
        print("[Bot] Daily reset — seen listings cleared")
        telegram_notifier.send_status_message(
            "🔄 <b>Daily reset complete.</b> Scanning fresh."
        )


def sleep_until_active():
    now = datetime.datetime.now(TIMEZONE)
    seconds_until_wake = ((QUIET_END - now.hour) * 3600) - (now.minute * 60) - now.second

    if seconds_until_wake <= 0:
        seconds_until_wake += 24 * 3600

    print(f"😴 Quiet hours. Sleeping {seconds_until_wake // 60} min...")
    telegram_notifier.send_daily_summary()
    telegram_notifier.send_status_message(
        "😴 <b>Bot paused for quiet hours</b>\n\nSleeping until <b>10:00 AM ET</b>."
    )
    time.sleep(max(1, seconds_until_wake))
    telegram_notifier.send_status_message("🟢 <b>Bot resumed.</b> Back to scanning.")


def run_loop():
    print("=" * 60)
    print("📱 Finder AI v2 — Fast Parallel Scanner")
    print("=" * 60)
    print(f"HOT every {config.HOT_INTERVAL}s   | {config.HOT_MODELS}")
    print(f"MID every {config.MID_INTERVAL}s   | {config.MID_MODELS}")
    print(f"RARE every {config.RARE_INTERVAL}s | {config.RARE_MODELS}")
    print("=" * 60)

    telegram_notifier.send_status_message(
        "🟢 <b>Finder AI v2 started</b>\n\n"
        "⚡ Parallel scanning enabled\n"
        "🆕 newest listings first"
    )

    seen_dict = seen_listings.load_seen()
    print(f"Loaded {len(seen_dict)} previously-seen listings")

    ebay = EbayMonitor()

    now_ts = time.time()
    next_hot = now_ts
    next_mid = now_ts
    next_rare = now_ts

    try:
        while True:
            if is_quiet_hours():
                sleep_until_active()
                now_ts = time.time()
                next_hot = next_mid = next_rare = now_ts

            reset_seen_if_new_day(seen_dict)

            if not config.EBAY_ENABLED:
                time.sleep(5)
                continue

            now_ts = time.time()

            try:
                if now_ts >= next_hot:
                    ebay.scan_models_parallel(config.HOT_MODELS, seen_dict, "HOT 🔥")
                    next_hot = time.time() + config.HOT_INTERVAL

                if now_ts >= next_mid:
                    ebay.scan_models_parallel(config.MID_MODELS, seen_dict, "MID ⚡")
                    next_mid = time.time() + config.MID_INTERVAL

                if now_ts >= next_rare:
                    ebay.scan_models_parallel(config.RARE_MODELS, seen_dict, "RARE 🐢")
                    next_rare = time.time() + config.RARE_INTERVAL

                seen_listings.save_seen(seen_dict)

            except Exception as e:
                print(f"[Loop] ❌ Error: {e}")
                traceback.print_exc()

            time.sleep(1)

    finally:
        ebay.close()


if __name__ == "__main__":
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN not set!")
        exit(1)

    try:
        run_loop()
    except KeyboardInterrupt:
        print("\n👋 Stopping bot")
        telegram_notifier.send_status_message("🔴 Finder AI v2 stopped.")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        traceback.print_exc()
        try:
            telegram_notifier.send_status_message(
                f"💥 <b>Bot crashed:</b>\n<code>{str(e)[:500]}</code>"
            )
        except Exception:
            pass
        exit(1)
