from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep
from smc.market_structure import MarketStructure
from smc.order_blocks import OrderBlock
from smc.retest import Retest
from utils.confidence import Confidence


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()
        self.structure = MarketStructure()
        self.rectangle = OrderBlock()
        self.retest = Retest()
        self.confidence = Confidence()

    def scan(self, candles, timeframe="M5"):

        trend = self.trend.detect(candles)

        liquidity = self.liquidity.detect(
            candles,
            timeframe
        )

        structure = self.structure.detect(candles)

        rectangle = self.rectangle.detect(
            candles,
            structure
        )

        retest = self.retest.detect(
            candles,
            rectangle
        )

        confidence = self.confidence.calculate(
            trend,
            liquidity,
            structure,
            rectangle,
            retest
        )

        signal = "NO TRADE"

        if (
            liquidity
            and structure
            and rectangle
            and retest
        ):

            if (
                liquidity["signal"]
                == structure["signal"]
                == rectangle["signal"]
                == retest["signal"]
            ):
                signal = liquidity["signal"]

        return {

            "signal": signal,

            "trend": trend,

            "liquidity": liquidity,

            "structure": structure,

            "rectangle": rectangle,

            "retest": retest,

            "confidence": confidence["confidence"],

            "score": confidence["score"],

            "quality": confidence["quality"],

            "confirmed": confidence["confirmed"],

            "reason": (
                "Complete SMC confirmation"
                if signal != "NO TRADE"
                else "Waiting for full confirmation"
            )

        }
