from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from scanner import Scanner
from data.deriv import DerivAPI
from signals.generator import SignalGenerator
from strategy import Strategy
from strategy_engine import StrategyEngine


app = FastAPI(title="Supastan AI Liquidity Scanner")


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


scanner = Scanner()
deriv = DerivAPI()
signal_generator = SignalGenerator()
strategy = Strategy()
strategy_engine = StrategyEngine()


@app.get("/")
def home():
    return FileResponse("static/index.html")


def get_deriv_candles(symbol):

    candles = deriv.get_candles(
        symbol=symbol,
        count=250
    )

    return candles


@app.get("/api")
def api_status():
    return {
        "status": "online",
        "scanner": "Supastan AI Liquidity Scanner",
        "version": "3.0"
    }


@app.get("/scan/{symbol}")
def scan_market(symbol: str):

    candles = get_deriv_candles(symbol.upper())

    if not candles:
        return {
            "symbol": symbol.upper(),
            "error": "No candle data received from Deriv API"
        }

    raw_signal = scanner.scan(candles)

    if isinstance(raw_signal, dict):
        direction = raw_signal.get("signal", "NO TRADE")
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


@app.get("/strategy/{symbol}/{mode}")
def run_strategy(symbol: str, mode: str):

    result = strategy.run(
        symbol.upper(),
        mode.upper()
    )

    return result


@app.get("/ai/{symbol}")
def ai_scan(symbol: str):

    result = strategy_engine.best_signal(
        symbol.upper()
    )

    return result
