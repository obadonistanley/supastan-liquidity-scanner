from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep


class Scanner:


    def __init__(self):

        self.trend = TrendFilter()

        self.liquidity = LiquiditySweep()



    def scan(self, candles, timeframe="M5"):


        trend = self.trend.detect(candles)


        liquidity = self.liquidity.detect(

            candles,

            timeframe

        )


        signal = "NO SWEEP"


        if liquidity:

            signal = liquidity["signal"]



        return {


            "signal": signal,


            "timeframe": timeframe,


            "trend": trend,


            "liquidity": liquidity,


            "status": (

                "LIQUIDITY SWEEP DETECTED"

                if liquidity

                else

                "WAITING"

            )

        }
