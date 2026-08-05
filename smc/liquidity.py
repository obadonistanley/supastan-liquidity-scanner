class LiquiditySweep:

    def __init__(self):
        pass


    def detect(self, candles, timeframe="M5"):

        if len(candles) < 20:
            return None


        timeframe = timeframe.upper()


        # scan last 10 candles
        for i in range(len(candles)-10, len(candles)):


            current = candles[i]

            previous = candles[max(0, i-20):i]


            if len(previous) < 5:
                continue


            previous_high = max(
                c["high"] for c in previous
            )

            previous_low = min(
                c["low"] for c in previous
            )


            candle_body = abs(
                current["close"] -
                current["open"]
            )


            upper_wick = (
                current["high"] -
                max(
                    current["open"],
                    current["close"]
                )
            )


            lower_wick = (
                min(
                    current["open"],
                    current["close"]
                )
                -
                current["low"]
            )



            # =========================
            # M5 / M1 WICK ONLY
            # =========================

            if timeframe in ["M1","M5"]:


                if (
                    current["high"] > previous_high
                    and current["close"] < previous_high
                    and upper_wick > candle_body
                ):

                    return {

                        "signal":"SELL",
                        "sweep":"WICK",
                        "level":previous_high,
                        "timeframe":timeframe,
                        "index":i

                    }



                if (
                    current["low"] < previous_low
                    and current["close"] > previous_low
                    and lower_wick > candle_body
                ):

                    return {

                        "signal":"BUY",
                        "sweep":"WICK",
                        "level":previous_low,
                        "timeframe":timeframe,
                        "index":i

                    }



            # =========================
            # H1/H4/D1
            # =========================

            else:


                if current["high"] > previous_high:

                    return {

                        "signal":"SELL",
                        "sweep":"WICK",
                        "level":previous_high,
                        "timeframe":timeframe,
                        "index":i

                    }


                if current["low"] < previous_low:

                    return {

                        "signal":"BUY",
                        "sweep":"WICK",
                        "level":previous_low,
                        "timeframe":timeframe,
                        "index":i

                    }


        return None
