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
        ("obi", "https://www.obi.de/search/midea%20portasplit/"),
        ("hornbach", "https://www.hornbach.de/suche/midea%20portasplit/"),
        ("bauhaus", "https://www.bauhaus.info/suche/produkte?query=midea%20portasplit"),
        ("toom", "https://toom.de/suche/?searchTerm=midea%20portasplit"),

        ("mediamarkt", "https://www.mediamarkt.de/de/search.html?query=midea%20portasplit"),
        ("saturn", "https://www.saturn.de/de/search.html?query=midea%20portasplit"),
        ("expert", "https://www.expert.de/search?query=midea%20portasplit"),

        ("otto", "https://www.otto.de/suche/midea%20portasplit/"),
        ("alternate", "https://www.alternate.de/listing.xhtml?q=midea+portasplit"),
        ("conrad", "https://www.conrad.de/de/search.html?search=midea%20portasplit"),

        ("amazon", "https://www.amazon.de/s?k=midea+portasplit"),
        ("ebay", "https://www.ebay.de/sch/i.html?_nkw=midea+portasplit"),
        ("kaufland", "https://www.kaufland.de/suche/?search_value=midea%20portasplit"),

        ("klimaworld", "https://www.klimaworld.com/search?sSearch=midea+portasplit"),
        ("klivatec", "https://klivatec.de/search?sSearch=midea+portasplit"),
    ]

    # ✅ Playwright Fallback
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

    # ✅ Otto Parser
    def parse_otto(self, html, url):
        results = []
        soup = BeautifulSoup(html, "html.parser")

        items = soup.select("[data-testid='productTile']")

        for item in items:
            try:
                name = item.get_text(" ", strip=True)

                if not is_relevant_product(name):
                    continue

                price_el = item.select_one("[data-testid='price']")
                if not price_el:
                    continue

                price_text = price_el.get_text()
                price_match = re.search(r"(\d+[.,]\d{2})", price_text)
                if not price_match:
                    continue

                price = float(price_match.group(1).replace(",", "."))

                link = item.find("a")
                if link and link.get("href"):
                    product_url = "https://www.otto.de" + link["href"]
                else:
                    product_url = url

                results.append(Product(
                    name=name[:120],
                    price=price,
                    url=product_url,
                    shop="otto",
                    available=True
                ))

            except:
                continue

        return results

    # ✅ MediaMarkt / Saturn Parser
    def parse_mediamarkt(self, html, url, shop):
        results = []
        soup = BeautifulSoup(html, "html.parser")

        items = soup.select(".product-wrapper")

        for item in items:
            try:
                name = item.get_text(" ", strip=True)

                if not is_relevant_product(name):
                    continue

                price_el = item.select_one(".price")
                if not price_el:
                    continue

                price_text = price_el.get_text()
                price_match = re.search(r"(\d+[.,]\d{2})", price_text)
                if not price_match:
                    continue

                price = float(price_match.group(1).replace(",", "."))

                results.append(Product(
                    name=name[:120],
                    price=price,
                    url=url,
                    shop=shop,
                    available=True
                ))

            except:
                continue

        return results

    # ✅ eBay Parser
    def parse_ebay(self, html, url):
        results = []
        soup = BeautifulSoup(html, "html.parser")

        items = soup.select(".s-item")

        for item in items:
            try:
                title = item.select_one(".s-item__title")
                price_el = item.select_one(".s-item__price")

                if not title or not price_el:
                    continue

                name = title.get_text()

                if not is_relevant_product(name):
                    continue

                price_text = price_el.get_text()
                price_match = re.search(r"(\d+[.,]\d{2})", price_text)
                if not price_match:
                    continue

                price = float(price_match.group(1).replace(",", "."))

                link = item.select_one("a")
                product_url = link["href"] if link else url

                results.append(Product(
                    name=name,
                    price=price,
                    url=product_url,
                    shop="ebay",
                    available=True
                ))

            except:
                continue

        return results

    def fetch(self):
        products = []

        for shop_name, url in self.URLS:
            print(f"DEBUG: Checking {shop_name}")

            try:
                html = self._get(url)

                if not html or len(html) < 5000:
                    print(f"DEBUG: {shop_name} blocked → using browser")
                    html = self.fetch_with_browser(url)

                if not html or len(html) < 5000:
                    print(f"DEBUG: {shop_name} still empty")
                    continue

                # ✅ Shop-spezifische Parser
                if shop_name == "otto":
                    products.extend(self.parse_otto(html, url))
                    continue

                if shop_name in ["mediamarkt", "saturn"]:
                    products.extend(self.parse_mediamarkt(html, url, shop_name))
                    continue

                if shop_name == "ebay":
                    products.extend(self.parse_ebay(html, url))
                    continue

                # ✅ Fallback Parser
                soup = BeautifulSoup(html, "html.parser")
                text_blocks = soup.get_text(" ", strip=True)

                matches = re.findall(
                    r"(midea.{0,200}?(\d{2,4}[.,]\d{2})\s?€)",
                    text_blocks.lower()
                )

                for match in matches:
                    full_text = match[0]
                    price_raw = match[1]

                    if "midea" not in full_text:
                        continue

                    if not any(k in full_text for k in ["porta", "split"]):
                        continue

                    try:
                        price = float(price_raw.replace(".", "").replace(",", "."))
                    except:
                        continue

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
