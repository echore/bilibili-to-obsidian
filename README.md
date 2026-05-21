# Bili Clipper

Chrome extension that clips Bilibili video transcripts directly to Obsidian.

- **Videos with CC subtitles** — extracts in ~2 seconds
- **Videos without subtitles** — local Whisper transcription (~2 min on M2 8GB), no API needed
- **Open source, free, local** — no data leaves your machine

## Requirements

- macOS (Apple Silicon M1/M2/M3 recommended; Intel works but slower)
- Python 3.11+
- Chrome

## Install

**Step 1 — Local server:**
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_HANDLE/bili-clipper/main/install.sh | bash
```
This installs the Python server as a background service that auto-starts with your Mac.
First run downloads the Whisper `large-v3-turbo` model (~1.6 GB).

**Step 2 — Chrome extension:**
1. Open `chrome://extensions`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked** → select the `extension/` folder from this repo

**Step 3 — Configure:**
Click the Bili Clipper icon in Chrome toolbar → set your Obsidian vault path.

## Usage

Navigate to any Bilibili video. A **Clip bar** appears below the title. Click **Clip**.
The note is saved to `Raw/[video title].md` in your vault.

## Output format

```markdown
---
title: 如何快速学习陌生领域
source: https://www.bilibili.com/video/BVxxx
platform: bilibili
date: 2026-05-20
tags: [transcript, bilibili]
transcript_method: cc_subtitle
---

[transcript text]
```

## Troubleshooting

**"本地服务未运行"**
```bash
# Check server logs
tail -f ~/.local/share/bili-clipper/server.log

# Restart manually
launchctl stop com.bili-clipper.server
launchctl start com.bili-clipper.server
```

**Whisper too slow / OOM**
Open extension popup → change ASR model to `medium` or `base`.

## Uninstall
```bash
bash uninstall.sh
```

## Credits
- [kangchainx/video-text-chrome-extension](https://github.com/kangchainx/video-text-chrome-extension) — architecture reference (MIT)
- [IndieKKY/bilibili-subtitle](https://github.com/IndieKKY/bilibili-subtitle) — Bilibili API reference
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
