class LiquiditySweep:

    def __init__(self):
        pass

    def detect(self, candles, timeframe="M5"):

        if len(candles) < 30:
            return None

        timeframe = timeframe.upper()

        # Scan only the latest 10 candles
        for i in range(len(candles)-10, len(candles)):

            current = candles[i]

            previous = candles[max(0, i-20):i]

            if len(previous) < 10:
                continue

            previous_high = max(c["high"] for c in previous)
            previous_low = min(c["low"] for c in previous)

            body = abs(current["close"] - current["open"])

            upper_wick = current["high"] - max(
                current["open"],
                current["close"]
            )

            lower_wick = min(
                current["open"],
                current["close"]
            ) - current["low"]

            # SELL Sweep
            if (
                current["high"] > previous_high
                and current["close"] < previous_high
                and upper_wick > body
            ):

                return {

                    "signal": "SELL",

                    "sweep": "WICK",

                    "level": previous_high,

                    "timeframe": timeframe,

                    "price": current["high"],

                    "time": current.get("time"),

                    "index": i

                }

            # BUY Sweep
            if (
                current["low"] < previous_low
                and current["close"] > previous_low
                and lower_wick > body
            ):

                return {

                    "signal": "BUY",

                    "sweep": "WICK",

                    "level": previous_low,

                    "timeframe": timeframe,

                    "price": current["low"],

                    "time": current.get("time"),

                    "index": i

                }

        return None
