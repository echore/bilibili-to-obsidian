from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from urllib.parse import quote
import httpx
import uvicorn

from transcriber import download_audio, transcribe
from writer import write_note

app = FastAPI(title="Bili Clipper Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class Config(BaseModel):
    obsidian_url: str = "https://127.0.0.1:27124"
    obsidian_api_key: str = ""
    folder: str = "Raw"
    output: str = "obsidian"
    model: str = "large-v3-turbo"
    bvid: Optional[str] = None


class ClipRequest(BaseModel):
    bvid: str
    title: str
    transcript: Optional[str] = None
    config: Config = Config()


class OpenRequest(BaseModel):
    path: str
    obsidian_url: str = "https://127.0.0.1:27124"
    obsidian_api_key: str = ""


@app.get("/health")
def health():
    return {"status": "ok", "model": "mlx-community/whisper-large-v3-turbo"}


@app.post("/open")
async def open_note(req: OpenRequest):
    """Proxy open-in-Obsidian so the browser never makes direct SSL calls."""
    url = req.obsidian_url.rstrip("/")
    headers = {"Authorization": f"Bearer {req.obsidian_api_key}"}
    try:
        async with httpx.AsyncClient(verify=False) as client:
            await client.post(
                f"{url}/open/{quote(req.path, safe='/')}",
                headers=headers,
            )
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/clip")
async def clip(req: ClipRequest):
    try:
        if req.transcript:
            path = await write_note(
                req.title,
                req.transcript,
                req.config.model_dump(),
                method="cc_subtitle",
            )
        else:
            audio_path = await download_audio(req.bvid)
            transcript_text = await transcribe(audio_path, req.config.model)
            path = await write_note(
                req.title,
                transcript_text,
                req.config.model_dump(),
                method=f"whisper_{req.config.model}",
            )
        return {"success": True, "path": path}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=27182, log_level="info")
