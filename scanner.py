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

        if liquidity is None:

            return {

                "signal": "NO TRADE",

                "trend": trend,

                "liquidity": None,

                "structure": None,

                "rectangle": None,

                "confidence": "25%",

                "reason": "Waiting for Liquidity Sweep"

            }

        structure = self.structure.detect(candles)

        if structure is None:

            return {

                "signal": "NO TRADE",

                "trend": trend,

                "liquidity": liquidity,

                "structure": None,

                "rectangle": None,

                "confidence": "50%",

                "reason": "Liquidity Sweep found. Waiting for BOS / CHOCH"

            }

        rectangle = self.rectangle.detect(
            candles,
            structure
        )

        if rectangle is None:

            return {

                "signal": "NO TRADE",

                "trend": trend,

                "liquidity": liquidity,

                "structure": structure,

                "rectangle": None,

                "confidence": "75%",

                "reason": "Waiting for fresh Order Block retest"

            }

        return {

            "signal": rectangle["signal"],

            "trend": trend,

            "liquidity": liquidity,

            "structure": structure,

            "rectangle": rectangle,

            "confidence": "100%",

            "reason": "Liquidity Sweep → BOS → CHOCH → Fresh Order Block → Retest confirmed"

        }
