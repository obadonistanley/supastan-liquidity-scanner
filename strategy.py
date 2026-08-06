from scanner import Scanner
from data.deriv import DerivAPI
from telegram_bot import send_signal


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


        signal = result["signal"]


        response = {

            "symbol": symbol,

            "timeframe": timeframe,

            "signal": signal,

            "trend": result["trend"],

            "liquidity": result["liquidity"],

            "status": (

                "LIQUIDITY SWEEP DETECTED"

                if result["liquidity"]

                else

                "WAITING"

            ),

            # Added for Telegram chart generation
            "candles": candles

        }


        # Send Telegram alert only on BUY/SELL sweep

        if signal in ["BUY", "SELL"]:

            send_signal(response)


        return response
