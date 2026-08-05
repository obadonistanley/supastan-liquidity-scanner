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

        if analysis.get("liquidity"):

            return analysis["liquidity"].get("signal")

        return None


    def get_signal(self, analysis):

        return analysis.get("signal")



    def run(self, symbol, mode):


        if mode == "D1_H4":

            d1 = self.deriv.get_candles(symbol,"D1",200)

            h4 = self.deriv.get_candles(symbol,"H4",200)

            m5 = self.deriv.get_candles(symbol,"M5",200)


            sweep_analysis = self.analyze(d1,"D1")

            confirmation_analysis = self.analyze(h4,"H4")

            entry_analysis = self.analyze(m5,"M5")


        elif mode == "H1":

            h1 = self.deriv.get_candles(symbol,"H1",200)

            m5 = self.deriv.get_candles(symbol,"M5",200)


            sweep_analysis = self.analyze(h1,"H1")

            confirmation_analysis = None

            entry_analysis = self.analyze(m5,"M5")


        elif mode == "M5":

            m5 = self.deriv.get_candles(symbol,"M5",200)

            m1 = self.deriv.get_candles(symbol,"M1",200)


            sweep_analysis = self.analyze(m5,"M5")

            confirmation_analysis = None

            entry_analysis = self.analyze(m1,"M1")


        else:

            return {
                "error":"Invalid mode"
            }



        final_signal="NO TRADE"



        if mode=="D1_H4":


            d1_liq=self.get_liquidity_signal(
                sweep_analysis
            )

            h4_liq=self.get_liquidity_signal(
                confirmation_analysis
            )


            entry_signal=self.get_signal(
                entry_analysis
            )


            if (

                d1_liq
                ==
                h4_liq
                ==
                entry_signal

                and

                entry_analysis.get("structure")

                and

                entry_analysis.get("rectangle")

                and

                entry_analysis.get("retest")

            ):

                final_signal=entry_signal



        elif mode=="H1":


            h1_liq=self.get_liquidity_signal(
                sweep_analysis
            )


            entry_signal=self.get_signal(
                entry_analysis
            )


            if (

                h1_liq==entry_signal

                and

                entry_analysis.get("structure")

                and

                entry_analysis.get("rectangle")

                and

                entry_analysis.get("retest")

            ):

                final_signal=entry_signal



        elif mode=="M5":


            m5_liq=self.get_liquidity_signal(
                sweep_analysis
            )


            entry_signal=self.get_signal(
                entry_analysis
            )


            if (

                m5_liq==entry_signal

                and

                entry_analysis.get("structure")

                and

                entry_analysis.get("rectangle")

                and

                entry_analysis.get("retest")

            ):

                final_signal=entry_signal



        return {

            "symbol":symbol,

            "mode":mode,

            "final_signal":final_signal,

            "sweep_analysis":sweep_analysis,

            "confirmation_analysis":confirmation_analysis,

            "entry_analysis":entry_analysis,

            "trade_plan":{

                "entry":"Order Block Retest",

                "stop_loss":"Beyond Liquidity Sweep",

                "take_profit":"1:3 RR",

                "risk_reward":"1:3+"

            }

        }
