class MarketStructure:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 10:
            return None

        recent = candles[-10:-1]
        current = candles[-1]

        previous_high = max(c["high"] for c in recent)
        previous_low = min(c["low"] for c in recent)

        # Bullish Market Structure Shift
        # Price breaks high and closes above it
        if (
            current["high"] > previous_high
            and current["close"] > previous_high
        ):
            return "BUY"

        # Bearish Market Structure Shift
        # Price breaks low and closes below it
        if (
            current["low"] < previous_low
            and current["close"] < previous_low
        ):
            return "SELL"

        return None
