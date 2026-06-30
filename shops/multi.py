import re
from bs4 import BeautifulSoup
from models import Product
from shops.base import BaseShop


KEYWORDS = [
    "portasplit",
    "porta split",
    "porta-split",
    "midea porta",
    "mobile split klimaanlage"
]


def is_relevant_product(text):
    text = text.lower()
    for keyword in KEYWORDS:
        if keyword in text:
            return True
    return False


class MultiShop(BaseShop):
    name = "multishop"

    URLS = [
        # ✅ Baumärkte
        ("obi", "https://www.obi.de/search/midea%20portasplit/"),
        ("hornbach", "https://www.hornbach.de/suche/midea%20portasplit/"),
        ("bauhaus", "https://www.bauhaus.info/suche/produkte?query=midea%20portasplit"),
        ("toom", "https://toom.de/suche/?searchTerm=midea%20portasplit"),

        # ✅ Elektrofachmärkte
        ("mediamarkt", "https://www.mediamarkt.de/de/search.html?query=midea%20portasplit"),
        ("saturn", "https://www.saturn.de/de/search.html?query=midea%20portasplit"),
        ("expert", "https://www.expert.de/search?query=midea%20portasplit"),

        # ✅ Online-Händler
        ("otto", "https://www.otto.de/suche/midea%20portasplit/"),
        ("alternate", "https://www.alternate.de/listing.xhtml?q=midea+portasplit"),
        ("conrad", "https://www.conrad.de/de/search.html?search=midea%20portasplit"),

        # ✅ Marktplätze
        ("amazon", "https://www.amazon.de/s?k=midea+portasplit"),
        ("ebay", "https://www.ebay.de/sch/i.html?_nkw=midea+portasplit"),
        ("kaufland", "https://www.kaufland.de/suche/?search_value=midea%20portasplit"),

        # ✅ Spezialshops
        ("klimaworld", "https://www.klimaworld.com/search?sSearch=midea+portasplit"),
        ("klivatec", "https://klivatec.de/search?sSearch=midea+portasplit"),
    ]

    # ✅ Browser-Fallback (gegen Bot-Block)
    def fetch_with_browser(self, url):
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                print("DEBUG: Browser loading", url)

                page.goto(url, timeout=30000)
                page.wait_for_timeout(3000)

                html = page.content()
                browser.close()

                return html

        except Exception as e:
            print("DEBUG: Playwright error:", e)
            return None

    def fetch(self):
        products = []

        for shop_name, url in self.URLS:
            print(f"DEBUG: Checking {shop_name}")

            try:
                # ✅ 1. Versuch: normaler Request
                html = self._get(url)

                # ✅ 2. Fallback: Browser wenn blockiert
                if not html or len(html) < 5000:
                    print(f"DEBUG: {shop_name} blocked → using browser")
                    html = self.fetch_with_browser(url)

                # ✅ Wenn weiterhin nichts
                if not html or len(html) < 5000:
                    print(f"DEBUG: {shop_name} still empty")
                    continue

                soup = BeautifulSoup(html, "html.parser")
                text_blocks = soup.get_text(separator=" ")

                matches = re.findall(
                    r"(Midea[^€]{0,120}?(\d{1,4}(?:[.,]\d{3})*[.,]\d{2})\s?€)",
                    text_blocks,
                    re.IGNORECASE
                )

                for match in matches:
                    full_text = match[0]
                    price_raw = match[1]

                    if not is_relevant_product(full_text):
                        continue

                    try:
                        price_clean = price_raw.replace(".", "").replace(",", ".")
                        price = float(price_clean)
                    except:
                        continue

                    print(f"✅ FOUND: {shop_name} - {price}€")

                    products.append(Product(
                        name=full_text[:120],
                        price=price,
                        url=url,
                        shop=shop_name,
                        available=True
                    ))

            except Exception as e:
                print(f"ERROR in {shop_name}: {e}")

        return products
