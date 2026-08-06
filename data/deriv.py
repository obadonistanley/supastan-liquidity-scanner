import websocket
import json


class DerivAPI:

    def __init__(self):

        self.app_id = "1089"

        self.url = (
            f"wss://ws.derivws.com/websockets/v3?app_id={self.app_id}"
        )

        self.timeframes = {

            "M1": 60,
            "M5": 300,
            "M15": 900,
            "H1": 3600,
            "H4": 14400,
            "D1": 86400

        }


    def normalize_symbol(self, symbol):

        mapping = {

            # Forex
            "GBPUSD": "frxGBPUSD",
            "GBPJPY": "frxGBPJPY",
            "EURJPY": "frxEURJPY",
            "NZDJPY": "frxNZDJPY",
            "EURUSD": "frxEURUSD",
            "USDCAD": "frxUSDCAD",
            "GBPNZD": "frxGBPNZD",

            # Crypto / Gold
            "XAUUSD": "frxXAUUSD",
            "BTCUSD": "cryBTCUSD",

            # Synthetic Indices
            "R_10": "R_10",
            "R_10 1s": "R_10",

            "R_25": "R_25",
            "R_25 1s": "R_25",

            "R_50": "R_50",

            "R_75": "R_75",
            "R_75 1s": "R_75",

            "R_100": "R_100",

            "R_150 1s": "R_150",

            # Indices
            "US30": "US30",
            "NAS": "NAS100"

        }


        return mapping.get(symbol, symbol)



    def get_candles(
        self,
        symbol,
        timeframe="M5",
        count=250
    ):


        symbol = self.normalize_symbol(symbol)


        granularity = self.timeframes.get(
            timeframe.upper(),
            300
        )


        try:

            ws = websocket.create_connection(
                self.url,
                timeout=10
            )


            request = {

                "ticks_history": symbol,

                "count": count,

                "end": "latest",

                "style": "candles",

                "granularity": granularity

            }


            ws.send(
                json.dumps(request)
            )


            response = json.loads(
                ws.recv()
            )


            ws.close()


        except Exception as e:

            print(
                "Deriv connection error:",
                e
            )

            return []



        candles = []


        if "candles" not in response:

            return candles



        for candle in response["candles"]:

            candles.append({

                "time": candle["epoch"],

                "open": float(candle["open"]),

                "high": float(candle["high"]),

                "low": float(candle["low"]),

                "close": float(candle["close"])

            })


        return candles




    def get_multi_timeframe(self, symbol):

        return {

            "D1": self.get_candles(symbol, "D1"),

            "H4": self.get_candles(symbol, "H4"),

            "H1": self.get_candles(symbol, "H1"),

            "M5": self.get_candles(symbol, "M5"),

            "M1": self.get_candles(symbol, "M1")

        }
