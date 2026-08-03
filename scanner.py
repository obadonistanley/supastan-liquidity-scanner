from utils.trend import TrendFilter
from smc.liquidity import LiquiditySweep


class Scanner:

    def __init__(self):
        self.trend = TrendFilter()
        self.liquidity = LiquiditySweep()

    def scan(self, candles):

        results = []

        trend = self.trend.detect(candles)

        signal = self.liquidity.detect(candles)

        if signal:
            results.append(signal)

        buy = results.count("BUY")
        sell = results.count("SELL")

        if trend == "BULLISH" and buy > sell:
            return "BUY"

        if trend == "BEARISH" and sell > buy:
            return "SELL"

        return "NO TRADE"
