class MarketStructure:

    def __init__(self):
        pass


    def detect(self, candles):

        if len(candles) < 20:
            return None


        recent = candles[-20:-1]

        current = candles[-1]


        previous_high = max(
            c["high"] for c in recent
        )

        previous_low = min(
            c["low"] for c in recent
        )


        # find recent swing points

        last_high = max(
            c["high"] for c in candles[-10:]
        )

        last_low = min(
            c["low"] for c in candles[-10:]
        )


        # ==========================
        # BULLISH BOS / CHOCH
        # ==========================

        if current["close"] > last_high:

            return {

                "signal":"BUY",

                "bos":"BULLISH_BOS",

                "choch":"BULLISH_CHOCH",

                "previous_high":previous_high,

                "previous_low":previous_low,

                "confirmation":"BODY_CLOSE"

            }



        # ==========================
        # BEARISH BOS / CHOCH
        # ==========================

        if current["close"] < last_low:

            return {

                "signal":"SELL",

                "bos":"BEARISH_BOS",

                "choch":"BEARISH_CHOCH",

                "previous_high":previous_high,

                "previous_low":previous_low,

                "confirmation":"BODY_CLOSE"

            }


        return None
