from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):
        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def run(self, symbol, mode):

        if mode == "D1_H4":

            higher_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=86400
            )

            h4_tf = self.deriv.get_candles(
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

            higher_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=3600
            )

            h4_tf = None

            entry_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=300
            )


        elif mode == "M5":

            higher_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=300
            )

            h4_tf = None

            entry_tf = self.deriv.get_candles(
                symbol,
                count=200,
                granularity=60
            )


        else:
            return {
                "error": "Invalid strategy mode"
            }


        sweep_analysis = self.scanner.scan(
            higher_tf
        )


        entry_analysis = self.scanner.scan(
            entry_tf
        )


        return {
            "mode": mode,
            "sweep_timeframe_signal": sweep_analysis,
            "entry_timeframe_signal": entry_analysis
        }
