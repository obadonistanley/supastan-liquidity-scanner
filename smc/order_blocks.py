class OrderBlock:

    def __init__(self):
        pass

    def detect(self, candles, structure):

        if not structure:
            return None

        bos_index = structure.get("index")

        if bos_index is None or bos_index < 2:
            return None

        # Search backwards from BOS candle for the last opposite candle
        for i in range(bos_index - 1, max(bos_index - 10, 0), -1):

            candle = candles[i]

            # BUY Order Block = last bearish candle before bullish BOS
            if structure["signal"] == "BUY":

                if candle["close"] < candle["open"]:

                    return {
                        "signal": "BUY",
                        "type": "BUY_ORDER_BLOCK",
                        "status": "FRESH",
                        "zone": "ENTIRE_CANDLE",
                        "high": candle["high"],
                        "low": candle["low"],
                        "open": candle["open"],
                        "close": candle["close"],
                        "index": i
                    }

            # SELL Order Block = last bullish candle before bearish BOS
            else:

                if candle["close"] > candle["open"]:

                    return {
                        "signal": "SELL",
                        "type": "SELL_ORDER_BLOCK",
                        "status": "FRESH",
                        "zone": "ENTIRE_CANDLE",
                        "high": candle["high"],
                        "low": candle["low"],
                        "open": candle["open"],
                        "close": candle["close"],
                        "index": i
                    }

        return None
