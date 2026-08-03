from fastapi import FastAPI
import requests

from scanner import Scanner

app = FastAPI(title="Supastan AI Liquidity Scanner")

scanner = Scanner()


@app.get("/")
def home():
    return {
        "status": "online",
        "scanner": "Supastan AI Liquidity Scanner",
        "version": "3.0"
    }


@app.get("/scan/{symbol}")
def scan_market(symbol: str):

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval=15m&limit=250"

    response = requests.get(url)
    data = response.json()

    candles = []

    for candle in data:
        candles.append({
            "time": candle[0],
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4])
        })

    signal = scanner.scan(candles)

    return {
        "symbol": symbol.upper(),
        "timeframe": "15m",
        "signal": signal,
        "candles": len(candles)
    }
