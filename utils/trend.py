import pandas as pd


class TrendFilter:


    def detect(self, candles):

        closes = [
            c["close"] for c in candles
        ]


        if len(closes) < 200:
            return "UNKNOWN"


        df = pd.DataFrame(
            closes,
            columns=["close"]
        )


        ema50 = (
            df["close"]
            .ewm(span=50)
            .mean()
        )


        ema200 = (
            df["close"]
            .ewm(span=200)
            .mean()
        )


        current_price = closes[-1]

        current_ema50 = ema50.iloc[-1]
        current_ema200 = ema200.iloc[-1]


        # Momentum check
        previous_price = closes[-20]



        # Strong bullish trend

        if (
            current_ema50 > current_ema200
            and current_price > current_ema50
            and current_price > previous_price
        ):
            return "BULLISH"



        # Strong bearish trend

        if (
            current_ema50 < current_ema200
            and current_price < current_ema50
            and current_price < previous_price
        ):
            return "BEARISH"



        return "SIDEWAYS"
