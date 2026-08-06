class TrendFilter:

    def __init__(self):
        pass

    def ema(self, values, period):

        multiplier = 2 / (period + 1)

        ema = values[0]

        for price in values[1:]:
            ema = (price - ema) * multiplier + ema

        return ema

    def detect(self, candles):

        if len(candles) < 200:
            return "SIDEWAYS"

        closes = [c["close"] for c in candles]

        ema50 = self.ema(closes[-100:], 50)

        ema200 = self.ema(closes, 200)

        if ema50 > ema200:
            return "BULLISH"

        if ema50 < ema200:
            return "BEARISH"

        return "SIDEWAYS"
