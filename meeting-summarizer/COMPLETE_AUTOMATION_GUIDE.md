# Meeting Summarizer - 完整自动化指南

## 🎯 你的原始流程（完整实现）

```
Fireflies Export mp3
    ↓
上传到监控文件夹 (~/meeting-recordings)
    ↓
Watch Folder（自动检测新文件）✅ 已实现
    ↓
Transcribe（Whisper API）✅ 已实现
    ↓
Analyze（Claude）✅ 已实现
    ↓
Extract Actions（提取行动项）✅ 已实现
    ↓
Slack Notification ✅ 已实现
    ↓
[Future: Auto-send to parties] 🔮 未来功能
```

## 🚀 快速开始

### 第 1 步：安装依赖

```bash
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate
pip install watchdog  # 文件夹监控
```

### 第 2 步：配置 API Keys

```bash
# 必需：OpenAI API（用于 Whisper 转录）
export OPENAI_API_KEY='sk-proj-...'

# 可选：Slack Webhook（用于通知）
export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'

# 已有：Claude API（用于分析）
# ANTHROPIC_AUTH_TOKEN 已配置
```

### 第 3 步：启动自动监控

```bash
python auto_monitor.py
```

### 第 4 步：使用

```bash
# 1. 从 Fireflies 下载 mp3 文件
# 2. 放入监控文件夹
cp ~/Downloads/meeting.mp3 ~/meeting-recordings/

# 3. 系统自动处理：
#    - 检测到新文件
#    - Whisper 转录
#    - Claude 分析
#    - 提取行动项
#    - 发送到 Slack
#    - 保存摘要文件
```

## 📋 完整功能清单

| 功能 | 状态 | 说明 |
|------|------|------|
| Watch Folder | ✅ | 自动监控 ~/meeting-recordings |
| Transcribe (Whisper) | ✅ | 需要 OPENAI_API_KEY |
| Analyze (Claude) | ✅ | 已配置 mmkg.cloud |
| Extract Actions | ✅ | 自动提取行动项 |
| Slack Notification | ✅ | 需要 SLACK_WEBHOOK_URL |
| Save Summary | ✅ | 自动保存 txt 文件 |
| Deduplication | ✅ | 文件哈希去重 |
| Cache | ✅ | 避免重复处理 |

## 🔧 配置说明

### OpenAI API Key（必需）

**用途**: Whisper 语音转文字

**获取方式**:
1. 注册：https://platform.openai.com/signup
2. 获取 key：https://platform.openai.com/api-keys
3. 充值至少 $5

**设置**:
```bash
export OPENAI_API_KEY='sk-proj-...'
```

**成本**: $0.006/分钟（1小时会议 = $0.36）

---

### Slack Webhook（可选）

**用途**: 自动发送摘要到 Slack

**获取方式**:
1. 访问：https://api.slack.com/apps
2. Create New App
3. Incoming Webhooks → Add New Webhook
4. 复制 Webhook URL

**设置**:
```bash
export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'
```

**成本**: 免费

---

### Claude API（已配置）

**用途**: AI 分析和提取行动项

**当前配置**:
- Token: your_claude_api_token_here
- Base URL: https://api.anthropic.com

**成本**: ~$0.03/小时会议

## 📊 成本分析

### 完整自动化方案

**单次处理（1小时会议）**:
- Whisper 转录: $0.36
- Claude 分析: $0.03
- Slack 通知: $0.00
- **总计: $0.39**

**月度成本（20次会议）**:
- **总成本: ~$8/月**
- 对比人工: $200+/月
- **节省: 96%**

### 半自动方案（无 Whisper）

如果不想注册 OpenAI，可以：

**流程**:
```
Fireflies 导出转录文本 → 放入文件夹 →
Claude 分析 → Slack 通知
```

**成本**: ~$0.03/会议（只有 Claude）

## 🎬 使用场景

### 场景 1：完全自动化

