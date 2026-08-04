from fastapi import FastAPI
from scanner import Scanner
from data.deriv import DerivAPI


app = FastAPI(title="Supastan AI Liquidity Scanner")

scanner = Scanner()
deriv = DerivAPI()


@app.get("/")
def home():
    return {
        "status": "online",
        "scanner": "Supastan AI Liquidity Scanner",
        "version": "3.0"
    }


def get_deriv_candles(symbol):

    candles = deriv.get_candles(
        symbol=symbol,
        count=250,
        granularity=900
    )

    return candles


@app.get("/scan/{symbol}")
def scan_market(symbol: str):

    candles = get_deriv_candles(symbol.upper())

    if not candles:
        return {
            "symbol": symbol.upper(),
            "error": "No candle data received from Deriv API"
        }


    signal = scanner.scan(candles)


    return {
        "symbol": symbol.upper(),
        "market": "Deriv Synthetic Index",
        "timeframe": "15m",
        "signal": signal,
        "candles": len(candles)
    }
