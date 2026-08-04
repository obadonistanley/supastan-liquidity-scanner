from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):
        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def analyze(self, candles):

        if not candles:
            return {
                "signal": "NO DATA"
            }

        return self.scanner.scan(candles)



    def run(self, symbol, mode):


        if mode == "D1_H4":

            sweep_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=86400
            )

            confirmation_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=14400
            )

            entry_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=300
            )


        elif mode == "H1":

            sweep_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=3600
            )

            confirmation_tf = None

            entry_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=300
            )


        elif mode == "M5":

            sweep_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=300
            )

            confirmation_tf = None

            entry_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=60
            )


        else:

            return {
                "error": "Choose D1_H4, H1, or M5"
            }



        sweep_signal = self.analyze(
            sweep_tf
        )


        if confirmation_tf:

            confirmation_signal = self.analyze(
                confirmation_tf
            )

        else:

            confirmation_signal = None



        entry_signal = self.analyze(
            entry_tf
        )



        return {

            "symbol": symbol,

            "mode": mode,

            "sweep_analysis": sweep_signal,

            "confirmation_analysis": confirmation_signal,

            "entry_analysis": entry_signal

        }
