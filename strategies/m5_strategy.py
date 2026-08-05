from scanner import Scanner
from data.deriv import DerivAPI


class M5Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()

    def run(self, symbol):

        m5 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=300
        )

        m1 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=60
        )

        if not m5 or not m1:

            return {
                "strategy": "M5",
                "final_signal": "NO DATA"
            }

        m5_analysis = self.scanner.scan(m5)

        m1_analysis = self.scanner.scan(m1)

        final_signal = "NO TRADE"

        if (
            m5_analysis["signal"] == "BUY"
            and
            m1_analysis["signal"] == "BUY"
        ):

            final_signal = "BUY"

        elif (
            m5_analysis["signal"] == "SELL"
            and
            m1_analysis["signal"] == "SELL"
        ):

            final_signal = "SELL"

        return {

            "strategy": "M5",

            "final_signal": final_signal,

            "higher_timeframe": m5_analysis,

            "execution": m1_analysis,

            "reason":
            "M5 Sweep → M1 BOS → CHOCH → Rectangle Retest"

        }
