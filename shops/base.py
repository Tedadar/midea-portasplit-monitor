import requests, random, time
from config import USER_AGENTS, REQUEST_TIMEOUT, RETRY_COUNT

class BaseShop:
    name = "base"

    def fetch(self):
        raise NotImplementedError

    def _get(self, url):
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        for _ in range(RETRY_COUNT):
            try:
                r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                if r.status_code == 200:
                    return r.text
            except Exception:
                pass
            time.sleep(2)
        return None
