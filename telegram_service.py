import os
import requests
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# =========================================================
# VALIDATE CONFIGURATION
# =========================================================

if not BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN is missing from .env"
    )


# =========================================================
# SEND TELEGRAM MESSAGE
# =========================================================

def send_telegram_message(message):
    """
    Send a message to the configured Telegram chat.
    """

    if not CHAT_ID:
        print("⚠️ TELEGRAM_CHAT_ID is not configured.")
        return False


    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )


    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }


    try:

        response = requests.post(
            url,
            json=payload,
            timeout=10
        )


        if response.status_code == 200:

            print("✅ Telegram alert sent.")

            return True


        print(
            "❌ Telegram error:",
            response.text
        )

        return False


    except requests.RequestException as error:

        print(
            "❌ Telegram connection error:",
            error
        )

        return False