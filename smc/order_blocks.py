class OrderBlock:

    def __init__(self):
        pass

    def detect(self, candles, structure):

        if structure is None:
            return None

        if len(candles) < 15:
            return None

        signal = structure["signal"]

        # ==========================
        # BUY Entry Rectangle
        # Previous swing low before BOS
        # ==========================

        if signal == "BUY":

            shoulder = candles[-6]

            for candle in candles[-10:-1]:

                if candle["low"] < shoulder["low"]:
                    shoulder = candle

            return {
                "type": "ENTRY_RECTANGLE",
                "signal": "BUY",
                "high": shoulder["high"],
                "low": shoulder["low"],
                "entry": (shoulder["high"] + shoulder["low"]) / 2
            }

        # ==========================
        # SELL Entry Rectangle
        # Previous swing high before BOS
        # ==========================

        if signal == "SELL":

            shoulder = candles[-6]

            for candle in candles[-10:-1]:

                if candle["high"] > shoulder["high"]:
                    shoulder = candle

            return {
                "type": "ENTRY_RECTANGLE",
                "signal": "SELL",
                "high": shoulder["high"],
                "low": shoulder["low"],
                "entry": (shoulder["high"] + shoulder["low"]) / 2
            }

        return None
