from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()

    def run(self, symbol, timeframe="M5"):

        candles = self.deriv.get_candles(
            symbol=symbol,
            timeframe=timeframe,
            count=200
        )

        if not candles:
            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "signal": "NO DATA"
            }

        result = self.scanner.scan(
            symbol,
            candles,
            timeframe
        )

        return {

            "symbol": symbol,

            "timeframe": timeframe,

            "signal": result["signal"],

            "trend": result["trend"],

            "order_block": result["order_block"],

            "liquidity": result["liquidity"],

            "status": result["status"],

            "candles": candles
        }
