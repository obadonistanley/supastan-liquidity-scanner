from scanner import Scanner
from data.deriv import DerivAPI
from smc.liquidity import LiquiditySweep


class D1H4Strategy:

    def __init__(self):

        self.scanner = Scanner()
        self.deriv = DerivAPI()
        self.liquidity = LiquiditySweep()

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

        # ==========================
        # HIGHER TIMEFRAME
        # LIQUIDITY SWEEP ONLY
        # ==========================

        d1_sweep = self.liquidity.detect(d1)

        h4_sweep = self.liquidity.detect(h4)

        # ==========================
        # ENTRY TIMEFRAME
        # BOS → CHOCH → ORDER BLOCK
        # RETEST
        # ==========================

        m5_analysis = self.scanner.scan(m5)

        final_signal = "NO TRADE"

        if (

            (d1_sweep == "BUY" or h4_sweep == "BUY")

            and

            m5_analysis["signal"] == "BUY"

        ):

            final_signal = "BUY"

        elif (

            (d1_sweep == "SELL" or h4_sweep == "SELL")

            and

            m5_analysis["signal"] == "SELL"

        ):

            final_signal = "SELL"

        return {

            "strategy": "D1/H4",

            "final_signal": final_signal,

            "higher_timeframe": {

                "D1_Liquidity": d1_sweep,

                "H4_Liquidity": h4_sweep

            },

            "execution": m5_analysis,

            "reason": "D1/H4 Liquidity Sweep → M5 BOS → CHOCH → Fresh Order Block → First Retest"

        }
