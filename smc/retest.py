class Retest:

    def __init__(self):
        pass

    def detect(self, candles, rectangle):

        if not rectangle:
            return None

        ob_index = rectangle.get("index")

        if ob_index is None:
            return None

        zone_high = rectangle["high"]
        zone_low = rectangle["low"]
        signal = rectangle["signal"]

        # Only check candles AFTER the order block
        for candle in candles[ob_index + 1:]:

            high = candle["high"]
            low = candle["low"]

            # ==========================
            # SELL RETEST
            # ==========================
            if signal == "SELL":

                if high >= zone_low and low <= zone_high:

                    return {
                        "signal": "SELL",
                        "status": "FIRST_RETEST",
                        "entry": zone_low,
                        "retest_candle": candle
                    }

            # ==========================
            # BUY RETEST
            # ==========================
            if signal == "BUY":

                if low <= zone_high and high >= zone_low:

                    return {
                        "signal": "BUY",
                        "status": "FIRST_RETEST",
                        "entry": zone_high,
                        "retest_candle": candle
                    }

        return None
