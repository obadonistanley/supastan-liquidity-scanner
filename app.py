from fastapi import FastAPI

from strategy import Strategy
from config import MARKETS

app = FastAPI()

scanner = Strategy()


@app.get("/")
def home():

    return {
        "name": "Supastan AI Liquidity Scanner",
        "version": "1.0",
        "status": "ONLINE"
    }


@app.get("/ai")
def ai_scan():

    signals = []

    for symbol in MARKETS:

        for timeframe in ["H4", "H1", "M5"]:

            try:

                result = scanner.run(
                    symbol,
                    timeframe
                )

                if result["signal"] != "NO SWEEP":

                    signals.append(result)

            except Exception as e:

                print(symbol, timeframe, e)

    return {

        "total_signals": len(signals),

        "signals": signals

    }
