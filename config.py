import os

PRODUCT_KEYWORDS = ["Midea PortaSplit"]
MAX_PRICE = 1500.0
REQUEST_TIMEOUT = 15
RETRY_COUNT = 3

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
]

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

DATA_DIR = "data"
HISTORY_FILE = f"{DATA_DIR}/history.json"
ALERTS_FILE = f"{DATA_DIR}/alerts.json"
