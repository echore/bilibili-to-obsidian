import asyncio
import sys
import tempfile
from pathlib import Path
import mlx_whisper

# Derive yt-dlp from the running Python's venv bin dir — works regardless
# of where server.py lives (repo vs install dir).
_YTDLP = Path(sys.executable).parent / "yt-dlp"

_DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"

# Map user-facing short names to mlx-community HuggingFace repo paths.
# Extension sends short names; server resolves to backend-specific paths.
# Only update here when switching backends or adding models.
_MODEL_ALIASES: dict[str, str] = {
    "large-v3-turbo": "mlx-community/whisper-large-v3-turbo",
    "large-v3":       "mlx-community/whisper-large-v3",
    "medium":         "mlx-community/whisper-medium-mlx",
    "small":          "mlx-community/whisper-small-mlx",
    "base":           "mlx-community/whisper-base-mlx",
}


def _resolve_model(name: str) -> str:
    return _MODEL_ALIASES.get(name, name)


def _find_ffmpeg() -> Path | None:
    for candidate in [
        Path("/opt/homebrew/bin/ffmpeg"),  # Apple Silicon Homebrew
        Path("/usr/local/bin/ffmpeg"),      # Intel Homebrew / manual install
        Path("/usr/bin/ffmpeg"),
    ]:
        if candidate.exists():
            return candidate
    return None


_FFMPEG = _find_ffmpeg()


def _transcribe_sync(audio_path: Path, model_name: str) -> str:
    result = mlx_whisper.transcribe(
        str(audio_path),
        path_or_hf_repo=model_name,
        language="zh",
        no_speech_threshold=0.6,
    )
    return result["text"]


async def transcribe(audio_path: Path, model_name: str = _DEFAULT_MODEL) -> str:
    return await asyncio.to_thread(_transcribe_sync, audio_path, _resolve_model(model_name))


async def download_audio(bvid: str) -> Path:
    tmp_dir = Path(tempfile.mkdtemp(prefix="bili-clipper-"))
    output_template = str(tmp_dir / "audio.%(ext)s")

    cmd = [
        str(_YTDLP),
        "-x",
        "--audio-format", "wav",
        "--audio-quality", "0",
        "--no-playlist",
        "--extractor-args", "bilibili:player_client=app",
        "-o", output_template,
        f"https://www.bilibili.com/video/{bvid}",
    ]
    if _FFMPEG:
        cmd += ["--ffmpeg-location", str(_FFMPEG.parent)]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {stderr.decode()}")

    wav_files = list(tmp_dir.glob("*.wav"))
    if not wav_files:
        audio_files = [f for f in tmp_dir.iterdir() if f.is_file()]
        if not audio_files:
            raise RuntimeError("No audio file downloaded")
        return audio_files[0]

    return wav_files[0]
