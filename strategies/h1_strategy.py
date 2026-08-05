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

        m1 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=60
        )

        if not h1 or not m5 or not m1:

            return {
                "final_signal": "NO DATA"
            }

        h1_analysis = self.scanner.scan(h1)

        m5_analysis = self.scanner.scan(m5)

        m1_analysis = self.scanner.scan(m1)

        final_signal = "NO TRADE"

        if (
            h1_analysis["signal"] == "BUY"
            and m5_analysis["signal"] == "BUY"
            and m1_analysis["signal"] == "BUY"
        ):
            final_signal = "BUY"

        elif (
            h1_analysis["signal"] == "SELL"
            and m5_analysis["signal"] == "SELL"
            and m1_analysis["signal"] == "SELL"
        ):
            final_signal = "SELL"

        return {

            "strategy": "H1",

            "final_signal": final_signal,

            "trend": h1_analysis,

            "entry": m5_analysis,

            "confirmation": m1_analysis

        }
