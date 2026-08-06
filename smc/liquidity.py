class LiquiditySweep:


    def __init__(self):
        pass



    def detect(self, candles, timeframe="M5"):


        if len(candles) < 30:
            return None


        timeframe = timeframe.upper()


        # Check latest candle only
        current = candles[-1]


        previous = candles[-21:-1]


        if len(previous) < 10:
            return None



        previous_high = max(
            c["high"] for c in previous
        )


        previous_low = min(
            c["low"] for c in previous
        )



        body = abs(
            current["close"] - current["open"]
        )


        upper_wick = (
            current["high"]
            -
            max(
                current["open"],
                current["close"]
            )
        )


        lower_wick = (
            min(
                current["open"],
                current["close"]
            )
            -
            current["low"]
        )


        # avoid division problems
        if body == 0:
            body = 0.00001



        # SELL liquidity sweep
        if (

            current["high"] > previous_high

            and current["close"] < previous_high

            and upper_wick > body * 1.2

        ):

            return {

                "signal": "SELL",

                "sweep": "WICK",

                "level": previous_high,

                "timeframe": timeframe,

                "price": current["high"],

                "time": current.get("time")

            }



        # BUY liquidity sweep
        if (

            current["low"] < previous_low

            and current["close"] > previous_low

            and lower_wick > body * 1.2

        ):

            return {

                "signal": "BUY",

                "sweep": "WICK",

                "level": previous_low,

                "timeframe": timeframe,

                "price": current["low"],

                "time": current.get("time")

            }



        return None
