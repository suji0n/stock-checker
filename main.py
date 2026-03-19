import requests
from bs4 import BeautifulSoup
import time

PRODUCT_URL = "https://quack.food/purchase"
WEBHOOK_URL = "https://discord.com/api/webhooks/1484028170729558190/ArJxKEKIGA_a2tteZWWEhPce2hDezVgfC_f8hPAa-Yd8o0ZmiCqq6tnDBE8lrhgR4KrJ"
CHECK_INTERVAL = 60

def check_stock():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(PRODUCT_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Look for "Sold Out" instead (more reliable)
        page_text = soup.get_text().lower()

        if "sold out" in page_text or "out of stock" in page_text:
            return False
        else:
            return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def send_webhook():
    data = {
        "content": f"🟢 ITEM IN STOCK!\n{PRODUCT_URL}"
    }

    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Webhook sent!")
    except Exception as e:
        print(f"Webhook error: {e}")


if __name__ == "__main__":
    print("Checking stock...")

    while True:
        if check_stock():
            send_webhook()
            break

        print("Still out of stock...")
        time.sleep(CHECK_INTERVAL)