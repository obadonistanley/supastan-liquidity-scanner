class LiquiditySweep:

    def __init__(self):
        pass

    def detect(self, candles, timeframe="M5"):

        if len(candles) < 30:
            return None

        timeframe = timeframe.upper()

        # Check the last 10 candles
        for i in range(len(candles) - 10, len(candles)):

            current = candles[i]

            recent = candles[max(0, i - 20):i]

            if len(recent) < 20:
                continue

            previous_high = max(c["high"] for c in recent)
            previous_low = min(c["low"] for c in recent)

            candle_body = abs(
                current["close"] - current["open"]
            )

            upper_wick = (
                current["high"] -
                max(current["open"], current["close"])
            )

            lower_wick = (
                min(current["open"], current["close"]) -
                current["low"]
            )

            # ==========================
            # M5 = WICK ONLY
            # ==========================

            if timeframe == "M5":

                if (
                    current["high"] > previous_high
                    and current["close"] < previous_high
                    and upper_wick > candle_body
                ):

                    return {
                        "signal": "SELL",
                        "sweep": "WICK",
                        "level": previous_high,
                        "timeframe": timeframe,
                        "index": i
                    }

                if (
                    current["low"] < previous_low
                    and current["close"] > previous_low
                    and lower_wick > candle_body
                ):

                    return {
                        "signal": "BUY",
                        "sweep": "WICK",
                        "level": previous_low,
                        "timeframe": timeframe,
                        "index": i
                    }

            # ==========================
            # H1 / H4 / D1
            # BODY OR WICK
            # ==========================

            else:

                if current["high"] > previous_high:

                    return {
                        "signal": "SELL",
                        "sweep": "BODY_OR_WICK",
                        "level": previous_high,
                        "timeframe": timeframe,
                        "index": i
                    }

                if current["low"] < previous_low:

                    return {
                        "signal": "BUY",
                        "sweep": "BODY_OR_WICK",
                        "level": previous_low,
                        "timeframe": timeframe,
                        "index": i
                    }

        return None
