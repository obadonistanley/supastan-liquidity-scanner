from fastapi import FastAPI
import os
import uvicorn

app = FastAPI(title="Supastan AI Liquidity Scanner")

@app.get("/")
def home():
    return {
        "status": "online",
        "scanner": "Supastan AI Liquidity Scanner",
        "version": "1.0"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port
    )
