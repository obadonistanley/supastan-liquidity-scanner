class LiquiditySweep:

    def __init__(self):
        pass

    def detect(self, candles, timeframe="M5"):

        if len(candles) < 20:
            return None

        recent = candles[-20:-1]
        current = candles[-1]

        previous_high = max(c["high"] for c in recent)
        previous_low = min(c["low"] for c in recent)

        candle_body = abs(current["close"] - current["open"])

        upper_wick = current["high"] - max(
            current["open"],
            current["close"]
        )

        lower_wick = min(
            current["open"],
            current["close"]
        ) - current["low"]

        timeframe = timeframe.upper()

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
                    "timeframe": timeframe
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
                    "timeframe": timeframe
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
                    "timeframe": timeframe
                }

            if current["low"] < previous_low:
                return {
                    "signal": "BUY",
                    "sweep": "BODY_OR_WICK",
                    "level": previous_low,
                    "timeframe": timeframe
                }

        return None
