from utils.trend import TrendFilter
from smc.order_block import OrderBlockDetector
from smc.liquidity import LiquiditySweep
from signal_memory import SignalMemory


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.order_block = OrderBlockDetector()
        self.liquidity = LiquiditySweep()
        self.memory = SignalMemory()

    def scan(self, symbol, candles, timeframe="M5"):

        # Detect trend
        trend = self.trend.detect(candles)

        # Detect latest Order Block
        order_block = self.order_block.detect(candles)

        liquidity = None
        signal = "NO SIGNAL"

        if order_block:

            liquidity = self.liquidity.detect(
                candles,
                order_block,
                timeframe
            )

            if liquidity:

                # Prevent duplicate alerts from the same Order Block
                if not self.memory.is_new(
                    symbol,
                    liquidity["order_block_id"]
                ):

                    return {
                        "signal": "NO SIGNAL",
                        "timeframe": timeframe,
                        "trend": trend,
                        "order_block": {
                            "id": order_block.id,
                            "type": order_block.type,
                            "high": order_block.high,
                            "low": order_block.low,
                            "time": order_block.time,
                        },
                        "liquidity": None,
                        "status": "ORDER BLOCK ALREADY ALERTED"
                    }

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
