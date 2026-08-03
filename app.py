from fastapi import FastAPI
import requests

app = FastAPI(title="Supastan AI Liquidity Scanner")


@app.get("/")
def home():
    return {
        "status": "online",
        "scanner": "Supastan AI Liquidity Scanner",
        "version": "2.0"
    }


@app.get("/scan/{symbol}")
def scan_market(symbol: str):

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval=15m&limit=50"

    response = requests.get(url)

    data = response.json()

    candles = []

    for candle in data:
        candles.append({
            "time": candle[0],
            "open": candle[1],
            "high": candle[2],
            "low": candle[3],
            "close": candle[4]
        })

    return {
        "symbol": symbol.upper(),
        "timeframe": "15m",
        "candles": candles
    }
