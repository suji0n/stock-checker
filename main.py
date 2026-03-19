import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime

# CONFIG
PRODUCT_URL = "https://quack.food/purchase"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
CHECK_INTERVAL = 30  # Increased to 30 seconds for faster alerts

def check_stock():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # We use a timeout to ensure the bot doesn't hang if the site is slow
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        
        # Convert to lowercase to make the check 'case-insensitive'
        content = response.text.lower()

        # TARGET: Only trigger if the specific purchase button text appears
        if "get account now" in content:
            print("🚨 ALERT: 'Get account now' button detected!")
            return True
        
        # LOGGING: Helps you see in Railway that it's working
        if "out of stock" in content:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: Out of Stock")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: Unknown (Page changed?)")
            
        return False

    except Exception as e:
        print(f"Error checking site: {e}")
        return False

def send_webhook(message):
    if not WEBHOOK_URL:
        print("ERROR: No WEBHOOK_URL found in Railway Variables!")
        return
        
    data = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Discord notification sent.")
    except Exception as e:
        print(f"Webhook failed: {e}")

if __name__ == "__main__":
    print("--- Stock Bot Starting ---")
    
    # Startup Confirmation
    send_webhook(f"🚀 **Monitor Active**\nTarget: {PRODUCT_URL}\nCheck Rate: {CHECK_INTERVAL}s")

    while True:
        if check_stock():
            # Bold alert with a direct link for quick clicking
            send_webhook(f"🚨 **PRODUCT AVAILABLE!** 🚨\n'Get account now' button is visible!\nLink: {PRODUCT_URL}")
            
            # The bot stops here so it doesn't spam you. 
            # Delete the 'break' below if you want it to keep alerting every 30s.
            break 

        time.sleep(CHECK_INTERVAL)
