# Meeting Summarizer - 系统架构

## 系统概览

```
┌─────────────────────────────────────────────────────────────┐
│                    Meeting Summarizer                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Monitor    │─────▶│  Processor   │─────▶│   Notifier   │
│  (watchdog)  │      │              │      │   (Slack)    │
└──────────────┘      └──────────────┘      └──────────────┘
                             │
                             ├─────▶ Transcriber (Whisper)
                             │
                             └─────▶ Analyzer (Claude)
```

## 核心组件

### 1. Monitor (monitor.py)
**职责：** 监控文件系统变化

**功能：**
- 使用 watchdog 监控指定文件夹
- 检测新的 mp3 文件
- 触发处理流程
- 避免重复处理

**关键类：**
- `MeetingMonitor`: 主监控器
- `MeetingFileHandler`: 文件事件处理器

### 2. Transcriber (transcriber.py)
**职责：** 音频转文字

**功能：**
- 调用 OpenAI Whisper API
- 文件哈希计算
- 转录结果缓存
- 元数据提取

**关键方法：**
- `transcribe()`: 转录音频文件
- `_get_file_hash()`: 计算文件哈希
- `_load_from_cache()`: 从缓存加载
- `_save_to_cache()`: 保存到缓存

**成本优化：**
- MD5 哈希避免重复转录
- 本地缓存转录结果
- 支持多种音频格式

### 3. Analyzer (analyzer.py)
**职责：** 分析转录文本

**功能：**
- 调用 Claude API
- 生成结构化摘要
- 提取决策点
- 识别行动项

**关键方法：**
- `analyze()`: 分析转录文本
- `_build_prompt()`: 构建分析提示词
- `_parse_response()`: 解析 Claude 响应

**输出格式：**
```python
{
    "summary": "会议摘要文本",
    "decisions": ["决策1", "决策2"],
    "action_items": [
        {
            "description": "任务描述",
            "assignee": "负责人",
            "deadline": "截止日期"
        }
    ]
}
```

### 4. Notifier (notifier.py)
**职责：** 发送通知

**功能：**
- 格式化分析结果
- 发送到 Slack
- 使用 Block Kit 美化消息

**关键方法：**
- `send_summary()`: 发送摘要到 Slack
- `_format_message()`: 格式化为 Slack 消息

**消息格式：**
- Header: 会议文件名
- Context: 处理时间
- Sections: 摘要、决策、行动项

### 5. Processor (processor.py)
**职责：** 编排整个处理流程

**功能：**
- 初始化所有组件
- 协调处理流程
- 错误处理
- 进度报告

**处理流程：**
```
1. 接收音频文件路径
2. 调用 Transcriber 转录
3. 调用 Analyzer 分析
4. 调用 Notifier 发送通知
5. 返回处理结果
```

## 数据流

```
┌─────────────┐
│ meeting.mp3 │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   Transcriber   │
│  (Whisper API)  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   transcript    │
│   (text + meta) │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│    Analyzer     │
│  (Claude API)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│    analysis     │
│ (structured)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│    Notifier     │
│  (Slack API)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Slack Message   │
└─────────────────┘
```

## 配置管理

### 配置文件位置
`~/.meeting-summarizer/config.yaml`

### 配置结构
```yaml
openai:
  api_key: "sk-..."

anthropic:
  api_key: "sk-ant-..."

slack:
  webhook_url: "https://hooks.slack.com/..."

monitoring:
  folder: "~/meeting-recordings"
  check_interval: 60

processing:
  cache_transcripts: true
  cache_dir: "~/.meeting-summarizer/cache"
```

## 缓存机制

### 缓存目录
`~/.meeting-summarizer/cache/`

### 缓存文件命名
`{file_md5_hash}.json`

### 缓存内容
```json
{
  "text": "转录文本...",
  "metadata": {
    "language": "zh",
    "duration": 3600.5,
    "file": "meeting.mp3"
  }
}
```

