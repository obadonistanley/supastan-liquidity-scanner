from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep
from smc.market_structure import MarketStructure
from smc.order_blocks import OrderBlock


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()
        self.structure = MarketStructure()
        self.rectangle = OrderBlock()

    def scan(self, candles):

        trend = self.trend.detect(candles)

        liquidity = self.liquidity.detect(candles)

        structure = self.structure.detect(candles)

        rectangle = self.rectangle.detect(
            candles,
            structure
        )

        missing = []

        if trend == "SIDEWAYS":
            missing.append("Trend")

        if liquidity is None:
            missing.append("Liquidity Sweep")

        if structure is None:
            missing.append("BOS / CHOCH")

        if rectangle is None:
            missing.append("Entry Rectangle")

        if len(missing) == 0:

            return {

                "signal": rectangle["signal"],

                "trend": trend,

                "liquidity": liquidity,

                "structure": structure,

                "rectangle": rectangle,

                "confidence": "100%",

                "reason": "All confirmations completed."

            }

        return {

            "signal": "NO TRADE",

            "trend": trend,

            "liquidity": liquidity,

            "structure": structure,

            "rectangle": rectangle,

            "confidence": f"{100 - (25 * len(missing))}%",

            "reason": "Waiting for: " + ", ".join(missing)

        }
