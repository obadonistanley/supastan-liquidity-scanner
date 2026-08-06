from utils.trend import TrendFilter

from smc.liquidity import LiquiditySweep
from smc.market_structure import MarketStructure
from smc.order_block import OrderBlock



class Scanner:


    def __init__(self):

        self.trend = TrendFilter()

        self.liquidity = LiquiditySweep()

        self.structure = MarketStructure()

        self.order_block = OrderBlock()



    def scan(self, candles, timeframe="M5"):


        trend = self.trend.detect(candles)



        # Liquidity sweep
        liquidity = self.liquidity.detect(
            candles,
            timeframe
        )



        # Market structure
        structure = self.structure.detect(
            candles
        )



        # Order block
        order_block = self.order_block.detect(
            candles
        )



        signal = "WAITING"



        # BUY CONDITIONS
        if liquidity:

            if liquidity["signal"] == "BUY":

                if structure:

                    if structure.get("direction") == "BULLISH":

                        if order_block:

                            signal = "BUY"



        # SELL CONDITIONS
        if liquidity:

            if liquidity["signal"] == "SELL":

                if structure:

                    if structure.get("direction") == "BEARISH":

                        if order_block:

                            signal = "SELL"



        return {


            "signal": signal,


            "timeframe": timeframe,


            "trend": trend,


            "liquidity": liquidity,


            "structure": structure,


            "order_block": order_block,


            "confidence": self.calculate_confidence(

                liquidity,

                structure,

                order_block

            ),


            "score": self.calculate_score(

                liquidity,

                structure,

                order_block

            ),


            "quality": (

                "A+ SMC SETUP"

                if signal in ["BUY","SELL"]

                else

                "WAITING"

            )


        }



    def calculate_score(
            self,
            liquidity,
            structure,
            order_block
    ):


        score = 0


        if liquidity:
            score += 1


        if structure:
            score += 1


        if order_block:
            score += 1


        return score



    def calculate_confidence(
            self,
            liquidity,
            structure,
            order_block
    ):


        score = self.calculate_score(

            liquidity,

            structure,

            order_block

        )


        if score == 3:
            return "HIGH"


        if score == 2:
            return "MEDIUM"


        return "LOW"
