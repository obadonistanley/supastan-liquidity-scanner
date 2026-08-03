class LiquiditySweep:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 10:
            return None

        recent = candles[-10:-1]
        current = candles[-1]

        previous_high = max(c["high"] for c in recent)
        previous_low = min(c["low"] for c in recent)

        # Buy-side liquidity sweep
        # Price takes highs but rejects and closes lower
        if (
            current["high"] > previous_high
            and current["close"] < previous_high
        ):
            return "SELL"

        # Sell-side liquidity sweep
        # Price takes lows but rejects and closes higher
        if (
            current["low"] < previous_low
            and current["close"] > previous_low
        ):
            return "BUY"

        return None
