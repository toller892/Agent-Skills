# 会议录音总结流程分析

## 你提出的原始流程

```
Fireflies Export mp3 → Watch Folder → Extract Audio → Transcribe →
Analyze (Claude + Gemini) → Extract Actions → Slack Notification →
[Future: Auto-send to parties]
```

## 可行性分析

### ✅ 可行的部分

1. **Fireflies Export mp3** - 完全可行
   - Fireflies 支持导出 mp3 格式
   - 可以手动下载或使用 API 自动获取

2. **Watch Folder** - 完全可行
   - 使用 Python `watchdog` 库监控文件夹
   - 已在当前实现中包含

3. **Transcribe** - 完全可行
   - OpenAI Whisper API 成熟稳定
   - 支持 99+ 种语言
   - 成本合理（$0.006/分钟）

4. **Analyze** - 完全可行
   - Claude Sonnet 4.5 分析能力强
   - 可以提取摘要、决策、行动项

5. **Slack Notification** - 完全可行
   - Webhook 集成简单
   - 支持富文本格式

### ⚠️ 需要优化的部分

1. **Extract Audio 步骤冗余**
   - Fireflies 已经导出 mp3，无需再次提取
   - **建议**: 删除此步骤

2. **双 AI 分析（Claude + Gemini）**
   - 增加成本和延迟
   - 两个模型结果可能不一致
   - **建议**: 只使用 Claude（质量更高，成本更低）
   - **替代方案**: 如果需要对比，可以在关键会议时手动运行

3. **Extract Actions 独立步骤**
   - 行动项提取应该在 Analyze 阶段完成
   - 无需单独步骤
   - **建议**: 合并到 Analyze 步骤

## 优化后的流程

```
Fireflies Export mp3
    ↓
Watch Folder (监控指定目录)
    ↓
Transcribe (Whisper API)
    ↓
Analyze (Claude Sonnet 4.5)
    ├─ 生成摘要
    ├─ 提取决策点
    └─ 提取行动项（描述 + 负责人 + 截止日期）
    ↓
Format Output (结构化 JSON/Markdown)
    ↓
Slack Notification (富文本消息)
    ↓
[Future Extensions]
    ├─ Email to participants
    ├─ Calendar events for action items
    ├─ CRM integration
    └─ Task management system sync
```

## 实现细节

### 1. Fireflies 集成

**手动方式**（当前实现）:
```bash
# 从 Fireflies 下载 mp3
# 放入监控文件夹
cp ~/Downloads/meeting.mp3 ~/meeting-recordings/
```

**自动方式**（未来扩展）:
```python
# 使用 Fireflies API
import requests

def fetch_fireflies_recordings():
    api_key = os.getenv('FIREFLIES_API_KEY')
    response = requests.get(
        'https://api.fireflies.ai/graphql',
        headers={'Authorization': f'Bearer {api_key}'},
        json={'query': '{ transcripts { id, audio_url } }'}
    )
    # 下载新录音
```

### 2. Watch Folder 实现

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MeetingHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.mp3'):
            process_meeting(event.src_path)

observer = Observer()
observer.schedule(MeetingHandler(), path='~/meeting-recordings')
observer.start()
```

### 3. Transcribe 实现

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def transcribe(audio_file):
    with open(audio_file, 'rb') as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="zh"  # 可选，自动检测
        )
    return transcript.text
```

### 4. Analyze 实现

```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def analyze(transcript):
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        system="你是会议分析专家，提取摘要、决策和行动项",
        messages=[{
            "role": "user",
            "content": f"分析这段会议转录：\n\n{transcript}"
        }]
    )

    # 解析结构化输出
    return {
        "summary": "...",
        "decisions": ["...", "..."],
        "action_items": [
            {"description": "...", "assignee": "...", "deadline": "..."}
        ]
    }
```

### 5. Slack Notification 实现

