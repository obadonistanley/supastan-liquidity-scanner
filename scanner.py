from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep
from smc.market_structure import MarketStructure
from smc.order_blocks import OrderBlock


class Scanner:

    def __init__(self):

        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()
        self.market = MarketStructure()
        self.order_block = OrderBlock()



    def scan(self, candles):

        results = []


        trend = self.trend.detect(candles)

        liquidity_signal = self.liquidity.detect(candles)

        structure_signal = self.market.detect(candles)

        order_block_signal = self.order_block.detect(candles)



        if liquidity_signal:
            results.append(liquidity_signal)


        if structure_signal:
            results.append(structure_signal)


        if order_block_signal:
            results.append(order_block_signal)



        buy = results.count("BUY")

        sell = results.count("SELL")



        score = 0



        if trend == "BULLISH":
            score += 1


        if trend == "BEARISH":
            score -= 1



        score += buy

        score -= sell



        if score >= 3:

            signal = "BUY"


        elif score <= -3:

            signal = "SELL"


        else:

            signal = "NO TRADE"



        return {

            "signal": signal,

            "trend": trend,

            "liquidity": liquidity_signal,

            "structure": structure_signal,

            "order_block": order_block_signal,

            "score": score

        }
