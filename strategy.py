from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def run(self, symbol, timeframe):

        candles = self.deriv.get_candles(
            symbol,
            timeframe,
            200
        )

        if not candles:

            return {

                "symbol": symbol,

                "error": "No candle data"

            }

        result = self.scanner.scan(
            candles,
            timeframe
        )

        return {

            "symbol": symbol,

            "timeframe": timeframe,

            "trend": result["trend"],

            "signal": result["signal"],

            "liquidity": result["liquidity"],

            "status": result["status"]

        }
