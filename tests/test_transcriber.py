import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))


def test_transcribe_joins_segments():
    seg1, seg2 = MagicMock(), MagicMock()
    seg1.text = "大家好"
    seg2.text = "今天分享"

    mock_model = MagicMock()
    mock_model.transcribe.return_value = ([seg1, seg2], MagicMock())

    with patch("transcriber.get_model", return_value=mock_model):
        from transcriber import _transcribe_sync
        result = _transcribe_sync(Path("fake.wav"), "large-v3-turbo")

    assert result == "大家好今天分享"


def test_transcribe_uses_vad_filter():
    mock_model = MagicMock()
    mock_model.transcribe.return_value = ([], MagicMock())

    with patch("transcriber.get_model", return_value=mock_model):
        from transcriber import _transcribe_sync
        _transcribe_sync(Path("fake.wav"), "large-v3-turbo")

    call_kwargs = mock_model.transcribe.call_args[1]
    assert call_kwargs.get("vad_filter") is True


def test_get_model_caches():
    import transcriber
    transcriber._model_cache.clear()

    mock_instance = MagicMock()
    with patch("transcriber.WhisperModel", return_value=mock_instance) as MockClass:
        from transcriber import get_model
        m1 = get_model("large-v3-turbo")
        m2 = get_model("large-v3-turbo")

    assert m1 is m2
    assert MockClass.call_count == 1
    transcriber._model_cache.clear()
