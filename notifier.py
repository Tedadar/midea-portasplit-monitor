def send_telegram(message: str):
    print("DEBUG TELEGRAM TOKEN:", TELEGRAM_TOKEN)
    print("DEBUG TELEGRAM CHAT ID:", TELEGRAM_CHAT_ID)

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram not configured")
        return

    import requests

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    r = requests.post(url, json=payload)

    print("DEBUG TELEGRAM RESPONSE:", r.text)
