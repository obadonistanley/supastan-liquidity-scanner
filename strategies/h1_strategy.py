from scanner import Scanner
from data.deriv import DerivAPI


class H1Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()

    def run(self, symbol):

        h1 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=3600
        )

        m5 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=300
        )

        if not h1 or not m5:

            return {
                "strategy": "H1",
                "final_signal": "NO DATA"
            }

        h1_analysis = self.scanner.scan(h1)

        m5_analysis = self.scanner.scan(m5)

        final_signal = "NO TRADE"

        if (
            h1_analysis["signal"] == "BUY"
            and
            m5_analysis["signal"] == "BUY"
        ):

            final_signal = "BUY"

        elif (
            h1_analysis["signal"] == "SELL"
            and
            m5_analysis["signal"] == "SELL"
        ):

            final_signal = "SELL"

        return {

            "strategy": "H1",

            "final_signal": final_signal,

            "higher_timeframe": h1_analysis,

            "execution": m5_analysis,

            "reason":
            "H1 Sweep → M5 BOS → CHOCH → Rectangle Retest"

        }
