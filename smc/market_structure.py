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

        # Market Context
        first_close = recent[0]["close"]
        last_close = recent[-1]["close"]

        bullish_context = last_close > first_close
        bearish_context = last_close < first_close

        # ==========================
        # BULLISH BOS
        # Body must CLOSE above structure
        # ==========================

        if (
            bullish_context
            and current["close"] > previous_high
        ):
            return {
                "type": "BULLISH_BOS",
                "signal": "BUY",
                "level": previous_high,
                "confirmation": "BODY_CLOSE"
            }

        # ==========================
        # BEARISH BOS
        # Body must CLOSE below structure
        # ==========================

        if (
            bearish_context
            and current["close"] < previous_low
