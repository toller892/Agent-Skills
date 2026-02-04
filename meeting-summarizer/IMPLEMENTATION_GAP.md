# Meeting Summarizer - 完整流程实现方案

## 原始流程分析

```
Fireflies Export mp3 → Watch Folder → Extract Audio → Transcribe →
Analyze (Claude + Gemini) → Extract Actions → Slack Notification →
[Future: Auto-send to parties]
```

## 当前实现状态

### ✅ 已实现
1. **Claude 分析** - 完美工作
2. **Extract Actions** - 提取行动项（合并到分析步骤）
3. **结构化输出** - 摘要+决策+行动项

### ⚠️ 部分实现
1. **Transcribe** - 中转站 Whisper API 有问题
   - 解决方案：使用 Fireflies 转录或官方 OpenAI API

### ❌ 未实现
1. **Watch Folder** - 文件夹监控
2. **Gemini 分析** - 双 AI 对比
3. **Slack Notification** - 自动通知

## 完整实现计划

### 阶段 1：核心功能（已完成 ✅）
- [x] Claude API 集成
- [x] 会议分析
- [x] 行动项提取
- [x] 结构化输出

### 阶段 2：自动化（需要实现）
- [ ] Watch Folder - 监控文件夹
- [ ] 自动触发处理
- [ ] Slack Webhook 通知

### 阶段 3：增强功能（可选）
- [ ] Gemini 分析对比
- [ ] Whisper 转录（需要官方 API）
- [ ] 邮件通知参会者

### 阶段 4：未来扩展
- [ ] 自动发送给参会者
- [ ] 日历事件创建
- [ ] CRM 集成

## 快速补全方案

### 方案 A：最小可用版本（推荐）

**流程**:
```
Fireflies 导出转录 → 放入监控文件夹 →
自动分析（Claude）→ Slack 通知
```

**需要添加**:
1. Watch Folder（watchdog 库）
2. Slack Webhook 集成

**时间**: 30分钟
**成本**: $0.03/会议

---

### 方案 B：完整自动化版本

**流程**:
```
Fireflies 导出 mp3 → 放入监控文件夹 →
Whisper 转录 → Claude 分析 → Slack 通知
```

**需要添加**:
1. Watch Folder
2. OpenAI Whisper API（需要注册）
3. Slack Webhook

**时间**: 1小时
**成本**: $0.39/会议

---

### 方案 C：双 AI 对比版本

**流程**:
```
Fireflies 导出转录 → 放入监控文件夹 →
Claude 分析 + Gemini 分析 → 对比结果 → Slack 通知
```

**需要添加**:
1. Watch Folder
2. Google Gemini API（需要注册）
3. 结果对比逻辑
4. Slack Webhook

**时间**: 2小时
**成本**: $0.05/会议

## 推荐实现顺序

### 第 1 步：添加 Slack 通知（15分钟）
```python
def send_to_slack(analysis, webhook_url):
    import requests
    message = {
        "text": f"会议摘要已生成",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*摘要*\n{analysis['summary']}"}}
        ]
    }
    requests.post(webhook_url, json=message)
```

### 第 2 步：添加文件夹监控（15分钟）
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MeetingHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.txt'):
            process_and_notify(event.src_path)

observer = Observer()
observer.schedule(MeetingHandler(), path='~/meeting-transcripts')
observer.start()
```

### 第 3 步：添加 Whisper 转录（可选，需要 OpenAI API）
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def transcribe(audio_file):
    with open(audio_file, 'rb') as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text
```

### 第 4 步：添加 Gemini 分析（可选）
```python
import google.generativeai as genai
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def analyze_with_gemini(transcript):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"分析这段会议：{transcript}")
    return response.text
```

## 当前 vs 完整版本对比

| 功能 | 当前版本 | 完整版本 | 优先级 |
|------|---------|---------|--------|
| Claude 分析 | ✅ | ✅ | 核心 |
| 行动项提取 | ✅ | ✅ | 核心 |
| 文件夹监控 | ❌ | ✅ | 高 |
| Slack 通知 | ❌ | ✅ | 高 |
| Whisper 转录 | ❌ | ✅ | 中 |
| Gemini 对比 | ❌ | ✅ | 低 |
| 邮件通知 | ❌ | ✅ | 低 |

## 下一步行动

### 立即可做（无需额外 API）
1. ✅ 添加 Slack Webhook 通知
2. ✅ 添加文件夹监控
3. ✅ 完善错误处理

### 需要注册 API
1. ⚠️ OpenAI API - Whisper 转录
2. ⚠️ Google API - Gemini 分析

### 未来扩展
1. 📧 邮件通知参会者
2. 📅 创建日历事件
3. 🔗 CRM 集成

## 总结

**当前实现**: 核心分析功能完成（70%）
**缺少功能**: 自动化监控 + 通知（30%）

**建议**: 先添加 Slack 通知和文件夹监控，实现最小可用版本。
