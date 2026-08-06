from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()

    def run(self, symbol, timeframe="M5"):

        # Force M5 only for Version 1.1
        timeframe = "M5"

        candles = self.deriv.get_candles(
            symbol=symbol,
            timeframe=timeframe,
            count=200
        )

        if not candles:
            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "signal": "NO DATA",
                "trend": None,
                "order_block": None,
                "liquidity": None,
                "status": "NO DATA",
                "candles": []
            }

        result = self.scanner.scan(
            candles,
            timeframe
        )

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "signal": result.get("signal", "NO SIGNAL"),
            "trend": result.get("trend"),
            "order_block": result.get("order_block"),
            "liquidity": result.get("liquidity"),
            "status": result.get("status"),
            "candles": candles
        }
