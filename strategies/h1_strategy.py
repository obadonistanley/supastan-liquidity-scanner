from scanner import Scanner
from data.deriv import DerivAPI
from smc.liquidity import LiquiditySweep


class H1Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()
        self.liquidity = LiquiditySweep()

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

        # ==========================
        # H1 LIQUIDITY SWEEP ONLY
        # ==========================

        h1_sweep = self.liquidity.detect(h1)

        # ==========================
        # M5 ENTRY CONFIRMATION
        # BOS → CHOCH → ORDER BLOCK
        # FIRST RETEST
        # ==========================

        m5_analysis = self.scanner.scan(m5)

        final_signal = "NO TRADE"

        if (

            h1_sweep == "BUY"

            and

            m5_analysis["signal"] == "BUY"

        ):

            final_signal = "BUY"

        elif (

            h1_sweep == "SELL"

            and

            m5_analysis["signal"] == "SELL"

        ):

            final_signal = "SELL"

        return {

            "strategy": "H1",

            "final_signal": final_signal,

            "higher_timeframe": {

                "H1_Liquidity": h1_sweep

            },

            "execution": m5_analysis,

            "reason": "H1 Liquidity Sweep → M5 BOS → CHOCH → Fresh Order Block → First Retest"

        }
