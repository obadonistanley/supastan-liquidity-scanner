from scanner import Scanner
from data.deriv import DerivAPI
from smc.liquidity import LiquiditySweep


class M5Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()
        self.liquidity = LiquiditySweep()

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

        # ==========================
        # M5 LIQUIDITY SWEEP ONLY
        # ==========================

        m5_sweep = self.liquidity.detect(m5)

        # ==========================
        # M1 ENTRY CONFIRMATION
        # BOS → CHOCH → ORDER BLOCK
        # FIRST RETEST
        # ==========================

        m1_analysis = self.scanner.scan(m1)

        final_signal = "NO TRADE"

        if (

            m5_sweep == "BUY"

            and

            m1_analysis["signal"] == "BUY"

        ):

            final_signal = "BUY"

        elif (

            m5_sweep == "SELL"

            and

            m1_analysis["signal"] == "SELL"

        ):

            final_signal = "SELL"

        return {

            "strategy": "M5",

            "final_signal": final_signal,

            "higher_timeframe": {

                "M5_Liquidity": m5_sweep

            },

            "execution": m1_analysis,

            "reason": "M5 Liquidity Sweep → M1 BOS → CHOCH → Fresh Order Block → First Retest"

        }
