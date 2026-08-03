from fastapi import FastAPI

app = FastAPI(title="Supastan AI Liquidity Scanner")

@app.get("/")
def home():
    return {
        "status": "online",
        "scanner": "Supastan AI Liquidity Scanner",
        "version": "1.0"
    }
