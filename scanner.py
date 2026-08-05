from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep
from smc.market_structure import MarketStructure
from smc.order_blocks import OrderBlock
from smc.retest import Retest
from smc.sequence import SequenceValidator


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()
        self.structure = MarketStructure()
        self.rectangle = OrderBlock()
        self.retest = Retest()
        self.sequence = SequenceValidator()

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

                "sequence": None,

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

                "sequence": None,

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

                "sequence": None,

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

                "sequence": None,

                "confidence": "80%",

                "reason": "Order Block already mitigated"

            }

        retest = self.retest.detect(
            candles,
            rectangle
        )

        sequence = self.sequence.validate(

            liquidity,

            structure,

            rectangle,

            retest

        )

        if not sequence["valid"]:

            return {

                "signal": "NO TRADE",

                "trend": trend,

                "liquidity": liquidity,

                "structure": structure,

                "rectangle": rectangle,

                "retest": retest,

                "sequence": sequence,

                "confidence": "90%",

                "reason": sequence["reason"]

            }

        return {

            "signal": rectangle["signal"],

            "trend": trend,

            "liquidity": liquidity,

            "structure": structure,

            "rectangle": rectangle,

            "retest": retest,

            "sequence": sequence,

            "confidence": "100%",

            "reason": "Liquidity Sweep → BOS / CHOCH → Fresh Order Block → First Retest → ENTRY"

        }
