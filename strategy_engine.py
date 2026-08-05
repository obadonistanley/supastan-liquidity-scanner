from strategies.d1_h4_strategy import D1H4Strategy
from strategies.h1_strategy import H1Strategy
from strategies.m5_strategy import M5Strategy


class StrategyEngine:

    def __init__(self):

        self.d1_h4 = D1H4Strategy()
        self.h1 = H1Strategy()
        self.m5 = M5Strategy()

    def scan_all(self, symbol):

        return {
            "D1_H4": self.d1_h4.run(symbol),
            "H1": self.h1.run(symbol),
            "M5": self.m5.run(symbol)
        }

    def best_signal(self, symbol):

        results = self.scan_all(symbol)

        priority = [
            results["D1_H4"],
            results["H1"],
            results["M5"]
        ]

        for setup in priority:

            if setup["final_signal"] in ["BUY", "SELL"]:

                return {
                    "symbol": symbol,
                    "overall_signal": setup["final_signal"],
                    "strategy": setup["strategy"],
                    "confidence": setup["confidence"],
                    "entry": setup["entry"],
                    "stop_loss": setup["stop_loss"],
                    "take_profit": setup["take_profit"],
                    "reason": setup["reason"],
                    "strategies": results
                }

        return {
            "symbol": symbol,
            "overall_signal": "NO TRADE",
            "strategies": results
        }
