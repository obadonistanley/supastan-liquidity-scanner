from scanner import Scanner
from data.deriv import DerivAPI


class Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()


    def analyze(self, candles, timeframe):

        if not candles:
            return {"signal": "NO DATA"}

        return self.scanner.scan(
            candles,
            timeframe
        )


    def get_liquidity(self, analysis):

        if analysis and analysis.get("liquidity"):

            return analysis["liquidity"].get("signal")

        return None


    def valid_execution(self, data):

        return (

            data.get("structure")

            and

            data.get("rectangle")

            and

            data.get("retest")

        )



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


            higher = self.analyze(d1,"D1")

            confirm = self.analyze(h4,"H4")

            entry = self.analyze(m5,"M5")



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


            higher = self.analyze(h1,"H1")

            confirm = None

            entry = self.analyze(m5,"M5")



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


            higher = self.analyze(m5,"M5")

            confirm = None

            entry = self.analyze(m1,"M1")


        else:

            return {
                "error":"Invalid mode"
            }



        final_signal = "NO TRADE"



        # =========================
        # D1/H4 STRATEGY
        # =========================

        if mode == "D1_H4":


            d1_signal = self.get_liquidity(higher)

            h4_signal = self.get_liquidity(confirm)


            if (

                d1_signal

                and

                d1_signal == h4_signal

                and

                self.valid_execution(entry)

                and

                entry.get("signal") == d1_signal

            ):

                final_signal = d1_signal



        # =========================
        # H1 STRATEGY
        # =========================

        elif mode == "H1":


            h1_signal = self.get_liquidity(higher)


            if (

                h1_signal

                and

                self.valid_execution(entry)

                and

                entry.get("signal") == h1_signal

            ):

                final_signal = h1_signal



        # =========================
        # M5 STRATEGY
        # =========================

        elif mode == "M5":


            if self.valid_execution(entry):

                final_signal = entry.get("signal")



        return {

            "symbol":symbol,

            "mode":mode,

            "final_signal":final_signal,

            "higher_timeframe":higher,

            "confirmation":confirm,

            "execution":entry,

            "trade_plan":{

                "entry":"Order Block Retest",

                "stop_loss":"Beyond Liquidity Sweep",

                "take_profit":"Minimum 1:3 RR",

                "risk_reward":"1:3+"

            }

        }
