from strategy import Strategy


class StrategyEngine:

    def __init__(self):
        self.strategy = Strategy()

    def scan_all(self, symbol):

        results = {}

        # Strategy 1
        results["D1_H4"] = self.strategy.run(
            symbol,
            "D1_H4"
        )

        # Strategy 2
        results["H1"] = self.strategy.run(
            symbol,
            "H1"
        )

        # Strategy 3
        results["M5"] = self.strategy.run(
            symbol,
            "M5"
        )

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

        if buy > sell:
            overall = "BUY"

        elif sell > buy:
            overall = "SELL"

        else:
            overall = "NO TRADE"

        return {
            "symbol": symbol,
            "overall_signal": overall,
            "strategies": results
        }
