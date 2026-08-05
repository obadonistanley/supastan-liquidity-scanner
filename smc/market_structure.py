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


        return None
