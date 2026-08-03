import pandas as pd


class TrendFilter:

    def detect(self, candles):

        closes = [c["close"] for c in candles]

        if len(closes) < 200:
            return "UNKNOWN"

        df = pd.DataFrame(closes, columns=["close"])

        ema50 = df["close"].ewm(span=50).mean().iloc[-1]
        ema200 = df["close"].ewm(span=200).mean().iloc[-1]

        if ema50 > ema200:
            return "BULLISH"

        if ema50 < ema200:
            return "BEARISH"

        return "SIDEWAYS"
