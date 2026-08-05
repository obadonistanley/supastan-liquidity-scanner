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

        # Trend Context
        last_close = recent[-1]["close"]
        first_close = recent[0]["close"]

        bullish_context = last_close > first_close
        bearish_context = last_close < first_close

        # ==========================
        # Bullish BOS
        # ==========================
        if (
            current["high"] > previous_high
            and current["close"] > previous_high
            and bullish_context
        ):
            return {
                "type": "BULLISH_BOS",
                "signal": "BUY",
                "level": previous_high
            }

        # ==========================
        # Bearish BOS
        # ==========================
        if (
            current["low"] < previous_low
            and current["close"] < previous_low
            and bearish_context
        ):
            return {
                "type": "BEARISH_BOS",
                "signal": "SELL",
                "level": previous_low
            }

        # ==========================
        # Bullish CHOCH
        # ==========================
        if (
            bearish_context
            and current["close"] > previous_high
        ):
            return {
                "type": "BULLISH_CHOCH",
                "signal": "BUY",
                "level": previous_high
            }

        # ==========================
        # Bearish CHOCH
        # ==========================
        if (
            bullish_context
            and current["close"] < previous_low
        ):
            return {
                "type": "BEARISH_CHOCH",
                "signal": "SELL",
                "level": previous_low
            }

        return None
