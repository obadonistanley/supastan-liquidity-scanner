import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CHAT_ID = "-1004474177840"


def send_telegram(result):

    message = f"""
🚨 SUPASTAN AI SIGNAL

Symbol: {result['symbol']}
Mode: {result['mode']}

Signal: {result['final_signal']}

Confidence:
{result['entry_analysis']['confidence']}

Entry:
{result['trade_plan']['entry']}

Stop Loss:
{result['trade_plan']['stop_loss']}

Take Profit:
{result['trade_plan']['take_profit']}

Risk Reward:
{result['trade_plan']['risk_reward']}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
