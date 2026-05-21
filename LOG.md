# Bili Clipper — 项目进度日志

> 内部进度看板。记录每个 Task 的执行状态、结果、问题。
> 对外文档见 README.md。

---

## 进度总览

| Task | 内容 | 状态 |
|------|------|------|
| Task 1 | Project Setup | ✅ 完成 |
| Task 2 | Python Server — /health | ⬜ 待开始 |
| Task 3 | writer.py — 笔记格式化 + 写入 | ⬜ 待开始 |
| Task 4 | transcriber.py — yt-dlp + Whisper | ⬜ 待开始 |
| Task 5 | server.py — /clip 端点串联 | ⬜ 待开始 |
| Task 6 | Chrome 扩展 — Manifest + Icons | ⬜ 待开始 |
| Task 7 | content.js — Bilibili API Helpers | ⬜ 待开始 |
| Task 8 | content.js — Clip Bar UI + 状态机 | ⬜ 待开始 |
| Task 9 | background.js + Popup | ⬜ 待开始 |
| Task 10 | install.sh + uninstall.sh | ⬜ 待开始 |
| Task 11 | E2E 测试 + README | ⬜ 待开始 |

---

## Task 1 — Project Setup ✅

**目标：** git 初始化 + .gitignore + README stub

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | git init + .gitignore | ✅ |
| Step 2 | stub README.md | ✅ |
| Step 3 | initial commit | ✅ |

**结果：**
- Commit: `chore: project scaffold`
- .gitignore 覆盖：`__pycache__/`, `.venv/`, `.DS_Store`, `*.log` 等

**问题：** 无

---

## Task 2 — Python Server /health ⬜

**目标：** FastAPI 骨架，`/health` 端点可响应

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 写 server/requirements.txt | ⬜ |
| Step 2 | 写 server/server.py（/health only） | ⬜ |
| Step 3 | uv venv + 安装依赖 | ⬜ |
| Step 4 | 验证 /health 响应 | ⬜ |
| Step 5 | commit | ⬜ |

**完成标准：**
```
curl http://localhost:27182/health
→ {"status":"ok","model":"large-v3-turbo"}
```

**结果：** —

**问题：** —

---

## Task 3 — writer.py ⬜

**目标：** 格式化 markdown 笔记并写入 Obsidian vault

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 写 tests/test_writer.py（先写失败测试） | ⬜ |
| Step 2 | 运行测试 — 预期 ModuleNotFoundError | ⬜ |
| Step 3 | 写 server/writer.py | ⬜ |
| Step 4 | 运行测试 — 预期 5 passed | ⬜ |
| Step 5 | commit | ⬜ |

**完成标准：**
```
.venv/bin/pytest tests/test_writer.py -v
→ 5 passed
```

**结果：** —

**问题：** —

---

## Task 4 — transcriber.py ⬜

**目标：** yt-dlp 下载音频 + faster-whisper 转录，模型缓存

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 写 tests/test_transcriber.py（mock，不真实下载） | ⬜ |
| Step 2 | 运行测试 — 预期 ModuleNotFoundError | ⬜ |
| Step 3 | 写 server/transcriber.py | ⬜ |
| Step 4 | 运行测试 — 预期 3 passed | ⬜ |
| Step 5 | commit | ⬜ |

**完成标准：**
```
.venv/bin/pytest tests/test_transcriber.py -v
→ 3 passed
```

**结果：** —

**问题：** —

---

## Task 5 — server.py /clip 端点 ⬜

**目标：** /clip 端点串联 transcriber + writer

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 替换 server.py 为完整版本（含 /clip） | ⬜ |
| Step 2 | curl 测试 /clip 快速路径（已有字幕） | ⬜ |
| Step 3 | commit | ⬜ |

**完成标准：**
```
curl POST /clip（带 transcript 字段）
→ {"success":true,"path":"Raw/Test Video.md"}
文件实际存在于 /tmp/test-vault/Raw/
```

**结果：** —

**问题：** —

---

## Task 6 — Chrome 扩展 Manifest + Icons ⬜

**目标：** extension/ 骨架能在 Chrome 加载无报错

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 写 extension/manifest.json | ⬜ |
| Step 2 | Python 脚本生成占位 icon（16/48/128px） | ⬜ |
| Step 3 | Chrome 加载扩展，确认无报错 | ⬜ |
| Step 4 | commit | ⬜ |

**完成标准：**
- `chrome://extensions` 显示扩展，无 error 标记

**结果：** —

**问题：** —

---

## Task 7 — content.js Bilibili API Helpers ⬜

**目标：** getBvId / getVideoInfo / getSubtitleList / fetchSubtitleText / isServerRunning / getSettings

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 写 extension/content.js（API helpers 部分） | ⬜ |
| Step 2 | B站视频页 DevTools Console 手动验证 | ⬜ |
| Step 3 | commit | ⬜ |

**完成标准：**
```javascript
// DevTools Console 验证
getBvId()           // → "BV1xx..."
getVideoInfo(...)   // → {cid: ..., title: "..."}
getSubtitleList(...) // → [] 或 [{subtitle_url, lan, ...}]
```

**结果：** —

