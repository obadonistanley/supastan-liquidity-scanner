import os
import requests


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")



def send_signal(result):


    if not BOT_TOKEN or not CHAT_ID:

        print("Telegram credentials missing")

        return False



    message = f"""
🚨 SUPASTAN AI LIQUIDITY ALERT

📊 Market: {result.get('symbol')}

⏱ Timeframe: {result.get('timeframe')}

🎯 Signal: {result.get('signal')}

Setup:
Wick Liquidity Sweep

Trend:
{result.get('trend')}

Status:
{result.get('status')}
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


        print(

            "Telegram error:",

            e

        )


        return False