```bash
# 1. 启动监控
python auto_monitor.py

# 2. Fireflies 录制会议后，下载 mp3

# 3. 放入监控文件夹
cp ~/Downloads/meeting_2026-02-04.mp3 ~/meeting-recordings/

# 4. 自动完成：
#    ✓ 转录
#    ✓ 分析
#    ✓ 提取行动项
#    ✓ Slack 通知
#    ✓ 保存文件
```

### 场景 2：批量处理

```bash
# 1. 将多个 mp3 文件放入文件夹
cp ~/Downloads/*.mp3 ~/meeting-recordings/

# 2. 启动监控
python auto_monitor.py

# 3. 系统依次处理所有文件
```

### 场景 3：手动处理单个文件

```bash
# 如果不想启动监控，可以手动处理
python -c "
from auto_monitor import process_audio_file
process_audio_file('~/meeting-recordings/meeting.mp3')
"
```

## 📱 Slack 通知示例

处理完成后，Slack 会收到：

```
📝 会议摘要: meeting_2026-02-04.mp3

会议摘要
本次会议讨论了项目进度和技术优化...

✅ 关键决策点
• 采用Redis缓存方案
• 增加2名开发人员

🎯 行动项
• 优化数据库查询性能
  👤 张三 | 📅 2026-02-10
• 完成Redis缓存集成
  👤 李四 | 📅 2026-02-12
```

## 🔍 监控日志示例

```
============================================================
Meeting Summarizer - Auto Monitor
============================================================

📁 Monitoring folder: /home/tony0523/meeting-recordings
💾 Cache directory: /home/tony0523/.meeting-summarizer/cache

✓ Ready! Drop audio files into: /home/tony0523/meeting-recordings
  Press Ctrl+C to stop

🔔 New file detected: meeting_2026-02-04.mp3

============================================================
Processing: meeting_2026-02-04.mp3
============================================================
  [1/3] Transcribing audio...
  ✓ Transcription complete (4521 characters)
  [2/3] Analyzing with Claude...
  ✓ Claude analysis complete
  [3/3] Sending to Slack...
  ✓ Slack notification sent

  ✓ Summary saved to: meeting_2026-02-04_summary.txt

============================================================
✓ Processing complete!
============================================================
```

## ⚠️ 故障排查

### 问题 1：OPENAI_API_KEY not set

**症状**: 跳过转录步骤

**解决方案**:
```bash
export OPENAI_API_KEY='sk-proj-...'
```

### 问题 2：Slack notification failed

**症状**: Slack 通知失败

**解决方案**:
1. 检查 Webhook URL 是否正确
2. 测试 Webhook：
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test"}' \
  YOUR_WEBHOOK_URL
```

### 问题 3：File already processed

**症状**: 文件被跳过

**解决方案**:
- 这是正常的去重机制
- 如果需要重新处理，删除缓存：
```bash
rm ~/.meeting-summarizer/processed.json
```

### 问题 4：Transcription timeout

**症状**: 大文件转录超时

**解决方案**:
- 将音频文件分割成小段
- 或增加 timeout 设置

## 🎯 下一步

### 立即可用
1. ✅ 启动自动监控
2. ✅ 处理 Fireflies 导出的 mp3
3. ✅ 接收 Slack 通知

### 未来扩展
1. 📧 邮件通知参会者
2. 📅 自动创建日历事件
3. 🔗 CRM 集成
4. 🤖 Gemini 对比分析

## 📁 文件位置

- **监控脚本**: `~/.claude/skills/meeting-summarizer/auto_monitor.py`
- **监控文件夹**: `~/meeting-recordings/`
- **缓存目录**: `~/.meeting-summarizer/cache/`
- **处理记录**: `~/.meeting-summarizer/processed.json`
- **输出文件**: 与输入文件同目录

## 🎉 开始使用

```bash
# 1. 安装依赖
pip install watchdog

# 2. 设置 API keys
export OPENAI_API_KEY='sk-proj-...'
export SLACK_WEBHOOK_URL='https://hooks.slack.com/...'

# 3. 启动监控
python auto_monitor.py

# 4. 放入音频文件
cp meeting.mp3 ~/meeting-recordings/

# 5. 等待自动处理完成！
```

就这么简单！🚀
