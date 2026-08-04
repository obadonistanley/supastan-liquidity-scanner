from fastapi import FastAPI

from scanner import Scanner
from data.deriv import DerivAPI
from signals.generator import SignalGenerator


app = FastAPI(title="Supastan AI Liquidity Scanner")


scanner = Scanner()
deriv = DerivAPI()
signal_generator = SignalGenerator()


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


    raw_signal = scanner.scan(candles)


    # Extract direction from scanner result
    if isinstance(raw_signal, dict):
        direction = raw_signal["signal"]
    else:
        direction = raw_signal


    trade_setup = signal_generator.generate(
        candles,
        direction
    )


    return {
        "symbol": symbol.upper(),
        "market": "Deriv Synthetic Index",
        "timeframe": "15m",
        "analysis": raw_signal,
        "trade_setup": trade_setup,
        "candles": len(candles)
    }
