
import websocket
import json
import time


class DerivAPI:

    def __init__(self):
        self.app_id = "1089"
        self.url = f"wss://ws.derivws.com/websockets/v3?app_id={self.app_id}"


    def get_candles(self, symbol, count=250, granularity=900):

        ws = websocket.create_connection(self.url)

        request = {
            "ticks_history": symbol,
            "count": count,
            "end": "latest",
            "style": "candles",
            "granularity": granularity
        }

        ws.send(json.dumps(request))

        response = json.loads(ws.recv())

        ws.close()

        candles = []

        if "candles" in response:

            for candle in response["candles"]:
                candles.append({
                    "time": candle["epoch"],
                    "open": float(candle["open"]),
                    "high": float(candle["high"]),
                    "low": float(candle["low"]),
                    "close": float(candle["close"])
                })

        return candles
