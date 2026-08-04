class SwingDetector:

    def swing_high(self, candles, lookback=5):

        if len(candles) < lookback * 2 + 1:
            return None

        for i in range(len(candles) - lookback - 1, lookback, -1):

            high = candles[i]["high"]

            left = candles[i - lookback:i]
            right = candles[i + 1:i + lookback + 1]

            if (
                all(high > c["high"] for c in left)
                and
                all(high > c["high"] for c in right)
            ):
                return high

        return None


    def swing_low(self, candles, lookback=5):

        if len(candles) < lookback * 2 + 1:
            return None

        for i in range(len(candles) - lookback - 1, lookback, -1):

            low = candles[i]["low"]

            left = candles[i - lookback:i]
            right = candles[i + 1:i + lookback + 1]

            if (
                all(low < c["low"] for c in left)
                and
                all(low < c["low"] for c in right)
            ):
                return low

        return None
