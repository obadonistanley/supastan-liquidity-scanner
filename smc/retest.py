class Retest:

    def __init__(self):
        pass


    def detect(self, candles, rectangle):

        if not rectangle:
            return None

        if len(candles) < 5:
            return None


        zone_high = rectangle["high"]
        zone_low = rectangle["low"]
        signal = rectangle["signal"]


        recent = candles[-5:]


        for candle in recent:


            candle_high = candle["high"]
            candle_low = candle["low"]


            # =====================
            # SELL ORDER BLOCK RETEST
            # =====================

            if signal == "SELL":

                if (
                    candle_high >= zone_low
                    and candle_low <= zone_high
                ):

                    return {

                        "signal": "SELL",
                        "status": "FIRST_RETEST",
                        "entry": zone_low,
                        "retest_candle": candle

                    }



            # =====================
            # BUY ORDER BLOCK RETEST
            # =====================

            if signal == "BUY":

                if (
                    candle_low <= zone_high
                    and candle_high >= zone_low
                ):

                    return {

                        "signal": "BUY",
                        "status": "FIRST_RETEST",
                        "entry": zone_high,
                        "retest_candle": candle

                    }


        return None
