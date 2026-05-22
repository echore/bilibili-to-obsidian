import re
from datetime import date
from urllib.parse import quote
import httpx


def sanitize_filename(title: str) -> str:
    sanitized = re.sub(r'[/\\:*?"<>|]', " ", title)
    sanitized = re.sub(r'\s+', ' ', sanitized)
    return sanitized[:100].strip()


async def write_note(title: str, transcript: str, config: dict, method: str) -> str:
    obsidian_url = config.get("obsidian_url", "https://127.0.0.1:27123").rstrip("/")
    api_key = config.get("obsidian_api_key", "")
    folder = config.get("folder", "Raw")
    bvid = config.get("bvid", "")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "text/markdown",
    }

    filename = sanitize_filename(title) + ".md"
    vault_path = f"{folder}/{filename}"

    source_url = f"https://www.bilibili.com/video/{bvid}" if bvid else ""
    content = f"""---
title: {title}
source: {source_url}
platform: bilibili
date: {date.today().isoformat()}
tags: [transcript, bilibili]
transcript_method: {method}
---

{transcript}
"""

    async with httpx.AsyncClient(verify=False) as client:
        check = await client.get(
            f"{obsidian_url}/vault/{quote(vault_path, safe='/')}",
            headers=headers,
        )
        if check.status_code == 200:
            filename = f"{sanitize_filename(title)}-{date.today().isoformat()}.md"
            vault_path = f"{folder}/{filename}"

        resp = await client.put(
            f"{obsidian_url}/vault/{quote(vault_path, safe='/')}",
            headers=headers,
            content=content.encode("utf-8"),
        )
        resp.raise_for_status()

    return vault_path
