class MarketStructure:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 30:
            return None

        current = candles[-1]
        history = candles[-21:-1]

        swing_high = max(history, key=lambda x: x["high"])
        swing_low = min(history, key=lambda x: x["low"])

        previous_high = swing_high["high"]
        previous_low = swing_low["low"]

        first_close = history[0]["close"]
        last_close = history[-1]["close"]

        bullish_context = last_close > first_close
        bearish_context = last_close < first_close

        signal = None
        bos = None
        choch = None

        # Bullish Break
        if current["close"] > previous_high:

            signal = "BUY"

            if bullish_context:
                bos = "BULLISH_BOS"
            else:
                choch = "BULLISH_CHOCH"

        # Bearish Break
        elif current["close"] < previous_low:

            signal = "SELL"

            if bearish_context:
                bos = "BEARISH_BOS"
            else:
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
                "BULLISH" if bullish_context else "BEARISH"
            )
        }
