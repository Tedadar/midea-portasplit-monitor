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
        ("otto", "https://www.otto.de/suche/midea%20portasplit/"),
    ]

    def fetch(self):
        products = []

        for shop_name, url in self.URLS:
            print(f"DEBUG: Checking {shop_name}")

            try:
                html = self._get(url)

                if not html or len(html) < 5000:
                    print(f"DEBUG: {shop_name} blocked or empty")
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

                    # ✅ Keyword-Filter
                    if not is_relevant_product(full_text):
                        continue

                    # ✅ Preis korrekt parsen
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
``
