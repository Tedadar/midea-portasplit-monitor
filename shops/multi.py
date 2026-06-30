import requests
from bs4 import BeautifulSoup
from models import Product

print("DEBUG: FAKE PRODUCT TEST")

products = [
    Product(
        name="Midea PortaSplit TEST",
        price=499,
        url="https://example.com",
        shop="test",
        available=True
    )
]

return products

from shops.base import BaseShop


class MultiShop(BaseShop):
    name = "multishop"

    URLS = [
        ("obi", "https://www.obi.de/search/midea%20portasplit/"),
        ("hornbach", "https://www.hornbach.de/suche/midea%20portasplit/"),
        ("bauhaus", "https://www.bauhaus.info/suche/produkte?query=midea%20portasplit"),
        ("otto", "https://www.otto.de/suche/midea%20portasplit/"),
        ("kaufland", "https://www.kaufland.de/suche/?search_value=midea%20portasplit")
    ]

    def fetch(self):
        products = []

        for shop_name, url in self.URLS:
            try:
                print(f"DEBUG: Checking {shop_name}")
                html = self._get(url)

                if not html:
                    print(f"DEBUG: {shop_name} blocked or empty")
                    continue

                soup = BeautifulSoup(html, "html.parser")

                # Sehr generische Suche (funktioniert überraschend gut)
                items = soup.find_all("a")

                for item in items:
                    text = item.get_text(strip=True)

                    if not text:
                        continue

                    if "midea" in text.lower():
                        price = self.extract_price(text)

                        if price:
                            link = item.get("href")

                            if link and not link.startswith("http"):
                                link = "https://" + shop_name + ".de" + link

                            products.append(Product(
                                name=text[:100],
                                price=price,
                                url=link or url,
                                shop=shop_name,
                                available=True
                            ))

                            print(f"✅ FOUND: {shop_name} - {price}€")

            except Exception as e:
                print(f"ERROR in {shop_name}: {e}")

        return products

    def extract_price(self, text):
        import re

        match = re.search(r"(\\d+[\\.,]\\d{2})", text)
        if match:
            try:
                return float(match.group(1).replace(",", "."))
            except:
                return None
        return None
