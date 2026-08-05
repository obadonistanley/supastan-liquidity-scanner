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

        if analysis.get("liquidity"):
            return analysis["liquidity"].get("signal")

        return None


    def run(self, symbol, mode):


        if mode == "D1_H4":

            d1 = self.deriv.get_candles(symbol,"D1",200)
            h4 = self.deriv.get_candles(symbol,"H4",200)
            m5 = self.deriv.get_candles(symbol,"M5",200)


            higher = self.analyze(d1,"D1")
            confirm = self.analyze(h4,"H4")
            entry = self.analyze(m5,"M5")


        elif mode == "H1":

            h1 = self.deriv.get_candles(symbol,"H1",200)
            m5 = self.deriv.get_candles(symbol,"M5",200)


            higher = self.analyze(h1,"H1")
            confirm = None
            entry = self.analyze(m5,"M5")


        elif mode == "M5":

            m5 = self.deriv.get_candles(symbol,"M5",200)
            m1 = self.deriv.get_candles(symbol,"M1",200)


            higher = self.analyze(m5,"M5")
            confirm = None
            entry = self.analyze(m1,"M1")


        else:

            return {"error":"Invalid mode"}



        final_signal="NO TRADE"


        entry_signal = entry.get("signal")


        valid_entry = (

            entry.get("structure")

            and

            entry.get("rectangle")

            and

            entry.get("retest")

        )


        if mode=="D1_H4":


            d1_liq = self.get_liquidity(higher)

            h4_liq = self.get_liquidity(confirm)


            if (

                d1_liq

                and

                d1_liq == h4_liq

                and

                valid_entry

                and

                entry_signal == d1_liq

            ):

                final_signal = entry_signal



        elif mode=="H1":


            h1_liq = self.get_liquidity(higher)


            if (

                h1_liq

                and

                valid_entry

                and

                entry_signal == h1_liq

            ):

                final_signal = entry_signal



        elif mode=="M5":


            if valid_entry:

                final_signal = entry_signal



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

                "take_profit":"1:3 RR",

                "risk_reward":"1:3+"

            }

        }
