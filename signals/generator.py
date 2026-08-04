class SignalGenerator:

    def __init__(self):
        pass


    def generate(self, candles, signal):

        if not candles or signal == "NO TRADE":
            return {
                "signal": "NO TRADE",
                "confidence": 0,
                "entry": None,
                "stop_loss": None,
                "take_profit": None,
                "risk_reward": None
            }


        current = candles[-1]

        entry = current["close"]


        # BUY setup

        if signal == "BUY":

            stop_loss = current["low"]

            risk = entry - stop_loss

            take_profit = entry + (risk * 2)


        # SELL setup

        elif signal == "SELL":

            stop_loss = current["high"]

            risk = stop_loss - entry

            take_profit = entry - (risk * 2)


        else:

            return {
                "signal": "NO TRADE",
                "confidence": 0,
                "entry": None,
                "stop_loss": None,
                "take_profit": None,
                "risk_reward": None
            }


        confidence = 70


        return {
            "signal": signal,
            "confidence": confidence,
            "entry": round(entry, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "risk_reward": "1:2"
        }
