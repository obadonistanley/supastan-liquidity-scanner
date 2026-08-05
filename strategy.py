from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def analyze(self, candles, timeframe):

        if not candles:
            return {
                "signal": "NO DATA"
            }

        return self.scanner.scan(
            candles,
            timeframe
        )


    def get_liquidity_signal(self, analysis):

        if analysis and analysis.get("liquidity"):

            return analysis["liquidity"].get("signal")

        return None


    def get_signal(self, analysis):

        if analysis:

            return analysis.get("signal")

        return None



    def run(self, symbol, mode):


        if mode == "D1_H4":

            d1 = self.deriv.get_candles(
                symbol,
                "D1",
                200
            )

            h4 = self.deriv.get_candles(
                symbol,
                "H4",
                200
            )

            m5 = self.deriv.get_candles(
                symbol,
                "M5",
                200
            )


            sweep_analysis = self.analyze(
                d1,
                "D1"
            )

            confirmation_analysis = self.analyze(
                h4,
                "H4"
            )

            entry_analysis = self.analyze(
                m5,
                "M5"
            )


        elif mode == "H1":

            h1 = self.deriv.get_candles(
                symbol,
                "H1",
                200
            )

            m5 = self.deriv.get_candles(
                symbol,
                "M5",
                200
            )


            sweep_analysis = self.analyze(
                h1,
                "H1"
            )

            confirmation_analysis = None

            entry_analysis = self.analyze(
                m5,
                "M5"
            )


        elif mode == "M5":

            m5 = self.deriv.get_candles(
                symbol,
                "M5",
                200
            )

            m1 = self.deriv.get_candles(
                symbol,
                "M1",
                200
            )


            sweep_analysis = self.analyze(
                m5,
                "M5"
            )

            confirmation_analysis = None

            entry_analysis = self.analyze(
                m1,
                "M1"
            )


        else:

            return {
                "error": "Invalid mode"
            }



        final_signal = "NO TRADE"



        # ===============================
        # D1/H4 LIQUIDITY → M5 EXECUTION
        # ===============================

        if mode == "D1_H4":


            d1_liq = self.get_liquidity_signal(
                sweep_analysis
            )

            h4_liq = self.get_liquidity_signal(
                confirmation_analysis
            )


            if (

                d1_liq == h4_liq

                and

                d1_liq in ["BUY","SELL"]

                and

                entry_analysis.get("structure")

                and

                entry_analysis["structure"]["signal"] == d1_liq

                and

                entry_analysis.get("rectangle")

                and

                entry_analysis["rectangle"]["signal"] == d1_liq

                and

                entry_analysis.get("retest")

                and

                entry_analysis["retest"]["signal"] == d1_liq

            ):

                final_signal = d1_liq



        # ===============================
        # H1 LIQUIDITY → M5 EXECUTION
        # ===============================

        elif mode == "H1":


            h1_liq = self.get_liquidity_signal(
                sweep_analysis
            )


            if (

                h1_liq in ["BUY","SELL"]

                and

                entry_analysis.get("structure")

                and

                entry_analysis["structure"]["signal"] == h1_liq

                and

                entry_analysis.get("rectangle")

                and

                entry_analysis["rectangle"]["signal"] == h1_liq

                and

                entry_analysis.get("retest")

                and

                entry_analysis["retest"]["signal"] == h1_liq

            ):

                final_signal = h1_liq



        # ===============================
        # M5 LIQUIDITY → M1 EXECUTION
        # ===============================

        elif mode == "M5":


            m5_liq = self.get_liquidity_signal(
                sweep_analysis
            )


            if (

                m5_liq in ["BUY","SELL"]

                and

                entry_analysis.get("structure")

                and

                entry_analysis["structure"]["signal"] == m5_liq

                and

                entry_analysis.get("rectangle")

                and

                entry_analysis["rectangle"]["signal"] == m5_liq
