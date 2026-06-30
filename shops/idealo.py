from bs4 import BeautifulSoup
from models import Product
from shops.base import BaseShop

class IdealoShop(BaseShop):
    name = "idealo"
    SEARCH_URL = "https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q=Midea+PortaSplit"

    def fetch(self):
        html = self._get(self.SEARCH_URL)

        print("DEBUG: HTML length =", len(html) if html else 0)
        
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        products = []
        items = soup.select(".offerList-item")

        print("DEBUG: Items found =", len(items))
        
        for item in items[:3]:
            print("DEBUG ITEM:", item.get_text(strip=True)[:200])


        for item in items:
            try:
                title = item.select_one(".offerList-item-title").get_text(strip=True)
                price_text = item.select_one(".price").get_text(strip=True)
                price = float(price_text.replace("€", "").replace(",", "."))
                link = item.select_one("a")["href"]

                products.append(Product(
                    name=title,
                    price=price,
                    url=f"https://www.idealo.de{link}",
                    shop=self.name,
                    available=True
                ))
            except Exception:
                continue

        return products
