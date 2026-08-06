from dataclasses import dataclass


@dataclass
class OrderBlock:
    id: str
    type: str          # "bullish" or "bearish"
    high: float
    low: float
    open: float
    close: float
    time: int


class OrderBlockDetector:

    def detect(self, candles):

        """
        Detect the latest M5 Order Block.

        candles = list of dictionaries:
        {
            "epoch": ...,
            "open": ...,
            "high": ...,
            "low": ...,
            "close": ...
        }
        """

        if len(candles) < 10:
            return None

        # Start from the newest candle and work backwards
        for i in range
