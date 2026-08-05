from scanner import Scanner
from data.deriv import DerivAPI


class D1H4Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()

    def run(self, symbol):

        d1 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=86400
        )

        h4 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=14400
        )

        m5 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=300
        )

        if not d1 or not h4 or not m5:

            return {
                "strategy": "D1/H4",
                "final_signal": "NO DATA"
            }

        d1_analysis = self.scanner.scan(d1)

        h4_analysis = self.scanner.scan(h4)

        m5_analysis = self.scanner.scan(m5)

        final_signal = "NO TRADE"

        # D1 or H4 must produce the HTF sweep
        htf_buy = (
            d1_analysis["signal"] == "BUY"
            or
            h4_analysis["signal"] == "BUY"
        )

        htf_sell = (
            d1_analysis["signal"] == "SELL"
            or
            h4_analysis["signal"] == "SELL"
        )

        # M5 must complete the setup
        if htf_buy and m5_analysis["signal"] == "BUY":

            final_signal = "BUY"

        elif htf_sell and m5_analysis["signal"] == "SELL":

            final_signal = "SELL"

        return {

            "strategy": "D1/H4",

            "final_signal": final_signal,

            "higher_timeframe": {

                "D1": d1_analysis,

                "H4": h4_analysis

            },

            "execution": m5_analysis,

            "reason":

            "D1/H4 Sweep → M5 BOS → CHOCH → Rectangle Retest"

        }
