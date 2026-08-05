class LiquiditySweep:

    def __init__(self):
        pass

    def detect(self, candles, timeframe="M5"):

        if len(candles) < 30:
            return None

        timeframe = timeframe.upper()

        # Scan from newest candle backwards
        for i in range(len(candles) - 1, 19, -1):

            current = candles[i]
            previous = candles[i-20:i]

            previous_high = max(c["high"] for c in previous)
            previous_low = min(c["low"] for c in previous)

            body = abs(current["close"] - current["open"])

            upper_wick = (
                current["high"] -
                max(current["open"], current["close"])
            )

            lower_wick = (
                min(current["open"], current["close"]) -
                current["low"]
            )

            # -------------------------
            # M1 / M5
            # Wick rejection required
            # -------------------------

            if timeframe in ["M1", "M5"]:

                # SELL liquidity
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
                        "index": i
                    }

                # BUY liquidity
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
                        "index": i
                    }

            # -------------------------
            # H1 / H4 / D1
            # Wick sweep only
            # -------------------------

            else:

                # SELL liquidity
                if (
                    current["high"] > previous_high
                    and current["close"] <= current["high"]
                ):

                    return {
                        "signal": "SELL",
                        "sweep": "WICK",
                        "level": previous_high,
                        "timeframe": timeframe,
                        "index": i
                    }

                # BUY liquidity
                if (
                    current["low"] < previous_low
                    and current["close"] >= current["low"]
                ):

                    return {
                        "signal": "BUY",
                        "sweep": "WICK",
                        "level": previous_low,
                        "timeframe": timeframe,
                        "index": i
                    }

        return None
