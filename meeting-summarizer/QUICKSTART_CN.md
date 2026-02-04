# Meeting Summarizer 快速开始指南

## 功能概述

自动将会议录音转换为结构化摘要，包括：
- 会议摘要（2-3段概述）
- 关键决策点
- 行动项（任务 + 负责人 + 截止日期）
- 自动发送到 Slack

## 5分钟快速设置

### 1. 安装依赖

```bash
cd /mnt/d/Code/skills/meeting-summarizer
pip install -r requirements.txt
```

### 2. 配置 API 密钥

**方法 A：使用环境变量（推荐）**

```bash
export OPENAI_API_KEY='sk-...'
export ANTHROPIC_API_KEY='sk-ant-...'
export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'
```

**方法 B：编辑配置文件**

```bash
python scripts/init_config.py
nano ~/.meeting-summarizer/config.yaml
```

### 3. 处理你的第一个录音

```bash
python scripts/process_meeting.py "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"
```

## 使用场景

### 场景 1：处理单个 Fireflies 导出文件

```bash
# 从 Fireflies 下载 mp3 文件到本地
# 然后运行：
python scripts/process_meeting.py /path/to/meeting.mp3
```

### 场景 2：自动监控文件夹

```bash
# 1. 配置监控文件夹（默认 ~/meeting-recordings）
mkdir -p ~/meeting-recordings

# 2. 启动监控
python scripts/monitor_meetings.py

# 3. 将 Fireflies 导出的 mp3 文件放入该文件夹
# 系统会自动处理并发送到 Slack
```

### 场景 3：批量处理历史录音

```bash
# 将所有历史录音放入监控文件夹
# 然后运行：
python scripts/process_all.py
```

## 工作流程

```
Fireflies 导出 mp3
    ↓
放入监控文件夹 (或手动指定文件)
    ↓
Whisper API 转录 (自动检测语言)
    ↓
Claude Sonnet 4.5 分析
    ↓
生成结构化摘要
    ↓
发送到 Slack
```

## 成本估算

- **单次处理（1小时会议）**: ~$0.39
  - Whisper 转录: $0.36
  - Claude 分析: $0.03

- **月度成本（20次会议）**: ~$8

## 输出示例

```json
{
  "summary": "会议讨论了新产品功能的优先级...",
  "decisions": [
    "决定优先开发移动端功能",
    "推迟桌面端更新到Q2"
  ],
  "action_items": [
    {
      "description": "完成移动端原型设计",
      "assignee": "张三",
      "deadline": "2026-02-15"
    },
    {
      "description": "准备用户测试方案",
      "assignee": "李四",
      "deadline": "2026-02-20"
    }
  ]
}
```

## 常见问题

### Q: 支持哪些音频格式？
A: mp3, m4a, wav, mp4, mpeg, mpga, webm

### Q: 如何避免重复处理？
A: 系统会自动计算文件哈希，缓存转录结果，避免重复处理

### Q: 转录支持哪些语言？
A: Whisper 支持 99+ 种语言，自动检测

### Q: 如果不需要 Slack 通知怎么办？
A: 可以不配置 SLACK_WEBHOOK_URL，系统会跳过通知步骤

### Q: 大文件处理超时怎么办？
A: 编辑 `meeting_summarizer/transcriber.py`，增加 timeout 参数

## 获取 API 密钥

### OpenAI (Whisper)
1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API key
3. 确保账户有余额

### Anthropic (Claude)
1. 访问 https://console.anthropic.com/settings/keys
2. 创建新的 API key
3. 确保账户有余额

### Slack Webhook
1. 访问 https://api.slack.com/apps
2. Create New App
3. 选择 "Incoming Webhooks"
4. Add New Webhook to Workspace
5. 复制 Webhook URL

## 高级配置

### 自定义分析提示词

编辑 `meeting_summarizer/analyzer.py` 中的 system prompt：

```python
system_prompt = """
你是一个专业的会议分析助手。
请根据转录文本生成：
1. 简洁的会议摘要
2. 关键决策点
3. 具体的行动项（包含负责人和截止日期）
"""
```

### 调整缓存策略

编辑 `~/.meeting-summarizer/config.yaml`：

```yaml
processing:
  cache_transcripts: true  # 是否缓存转录结果
  cache_dir: "~/.meeting-summarizer/cache"  # 缓存目录
```

## 故障排查

### 错误：OPENAI_API_KEY not set
**解决方案**: 设置环境变量或编辑 config.yaml

### 错误：Transcription failed
**可能原因**:
- API key 无效
- 账户余额不足
- 音频格式不支持
- 网络连接问题

### 错误：Analysis failed
**可能原因**:
- Anthropic API key 无效
- 转录文本过长（超过 200k tokens）
- 账户余额不足

### Slack 通知未收到
**检查项**:
- Webhook URL 是否正确
- Webhook 是否被禁用
- 网络连接是否正常

## 生产环境部署

参考 `DEPLOYMENT.md` 了解：
- systemd 服务配置
- Docker 容器化部署
- 日志管理
- 监控告警
