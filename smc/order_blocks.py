class OrderBlock:

    def __init__(self):
        pass

    def detect(self, candles, structure):

        if structure is None:
            return None

        if len(candles) < 20:
            return None

        signal = structure["signal"]

        # BOS / CHOCH candle index
        structure_index = len(candles) - 1

        # ==========================
        # BUY ORDER BLOCK
        # Last bearish candle BEFORE BOS
        # ==========================

        if signal == "BUY":

            for i in range(structure_index - 1, -1, -1):

                candle = candles[i]

                if candle["close"] < candle["open"]:

                    high = candle["high"]
                    low = candle["low"]

                    fresh = True

                    for future in candles[i + 1:]:

                        # Invalidate only if body closes below OB
                        if future["close"] < low:
                            fresh = False
                            break

                    return {

                        "signal": "BUY",

                        "type": "BUY_ORDER_BLOCK",

                        "status": "FRESH" if fresh else "USED",

                        "zone": "ENTIRE_CANDLE",

                        "high": high,

                        "low": low,

                        "open": candle["open"],

                        "close": candle["close"],

                        "index": i

                    }

        # ==========================
        # SELL ORDER BLOCK
        # Last bullish candle BEFORE BOS
        # ==========================

        if signal == "SELL":

            for i in range(structure_index - 1, -1, -1):

                candle = candles[i]

                if candle["close"] > candle["open"]:

                    high = candle["high"]
                    low = candle["low"]

                    fresh = True

                    for future in candles[i + 1:]:

                        # Invalidate only if body closes above OB
                        if future["close"] > high:
                            fresh = False
                            break

                    return {

                        "signal": "SELL",

                        "type": "SELL_ORDER_BLOCK",

                        "status": "FRESH" if fresh else "USED",

                        "zone": "ENTIRE_CANDLE",

                        "high": high,

                        "low": low,

                        "open": candle["open"],

                        "close": candle["close"],

                        "index": i

                    }

        return None
