class OrderBlock:

    def __init__(self):
        pass

    def detect(self, candles, structure):

        if structure is None or len(candles) < 20:
            return None

        signal = structure["signal"]

        # BOS/CHOCH candle
        structure_index = len(candles) - 1

        # Search only the last 10 candles before BOS
        start = max(0, structure_index - 10)

        if signal == "BUY":

            for i in range(structure_index - 1, start - 1, -1):

                candle = candles[i]

                # Last bearish candle
                if candle["close"] < candle["open"]:

                    fresh = True

                    for future in candles[i + 1:]:

                        if future["close"] < candle["low"]:
                            fresh = False
                            break

                    return {
                        "signal": "BUY",
                        "type": "BUY_ORDER_BLOCK",
                        "status": "FRESH" if fresh else "USED",
                        "zone": "ENTIRE_CANDLE",
                        "high": candle["high"],
                        "low": candle["low"],
                        "open": candle["open"],
                        "close": candle["close"],
                        "index": i
                    }

        elif signal == "SELL":

            for i in range(structure_index - 1, start - 1, -1):

                candle = candles[i]

                # Last bullish candle
                if candle["close"] > candle["open"]:

                    fresh = True

                    for future in candles[i + 1:]:

                        if future["close"] > candle["high"]:
                            fresh = False
                            break

                    return {
                        "signal": "SELL",
                        "type": "SELL_ORDER_BLOCK",
                        "status": "FRESH" if fresh else "USED",
                        "zone": "ENTIRE_CANDLE",
                        "high": candle["high"],
                        "low": candle["low"],
                        "open": candle["open"],
                        "close": candle["close"],
                        "index": i
                    }

        return None
