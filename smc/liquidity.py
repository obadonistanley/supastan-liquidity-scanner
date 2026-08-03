
class LiquiditySweep:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 5:
            return None

        highs = [c["high"] for c in candles[-5:]]
        lows = [c["low"] for c in candles[-5:]]

        current = candles[-1]

        if current["high"] > max(highs[:-1]):
            return "SELL"

        if current["low"] < min(lows[:-1]):
            return "BUY"

        return None
