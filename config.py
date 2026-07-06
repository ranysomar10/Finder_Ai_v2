import os

# ------------------------
# ENVIRONMENT VARIABLES
# ------------------------
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6742644884")

EBAY_ENABLED = os.environ.get("EBAY_ENABLED", "true").lower() == "true"
EBAY_APP_ID = os.environ.get("EBAY_APP_ID", "")
EBAY_CERT_ID = os.environ.get("EBAY_CERT_ID", "")

# ------------------------
# PRICE THRESHOLDS
# Alert if price <= threshold
# ------------------------
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

# Ignore suspiciously low prices per model
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

# ------------------------
# FILTERS
# ------------------------
EXCLUDE_KEYWORDS = [
    "16e", "17e", "iphone 16e", "iphone 17e",
]

SCAM_KEYWORDS = [
    "check esn", "bad esn", "unknown esn", "esn bad",
    "icloud locked", "icloud lock", "locked to icloud", "activation lock",
    "not paid off", "still financed", "still on contract",
    "blacklisted", "blocked imei", "bad imei",
]

AUCTION_ENDING_ALERT_MINUTES = 15

# Only alert listings that eBay says are newer than this.
# Use 0 to disable age filter.
MAX_LISTING_AGE_SECONDS = 300

# ------------------------
# QUIET HOURS, EASTERN TIME
# ------------------------
PAUSE_START_HOUR = 2
PAUSE_END_HOUR = 10

# ------------------------
# MODEL GROUPS
# Keep hot small so it runs often.
# ------------------------
HOT_MODELS = [
    "iphone 15 pro max",
    "iphone 16 pro max",
]

MID_MODELS = [
    "iphone 14 pro max",
    "iphone 15 pro",
    "iphone 16",
    "iphone 16 pro",
]

RARE_MODELS = [
    "iphone 17",
    "iphone 17 pro",
    "iphone 17 pro max",
]

# ------------------------
# SCAN SPEED
# This stays under 5k/day because quiet hours pause 8 hours.
# HOT: 2 models every 25s = 288 calls/hr
# MID: 4 models every 120s = 120 calls/hr
# RARE: 3 models every 360s = 30 calls/hr
# Total ≈ 438 calls/hr × 16 hrs = 7008 calls, too high if all active.
# Safer default below ≈ 4432 calls over 16 active hrs.
# ------------------------
HOT_INTERVAL = 40
MID_INTERVAL = 180
RARE_INTERVAL = 480

# If you want more aggressive later:
# HOT_INTERVAL = 25
# MID_INTERVAL = 180
# RARE_INTERVAL = 600

REQUEST_TIMEOUT_SECONDS = 8
MAX_WORKERS = 9

SEEN_LISTINGS_FILE = "seen_listings.json"
