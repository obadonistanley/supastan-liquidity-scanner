from utils.trend import TrendFilter
from smc.order_block import OrderBlockDetector
from smc.liquidity import LiquiditySweep


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.order_block = OrderBlockDetector()
        self.liquidity = LiquiditySweep()

    def scan(self, candles, timeframe="M5"):

        # Detect M5 trend
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

                # BUY only in UPTREND with bullish Order Block
                if (
                    trend == "UPTREND"
                    and order_block.type == "bullish"
                    and liquidity["signal"] == "BUY"
                ):
                    signal = "BUY"

                # SELL only in DOWNTREND with bearish Order Block
                elif (
                    trend == "DOWNTREND"
                    and order_block.type == "bearish"
                    and liquidity["signal"] == "SELL"
                ):
                    signal = "SELL"

                else:
                    liquidity = None

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
                if signal in ("BUY", "SELL")
                else "WAITING"
            )
        }
