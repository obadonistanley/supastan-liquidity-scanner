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

        # Check ONLY candles after the Order Block formed
        future = candles[index + 1:]

        if len(future) == 0:
            return None

        for candle in future:

            # ==========================
            # BUY RETEST
            # ==========================

            if signal == "BUY":

                # Price enters OB with wick/body
                if candle["low"] <= high:

                    # Order Block must not be broken
                    if candle["close"] < low:
                        return None

                    return {

                        "signal": "BUY",

                        "status": "FIRST_RETEST",

                        "entry": high

                    }

            # ==========================
            # SELL RETEST
            # ==========================

            if signal == "SELL":

                if candle["high"] >= low:

                    if candle["close"] > high:
                        return None

                    return {

                        "signal": "SELL",

                        "status": "FIRST_RETEST",

                        "entry": low

                    }

        return None
