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
            timeframe="M5",
            count=250
        )

        m1 = self.deriv.get_candles(
            symbol,
            timeframe="M1",
            count=250
        )

        if not m5 or not m1:
            return {
                "strategy": "M5",
                "final_signal": "NO DATA"
            }

        m5_sweep = self.liquidity.detect(m5)
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
