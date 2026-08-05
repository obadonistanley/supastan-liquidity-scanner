from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep
from smc.market_structure import MarketStructure
from smc.order_blocks import OrderBlock
from smc.retest import Retest


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()
        self.structure = MarketStructure()
        self.rectangle = OrderBlock()
        self.retest = Retest()

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

                "retest": None,

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

                "retest": None,

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

                "retest": None,

                "confidence": "75%",

                "reason": "Waiting for Fresh Order Block"

            }

        if rectangle["status"] != "FRESH":

            return {

                "signal": "NO TRADE",

                "trend": trend,

                "liquidity": liquidity,

                "structure": structure,

                "rectangle": rectangle,

                "retest": None,

                "confidence": "80%",

                "reason": "Order Block already mitigated"

            }

        retest = self.retest.detect(
            candles,
            rectangle
        )

        if retest is None:

            return {

                "signal": "NO TRADE",

                "trend": trend,

                "liquidity": liquidity,

                "structure": structure,

                "rectangle": rectangle,

                "retest": None,

                "confidence": "90%",

                "reason": "Waiting for Order Block Retest"

            }

        return {

            "signal": rectangle["signal"],

            "trend": trend,

            "liquidity": liquidity,

            "structure": structure,

            "rectangle": rectangle,

            "retest": retest,

            "confidence": "100%",

            "reason": "Liquidity Sweep → BOS / CHOCH → Fresh Order Block → Retest confirmed"

        }
