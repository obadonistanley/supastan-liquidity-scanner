from scanner import Scanner
from data.deriv import DerivAPI
from telegram_bot import send_signal


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

    def get_signal(self, analysis):

        if isinstance(analysis, dict):
            return analysis.get("signal")

        return analysis

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

           
