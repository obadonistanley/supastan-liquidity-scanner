from scanner import Scanner
from data.deriv import DerivAPI
from telegram import TelegramBot


class Strategy:


    def __init__(self):

        self.scanner = Scanner()

        self.deriv = DerivAPI()

        self.telegram = TelegramBot()



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



        # Send Telegram alert only when sweep is detected
        if signal in ["BUY", "SELL"]:


            message = f"""
🚨 SUPASTAN AI LIQUIDITY ALERT

Market: {symbol}

Timeframe: {timeframe}

Signal: {signal}

Setup:
Wick Liquidity Sweep

Trend:
{result['trend']}
"""


            self.telegram.send(message)



        return {


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

            )

        }
