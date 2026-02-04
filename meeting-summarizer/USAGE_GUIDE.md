# Meeting Summarizer - 使用指南

## 当前状态

✅ Skill 已创建并部署
✅ 依赖已安装（在虚拟环境中）
⚠️ 需要配置 API keys

## 快速开始

### 方法 1：使用环境变量（推荐）

```bash
# 1. 设置 API keys
export OPENAI_API_KEY='sk-proj-...'  # 你的 OpenAI API key
export ANTHROPIC_API_KEY='sk-ant-...'  # 你的 Anthropic API key
export SLACK_WEBHOOK_URL='https://hooks.slack.com/...'  # 可选

# 2. 激活虚拟环境
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate

# 3. 处理录音文件
python scripts/process_meeting.py "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"
```

### 方法 2：使用配置文件

```bash
# 1. 初始化配置
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate
python scripts/init_config.py

# 2. 编辑配置文件
nano ~/.meeting-summarizer/config.yaml

# 填入以下内容：
# openai:
#   api_key: "sk-proj-..."
# anthropic:
#   api_key: "sk-ant-..."
# slack:
#   webhook_url: "https://hooks.slack.com/..."  # 可选

# 3. 处理录音文件
python scripts/process_meeting.py "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"
```

## 获取 API Keys

### OpenAI API Key
1. 访问 https://platform.openai.com/api-keys
2. 点击 "Create new secret key"
3. 复制 key（格式：sk-proj-...）
4. 确保账户有余额（至少 $5）

### Anthropic API Key
1. 访问 https://console.anthropic.com/settings/keys
2. 点击 "Create Key"
3. 复制 key（格式：sk-ant-...）
4. 确保账户有余额（至少 $5）

### Slack Webhook（可选）
1. 访问 https://api.slack.com/apps
2. 创建新应用或选择现有应用
3. 启用 "Incoming Webhooks"
4. 添加新的 Webhook to Workspace
5. 复制 Webhook URL

## 使用示例

### 处理单个文件

```bash
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate

# 确保已设置环境变量
export OPENAI_API_KEY='your-key'
export ANTHROPIC_API_KEY='your-key'

# 处理文件
python scripts/process_meeting.py "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"
```

### 监控文件夹（自动处理）

```bash
# 1. 创建监控文件夹
mkdir -p ~/meeting-recordings

# 2. 启动监控
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate
python scripts/monitor_meetings.py

# 3. 将录音文件放入文件夹
cp "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3" ~/meeting-recordings/

# 系统会自动处理并发送到 Slack
```

### 批量处理历史文件

```bash
# 1. 将所有录音放入监控文件夹
cp *.mp3 ~/meeting-recordings/

# 2. 批量处理
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate
python scripts/process_all.py
```

## 输出示例

处理完成后，你会看到：

```
============================================================
MEETING SUMMARY
============================================================
[2-3段会议概述]

============================================================
KEY DECISIONS
============================================================
1. [决策1]
2. [决策2]
3. [决策3]

============================================================
ACTION ITEMS
============================================================

1. [任务描述]
   Assignee: [负责人]
   Deadline: [截止日期]

2. [任务描述]
   Assignee: [负责人]
   Deadline: [截止日期]
```

同时会生成一个 `*_summary.txt` 文件保存结果。

## 成本估算

- **1小时会议**: ~$0.39
  - Whisper 转录: $0.36
  - Claude 分析: $0.03

- **20次会议/月**: ~$8

## 故障排查

### 错误：OPENAI_API_KEY not set
**解决方案**:
```bash
export OPENAI_API_KEY='sk-proj-...'
```

### 错误：ANTHROPIC_API_KEY not set
**解决方案**:
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

### 错误：Insufficient funds
**解决方案**:
- 检查 OpenAI 账户余额：https://platform.openai.com/account/billing
- 检查 Anthropic 账户余额：https://console.anthropic.com/settings/billing

### 错误：Audio file not found
**解决方案**:
- 确认文件路径正确
- 使用绝对路径
- 检查文件权限

### 转录失败
**可能原因**:
- 音频格式不支持（支持：mp3, m4a, wav, mp4, mpeg, mpga, webm）
- 文件损坏
- 文件过大（>25MB 需要分割）

## 高级配置

### 自定义分析提示词

编辑 `meeting_summarizer/analyzer.py`：

```python
system_prompt = """
你是一个专业的会议分析助手。
请根据转录文本生成：
1. 简洁的会议摘要（2-3段）
2. 关键决策点（列表）
3. 具体的行动项（包含负责人和截止日期）

注意：
- 摘要要突出重点，不要流水账
- 决策点要明确，避免模糊表述
- 行动项要具体可执行
"""
```

### 调整缓存策略

编辑 `~/.meeting-summarizer/config.yaml`：

```yaml
processing:
  cache_transcripts: true  # 是否缓存转录结果
  cache_dir: "~/.meeting-summarizer/cache"  # 缓存目录
```

### 修改监控间隔

编辑 `~/.meeting-summarizer/config.yaml`：

```yaml
monitoring:
  folder: "~/meeting-recordings"  # 监控文件夹
  check_interval: 60  # 检查间隔（秒）
```

## 下一步

1. **获取 API keys** - 从 OpenAI 和 Anthropic 获取
2. **设置环境变量** - 或编辑配置文件
3. **测试处理** - 使用提供的录音文件
4. **配置 Slack** - 可选，用于自动通知
5. **开始使用** - 处理实际的会议录音

## 文件位置

- **Skill 目录**: `~/.claude/skills/meeting-summarizer/`
- **配置文件**: `~/.meeting-summarizer/config.yaml`
- **缓存目录**: `~/.meeting-summarizer/cache/`
- **虚拟环境**: `~/.claude/skills/meeting-summarizer/venv/`
- **测试录音**: `/mnt/d/Code/skills/2026_1_30 14_27_47.mp3`

## 支持的音频格式

- mp3
- m4a
- wav
- mp4
- mpeg
- mpga
- webm

## 支持的语言

Whisper 支持 99+ 种语言，自动检测：
- 中文（简体/繁体）
- 英语
- 日语
- 韩语
- 法语
- 德语
- 西班牙语
- 等等...

## 需要帮助？

查看完整文档：
- `QUICKSTART_CN.md` - 快速开始指南
- `WORKFLOW_ANALYSIS.md` - 流程分析
- `COMPLETION_SUMMARY.md` - 项目总结
- `ARCHITECTURE.md` - 架构设计
- `DEPLOYMENT.md` - 部署指南
