class LiquiditySweep:

    def detect(self, candles, order_block, timeframe="M5"):

        if not candles or order_block is None:
            return None

        last = candles[-1]

        # ==========================
        # BUY - Bullish Order Block Sweep
        # ==========================
        if order_block.type == "bullish":

            # Wick enters the Order Block
            if (
                last["low"] <= order_block.low
                and last["close"] > order_block.high
            ):

                return {
                    "signal": "BUY",
                    "sweep": "WICK",
                    "price": last["close"],
                    "level": order_block.high,
                    "order_block_id": order_block.id,
                    "timeframe": timeframe,
                    "time": last.get("epoch")
                }

        # ==========================
        # SELL - Bearish Order Block Sweep
        # ==========================
        if order_block.type == "bearish":

            # Wick enters the Order Block
            if (
                last["high"] >= order_block.high
                and last["close"] < order_block.low
            ):

                return {
                    "signal": "SELL",
                    "sweep": "WICK",
                    "price": last["close"],
                    "level": order_block.low,
                    "order_block_id": order_block.id,
                    "timeframe": timeframe,
                    "time": last.get("epoch")
                }

        return None
