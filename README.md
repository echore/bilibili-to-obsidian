# Bili Clipper

Chrome extension that clips Bilibili video transcripts directly to Obsidian.

- **Videos with CC subtitles** — extracts in ~2 seconds
- **Videos without subtitles** — local Whisper transcription (~2 min on M2 8GB), no API needed
- **Open source, free, local** — no data leaves your machine

## Requirements

- macOS (Apple Silicon M1/M2/M3 recommended; Intel works but slower)
- Python 3.11+
- Chrome
- [Obsidian](https://obsidian.md) with the [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) community plugin

## Install

**Step 1 — Local server:**
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_HANDLE/bili-clipper/main/install.sh | bash
```
Installs the Python server as a background service that auto-starts with your Mac.
First run downloads the Whisper `large-v3-turbo` model (~1.6 GB).

**Step 2 — Obsidian Local REST API plugin:**
1. In Obsidian → Settings → Community Plugins → Browse → search **Local REST API** → Install → Enable
2. Go to the plugin settings and copy your **API Key**

**Step 3 — Chrome extension:**
1. Open `chrome://extensions`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked** → select the `extension/` folder from this repo

**Step 4 — Configure:**
Click the Bili Clipper icon in Chrome toolbar → paste your Obsidian API Key.

## Usage

Navigate to any Bilibili video. A **Clip bar** appears below the title. Click **Clip**.

- The transcript is saved to `Raw/[video title].md` in your vault
- Chrome shows an **"Open Obsidian?"** dialog — click it to jump directly to the new note

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
# Check server status
curl http://localhost:27182/health

# View logs
tail -f ~/.local/share/bili-clipper/server.log

# Restart
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.bili-clipper.server.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.bili-clipper.server.plist
```

**"Open Obsidian?" dialog doesn't appear**
Make sure the Obsidian Local REST API plugin is enabled and Obsidian is running.

**Whisper too slow / out of memory**
Open extension popup → change ASR model to `medium` or `base`.

## Uninstall
```bash
bash uninstall.sh
```

## Credits
- [kangchainx/video-text-chrome-extension](https://github.com/kangchainx/video-text-chrome-extension) — architecture reference (MIT)
- [IndieKKY/bilibili-subtitle](https://github.com/IndieKKY/bilibili-subtitle) — Bilibili API reference
- [yt-dlp](https://github.com/yt-dlp/yt-dlp), [mlx-whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper), [coddingtonbear/obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api)
