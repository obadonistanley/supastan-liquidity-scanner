from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep
from smc.order_blocks import OrderBlock
from smc.fvg import FairValueGap
from smc.market_structure import MarketStructure


class Scanner:

    def __init__(self):
        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()
        self.orderblock = OrderBlock()
        self.fvg = FairValueGap()
        self.market = MarketStructure()

    def scan(self, candles):

        results = []

        trend = self.trend.detect(candles)
        signal = self.liquidity.detect(candles)
        if signal:
            results.append(signal)

        signal = self.orderblock.detect(candles)
        if signal:
            results.append(signal)

        signal = self.fvg.detect(candles)
        if signal:
            results.append(signal)

        signal = self.market.detect(candles)
        if signal:
            results.append(signal)

        buy = results.count("BUY")
sell = results.count("SELL")

if trend == "BULLISH" and buy > sell:
    return "BUY"

if trend == "BEARISH" and sell > buy:
    return "SELL"

return "NO TRADE"
