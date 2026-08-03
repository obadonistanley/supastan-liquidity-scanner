class OrderBlock:

    def __init__(self):
        pass

    def detect(self, candles):

        if len(candles) < 4:
            return None

        last = candles[-1]
        prev = candles[-2]

        # Bullish Order Block
        if prev["close"] < prev["open"] and last["close"] > prev["high"]:
            return "BUY"

        # Bearish Order Block
        if prev["close"] > prev["open"] and last["close"] < prev["low"]:
            return "SELL"

        return None