```python
import requests

def send_to_slack(analysis, webhook_url):
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "会议摘要"}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": analysis['summary']}
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*关键决策*\n" + "\n".join(f"• {d}" for d in analysis['decisions'])
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*行动项*\n" + "\n".join(
                        f"• {item['description']}\n  负责人: {item['assignee']} | 截止: {item['deadline']}"
                        for item in analysis['action_items']
                    )
                }
            }
        ]
    }

    requests.post(webhook_url, json=message)
```

## 成本分析

### 单次处理（1小时会议）

| 服务 | 成本 | 说明 |
|------|------|------|
| Whisper 转录 | $0.36 | $0.006/分钟 × 60分钟 |
| Claude 分析 | $0.03 | ~10k tokens input + 2k output |
| **总计** | **$0.39** | 每次会议 |

### 月度成本（20次会议）

- **总成本**: ~$8/月
- **对比人工**: 人工转录 $200+/月
- **节省**: 96%

### 如果使用双 AI（Claude + Gemini）

| 服务 | 成本 | 说明 |
|------|------|------|
| Whisper 转录 | $0.36 | 同上 |
| Claude 分析 | $0.03 | 同上 |
| Gemini 分析 | $0.02 | Gemini 1.5 Pro |
| **总计** | **$0.41** | 增加 5% 成本 |

**结论**: 双 AI 成本增加不大，但增加复杂度和延迟。建议只在需要对比时使用。

## 未来扩展建议

### 1. 自动发送给参会者

```python
def send_to_participants(analysis, participants):
    for email in participants:
        send_email(
            to=email,
            subject="会议摘要",
            body=format_email(analysis)
        )
```

### 2. 创建日历事件

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_calendar_events(action_items):
    service = build('calendar', 'v3', credentials=creds)

    for item in action_items:
        event = {
            'summary': item['description'],
            'start': {'date': item['deadline']},
            'attendees': [{'email': item['assignee']}]
        }
        service.events().insert(calendarId='primary', body=event).execute()
```

### 3. 任务管理系统集成

```python
# Notion 集成
def create_notion_tasks(action_items):
    for item in action_items:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": item['description']}}]},
                "Assignee": {"people": [{"name": item['assignee']}]},
                "Due Date": {"date": {"start": item['deadline']}}
            }
        )

# Jira 集成
def create_jira_issues(action_items):
    for item in action_items:
        jira.create_issue(
            project='PROJ',
            summary=item['description'],
            assignee={'name': item['assignee']},
            duedate=item['deadline']
        )
```

### 4. CRM 集成

```python
# Salesforce 集成
def update_salesforce(analysis, meeting_id):
    sf.Meeting__c.update(
        meeting_id,
        {
            'Summary__c': analysis['summary'],
            'Decisions__c': '\n'.join(analysis['decisions']),
            'Action_Items__c': json.dumps(analysis['action_items'])
        }
    )
```

## 技术栈建议

### 当前实现
- Python 3.8+
- OpenAI Python SDK (Whisper)
- Anthropic Python SDK (Claude)
- watchdog (文件监控)
- requests (Slack webhook)
- PyYAML (配置管理)

### 未来扩展
- FastAPI (Web API)
- Celery (异步任务队列)
- Redis (缓存和队列)
- PostgreSQL (数据持久化)
- Docker (容器化部署)

## 部署建议

### 开发环境
```bash
python scripts/monitor_meetings.py
```

### 生产环境（systemd）
```ini
[Unit]
Description=Meeting Summarizer
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/meeting-summarizer
ExecStart=/usr/bin/python3 scripts/monitor_meetings.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Docker 部署
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "scripts/monitor_meetings.py"]
```

## 总结

你的原始流程整体可行，主要优化点：

1. ✅ **删除 Extract Audio 步骤** - Fireflies 已提供 mp3
2. ✅ **简化为单 AI 分析** - Claude 足够强大
3. ✅ **合并 Extract Actions** - 在 Analyze 阶段完成
4. ✅ **添加缓存机制** - 避免重复处理
5. ✅ **结构化输出** - 便于后续集成

当前实现已经包含了核心功能，可以直接使用。未来扩展可以根据实际需求逐步添加。
