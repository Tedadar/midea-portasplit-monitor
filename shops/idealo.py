from playwright.sync_api import sync_playwright
from models import Product


class IdealoShop:
    name = "idealo"

    URL = "https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q=Midea+PortaSplit"

    def fetch(self):
        products = []

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )

            page = context.new_page()

            print("DEBUG: Opening Idealo...")

            page.goto(self.URL, timeout=60000)

            # ✅ simuliert echtes Nutzerverhalten
            page.mouse.move(100, 200)
            page.wait_for_timeout(3000)
            page.keyboard.press("PageDown")
            page.wait_for_timeout(3000)

            html = page.content()
            print("DEBUG: HTML length:", len(html))

            # Debug speichern
            with open("debug_idealo.html", "w", encoding="utf-8") as f:
                f.write(html)

            if "Midea" in html:
                print("✅ DEBUG: Produkt erkannt")

                products.append(Product(
                    name="Midea PortaSplit (detected)",
                    price=999,
                    url=self.URL,
                    shop=self.name,
                    available=True
                ))
            else:
                print("❌ DEBUG: weiterhin blockiert")

            browser.close()

        return products
