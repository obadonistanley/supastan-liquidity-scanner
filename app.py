from fastapi import FastAPI
import asyncio

from strategy import Strategy
from config import MARKETS
from background import auto_scan
from signals_store import get_signals


app = FastAPI()

scanner = Strategy()


@app.on_event("startup")
async def startup_event():

    asyncio.create_task(
        auto_scan()
    )


@app.get("/")
def home():

    return {

        "name": "Supastan AI Liquidity Scanner",

        "version": "1.0",

        "status": "ONLINE",

        "strategy": "Wick Liquidity Sweep Detection"

    }


@app.get("/ai")
def ai_scan():

    signals = []

    timeframes = [

        "D1",

        "H4",

        "H1",

        "M5"

    ]

    for symbol in MARKETS:

        for timeframe in timeframes:

            try:

                result = scanner.run(

                    symbol,

                    timeframe

                )

                if result.get("signal") in [

                    "BUY",

                    "SELL"

                ]:

                    signals.append(result)

            except Exception as e:

                print(

                    symbol,

                    timeframe,

                    e

                )

    return {

        "scanner": "Supastan AI Liquidity Scanner",

        "strategy": "Liquidity Sweep Only",

        "total_signals": len(signals),

        "signals": signals

    }


@app.get("/signals")
def signals():

    return {

        "scanner": "Supastan AI Liquidity Scanner",

        "strategy": "Live Background Scanner",

        "total": len(get_signals()),

        "signals": get_signals()

    }
