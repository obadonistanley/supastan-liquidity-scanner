class LiquiditySweep:

    def detect(self, candles):

        if len(candles) < 55:
            return None

        tolerance = 0.0005

        last = candles[-1]

        # Search between 5 and 50 candles back
        for i in range(len(candles) - 50, len(candles) - 5):

            c1 = candles[i]

            for j in range(i + 1, len(candles) - 1):

                c2 = candles[j]

                # ==========================
                # BUY - Equal Lows
                # ==========================

                if abs(c1["low"] - c2["low"]) <= tolerance:

                    level = min(c1["low"], c2["low"])

                    if (
                        last["low"] < level
                        and last["close"] > level
                    ):

                        return {

                            "signal": "BUY",

                            "sweep": "WICK",

                            "level": round(level, 5),

                            "price": last["close"]

                        }

                # ==========================
                # SELL - Equal Highs
                # ==========================

                if abs(c1["high"] - c2["high"]) <= tolerance:

                    level = max(c1["high"], c2["high"])

                    if (
                        last["high"] > level
                        and last["close"] < level
                    ):

                        return {

                            "signal": "SELL",

                            "sweep": "WICK",

                            "level": round(level, 5),

                            "price": last["close"]

                        }

        return None
