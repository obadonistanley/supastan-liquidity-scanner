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

        m1 = self.deriv.get_candles(
            symbol,
            count=250,
            granularity=60
        )

        if not d1 or not h4 or not m5 or not m1:

            return {
                "final_signal": "NO DATA"
            }

        d1_analysis = self.scanner.scan(d1)

        h4_analysis = self.scanner.scan(h4)

        m5_analysis = self.scanner.scan(m5)

        m1_analysis = self.scanner.scan(m1)

        final_signal = "NO TRADE"

        if (
            d1_analysis["signal"] == "BUY"
            and h4_analysis["signal"] == "BUY"
            and m5_analysis["signal"] == "BUY"
            and m1_analysis["signal"] == "BUY"
        ):
            final_signal = "BUY"

        elif (
            d1_analysis["signal"] == "SELL"
            and h4_analysis["signal"] == "SELL"
            and m5_analysis["signal"] == "SELL"
            and m1_analysis["signal"] == "SELL"
        ):
            final_signal = "SELL"

        return {

            "strategy": "D1/H4",

            "final_signal": final_signal,

            "trend": d1_analysis,

            "liquidity": h4_analysis,

            "entry": m5_analysis,

            "confirmation": m1_analysis

        }
