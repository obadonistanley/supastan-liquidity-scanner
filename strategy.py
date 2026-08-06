from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def run(self, symbol, higher_tf, entry_tf):


        # 1. Get higher timeframe candles
        higher_candles = self.deriv.get_candles(

            symbol=symbol,
            timeframe=higher_tf,
            count=200

        )


        if not higher_candles:

            return {

                "symbol": symbol,
                "higher_tf": higher_tf,
                "entry_tf": entry_tf,
                "signal": "NO DATA"

            }


        # 2. Detect liquidity sweep on higher timeframe
        higher_result = self.scanner.scan(

            higher_candles,
            higher_tf

        )


        liquidity = higher_result.get("liquidity")


        if not liquidity:

            return {

                "symbol": symbol,
                "higher_tf": higher_tf,
                "entry_tf": entry_tf,
                "signal": "WAITING",
                "reason": "No liquidity sweep"

            }



        # 3. Get entry timeframe candles
        entry_candles = self.deriv.get_candles(

            symbol=symbol,
            timeframe=entry_tf,
            count=200

        )


        if not entry_candles:

            return {

                "symbol": symbol,
                "higher_tf": higher_tf,
                "entry_tf": entry_tf,
                "signal": "NO ENTRY DATA"

            }



        # 4. Confirm BOS / CHOCH / Order Block
        entry_result = self.scanner.scan(

            entry_candles,
            entry_tf

        )



        if entry_result.get("signal") not in ["BUY", "SELL"]:

            return {

                "symbol": symbol,
                "higher_tf": higher_tf,
                "entry_tf": entry_tf,
                "signal": "WAITING",
                "reason": "No BOS CHOCH confirmation"

            }



        return {

            "symbol": symbol,

            "higher_tf": higher_tf,

            "entry_tf": entry_tf,

            "liquidity": liquidity,

            "structure": entry_result.get("structure"),

            "order_block": entry_result.get("order_block"),

            "signal": entry_result.get("signal"),

            "confidence": entry_result.get("confidence"),

            "score": entry_result.get("score"),

            "quality": entry_result.get("quality")

        }
