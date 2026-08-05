class Retest:

    def __init__(self):
        pass

    def detect(self, candles, rectangle):

        if rectangle is None:
            return None

        current = candles[-1]

        high = rectangle["high"]
        low = rectangle["low"]

        signal = rectangle["signal"]

        # ==========================
        # BUY RETEST
        # ==========================

        if signal == "BUY":

            if current["low"] <= high and current["close"] >= low:

                return {

                    "status": "RETEST_CONFIRMED",

                    "signal": "BUY",

                    "zone": "ORDER_BLOCK"

                }

        # ==========================
        # SELL RETEST
        # ==========================

        if signal == "SELL":

            if current["high"] >= low and current["close"] <= high:

                return {

                    "status": "RETEST_CONFIRMED",

                    "signal": "SELL",

                    "zone": "ORDER_BLOCK"

                }

        return None
