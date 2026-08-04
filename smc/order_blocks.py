class OrderBlock:

    def __init__(self):
        pass


    def detect(self, candles):

        if len(candles) < 10:
            return None


        ob_candle = candles[-2]
        confirmation = candles[-1]


        body = abs(
            ob_candle["close"] - ob_candle["open"]
        )


        candle_range = (
            ob_candle["high"] - ob_candle["low"]
        )


        if candle_range == 0:
            return None



        strength = body / candle_range



        # Ignore weak candles
        if strength < 0.5:
            return None



        # Bullish Order Block
        # Last bearish candle before bullish displacement

        if (
            ob_candle["close"] < ob_candle["open"]
            and confirmation["close"] > ob_candle["high"]
        ):
            return "BUY"



        # Bearish Order Block
        # Last bullish candle before bearish displacement

        if (
            ob_candle["close"] > ob_candle["open"]
            and confirmation["close"] < ob_candle["low"]
        ):
            return "SELL"



        return None
