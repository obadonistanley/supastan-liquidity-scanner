from fastapi import FastAPI

from strategy import Strategy

app = FastAPI(
    title="Supastan AI Liquidity Scanner",
    version="1.0"
)

strategy = Strategy()


@app.get("/")
def home():

    return {
        "status": "online",
        "project": "Supastan AI Liquidity Scanner v1.0"
    }


@app.get("/api")
def api():

    return {
        "status": "running"
    }


@app.get("/scan/{symbol}")
def scan(symbol: str):

    return {

        "symbol": symbol,

        "H4": strategy.run(symbol, "H4"),

        "H1": strategy.run(symbol, "H1"),

        "M5": strategy.run(symbol, "M5")

    }


@app.get("/strategy/{symbol}/{timeframe}")
def run_strategy(
    symbol: str,
    timeframe: str
):

    timeframe = timeframe.upper()

    if timeframe not in ["H4", "H1", "M5"]:

        return {
            "error": "Choose H4, H1 or M5"
        }

    return strategy.run(
        symbol,
        timeframe
    )
