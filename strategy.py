from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def analyze(self, candles, timeframe="M5"):

        if not candles:
            return {
                "signal": "NO DATA"
            }

        return self.scanner.scan(
            candles,
            timeframe
        )


    def get_signal(self, analysis):

        if isinstance(analysis, dict):
            return analysis.get("signal")

        return analysis



    def valid_confirmation(self, analysis):

        if not analysis:
            return False

        return (
            analysis.get("structure")
            and
            analysis.get("rectangle")
            and
            analysis.get("retest")
        )



    def run(self, symbol, mode):


        if mode == "D1_H4":

            d1 = self.deriv.get_candles(
                symbol=symbol,
                timeframe="D1",
                count=200
            )

            h4 = self.deriv.get_candles(
                symbol=symbol,
                timeframe="H4",
                count=200
            )

            m5 = self.deriv.get_candles(
                symbol=symbol,
                timeframe="M5",
                count=200
            )


            sweep_analysis = self.analyze(d1,"D1")

            confirmation_analysis = self.analyze(h4,"H4")

            entry_analysis = self.analyze(m5,"M5")



        elif mode == "H1":

            h1 = self.deriv.get_candles(
                symbol=symbol,
                timeframe="H1",
                count=200
            )

            m5 = self.deriv.get_candles(
                symbol=symbol,
                timeframe="M5",
                count=200
            )


            sweep_analysis = self.analyze(h1,"H1")

            confirmation_analysis = None

            entry_analysis = self.analyze(m5,"M5")



        elif mode == "M5":

            m5 = self.deriv.get_candles(
                symbol=symbol,
                timeframe="M5",
                count=200
            )

            m1 = self.deriv.get_candles(
                symbol=symbol,
                timeframe="M1",
                count=200
            )


            sweep_analysis = self.analyze(m5,"M5")

            confirmation_analysis = None

            entry_analysis = self.analyze(m1,"M1")



        else:

            return {
                "error":"Choose D1_H4, H1, or M5"
            }



        sweep_signal = self.get_signal(
            sweep_analysis
        )


        confirmation_signal = self.get_signal(
            confirmation_analysis
        )


        entry_signal = self.get_signal(
            entry_analysis
        )


        final_signal = "NO TRADE"



        # ==========================
        # D1/H4
        # ==========================

        if mode == "D1_H4":


            if (

                sweep_signal in ["BUY","SELL"]

                and

                confirmation_signal == sweep_signal

                and

                entry_signal == sweep_signal

                and

                self.valid_confirmation(entry_analysis)

            ):

                final_signal = sweep_signal



        # ==========================
        # H1
        # ==========================

        elif mode == "H1":


            if (

                sweep_signal in ["BUY","SELL"]

                and

                entry_signal == sweep_signal

                and

                self.valid_confirmation(entry_analysis)

            ):

                final_signal = sweep_signal



        # ==========================
        # M5
        # ==========================

        elif mode == "M5":


            if (

                sweep_signal in ["BUY","SELL"]

                and

                entry_signal == sweep_signal

                and

                self.valid_confirmation(entry_analysis)

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

                "entry":"Order Block Retest",

                "stop_loss":"Beyond Liquidity Sweep",

                "take_profit":"Minimum 1:3 RR",

                "risk_reward":"1:3+"

            }

        }
