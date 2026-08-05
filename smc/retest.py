class Retest:

    def __init__(self):
        pass

    def detect(self, candles, rectangle):

        if rectangle is None:
            return None

        signal = rectangle["signal"]

        high = rectangle["high"]
        low = rectangle["low"]

        ob_index = rectangle["index"]

        # Start checking AFTER the BOS candle
        future = candles[ob_index + 2:]

        if not future:
            return None

        for candle in future:

            if signal == "BUY":

                # Order block invalidated
                if candle["close"] < low:
                    return None

                # First touch of the order block
                if low <= candle["low"] <= high:

                    return {
                        "signal": "BUY",
                        "status": "FIRST_RETEST",
                        "entry": high,
                        "retest_candle": candle
                    }

            elif signal == "SELL":

                # Order block invalidated
                if candle["close"] > high:
                    return None

                # First touch of the order block
                if low <= candle["high"] <= high:

                    return {
                        "signal": "SELL",
                        "status": "FIRST_RETEST",
                        "entry": low,
                        "retest_candle": candle
                    }

        return None
