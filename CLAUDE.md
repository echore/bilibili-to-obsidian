# Bili Clipper — 项目协作契约

## 项目名称
Bili Clipper

## 一句话目标
Chrome 扩展：在 B站视频页注入 Clip bar，提取字幕或本地 Whisper 转录，写入 Obsidian vault。

## 技术栈
- 框架：FastAPI / Chrome Manifest V3
- 语言：Python 3.11+ / vanilla JS / bash
- 部署平台：本地 macOS launchd daemon（端口 27182）
- 其他工具：uv / uvicorn / faster-whisper / yt-dlp

## 设计文档
`/Users/liyachen/Documents/Obsidian Vault/Raw/Superpower/2026-05-20-bili-clipper-design.md`

## 执行计划
`docs/superpowers/plans/2026-05-20-bili-clipper.md`

## 敏感数据情况
- 是否有 API 密钥：否（Bilibili API 公开，无需 key）
- 是否有数据库：否
- 其他敏感信息：无

## 文件结构

```
bili-clipper/
├── extension/
│   ├── manifest.json
│   ├── content.js
│   ├── background.js
│   ├── popup.html
│   ├── popup.js
│   └── icons/
├── server/
│   ├── server.py
│   ├── transcriber.py
│   ├── writer.py
│   └── requirements.txt
├── tests/
│   ├── test_writer.py
│   └── test_transcriber.py
├── install.sh
├── uninstall.sh
└── README.md
```

## 阶段划分

### Task 1: Project Setup ✅ DONE
- commit: `chore: project scaffold`

### Task 2: Python Server — /health Endpoint
目标：FastAPI 骨架，/health 端点可响应
完成标准：`curl http://localhost:27182/health` 返回 `{"status":"ok","model":"large-v3-turbo"}`

### Task 3: writer.py — Note Formatter + Vault Writer
目标：写入格式化 markdown 笔记到 Obsidian vault
完成标准：`pytest tests/test_writer.py -v` 全部通过（5 passed）

### Task 4: transcriber.py — yt-dlp + faster-whisper
目标：模型缓存 + 音频转录
完成标准：`pytest tests/test_transcriber.py -v` 全部通过（3 passed）

### Task 5: server.py — Wire /clip Endpoint
目标：/clip 端点串联 transcriber + writer
完成标准：curl POST /clip（带 transcript 快速路径）返回 `{"success":true,"path":"Raw/...md"}`；文件实际存在于 /tmp/test-vault/

### Task 6: Chrome Extension — Manifest + Icons
目标：extension/ 骨架，能在 Chrome 加载无报错
完成标准：chrome://extensions 显示扩展正常加载，无 error

### Task 7: content.js — Bilibili API Helpers
目标：getBvId / getVideoInfo / getSubtitleList / fetchSubtitleText
完成标准：在 B站视频页 DevTools Console 中调用 API helpers 返回正确数据

### Task 8: content.js — Clip Bar UI + State Machine
目标：Clip bar 注入 + 完整状态机（loading/idle/processing/success/error）
完成标准：Clip bar 在 B站视频页出现；CC 字幕视频显示绿色 badge；点击 Clip 流程走通

### Task 9: background.js + Popup
目标：service worker + 设置面板 + 服务健康检测
完成标准：popup 正常打开；服务运行时绿点，未运行时红点

### Task 10: install.sh + uninstall.sh
目标：一键安装 Python env + 注册 launchd daemon
完成标准：`bash install.sh` 最终输出 `✓ 服务运行中 → http://localhost:27182`

### Task 11: End-to-End Test + README
目标：完整 E2E 验证 + 最终 README
完成标准：CC 字幕视频 clip 成功写入 vault；Whisper 路径 clip 成功；README 完整

## 协作原则

1. **长期主义** — 每个决策都要考虑开源用户、安全与隐私、可维护性。不只解决眼前问题。

2. **先调研再提案** — 不确定时先搜索真实案例，再提方案。提案时显式说明置信度。

3. **先写计划再执行** — 用 `superpowers:writing-plans` skill 写计划，执行前确认验收标准（"done" 长什么样）。

4. **进度可见** — 及时更新 LOG.md，重要节点 commit，让进度随时可追溯。

5. **卡住时问"为什么"** — 遇到障碍，先停下来问清楚根本原因，不要一直在"怎么做"上打转。

6. **验证假设** — 实现后必须验证效果真的符合预期，不能只说"应该好了"。

7. **读源再提案** — 对现有文件提改动前，先读原文，不凭印象改。

8. **改动要小** — 大改拆成小步，每步可验证、可回滚。

9. **用对 SuperPower Skills** — 调研、计划、调试、并行任务等场景，用对应的 skill，不跳过。

## 沟通约定
- 每步完成后汇报：测试结果（命令 + 输出）+ 潜在风险
- 出问题时：先复现，再分析原因，再动手修复
- 编辑现有文件前：先说明改什么、为什么

## 回滚机制
- 工具：Git
- 每个 Task 完成后 commit，message 格式：`feat/chore/docs(scope): 描述`

## 本项目专属 DoD
- 类型检查命令：无（vanilla JS + Python，不用 mypy/tsc）
- 测试命令：`.venv/bin/pytest tests/ -v`
- 本地预览方式：curl localhost:27182/health；Chrome DevTools Console；B站视频页目视验证
- 验收方式：API 返回值检查 + 浏览器操作验证

## Session 交接记录

### Session 1（2026-05-21）
**这次做了什么：**
- 读取并理解完整执行计划（docs/superpowers/plans/2026-05-20-bili-clipper.md）
- 建立 CLAUDE.md 项目协作契约

**下一步：**
- Task 2: 创建 server/requirements.txt + server/server.py（/health endpoint）
- 配置 Python 虚拟环境（uv）

**当前状态：**
- 最新 commit：`chore: project scaffold`
- Task 1 完成，Tasks 2–11 待开始