### 缓存策略
1. 计算音频文件 MD5 哈希
2. 检查缓存是否存在
3. 存在则直接返回
4. 不存在则调用 API 并缓存

## 错误处理

### 转录错误
- API 认证失败
- 配额不足
- 文件格式不支持
- 网络错误

**处理策略：**
- 记录错误日志
- 跳过当前文件
- 继续处理下一个

### 分析错误
- API 认证失败
- 速率限制
- Token 超限
- 网络错误

**处理策略：**
- 记录错误日志
- 保留转录结果
- 可手动重试分析

### 通知错误
- Webhook 无效
- 网络错误
- 消息格式错误

**处理策略：**
- 记录错误日志
- 不影响主流程
- 结果仍然保存

## 扩展点

### 1. 添加新的通知渠道
实现类似 `SlackNotifier` 的接口：

```python
class EmailNotifier:
    def __init__(self, config):
        pass

    def send_summary(self, analysis, meeting_file):
        pass
```

### 2. 自定义分析逻辑
修改 `Analyzer._build_prompt()` 方法：

```python
def _build_prompt(self, transcript, metadata):
    # 自定义提示词
    return custom_prompt
```

### 3. 支持其他转录服务
实现类似 `Transcriber` 的接口：

```python
class AssemblyAITranscriber:
    def transcribe(self, audio_file_path):
        # 返回相同格式的结果
        return {"text": "...", "metadata": {...}}
```

### 4. 添加后处理步骤
在 `Processor.process()` 中添加：

```python
# 在分析后添加
post_processed = self.post_processor.process(analysis)
```

## 性能优化

### 1. 并行处理
使用 `concurrent.futures` 并行处理多个文件：

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(processor.process, f) for f in files]
```

### 2. 异步 API 调用
使用 `asyncio` 异步调用 API：

```python
import asyncio

async def process_async(file_path):
    transcript = await transcribe_async(file_path)
    analysis = await analyze_async(transcript)
    await notify_async(analysis)
```

### 3. 批量转录
将多个短音频合并后转录：

```python
def batch_transcribe(audio_files):
    # 合并音频
    combined = combine_audio(audio_files)
    # 转录
    transcript = transcribe(combined)
    # 分割结果
    return split_transcript(transcript, audio_files)
```

## 安全考虑

### 1. API 密钥保护
- 使用环境变量
- 文件权限限制（600）
- 不提交到版本控制

### 2. 数据隐私
- 转录结果本地缓存
- 可选择不发送到 Slack
- 定期清理缓存

### 3. 访问控制
- 限制监控文件夹权限
- 只允许授权用户访问
- 记录所有操作日志

## 监控和日志

### 日志级别
- INFO: 正常处理流程
- WARNING: 可恢复的错误
- ERROR: 处理失败

### 日志内容
- 文件处理开始/结束
- API 调用时间
- 错误详情
- 成本统计

### 监控指标
- 处理文件数量
- 成功/失败率
- API 调用次数
- 平均处理时间
- 总成本

## 部署架构

### 开发环境
```
本地机器
├── Python 3.11+
├── 依赖包
└── 配置文件
```

### 生产环境（选项 1：systemd）
```
Linux 服务器
├── systemd 服务
├── 自动重启
└── 日志管理
```

### 生产环境（选项 2：Docker）
```
Docker 容器
├── 独立环境
├── 易于部署
└── 资源隔离
```

### 生产环境（选项 3：云函数）
```
AWS Lambda / Google Cloud Functions
├── 事件触发
├── 按需计费
└── 自动扩展
```

## 成本分析

### 单次处理成本
- Whisper: $0.006/分钟
- Claude: $0.03-0.05/次
- Slack: 免费

### 月度成本估算
- 20 次会议/月（每次 1 小时）
- 转录: $7.20
- 分析: $1.00
- **总计: ~$8.20/月**

### 成本优化
- 缓存转录结果：节省 50%
- 批量处理：减少 API 调用
- 选择性处理：只处理重要会议
