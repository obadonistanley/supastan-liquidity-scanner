class OrderBlock:

    def __init__(self):
        pass

    def detect(self, candles, structure):

        if not structure:
            return None

        if len(candles) < 20:
            return None

        signal = structure["signal"]

        # Look back for the last opposite candle
        for i in range(len(candles) - 2, 5, -1):

            candle = candles[i]

            # ==========================
            # BUY ORDER BLOCK
            # Last bearish candle before bullish BOS
            # ==========================
            if signal == "BUY":

                if candle["close"] < candle["open"]:

                    return {

                        "signal": "BUY",
                        "type": "BUY_ORDER_BLOCK",
                        "status": "FRESH",
                        "zone": "BODY",

                        "high": candle["open"],
                        "low": candle["low"],

                        "open": candle["open"],
                        "close": candle["close"],

                        "index": i

                    }

            # ==========================
            # SELL ORDER BLOCK
            # Last bullish candle before bearish BOS
            # ==========================
            if signal == "SELL":

                if candle["close"] > candle["open"]:

                    return {

                        "signal": "SELL",
                        "type": "SELL_ORDER_BLOCK",
                        "status": "FRESH",
                        "zone": "BODY",

                        "high": candle["high"],
                        "low": candle["open"],

                        "open": candle["open"],
                        "close": candle["close"],

                        "index": i

                    }

        return None
