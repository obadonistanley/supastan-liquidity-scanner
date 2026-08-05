class MarketStructure:

    def __init__(self):
        pass


    def detect(self, candles):

        if len(candles) < 30:
            return None


        # Last candle
        current = candles[-1]


        # Look for recent structure
        lookback = candles[-15:-1]


        previous_high = max(
            c["high"] for c in lookback
        )

        previous_low = min(
            c["low"] for c in lookback
        )


        # ==========================
        # BULLISH BOS
        # ==========================

        if current["close"] > previous_high:

            return {

                "signal": "BUY",

                "bos": "BULLISH_BOS",

                "choch": "BULLISH_CHOCH",

                "previous_high": previous_high,

                "previous_low": previous_low,

                "confirmation": "BODY_CLOSE"

            }


        # ==========================
        # BEARISH BOS
        # ==========================

        if current["close"] < previous_low:

            return {

                "signal": "SELL",

                "bos": "BEARISH_BOS",

                "choch": "BEARISH_CHOCH",

                "previous_high": previous_high,

                "previous_low": previous_low,

                "confirmation": "BODY_CLOSE"

            }


        # ==========================
        # DISPLACEMENT CHECK
        # ==========================

        last_three = candles[-3:]


        bullish_move = (
            last_three[-1]["close"] >
            last_three[0]["high"]
        )


        bearish_move = (
            last_three[-1]["close"] <
            last_three[0]["low"]
        )


        if bullish_move:

            return {

                "signal":"BUY",

                "bos":"BULLISH_BOS",

                "choch":"BULLISH_CHOCH",

                "confirmation":"DISPLACEMENT"

            }


        if bearish_move:

            return {

                "signal":"SELL",

                "bos":"BEARISH_BOS",

                "choch":"BEARISH_CHOCH",

                "confirmation":"DISPLACEMENT"

            }


        return None
