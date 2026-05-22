import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from writer import write_note, sanitize_filename


def test_sanitize_filename_strips_invalid_chars():
    assert sanitize_filename('He said "hello/world"') == "He said hello world"


def test_sanitize_filename_truncates_at_100():
    assert len(sanitize_filename("a" * 200)) == 100


CONFIG = {
    "obsidian_url": "https://127.0.0.1:27123",
    "obsidian_api_key": "test-key-abc",
    "folder": "Raw",
    "bvid": "BV1xx411c7mD",
}


def make_mock_client(get_status=404, put_status=201):
    mock_get = MagicMock()
    mock_get.status_code = get_status

    mock_put = MagicMock()
    mock_put.status_code = put_status
    mock_put.raise_for_status = MagicMock()

    client = AsyncMock()
    client.get = AsyncMock(return_value=mock_get)
    client.put = AsyncMock(return_value=mock_put)
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)
    return client


@pytest.mark.asyncio
async def test_write_note_new_file_returns_path():
    client = make_mock_client(get_status=404)
    with patch("writer.httpx.AsyncClient", return_value=client):
        path = await write_note("Test Video", "line1\nline2", CONFIG, "cc_subtitle")
    assert path == "Raw/Test Video.md"


@pytest.mark.asyncio
async def test_write_note_duplicate_adds_date():
    client = make_mock_client(get_status=200)
    with patch("writer.httpx.AsyncClient", return_value=client):
        path = await write_note("Test Video", "line1\nline2", CONFIG, "cc_subtitle")
    from datetime import date
    assert date.today().isoformat() in path
    assert path.startswith("Raw/")


@pytest.mark.asyncio
async def test_write_note_content_has_frontmatter():
    client = make_mock_client(get_status=404)
    with patch("writer.httpx.AsyncClient", return_value=client):
        await write_note("My Video", "transcript here", CONFIG, "whisper_large-v3-turbo")
    body = client.put.call_args[1]["content"].decode("utf-8")
    assert "title: My Video" in body
    assert "platform: bilibili" in body
    assert "transcript_method: whisper_large-v3-turbo" in body
    assert "transcript here" in body


@pytest.mark.asyncio
async def test_write_note_sets_auth_header():
    client = make_mock_client(get_status=404)
    with patch("writer.httpx.AsyncClient", return_value=client):
        await write_note("Vid", "text", CONFIG, "cc_subtitle")
    headers = client.put.call_args[1]["headers"]
    assert headers["Authorization"] == "Bearer test-key-abc"
