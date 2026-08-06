import asyncio

from strategy import Strategy
from config import MARKETS
from signal_memory import SignalMemory
from signals_store import add_signal
from telegram_bot import send_signal

strategy = Strategy()
memory = SignalMemory()


def get_timeframes(symbol):
    return ["M5"]


async def auto_scan():

    while True:

        print("🔎 Supastan AI Auto Scan Running...")

        for symbol in MARKETS:

            try:

                result = strategy.run(symbol, "M5")

                if result and result.get("signal") in ("BUY", "SELL"):

                    order_block = result.get("order_block")

                    if (
                        order_block
                        and memory.is_new(
                            result["symbol"],
                            order_block["id"]
                        )
                    ):

                        add_signal(result)

                        send_signal(result)

                        print("✅ NEW SIGNAL:", result)

                    else:

                        print(
                            "⏭ Duplicate Order Block skipped:",
                            result.get("symbol")
                        )

            except Exception as e:

                print(f"❌ Scan error: {symbol} -> {e}")

        print("⏳ Waiting 30 seconds...")

        await asyncio.sleep(30)
