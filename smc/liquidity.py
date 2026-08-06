class LiquiditySweep:

    def detect(self, candles):

        if len(candles) < 55:
            return None

        last = candles[-1]

        tolerance = 0.0005

        # Search equal highs/lows between 5 and 50 candles back
        for i in range(len(candles) - 50, len(candles) - 5):

            first = candles[i]

            for j in range(i + 1, len(candles) - 1):

                second = candles[j]

                # =========================
                # BUY - Equal Lows
                # =========================

                if abs(first["low"] - second["low"]) <= tolerance:

                    level = (first["low"] + second["low"]) / 2

                    if (
                        last["low"] < level
                        and last["close"] > level
                    ):

                        return {
                            "signal": "BUY",
                            "sweep": "WICK",
                            "level": round(level, 5),
                            "price": last["close"],
                            "timeframe": "",
                            "time": last.get("time")
                        }

                # =========================
                # SELL - Equal Highs
                # =========================

                if abs(first["high"] - second["high"]) <= tolerance:

                    level = (first["high"] + second["high"]) / 2

                    if (
                        last["high"] > level
                        and last["close"] < level
                    ):

                        return {
                            "signal": "SELL",
                            "sweep": "WICK",
                            "level": round(level, 5),
                            "price": last["close"],
                            "timeframe": "",
                            "time": last.get("time")
                        }

        return None
