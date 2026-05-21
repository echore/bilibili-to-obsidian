from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Bili Clipper Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model": "large-v3-turbo"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=27182, log_level="info")
