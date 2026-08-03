class FairValueGap:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 3:
            return None

        c1 = candles[-3]
        c2 = candles[-2]
        c3 = candles[-1]

        # Bullish FVG
        if c1["high"] < c3["low"]:
            return "BUY"

        # Bearish FVG
        if c1["low"] > c3["high"]:
            return "SELL"

        return None
