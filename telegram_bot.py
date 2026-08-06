import os
import requests
from datetime import datetime, UTC


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_signal(result):

    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Telegram credentials missing")
        return False

    liquidity = result.get("liquidity", {})

    message = f"""
🚨 SUPASTAN AI LIQUIDITY SWEEP ALERT

📊 Market: {result.get("symbol")}

⏰ Timeframe: {result.get("timeframe")}

🎯 Signal: {result.get("signal")}

💧 Sweep: {liquidity.get("sweep", "N/A")}

📍 Liquidity Level: {liquidity.get("level", "N/A")}

💰 Current Price: {liquidity.get("price", "N/A")}

📈 Trend: {result.get("trend")}

📌 Status:
{result.get("status")}

🕒 Scan Time:
{datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")}

⚡ Supastan AI Liquidity Scanner
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=10
        )

        if response.status_code == 200:
            print("✅ Telegram alert sent")
            return True

        print("Telegram Error:", response.text)
        return False

    except Exception as e:
        print("Telegram Exception:", e)
        return False
