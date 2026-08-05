class Retest:

    def __init__(self):
        pass

    def detect(self, candles, rectangle):

        if rectangle is None:
            return None

        signal = rectangle["signal"]

        high = rectangle["high"]
        low = rectangle["low"]

        index = rectangle["index"]

        # Only candles AFTER the Order Block
        future = candles[index + 1:]

        if len(future) == 0:
            return None

        for candle in future:

            # ==========================
            # BUY RETEST
            # ==========================

            if signal == "BUY":

                # Order Block invalidated
                if candle["close"] < low:
                    return None

                # First touch of the zone
                if candle["low"] <= high:

                    return {

                        "signal": "BUY",

                        "status": "FIRST_RETEST",

                        "entry": high,

                        "retest_candle": candle

                    }

            # ==========================
            # SELL RETEST
            # ==========================

            elif signal == "SELL":

                # Order Block invalidated
                if candle["close"] > high:
                    return None

                # First touch of the zone
                if candle["high"] >= low:

                    return {

                        "signal": "SELL",

                        "status": "FIRST_RETEST",

                        "entry": low,

                        "retest_candle": candle

                    }

        return None
