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
        "status": "ONLINE",
        "strategy": "SMC Liquidity Sweep + BOS + CHOCH + Order Block Retest"
    }


@app.get("/ai")
def ai_scan():

    signals = []


    strategies = [
        {
            "higher_tf": "D1",
            "entry_tf": "M5"
        },
        {
            "higher_tf": "H4",
            "entry_tf": "M5"
        },
        {
            "higher_tf": "H1",
            "entry_tf": "M5"
        },
        {
            "higher_tf": "M5",
            "entry_tf": "M1"
        }
    ]


    for symbol in MARKETS:


        for setup in strategies:

            try:

                result = scanner.run(
                    symbol,
                    setup["higher_tf"],
                    setup["entry_tf"]
                )


                if result.get("signal") == "BUY" or result.get("signal") == "SELL":

                    signals.append(result)


            except Exception as e:

                print(
                    symbol,
                    setup,
                    e
                )


    return {

        "scanner": "Supastan AI Liquidity Scanner",

        "total_signals": len(signals),

        "signals": signals

    }
