from scanner import Scanner
from data.deriv import DerivAPI
from telegram_bot import send_telegram


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

        sweep_analysis = self.analyze(sweep_tf)
        entry_analysis = self.analyze(entry_tf)

        if confirmation_tf:
            confirmation_analysis = self.analyze(confirmation_tf)
        else:
            confirmation_analysis = None

        sweep_signal = self.get_signal(sweep_analysis)
        entry_signal = self.get_signal(entry_analysis)
        confirmation_signal = self.get_signal(confirmation_analysis)

        final_signal = "NO TRADE"

        if (
            sweep_signal == "BUY"
            and entry_signal == "BUY"
        ):
            final_signal = "BUY"

        elif (
            sweep_signal == "SELL"
            and entry_signal == "SELL"
        ):
            final_signal = "SELL"

        if mode == "D1_H4":

            if (
                sweep_signal == confirmation_signal
                and confirmation_signal == entry_signal
                and sweep_signal in ["BUY", "SELL"]
            ):
                final_signal = sweep_signal
            else:
                final_signal = "NO TRADE"

        result = {

            "symbol": symbol,

            "mode": mode,

            "final_signal": final_signal,

            "sweep_analysis": sweep_analysis,

            "confirmation_analysis": confirmation_analysis,

            "entry_analysis": entry_analysis,

            "trade_plan": {
                "entry": "SMC Entry Zone",
                "stop_loss": "Below/Above Liquidity Sweep",
                "take_profit": "Minimum 1:3 RR",
                "risk_reward": "1:3+"
            }

        }

        if final_signal != "NO TRADE":
            send_telegram(result)

        return result
