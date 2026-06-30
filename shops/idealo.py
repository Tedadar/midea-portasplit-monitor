from playwright.sync_api import sync_playwright
from models import Product


class IdealoShop:
    name = "idealo"

    URL = "https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q=Midea+PortaSplit"

    def fetch(self):
        products = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("DEBUG: Opening Idealo...")
            page.goto(self.URL, timeout=30000)

            page.wait_for_timeout(5000)

            html = page.content()
            print("DEBUG: HTML length:", len(html))

            # simple detection
            if "Midea" not in html:
                print("DEBUG: No products found in HTML")
                return []

            # EXTREM simpel erstmal:
            products.append(Product(
                name="Midea PortaSplit (detected via Playwright)",
                price=999,  # placeholder
                url=self.URL,
                shop=self.name,
                available=True
            ))

            browser.close()

        return products
