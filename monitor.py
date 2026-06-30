import logging
from config import MAX_PRICE
from storage import is_new_alert, mark_alert, add_price_history
from notifier import send_telegram
from shops.multi import MultiShop

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def product_id(product):
    return f"{product.shop}:{product.url}:{product.price}"

def format_message(p):
    return (
        f"🔥 *Deal gefunden!*\n\n"
        f"*{p.name}*\n"
        f"💰 {p.price} €\n"
        f"🏪 {p.shop}\n"
        f"✅ Verfügbar\n\n"
        f"{p.url}"
    )

def process_products(products):
    for p in products:
        add_price_history(p)

        if not p.available:
            continue
        if p.price >= MAX_PRICE:
            continue

        pid = product_id(p)
        if not is_new_alert(pid):
            continue

        logging.info(f"New deal: {p.name} - {p.price}")
        send_telegram(format_message(p))
        mark_alert(pid)

def main():
    shops = [MultiShop()]
    for shop in shops:
        try:
            logging.info(f"Checking {shop.name}")
            products = shop.fetch()
            process_products(products)
        except Exception as e:
            logging.error(f"Error in {shop.name}: {e}")

if __name__ == "__main__":
    main()
