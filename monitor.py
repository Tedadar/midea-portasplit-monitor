import logging
import traceback

from config import MAX_PRICE
from storage import is_new_alert, mark_alert, add_price_history
from notifier import send_telegram
from shops.multi import MultiShop


# ✅ Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ✅ eindeutig pro Angebot
def product_id(product):
    return f"{product.shop}:{product.url}:{product.price}"


# ✅ Nachricht für echte Deals
def format_message(p):
    return (
        f"🔥 *Deal gefunden!*\n\n"
        f"*{p.name}*\n"
        f"💰 {p.price} €\n"
        f"🏪 {p.shop}\n"
        f"✅ Verfügbar\n\n"
        f"{p.url}"
    )


# ✅ Radar-Nachricht (Preis egal)
def format_radar_message(p):
    return (
        f"📡 *PortaSplit gesichtet!*\n\n"
        f"*{p.name}*\n"
        f"💰 {p.price} €\n"
        f"🏪 {p.shop}\n\n"
        f"{p.url}"
    )


# ✅ Hauptlogik
def process_products(products):
    for p in products:
        try:
            # Verlauf speichern
            add_price_history(p)

            # nur verfügbare Produkte
            if not p.available:
                continue

            pid = product_id(p)

            # doppelte vermeiden
            if not is_new_alert(pid):
                continue

            # ✅ RADAR vs DEAL
            if p.price < MAX_PRICE:
                logging.info(f"🔥 Deal: {p.name} - {p.price} €")
                send_telegram(format_message(p))
            else:
                logging.info(f"📡 Radar: {p.name} - {p.price} €")
                send_telegram(format_radar_message(p))

            # markieren als gemeldet
            mark_alert(pid)

        except Exception as e:
            logging.error(f"Error processing product: {e}")
            traceback.print_exc()


# ✅ MAIN LOOP
def main():
    shops = [
        MultiShop(),
    ]

    for shop in shops:
        try:
            logging.info(f"Checking {shop.name}")
            products = shop.fetch()

            if not products:
                logging.info("No products found")
                continue

            process_products(products)

        except Exception as e:
            logging.error(f"Error in {shop.name}: {e}")
            traceback.print_exc()


# ✅ Startpunkt
if __name__ == "__main__":
    main()
