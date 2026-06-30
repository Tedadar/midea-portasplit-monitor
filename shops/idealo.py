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

            # ✅ WICHTIG: Cookie-Banner akzeptieren
            try:
                page.click('button:has-text("Akzeptieren")', timeout=5000)
                print("DEBUG: Cookie accepted")
            except:
                print("DEBUG: No cookie popup found")

            # ✅ warten bis Inhalt geladen ist
            page.wait_for_timeout(5000)

            html = page.content()
            print("DEBUG: HTML length:", len(html))

            # 👉 Debug: prüfen ob Inhalte da sind
            if "Midea" in html:
                print("DEBUG: Found 'Midea' in HTML")

                products.append(Product(
                    name="Midea PortaSplit (Playwright)",
                    price=999,
                    url=self.URL,
                    shop=self.name,
                    available=True
                ))
            else:
                print("DEBUG: Still no products detected")

            browser.close()

        return products
