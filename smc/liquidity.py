class LiquiditySweep:

    def __init__(self):
        pass


    def detect(self, candles):

        if len(candles) < 20:
            return None


        recent = candles[-20:-1]
        current = candles[-1]


        previous_high = max(c["high"] for c in recent)
        previous_low = min(c["low"] for c in recent)


        candle_body = abs(
            current["close"] - current["open"]
        )


        upper_wick = (
            current["high"] - max(
                current["open"],
                current["close"]
            )
        )


        lower_wick = (
            min(
                current["open"],
                current["close"]
            ) - current["low"]
        )


        # BUY SIDE LIQUIDITY SWEEP
        # Price grabs previous highs and rejects

        if (
            current["high"] > previous_high
            and current["close"] < previous_high
            and upper_wick > candle_body
        ):
            return "SELL"



        # SELL SIDE LIQUIDITY SWEEP
        # Price grabs previous lows and rejects

        if (
            current["low"] < previous_low
            and current["close"] > previous_low
            and lower_wick > candle_body
        ):
            return "BUY"


        return None
