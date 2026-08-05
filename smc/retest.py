class Retest:

    def __init__(self):
        pass


    def detect(self, candles, rectangle):

        if not rectangle:
            return None

        if len(candles) < 5:
            return None


        current = candles[-1]


        zone_high = rectangle.get("high")
        zone_low = rectangle.get("low")
        signal = rectangle.get("signal")


        if zone_high is None or zone_low is None:
            return None


        # ==========================
        # BUY ORDER BLOCK RETEST
        # ==========================

        if signal == "BUY":

            if (
                current["low"] <= zone_high
                and current["low"] >= zone_low
            ):

                return {

                    "signal": "BUY",
                    "status": "FIRST_RETEST",
                    "entry": zone_high,
                    "retest_candle": current

                }


        # ==========================
        # SELL ORDER BLOCK RETEST
        # ==========================

        if signal == "SELL":

            if (
                current["high"] >= zone_low
                and current["high"] <= zone_high
            ):

                return {

                    "signal": "SELL",
                    "status": "FIRST_RETEST",
                    "entry": zone_low,
                    "retest_candle": current

                }


        return None
