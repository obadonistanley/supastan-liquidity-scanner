class MarketStructure:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 6:
            return None

        highs = [c["high"] for c in candles[-6:]]
        lows = [c["low"] for c in candles[-6:]]

        current = candles[-1]

        # Break of Structure (Bullish)
        if current["high"] > max(highs[:-1]):
            return "BUY"

        # Break of Structure (Bearish)
        if current["low"] < min(lows[:-1]):
            return "SELL"

        return None
