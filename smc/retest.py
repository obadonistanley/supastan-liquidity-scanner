class Retest:

    def __init__(self):
        pass


    def detect(self, candles, rectangle):

        if not rectangle:
            return None

        if len(candles) < 10:
            return None


        zone_high = rectangle["high"]
        zone_low = rectangle["low"]
        signal = rectangle["signal"]


        # check last 10 candles for OB touch
        recent = candles[-10:]


        for candle in recent:


            # SELL retest
            if signal == "SELL":

                if (
                    candle["high"] >= zone_low
                    and candle["high"] <= zone_high
                ):

                    return {

                        "signal": "SELL",
                        "status": "FIRST_RETEST",
                        "entry": zone_low,
                        "retest_candle": candle

                    }



            # BUY retest
            if signal == "BUY":

                if (
                    candle["low"] <= zone_high
                    and candle["low"] >= zone_low
                ):

                    return {

                        "signal": "BUY",
                        "status": "FIRST_RETEST",
                        "entry": zone_high,
                        "retest_candle": candle

                    }


        return None
