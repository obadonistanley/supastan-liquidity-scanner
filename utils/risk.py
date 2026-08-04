from utils.swings import SwingDetector


class RiskManager:

    def __init__(self):
        self.swing = SwingDetector()


    def calculate(self, candles, signal):

        if not candles:
            return None

        entry = candles[-1]["close"]

        if signal == "BUY":

            stop = candles[-1]["low"]

            risk = entry - stop

            if risk <= 0:
                return None

            tp = entry + (risk * 3)

            return {
                "entry": round(entry, 2),
                "stop_loss": round(stop, 2),
                "take_profit": round(tp, 2),
                "rr": "1:3"
            }


        elif signal == "SELL":

            stop = candles[-1]["high"]

            risk = stop - entry

            if risk <= 0:
                return None

            tp = entry - (risk * 3)

            return {
                "entry": round(entry, 2),
                "stop_loss": round(stop, 2),
                "take_profit": round(tp, 2),
                "rr": "1:3"
            }

        return None
