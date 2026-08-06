import os
import requests
from datetime import datetime


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_signal(result):

    if not BOT_TOKEN or not CHAT_ID:

        print("Telegram credentials missing")

        return False


    liquidity = result.get("liquidity", {})

    sweep_type = liquidity.get("sweep", "Unknown")
    sweep_level = liquidity.get("level", "Unknown")
    sweep_price = liquidity.get("price", "Unknown")

    scan_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


    message = f"""
🚨 SUPASTAN AI LIQUIDITY ALERT

📊 Market: {result.get("symbol")}

⏱ Timeframe: {result.get("timeframe")}

🎯 Signal: {result.get("signal")}

💧 Sweep Type: {sweep_type}

📍 Sweep Level: {sweep_level}

💰 Sweep Price: {sweep_price}

📈 Trend: {result.get("trend")}

📌 Status:
{result.get("status")}

🕒 Scan Time:
{scan_time}

⚡ Powered by Supastan AI
"""


    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )


    try:

        response = requests.post(

            url,

            data={

                "chat_id": CHAT_ID,

                "text": message

            },

            timeout=10

        )

        return response.status_code == 200


    except Exception as e:

        print("Telegram error:", e)

        return False
