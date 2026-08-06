from utils.trend import TrendFilter
from smc.order_block import OrderBlockDetector
from smc.liquidity import LiquiditySweep


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.order_block = OrderBlockDetector()
        self.liquidity = LiquiditySweep()

    def scan(self, candles, timeframe="M5"):

        # Detect trend
        trend = self.trend.detect(candles)

        # Detect latest Order Block
        order_block = self.order_block.detect(candles)

        liquidity = None
        signal = "NO SIGNAL"

        # Only check liquidity if an Order Block exists
        if order_block:
            liquidity = self.liquidity.detect(
                candles,
                order_block,
                timeframe
            )

            if liquidity:
                signal = liquidity["signal"]

        return {

            "signal": signal,

            "timeframe": timeframe,

            "trend": trend,

            "order_block": (
                {
                    "id": order_block.id,
                    "type": order_block.type,
                    "high": order_block.high,
                    "low": order_block.low,
                    "time": order_block.time,
                }
                if order_block
                else None
            ),

            "liquidity": liquidity,

            "status": (
                "SIGNAL DETECTED"
                if liquidity
                else "WAITING"
            )
        }
