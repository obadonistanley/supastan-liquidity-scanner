from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):
        self.scanner = Scanner()
        self.deriv = DerivAPI()

    def analyze(self, candles, timeframe="M5"):

        if not candles:
            return {"signal": "NO DATA"}

        return self.scanner.scan(candles, timeframe)

    def get_signal(self, analysis):

        if isinstance(analysis, dict):
            return analysis.get("signal")

        return analysis

    def run(self, symbol, mode):

        if mode == "D1_H4":

            sweep_tf = self.deriv.get_candles(
                symbol=symbol,
                timeframe="D1",
                count=200
            )

            confirmation_tf = self.deriv.get_candles(
                symbol=symbol,
                timeframe="H4",
                count=200
            )

            entry_tf = self.deriv.get_candles(
                symbol=symbol,
                timeframe="M5",
                count=200
            )

            sweep_analysis = self.analyze(sweep_tf, "D1")
            confirmation_analysis = self.analyze(confirmation_tf, "H4")
            entry_analysis = self.analyze(entry_tf, "M5")

        elif mode == "H1":

            sweep_tf = self.deriv.get_candles(
                symbol=symbol,
                timeframe="H1",
                count=200
            )

            entry_tf = self.deriv.get_candles(
                symbol=symbol,
                timeframe="M5",
                count=200
            )

            sweep_analysis = self.analyze(sweep_tf, "H1")
            confirmation_analysis = None
            entry_analysis = self.analyze(entry_tf, "M5")

        elif mode == "M5":

            sweep_tf = self.deriv.get_candles(
                symbol=symbol,
                timeframe="M5",
                count=200
            )

            entry_tf = self.deriv.get_candles(
                symbol=symbol,
                timeframe="M1",
                count=200
            )

            sweep_analysis = self.analyze(sweep_tf, "M5")
            confirmation_analysis = None
            entry_analysis = self.analyze(entry_tf, "M1")

        else:

            return {
                "error": "Choose D1_H4, H1, or M5"
            }

        sweep_signal = self.get_signal(sweep_analysis)
        entry_signal = self.get_signal(entry_analysis)

        if confirmation_analysis:
            confirmation_signal = self.get_signal(confirmation_analysis)
        else:
            confirmation_signal = None

        final_signal = "NO TRADE"

        if mode == "D1_H4":

            if (
                sweep_signal == confirmation_signal ==
                entry_signal and
                sweep_signal in ["BUY", "SELL"]
            ):
                final_signal = sweep_signal

        else:

            if (
                sweep_signal == entry_signal and
                sweep_signal in ["BUY", "SELL"]
            ):
                final_signal = sweep_signal

        return {
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
