import json
import os
from config import HISTORY_FILE, ALERTS_FILE

def _load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def _save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_history():
    return _load_json(HISTORY_FILE)

def save_history(history):
    _save_json(HISTORY_FILE, history)

def load_alerts():
    return _load_json(ALERTS_FILE)

def save_alerts(alerts):
    _save_json(ALERTS_FILE, alerts)

def is_new_alert(product_id):
    alerts = load_alerts()
    return product_id not in alerts

def mark_alert(product_id):
    alerts = load_alerts()
    alerts[product_id] = True
    save_alerts(alerts)

def add_price_history(product):
    history = load_history()
    key = product.url

    if key not in history:
        history[key] = []

    history[key].append({
        "price": product.price,
        "ts": product.timestamp
    })

    save_history(history)
