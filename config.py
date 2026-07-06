import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6742644884")

EBAY_ENABLED = os.environ.get("EBAY_ENABLED", "true").lower() == "true"
EBAY_APP_ID = os.environ.get("EBAY_APP_ID", "")
EBAY_CERT_ID = os.environ.get("EBAY_CERT_ID", "")

PRICE_THRESHOLDS = {
    "iphone 14 pro max": 321,
    "iphone 15 pro": 389,
    "iphone 15 pro max": 459,
    "iphone 16": 392,
    "iphone 16 pro": 479,
    "iphone 16 pro max": 620,
    "iphone 17": 575,
    "iphone 17 pro": 837,
    "iphone 17 pro max": 919,
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

EXCLUDE_KEYWORDS = [
    "16e",
    "17e",
    "iphone 16e",
    "iphone 17e",
]

SCAM_KEYWORDS = [
    "check esn", "bad esn", "unknown esn", "esn bad",
    "icloud locked", "icloud lock", "locked to icloud", "activation lock",
    "not paid off", "still financed", "still on contract",
    "blacklisted", "blocked imei", "bad imei",
]

MAX_LISTING_AGE_SECONDS = 300
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
    "iphone 17",
    "iphone 17 pro",
    "iphone 17 pro max",
]

HOT_INTERVAL = 30
MID_INTERVAL = 90
RARE_INTERVAL = 240

MAX_WORKERS = 3
REQUEST_TIMEOUT_SECONDS = 10
RATE_LIMIT_COOLDOWN_SECONDS = 120

SEEN_LISTINGS_FILE = "seen_listings.json"
