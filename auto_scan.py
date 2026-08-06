import time

from config import MARKETS
from strategy import Strategy

scanner = Strategy()

while True:

    print("\n========== NEW SCAN ==========\n")

    for symbol in MARKETS:

        try:

            print(f"Scanning {symbol}...")

            h4 = scanner.run(symbol, "H4")
            h1 = scanner.run(symbol, "H1")
            m5 = scanner.run(symbol, "M5")

            print("H4:", h4)
            print("H1:", h1)
            print("M5:", m5)

        except Exception as e:

            print(symbol, e)

    print("\nWaiting 60 seconds...\n")

    time.sleep(60)
