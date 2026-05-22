# Bili Clipper

Chrome extension that clips Bilibili video transcripts directly to Obsidian.

- **Videos with CC subtitles** — extracts in ~2 seconds
- **Videos without subtitles** — local Whisper transcription (~2 min on M2 8GB), no API needed
- **Open source, free, local** — no data leaves your machine

## Requirements

- macOS (Apple Silicon M1/M2/M3 recommended; Intel works but slower)
- Python 3.11+
- Chrome
- [Obsidian](https://obsidian.md)

## Install

**Step 1 — Local server:**
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_HANDLE/bili-clipper/main/install.sh | bash
```
Installs the Python server as a background service that auto-starts with your Mac.
First run downloads the Whisper `large-v3-turbo` model (~1.6 GB).

**Step 2 — Chrome extension:**
1. Open `chrome://extensions`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked** → select the `extension/` folder from this repo

**Step 3 — Configure:**
Click the Bili Clipper icon in Chrome toolbar → enter your **Obsidian vault name** (the folder name shown in the Obsidian title bar).

## Usage

Navigate to any Bilibili video. A **Clip bar** appears below the title. Click **Clip**.

- The note is written to `Raw/[video title].md` in your vault and Obsidian opens automatically
- Videos with CC subtitles complete in ~2 seconds; Whisper transcription takes ~2 minutes

## Output format

```markdown
---
title: "如何快速学习陌生领域"
source: https://www.bilibili.com/video/BVxxx
platform: bilibili
author: "UP主名字"
date: 2026-05-22
tags: [transcript, bilibili]
transcript_method: cc_subtitle
---

<iframe src="https://player.bilibili.com/player.html?bvid=BVxxx&..." ...></iframe>

## 简介
视频描述文字（仅在有简介时出现）

## 字幕

### 章节名 `0:00`
合并后的段落文字…

### 章节名 `5:30`
合并后的段落文字…
```

Videos without chapters show the transcript as time-gap-merged paragraphs directly under `## 字幕`.

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

**Obsidian doesn't open automatically**
Make sure Obsidian is running and the vault name in the extension popup matches exactly.

**Whisper too slow / out of memory**
Open extension popup → change ASR model to `medium` or `base`.

## Uninstall
```bash
bash uninstall.sh
```

## Credits
- [haixiong1997/Bilibili-Obsidian-Clipper](https://github.com/haixiong1997/Bilibili-Obsidian-Clipper) — note format reference
- [kangchainx/video-text-chrome-extension](https://github.com/kangchainx/video-text-chrome-extension) — architecture reference (MIT)
- [IndieKKY/bilibili-subtitle](https://github.com/IndieKKY/bilibili-subtitle) — Bilibili API reference
- [yt-dlp](https://github.com/yt-dlp/yt-dlp), [mlx-whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper)
