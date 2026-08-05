class MarketStructure:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 40:
            return None

        # Look back over recent candles
        for i in range(len(candles) - 2, 15, -1):

            current = candles[i]

            previous = candles[i-15:i]

            previous_high = max(c["high"] for c in previous)
            previous_low = min(c["low"] for c in previous)

            # Bullish BOS
            if current["close"] > previous_high:

                return {
                    "signal": "BUY",
                    "bos": "BULLISH_BOS",
                    "choch": "BULLISH_CHOCH",
                    "previous_high": previous_high,
                    "previous_low": previous_low,
                    "confirmation": "BODY_CLOSE",
                    "index": i
                }

            # Bearish BOS
            if current["close"] < previous_low:

                return {
                    "signal": "SELL",
                    "bos": "BEARISH_BOS",
                    "choch": "BEARISH_CHOCH",
                    "previous_high": previous_high,
                    "previous_low": previous_low,
                    "confirmation": "BODY_CLOSE",
                    "index": i
                }

        # Displacement search
        for i in range(len(candles)-2, 3, -1):

            if candles[i]["close"] > candles[i-2]["high"]:

                return {
                    "signal": "BUY",
                    "bos": "BULLISH_BOS",
                    "choch": "BULLISH_CHOCH",
                    "confirmation": "DISPLACEMENT",
                    "index": i
                }

            if candles[i]["close"] < candles[i-2]["low"]:

                return {
                    "signal": "SELL",
                    "bos": "BEARISH_BOS",
                    "choch": "BEARISH_CHOCH",
                    "confirmation": "DISPLACEMENT",
                    "index": i
                }

        return None
