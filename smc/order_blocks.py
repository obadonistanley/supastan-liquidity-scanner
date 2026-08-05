class OrderBlock:

    def __init__(self):
        pass

    def detect(self, candles, structure):

        if not structure:
            return None

        if len(candles) < 20:
            return None

        signal = structure["signal"]

        # =====================================
        # BUY ORDER BLOCK
        # Last Bearish Candle before BOS
        # =====================================

        if signal == "BUY":

            for i in range(len(candles) - 2, 0, -1):

                candle = candles[i]

                if candle["close"] < candle["open"]:

                    high = candle["high"]
                    low = candle["low"]

                    fresh = True

                    for future in candles[i + 1:]:

                        # Only invalidate if candle BODY closes below the Order Block
                        if future["close"] < low:

                            fresh = False
                            break

                    if fresh:

                        return {

                            "signal": "BUY",

                            "type": "BUY_ORDER_BLOCK",

                            "status": "FRESH",

                            "zone": "ENTIRE_CANDLE",

                            "high": high,

                            "low": low,

                            "open": candle["open"],

                            "close": candle["close"],

                            "index": i

                        }

                    return {

                        "signal": "BUY",

                        "type": "BUY_ORDER_BLOCK",

                        "status": "USED",

                        "zone": "ENTIRE_CANDLE",

                        "high": high,

                        "low": low,

                        "open": candle["open"],

                        "close": candle["close"],

                        "index": i

                    }

        # =====================================
        # SELL ORDER BLOCK
        # Last Bullish Candle before BOS
        # =====================================

        if signal == "SELL":

            for i in range(len(candles) - 2, 0, -1):

                candle = candles[i]

                if candle["close"] > candle["open"]:

                    high = candle["high"]
                    low = candle["low"]

                    fresh = True

                    for future in candles[i + 1:]:

                        # Only invalidate if candle BODY closes above the Order Block
                        if future["close"] > high:

                            fresh = False
                            break

                    if fresh:

                        return {

                            "signal": "SELL",

                            "type": "SELL_ORDER_BLOCK",

                            "status": "FRESH",

                            "zone": "ENTIRE_CANDLE",

                            "high": high,

                            "low": low,

                            "open": candle["open"],

                            "close": candle["close"],

                            "index": i

                        }

                    return {

                        "signal": "SELL",

                        "type": "SELL_ORDER_BLOCK",

                        "status": "USED",

                        "zone": "ENTIRE_CANDLE",

                        "high": high,

                        "low": low,

                        "open": candle["open"],

                        "close": candle["close"],

                        "index": i

                    }

        return None
