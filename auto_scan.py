import time

from strategy import Strategy

scanner = Strategy()

symbols = [
    "R_10",
    "R_25",
    "R_50",
    "R_75",
    "R_100",
    "BOOM300",
    "BOOM500",
    "CRASH300",
    "CRASH500",
]

modes = [
    "H4",
    "H1",
    "M5"
]

last_signal = {}

while True:

    for symbol in symbols:

        for mode in modes:

            try:

                result = scanner.run(symbol, mode)

                liquidity = result.get("liquidity")

                if liquidity:

                    key = f"{symbol}_{mode}"

                    current = (
                        liquidity["signal"],
                        liquidity["level"]
                    )

                    if last_signal.get(key) != current:

                        print(
                            f"{symbol} | {mode} | "
                            f"{liquidity['signal']} "
                            f"Liquidity Sweep @ "
                            f"{liquidity['level']}"
                        )

                        last_signal[key] = current

            except Exception as e:

                print(symbol, mode, e)

    time.sleep(10)
