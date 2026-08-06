from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def run(self, symbol, higher_tf, entry_tf):


        # Get higher timeframe candles
        candles = self.deriv.get_candles(
            symbol=symbol,
            timeframe=higher_tf,
            count=200
        )


        if not candles:

            return {

                "symbol": symbol,
                "higher_tf": higher_tf,
                "entry_tf": entry_tf,
                "signal": "NO DATA"

            }


        result = self.scanner.scan(
            candles,
            higher_tf
        )


        if not result["liquidity"]:

            return {

                "symbol": symbol,

                "higher_tf": higher_tf,

                "entry_tf": entry_tf,

                "signal": "NO SWEEP",

                "status": "WAITING"

            }


        return {

            "symbol": symbol,

            "higher_tf": higher_tf,

            "entry_tf": entry_tf,

            "signal": result["signal"],

            "trend": result["trend"],

            "liquidity": result["liquidity"],

            "status": "LIQUIDITY SWEEP DETECTED"

        }
