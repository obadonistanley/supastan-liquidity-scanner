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


        # Calculate recent trend direction

        last_close = recent[-1]["close"]
        first_close = recent[0]["close"]


        bullish_context = last_close > first_close
        bearish_context = last_close < first_close



        # Bullish BOS
        # Price breaks structure and confirms above

        if (
            current["high"] > previous_high
            and current["close"] > previous_high
            and bullish_context
        ):
            return "BUY"



        # Bearish BOS
        # Price breaks structure and confirms below

        if (
            current["low"] < previous_low
            and current["close"] < previous_low
            and bearish_context
        ):
            return "SELL"



        # CHoCH bullish reversal
        # Previous bearish movement but breaks upward

        if (
            bearish_context
            and current["close"] > previous_high
        ):
            return "BUY"



        # CHoCH bearish reversal
        # Previous bullish movement but breaks downward

        if (
            bullish_context
            and current["close"] < previous_low
        ):
            return "SELL"



        return None
