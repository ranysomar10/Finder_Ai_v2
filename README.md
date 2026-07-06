# Finder AI v2

Fast eBay deal scanner for Avuex.

## What is different

- Searches each model separately.
- Runs model searches in parallel using threads.
- Uses `sort=newlyListed`.
- Reuses one eBay OAuth token until expiration.
- Reuses one requests session.
- Sends Telegram alerts immediately.

## Railway variables

Set these in Railway:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `EBAY_APP_ID`
- `EBAY_CERT_ID`
- `EBAY_ENABLED=true`

## Run locally

```bash
pip install -r requirements.txt
python main.py
```
