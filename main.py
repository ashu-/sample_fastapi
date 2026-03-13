from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Simple FastAPI Server",
    description="A simple FastAPI server with healthcheck endpoint",
    version="1.0.0"
)

@app.get("/health")
async def healthcheck():
    """
    Healthcheck endpoint to verify the server is running
    """
    return {
        "status": "healthy server",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "simple-fastapi-server"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
