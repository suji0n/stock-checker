import requests
from bs4 import BeautifulSoup
import time
import os

# This looks at the "Key" you just made in Railway
PRODUCT_URL = "https://quack.food/purchase"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
CHECK_INTERVAL = 60

def check_stock():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        page_text = soup.get_text().lower()

        # Logic: If these words are NOT there, it might be in stock
        if "sold out" in page_text or "out of stock" in page_text:
            return False
        return True

    except Exception as e:
        print(f"Error checking site: {e}")
        return False

def send_webhook(message):
    if not WEBHOOK_URL:
        print("ERROR: WEBHOOK_URL variable is missing in Railway!")
        return
        
    data = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Notification sent to Discord!")
    except Exception as e:
        print(f"Webhook error: {e}")

if __name__ == "__main__":
    print("Bot is starting up...")
    
    # TEST RUN: This sends a message immediately so you know it works
    send_webhook("🚀 Stock Checker is now LIVE on Railway!")

    while True:
        if check_stock():
            send_webhook(f"🟢 ITEM MIGHT BE IN STOCK!\n{PRODUCT_URL}")
            # Optional: remove 'break' if you want it to keep messaging you
            break 

        print("Checked: Still out of stock...")
        time.sleep(CHECK_INTERVAL)
