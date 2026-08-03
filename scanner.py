from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep
from smc.market_structure import MarketStructure


class Scanner:

    def __init__(self):
        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()
        self.market = MarketStructure()


    def scan(self, candles):

        results = []

        trend = self.trend.detect(candles)

        liquidity_signal = self.liquidity.detect(candles)

        if liquidity_signal:
            results.append(liquidity_signal)


        structure_signal = self.market.detect(candles)

        if structure_signal:
            results.append(structure_signal)


        buy = results.count("BUY")
        sell = results.count("SELL")


        score = 0


        if trend == "BULLISH":
            score += 1

        if trend == "BEARISH":
            score -= 1


        score += buy
        score -= sell



        if score >= 2:
            return "BUY"


        if score <= -2:
            return "SELL"


        return "NO TRADE"