**问题：** —

---

## Task 8 — content.js Clip Bar UI + 状态机 ⬜

**目标：** 注入 Clip bar；完整状态机（loading / idle / processing / success / error）

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 追加 Clip Bar UI 代码到 content.js | ⬜ |
| Step 2 | Chrome 重载扩展 + B站视频页目视验证 | ⬜ |
| Step 3 | commit | ⬜ |

**完成标准：**
- Clip bar 出现在视频标题下方（紫色边框）
- CC 字幕视频 → 绿色 "CC 字幕 ✓" badge
- 无字幕视频 → 黄色 "Whisper 转录" badge
- 点击 Clip → 走通完整流程

**结果：** —

**问题：** —

---

## Task 9 — background.js + Popup ⬜

**目标：** MV3 service worker + 设置面板 + 服务健康检测

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 写 extension/background.js | ⬜ |
| Step 2 | 写 extension/popup.html | ⬜ |
| Step 3 | 写 extension/popup.js | ⬜ |
| Step 4 | 重载扩展 + 验证 popup 和健康检测 | ⬜ |
| Step 5 | commit | ⬜ |

**完成标准：**
- 点击扩展图标 → popup 打开，所有字段正常
- 服务运行时 → 绿点 + "本地服务运行中 · :27182"
- 服务未运行 → 红点 + "本地服务未运行"

**结果：** —

**问题：** —

---

## Task 10 — install.sh + uninstall.sh ⬜

**目标：** 一键安装 Python 环境 + 注册 launchd 开机自启

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | 写 install.sh | ⬜ |
| Step 2 | 写 uninstall.sh | ⬜ |
| Step 3 | chmod +x | ⬜ |
| Step 4 | 端到端测试 bash install.sh | ⬜ |
| Step 5 | commit | ⬜ |

**完成标准：**
```
bash install.sh
→ ✓ 服务运行中 → http://localhost:27182
→ === 安装完成 ✓ ===
```

**结果：** —

**问题：** —

---

## Task 11 — E2E 测试 + README ⬜

**目标：** 完整端到端验证 + 最终 README.md

| 步骤 | 描述 | 状态 |
|------|------|------|
| Step 1 | E2E：有字幕视频 clip → vault 写入成功 | ⬜ |
| Step 2 | E2E：无字幕视频 clip → Whisper 转录写入成功 | ⬜ |
| Step 3 | 写最终 README.md | ⬜ |
| Step 4 | 最终 commit + tag v0.1.0 | ⬜ |

**完成标准：**
- CC 字幕视频：3 秒内绿色成功状态，vault 文件含正确 frontmatter
- Whisper 路径：约 2 分钟后成功，文件正常
- `git tag v0.1.0` 打上

**结果：** —

**问题：** —

---

## 参考 Repo 分析（2026-05-21）

读取了两个参考 repo 的完整源码，发现以下关键信息：

### kangchainx/video-text-chrome-extension
- 架构：native messaging（不是 HTTP server），比我们的方案复杂，不采用
- yt-dlp 有多层 fallback 策略：cookies → android/ios 客户端 → 报错，**我们的 transcriber.py 需要加 fallback**
- faster-whisper 配置：`device="auto"`, `compute_type="int8"`，长音频自动分 chunk（>45 min）
- 用 SQLite 持久化 task 状态 + 进度，超出 MVP 范围，暂不采用

### IndieKKY/bilibili-subtitle
- **⚠️ 计划里 Bilibili API 端点写错了**：
  - 计划用：`/x/player/v2?bvid=${bvid}&cid=${cid}`
  - 实际应用：`/x/player/wbi/v2?aid=${aid}&cid=${cid}`（`aid` 是数字，不是 bvid）
  - 所有 API 调用需加 `credentials: 'include'`（利用用户已登录的 session cookie）
  - 字幕 URL 需过滤空值：`.filter(item => item.subtitle_url)`
  - 字幕 URL 如为 `http://` 需转为 `https://`
- 字幕 content 在 `data.body[].content` 字段，与计划一致

### 对计划的修正
- Task 7 `content.js` 中 `getSubtitleList` 函数需要修正：
  1. 先从 view API 拿到 `aid`（已有）
  2. 用 `wbi/v2?aid=${aid}&cid=${cid}` 获取字幕列表（**不是 `v2?bvid=...`**）
  3. 过滤空 subtitle_url
- Task 4 `transcriber.py` 需加 yt-dlp fallback（android/ios 客户端）

---

## 问题汇总

> 遇到的问题在这里统一归档。

| # | Task | 问题描述 | 状态 | 解决方案 |
|---|------|---------|------|---------|
| 1 | Task 7 | 计划中 Bilibili subtitle API 端点错误（`v2` vs `wbi/v2`，bvid vs aid） | ✅ 已识别 | 执行时使用 `wbi/v2?aid=&cid=`，加 `credentials:'include'` |
| 2 | Task 4 | yt-dlp 无 fallback，遇 B站限制会挂 | ✅ 已识别 | 加 android/ios 客户端 fallback 策略 |

---

*最后更新：2026-05-21 · 参考 repo 读取完成，发现 API 端点问题*
