from fastapi import FastAPI
from scanner import Scanner
import random
import time

app = FastAPI(title="Supastan AI Liquidity Scanner")

scanner = Scanner()


@app.get("/")
def home():
    return {
        "status": "online",
        "scanner": "Supastan AI Liquidity Scanner",
        "version": "3.0"
    }


def get_deriv_candles(symbol: str):
    """
    Temporary candle generator.
    Replace with Deriv API WebSocket connection.
    """

    candles = []

    price = 10000

    for i in range(250):
        open_price = price
        high = open_price + random.randint(1, 50)
        low = open_price - random.randint(1, 50)
        close = random.randint(low, high)

        candles.append({
            "time": int(time.time()) - (i * 900),
            "open": float(open_price),
            "high": float(high),
            "low": float(low),
            "close": float(close)
        })

        price = close

    return candles


@app.get("/scan/{symbol}")
def scan_market(symbol: str):

    candles = get_deriv_candles(symbol.upper())

    signal = scanner.scan(candles)

    return {
        "symbol": symbol.upper(),
        "market": "Deriv Synthetic Index",
        "timeframe": "15m",
        "signal": signal,
        "candles": len(candles)
    }
