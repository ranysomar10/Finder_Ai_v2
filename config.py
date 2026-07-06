import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6742644884")

EBAY_ENABLED = os.environ.get("EBAY_ENABLED", "true").lower() == "true"
EBAY_APP_ID = os.environ.get("EBAY_APP_ID", "")
EBAY_CERT_ID = os.environ.get("EBAY_CERT_ID", "")

PRICE_THRESHOLDS = {
    "iphone 14 pro max": 999,
    "iphone 15 pro": 389,
    "iphone 15 pro max": 999,
    "iphone 16": 392,
    "iphone 16 pro": 479,
    "iphone 16 pro max": 999,
    "iphone 17": 575,
    "iphone 17 pro": 999,
    "iphone 17 pro max": 1400,
}

MODEL_MIN_PRICE = {
    "iphone 14 pro max": 100,
    "iphone 15 pro": 110,
    "iphone 15 pro max": 130,
    "iphone 16": 120,
    "iphone 16 pro": 150,
    "iphone 16 pro max": 170,
    "iphone 17": 170,
    "iphone 17 pro": 300,
    "iphone 17 pro max": 350,
}

MIN_PRICE = 75

EXCLUDE_KEYWORDS = ["16e", "17e", "iphone 16e", "iphone 17e"]

SCAM_KEYWORDS = [
    "check esn", "bad esn", "unknown esn", "esn bad",
    "icloud locked", "icloud lock", "locked to icloud", "activation lock",
    "not paid off", "still financed", "still on contract",
    "blacklisted", "blocked imei", "bad imei",
]

MAX_LISTING_AGE_SECONDS = 240
AUCTION_ENDING_ALERT_MINUTES = 15

PAUSE_START_HOUR = 2
PAUSE_END_HOUR = 10

HOT_MODELS = [
    "iphone 14 pro max",
    "iphone 15 pro max",
    "iphone 16 pro max",
]

MID_MODELS = [
    "iphone 15 pro",
    "iphone 16",
    "iphone 16 pro",
]

RARE_MODELS = [
    "iphone 17 pro max",
    "iphone 17 pro",
    "iphone 17",
]

HOT_INTERVAL = 20
MID_INTERVAL = 60
RARE_INTERVAL = 180

MAX_WORKERS = 3
REQUEST_TIMEOUT_SECONDS = 10

SEEN_LISTINGS_FILE = "seen_listings.json"
