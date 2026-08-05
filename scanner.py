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

        structure = self.structure.detect(candles)

        rectangle = self.rectangle.detect(
            candles,
            structure
        )

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

        if sequence["valid"]:

            return {

                "signal": sequence["signal"],

                "trend": trend,

                "liquidity": liquidity,

                "structure": structure,

                "rectangle": rectangle,

                "retest": retest,

                "confidence": "100%",

                "reason": sequence["reason"]

            }

        confidence = "25%"

        if liquidity:
            confidence = "40%"

        if liquidity and structure:
            confidence = "60%"

        if liquidity and structure and rectangle:
            confidence = "80%"

        if liquidity and structure and rectangle and retest:
            confidence = "90%"

        return {

            "signal": "NO TRADE",

            "trend": trend,

            "liquidity": liquidity,

            "structure": structure,

            "rectangle": rectangle,

            "retest": retest,

            "confidence": confidence,

            "reason": sequence["reason"]

        }
