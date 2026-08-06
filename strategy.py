from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def run(self, symbol, timeframe):

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

            candles,
            timeframe

        )

        return {

            "symbol": symbol,

            "timeframe": timeframe,

            "trend": result["trend"],

            "liquidity": result["liquidity"],

            "signal": (
                result["liquidity"]["signal"]
                if result["liquidity"]
                else "NO SWEEP"
            ),

            "status": (
                "LIQUIDITY SWEEP"
                if result["liquidity"]
                else "WAITING"
            ),

            "confidence": result["confidence"],

            "score": result["score"],

            "quality": result["quality"]

        }
