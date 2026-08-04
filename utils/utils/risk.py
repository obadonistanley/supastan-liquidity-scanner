class RiskManager:


    def __init__(self):
        pass



    def calculate(self, candles, signal):

        if not candles:
            return None


        current = candles[-1]


        entry = current["close"]



        recent = candles[-10:]

        highs = [
            candle["high"]
            for candle in recent
        ]

        lows = [
            candle["low"]
            for candle in recent
        ]



        if signal == "BUY":

            stop_loss = min(lows)

            risk = entry - stop_loss


            if risk <= 0:
                return None


            take_profit_1 = entry + (risk * 2)

            take_profit_2 = entry + (risk * 3)



        elif signal == "SELL":

            stop_loss = max(highs)

            risk = stop_loss - entry


            if risk <= 0:
                return None


            take_profit_1 = entry - (risk * 2)

            take_profit_2 = entry - (risk * 3)



        else:

            return {
                "entry": entry,
                "stop_loss": None,
                "take_profit_1": None,
                "take_profit_2": None,
                "risk_reward": "NO TRADE"
            }



        return {

            "entry": round(entry, 2),

            "stop_loss": round(stop_loss, 2),

            "take_profit_1": round(take_profit_1, 2),

            "take_profit_2": round(take_profit_2, 2),

            "risk_reward": "1:2 / 1:3"

        }
