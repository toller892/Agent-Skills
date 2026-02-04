# Meeting Summarizer

自动监控会议录音文件，使用 Whisper 转录并通过 Claude 生成结构化摘要，发送到 Slack。

**🚀 [快速开始 - 30 分钟上线](QUICKSTART.md)**

## 功能特性

- **自动监控**: 监控 `~/meeting-recordings` 文件夹中的新 mp3 文件
- **智能转录**: 使用 OpenAI Whisper API 进行高质量语音转文字
- **AI 分析**: 使用 Claude API 生成结构化会议摘要
- **即时通知**: 自动发送结果到 Slack
- **成本优化**:
  - 文件哈希去重，避免重复处理
  - 转录结果缓存
  - 支持批量处理模式

## 快速开始

### 1. 安装依赖

```bash
cd meeting-summarizer
pip install -r requirements.txt
```

### 2. 初始化配置

```bash
python scripts/init_config.py
```

这会在 `~/.meeting-summarizer/config.yaml` 创建配置文件。

### 3. 配置 API 密钥

编辑 `~/.meeting-summarizer/config.yaml`，填入你的 API 密钥：

```yaml
openai:
  api_key: "sk-..."

anthropic:
  api_key: "sk-ant-..."

slack:
  webhook_url: "https://hooks.slack.com/services/..."

monitoring:
  folder: "~/meeting-recordings"
  check_interval: 60

processing:
  cache_transcripts: true
  cache_dir: "~/.meeting-summarizer/cache"
```

或者使用环境变量：

```bash
export OPENAI_API_KEY='sk-...'
export ANTHROPIC_API_KEY='sk-ant-...'
export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'
```

### 4. 启动监控

```bash
python scripts/monitor_meetings.py
```

系统会自动监控 `~/meeting-recordings` 文件夹，处理新的 mp3 文件。

## 使用方式

### 自动监控模式

```bash
python scripts/monitor_meetings.py
```

将 mp3 文件放入 `~/meeting-recordings` 文件夹，系统会自动处理。

### 手动处理单个文件

```bash
python scripts/process_meeting.py /path/to/meeting.mp3
```

## 输出格式

系统会生成以下内容：

### 1. 会议摘要
2-3 段话概括会议的主要内容和讨论重点

### 2. 关键决策点
列出会议中做出的重要决策

### 3. 行动项
包含以下信息：
- 行动项描述
- 负责人
- 截止日期

## 成本控制

### 转录成本（Whisper API）
- 价格: $0.006 / 分钟
- 1 小时会议 ≈ $0.36

### 分析成本（Claude API）
- Claude Sonnet 4.5: $3 / MTok (输入), $15 / MTok (输出)
- 1 小时转录约 10K tokens
- 单次分析 ≈ $0.03-0.05

### 优化策略
1. **缓存转录结果**: 避免重复转录同一文件
2. **文件哈希检查**: 自动识别已处理文件
3. **批量处理**: 可以关闭实时监控，定期批量处理

## 目录结构

```
meeting-summarizer/
├── SKILL.md                    # Skill 定义
├── README.md                   # 使用说明
├── requirements.txt            # 依赖包
├── meeting_summarizer/         # 核心模块
│   ├── __init__.py
│   ├── transcriber.py         # Whisper 转录
│   ├── analyzer.py            # Claude 分析
│   ├── notifier.py            # Slack 通知
│   ├── monitor.py             # 文件监控
│   └── processor.py           # 主处理流程
└── scripts/                    # 可执行脚本
    ├── init_config.py         # 初始化配置
    ├── process_meeting.py     # 处理单个文件
    └── monitor_meetings.py    # 监控模式
```

## 配置说明

### config.yaml

```yaml
# OpenAI API 配置
openai:
  api_key: "your-openai-api-key"

# Anthropic API 配置
anthropic:
  api_key: "your-anthropic-api-key"

# Slack 配置
slack:
  webhook_url: "your-slack-webhook-url"

# 监控配置
monitoring:
  folder: "~/meeting-recordings"  # 监控文件夹
  check_interval: 60              # 检查间隔（秒）

# 处理配置
processing:
  cache_transcripts: true                    # 是否缓存转录结果
  cache_dir: "~/.meeting-summarizer/cache"  # 缓存目录
```

## 获取 API 密钥

### OpenAI API Key
1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API key
3. 确保账户有余额

### Anthropic API Key
1. 访问 https://console.anthropic.com/
2. 创建新的 API key
3. 确保账户有余额

### Slack Webhook URL
1. 访问 https://api.slack.com/apps
2. 创建新应用或选择现有应用
3. 启用 Incoming Webhooks
4. 添加新的 Webhook 到工作区
5. 复制 Webhook URL

## 故障排查

### 问题: 转录失败
- 检查 OpenAI API key 是否正确
- 确认账户有余额
- 检查音频文件格式（支持 mp3, mp4, wav, m4a 等）

### 问题: 分析失败
- 检查 Anthropic API key 是否正确
- 确认账户有余额
- 检查转录文本是否过长（Claude 有 token 限制）

### 问题: Slack 通知失败
- 检查 Webhook URL 是否正确
- 确认 Webhook 未被禁用
- 检查网络连接

## 高级用法

### 自定义分析提示词

编辑 `meeting_summarizer/analyzer.py` 中的 `_build_prompt` 方法，自定义分析提示词。

### 支持其他音频格式

Whisper API 支持多种格式：mp3, mp4, mpeg, mpga, m4a, wav, webm

### 批量处理历史文件

```python
from pathlib import Path
from meeting_summarizer.processor import MeetingProcessor
import yaml

# Load config
with open(Path.home() / '.meeting-summarizer' / 'config.yaml') as f:
    config = yaml.safe_load(f)

# Create processor
processor = MeetingProcessor(config)

# Process all mp3 files
for file in Path('~/meeting-recordings').expanduser().glob('*.mp3'):
    processor.process(str(file))
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
