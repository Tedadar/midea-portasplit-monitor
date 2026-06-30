import requests
from bs4 import BeautifulSoup
from models import Product
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

    def extract_price(self, text):
        import re

        match = re.search(r"(\\d+[\\.,]\\d{2})", text)
        if match:
            try:
                return float(match.group(1).replace(",", "."))
            except:
                return None
        return None
