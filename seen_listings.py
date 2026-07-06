import json
import os
import config


def load_seen():
    if os.path.exists(config.SEEN_LISTINGS_FILE):
        try:
            with open(config.SEEN_LISTINGS_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {k: True for k in data}
                if isinstance(data, dict):
                    return data
        except Exception:
            return {}
    return {}


def save_seen(seen_dict):
    try:
        with open(config.SEEN_LISTINGS_FILE, "w") as f:
            json.dump(seen_dict, f)
    except Exception:
        pass


def is_seen(listing_id, seen_dict):
    return listing_id in seen_dict


def mark_seen(listing_id, seen_dict):
    if listing_id:
        seen_dict[listing_id] = True
