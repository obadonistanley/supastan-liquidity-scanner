class OrderBlock:

    def __init__(self):
        pass

    def detect(self, candles, structure):

        if not structure:
            return None

        if len(candles) < 20:
            return None

        signal = structure["signal"]

        # ===========================
        # BUY ORDER BLOCK
        # Last Bearish Candle
        # ===========================

        if signal == "BUY":

            for i in range(len(candles)-2, 0, -1):

                candle = candles[i]

                if candle["close"] < candle["open"]:

                    high = candle["high"]
                    low = candle["low"]

                    # Fresh Order Block Check
                    fresh = True

                    for future in candles[i+1:]:

                        if future["low"] <= high and future["high"] >= low:
                            fresh = False
                            break

                    if fresh:

                        return {
                            "type": "BUY_ORDER_BLOCK",
                            "status": "FRESH",
                            "high": high,
                            "low": low,
                            "open": candle["open"],
                            "close": candle["close"],
                            "index": i
                        }

                    else:

                        return {
                            "type": "BUY_ORDER_BLOCK",
                            "status": "USED",
                            "high": high,
                            "low": low,
                            "open": candle["open"],
                            "close": candle["close"],
                            "index": i
                        }

        # ===========================
        # SELL ORDER BLOCK
        # Last Bullish Candle
        # ===========================

        if signal == "SELL":

            for i in range(len(candles)-2, 0, -1):

                candle = candles[i]

                if candle["close"] > candle["open"]:

                    high = candle["high"]
                    low = candle["low"]

                    # Fresh Order Block Check
                    fresh = True

                    for future in candles[i+1:]:

                        if future["low"] <= high and future["high"] >= low:
                            fresh = False
                            break

                    if fresh:

                        return {
                            "type": "SELL_ORDER_BLOCK",
                            "status": "FRESH",
                            "high": high,
                            "low": low,
                            "open": candle["open"],
                            "close": candle["close"],
                            "index": i
                        }

                    else:

                        return {
                            "type": "SELL_ORDER_BLOCK",
                            "status": "USED",
                            "high": high,
                            "low": low,
                            "open": candle["open"],
                            "close": candle["close"],
                            "index": i
                        }

        return None
