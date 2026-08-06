from dataclasses import dataclass


@dataclass
class OrderBlock:
    id: str
    type: str          # bullish or bearish
    high: float
    low: float
    open: float
    close: float
    time: int


class OrderBlockDetector:

    def detect(self, candles):

        if len(candles) < 10:
            return None

        # Search from newest candle backwards
        for i in range(len(candles) - 2, 1, -1):

            current = candles[i]
            next_candle = candles[i + 1]

            # -------------------------
            # Bullish Order Block
            # Last bearish candle before bullish move
            # -------------------------
            if (
                current["close"] < current["open"]
                and next_candle["close"] > next_candle["open"]
            ):

                return OrderBlock(
                    id=f"BULL_{current['epoch']}",
                    type="bullish",
                    high=current["high"],
                    low=current["low"],
                    open=current["open"],
                    close=current["close"],
                    time=current["epoch"]
                )

            # -------------------------
            # Bearish Order Block
            # Last bullish candle before bearish move
            # -------------------------
            if (
                current["close"] > current["open"]
                and next_candle["close"] < next_candle["open"]
            ):

                return OrderBlock(
                    id=f"BEAR_{current['epoch']}",
                    type="bearish",
                    high=current["high"],
                    low=current["low"],
                    open=current["open"],
                    close=current["close"],
                    time=current["epoch"]
                )

        return None
