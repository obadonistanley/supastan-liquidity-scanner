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

        bos = None
        choch = None
        signal = None

        # ==========================
        # BULLISH STRUCTURE
        # ==========================

        if current["close"] > previous_high:

            signal = "BUY"

            if bullish_context:
                bos = "BULLISH_BOS"

            if bearish_context:
                choch = "BULLISH_CHOCH"

        # ==========================
        # BEARISH STRUCTURE
        # ==========================

        elif current["close"] < previous_low:

            signal = "SELL"

            if bearish_context:
                bos = "BEARISH_BOS"

            if bullish_context:
                choch = "BEARISH_CHOCH"

        if signal is None:
            return None

        return {

            "signal": signal,

            "bos": bos,

            "choch": choch,

            "previous_high": previous_high,

            "previous_low": previous_low,

            "confirmation": "BODY_CLOSE",

            "market_context": (
                "BULLISH"
                if bullish_context
                else "BEARISH"
            )

        }
