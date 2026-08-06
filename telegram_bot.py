import os
import requests
from datetime import datetime, UTC

from chart import create_chart


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


    try:

        # create chart
        candles = result.get("candles")

        chart_file = None

        if candles:
            chart_file = create_chart(
                candles,
                result
            )


        # send image if available
        if chart_file:

            url = (
                f"https://api.telegram.org/"
                f"bot{BOT_TOKEN}/sendPhoto"
            )


            with open(chart_file, "rb") as image:

                response = requests.post(
                    url,
                    data={
                        "chat_id": CHAT_ID,
                        "caption": message
                    },
                    files={
                        "photo": image
                    },
                    timeout=20
                )


        else:

            url = (
                f"https://api.telegram.org/"
                f"bot{BOT_TOKEN}/sendMessage"
            )


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

        print(
            "Telegram Exception:",
            e
        )

        return False
