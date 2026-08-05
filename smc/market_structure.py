class MarketStructure:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 40:
            return None

        current = candles[-1]

        previous = candles[-2]

        swing = candles[-21:-1]

        previous_high = max(
            c["high"] for c in swing
        )

        previous_low = min(
            c["low"] for c in swing
        )

        body = abs(
            current["close"] - current["open"]
        )

        candle_range = (
            current["high"] - current["low"]
        )

        if candle_range == 0:
            return None

        body_ratio = body / candle_range

        displacement = body_ratio >= 0.60

        # ==========================
        # BULLISH BOS
        # ==========================

        if (

            current["close"] > previous_high

            and

            displacement

        ):

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

        if (

            current["close"] < previous_low

            and

            displacement

        ):

            return {

                "signal": "SELL",

                "bos": "BEARISH_BOS",

                "choch": "BEARISH_CHOCH",

                "previous_high": previous_high,

                "previous_low": previous_low,

                "confirmation": "BODY_CLOSE"

            }

        # ==========================
        # BULLISH CHOCH
        # ==========================

        if (

            previous["close"] < previous["open"]

            and

            current["close"] > previous["high"]

            and

            displacement

        ):

            return {

                "signal": "BUY",

                "bos": "BULLISH_BOS",

                "choch": "BULLISH_CHOCH",

                "previous_high": previous_high,

                "previous_low": previous_low,

                "confirmation": "DISPLACEMENT"

            }

        # ==========================
        # BEARISH CHOCH
        # ==========================

        if (

            previous["close"] > previous["open"]

            and

            current["close"] < previous["low"]

            and

            displacement

        ):

            return {

                "signal": "SELL",

                "bos": "BEARISH_BOS",

                "choch": "BEARISH_CHOCH",

                "previous_high": previous_high,

                "previous_low": previous_low,

                "confirmation": "DISPLACEMENT"

            }

        return None
