import os
import requests


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_signal(signal):

    if signal.get("final_signal") == "NO TRADE":
        return

    message = f"""
🚨 SUPASTAN AI LIQUIDITY SCANNER

📊 Symbol: {signal['symbol']}
📈 Strategy: {signal['mode']}

✅ Signal: {signal['final_signal']}

Entry:
{signal.get('trade_plan', {}).get('entry', 'N/A')}

Stop Loss:
{signal.get('trade_plan', {}).get('stop_loss', 'N/A')}

Take Profit:
{signal.get('trade_plan', {}).get('take_profit', 'N/A')}

Risk Reward:
{signal.get('trade_plan', {}).get('risk_reward', '1:3+')}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
