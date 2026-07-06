import re
import config


def detect_model(title, description=""):
    text = (title + " " + (description or "")).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = " ".join(text.split())
    text_clean = text.replace(" ", "")

    models_sorted = sorted(
        config.PRICE_THRESHOLDS.keys(),
        key=len,
        reverse=True,
    )

    for model in models_sorted:
        model_clean = model.replace(" ", "")

        if model_clean in text_clean:
            return model

    return None


def is_excluded(title, description=""):
    text = (title + " " + (description or "")).lower()

    for keyword in config.EXCLUDE_KEYWORDS:
        if keyword.lower() in text:
            return True

    return False


def should_alert(title, price, description=""):
    try:
        price_num = float(price)
    except (ValueError, TypeError):
        return False, None, None

    if price_num < config.MIN_PRICE:
        return False, None, None

    model = detect_model(title, description)

    if not model:
        return False, None, None

    if is_excluded(title, description):
        return False, model, None

    threshold = config.PRICE_THRESHOLDS[model]

    if price_num <= threshold:
        return True, model, threshold

    return False, model, threshold


if __name__ == "__main__":
    tests = [
        ("iPhone 16 Pro Max 256GB", 600, True, "iphone 16 pro max"),
        ("iphone16promax unlocked", 600, True, "iphone 16 pro max"),
        ("iPhone 16 Pro 128GB", 400, True, "iphone 16 pro"),
        ("iPhone 16 128GB", 300, True, "iphone 16"),
    ]

    for title, price, expected, expected_model in tests:
        result, model, threshold = should_alert(title, price)
        status = "OK" if result == expected and model == expected_model else "FAIL"
        print(f"{status} '{title}' @ ${price} -> alert={result}, model={model}")