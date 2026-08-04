import time

from strategy import Strategy
from telegram_bot import send_telegram


strategy = Strategy()

SYMBOLS = [
    "R_10",
    "R_25",
    "R_50",
    "R_75",
    "R_100"
]

MODES = [
    "D1_H4",
    "H1",
    "M5"
]


while True:

    for symbol in SYMBOLS:

        for mode in MODES:

            result = strategy.run(symbol, mode)

            if result["final_signal"] != "NO TRADE":

                send_telegram(result)

                print(result)

    time.sleep(60)
