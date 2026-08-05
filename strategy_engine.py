from strategies.d1_h4_strategy import D1H4Strategy
from strategies.h1_strategy import H1Strategy
from strategies.m5_strategy import M5Strategy


class StrategyEngine:

    def __init__(self):

        self.d1_h4 = D1H4Strategy()
        self.h1 = H1Strategy()
        self.m5 = M5Strategy()

    def scan_all(self, symbol):

        results = {}

        results["D1_H4"] = self.d1_h4.run(symbol)

        results["H1"] = self.h1.run(symbol)

        results["M5"] = self.m5.run(symbol)

        return results

    def best_signal(self, symbol):

        results = self.scan_all(symbol)

        buy = 0
        sell = 0

        for value in results.values():

            if value["final_signal"] == "BUY":
                buy += 1

            elif value["final_signal"] == "SELL":
                sell += 1

        if buy >= 2:
            overall = "BUY"

        elif sell >= 2:
            overall = "SELL"

        else:
            overall = "NO TRADE"

        return {
            "symbol": symbol,
            "overall_signal": overall,
            "strategies": results
        }
