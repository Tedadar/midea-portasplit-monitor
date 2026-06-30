import re
from bs4 import BeautifulSoup
from models import Product
from shops.base import BaseShop


# ✅ Flexible Keywords für Schreibvarianten
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
            try:
