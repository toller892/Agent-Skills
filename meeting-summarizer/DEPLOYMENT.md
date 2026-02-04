# Meeting Summarizer - 快速部署指南

## 30 分钟快速上线

### 第 1 步：安装依赖（2 分钟）

```bash
cd meeting-summarizer
pip install -r requirements.txt
```

### 第 2 步：获取 API 密钥（10 分钟）

#### OpenAI API Key
1. 访问 https://platform.openai.com/api-keys
2. 点击 "Create new secret key"
3. 复制密钥（格式：sk-...）

#### Anthropic API Key
1. 访问 https://console.anthropic.com/settings/keys
2. 点击 "Create Key"
3. 复制密钥（格式：sk-ant-...）

#### Slack Webhook URL
1. 访问 https://api.slack.com/apps
2. 点击 "Create New App" → "From scratch"
3. 输入应用名称（如 "Meeting Summarizer"）
4. 选择工作区
5. 在左侧菜单选择 "Incoming Webhooks"
6. 打开 "Activate Incoming Webhooks"
7. 点击 "Add New Webhook to Workspace"
8. 选择要发送消息的频道
9. 复制 Webhook URL（格式：https://hooks.slack.com/services/...）

### 第 3 步：配置系统（3 分钟）

```bash
# 初始化配置文件
python scripts/init_config.py

# 编辑配置文件
nano ~/.meeting-summarizer/config.yaml
```

填入你的 API 密钥：

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

### 第 4 步：测试设置（2 分钟）

```bash
python scripts/test_setup.py
```

确保所有检查项都通过。

### 第 5 步：启动系统（1 分钟）

```bash
python scripts/monitor_meetings.py
```

### 第 6 步：测试功能（5 分钟）

1. 将一个测试 mp3 文件放入 `~/meeting-recordings` 文件夹
2. 等待系统自动处理
3. 检查 Slack 频道是否收到摘要

## 成本估算

### 单次会议处理成本

**1 小时会议录音：**
- Whisper 转录：$0.006/分钟 × 60 = **$0.36**
- Claude 分析：约 10K tokens × $3/MTok = **$0.03**
- **总计：约 $0.39**

**每月 20 次会议（每次 1 小时）：**
- 月成本：$0.39 × 20 = **$7.80**

### 成本优化建议

1. **启用缓存**（已默认开启）
   - 避免重复转录同一文件
   - 节省约 50% 成本

2. **批量处理模式**
   - 关闭实时监控
   - 每天定时处理一次
   - 适合非紧急场景

3. **选择性处理**
   - 只处理重要会议
   - 手动模式：`python scripts/process_meeting.py file.mp3`

## 故障排查

### 问题 1：转录失败

**错误信息：** `Authentication failed` 或 `Insufficient quota`

**解决方案：**
1. 检查 OpenAI API key 是否正确
2. 访问 https://platform.openai.com/account/billing 检查余额
3. 确认 API key 有 Whisper API 访问权限

### 问题 2：分析失败

**错误信息：** `Invalid API key` 或 `Rate limit exceeded`

**解决方案：**
1. 检查 Anthropic API key 是否正确
2. 访问 https://console.anthropic.com/settings/limits 检查配额
3. 如果超过速率限制，等待几分钟后重试

### 问题 3：Slack 通知失败

**错误信息：** `Invalid webhook URL` 或 `404 Not Found`

**解决方案：**
1. 检查 Webhook URL 是否完整
2. 确认 Webhook 未被删除或禁用
3. 在 Slack 应用设置中重新生成 Webhook

### 问题 4：文件监控不工作

**症状：** 放入文件后没有自动处理

**解决方案：**
1. 确认文件格式为 `.mp3`
2. 检查文件是否完全上传完成
3. 查看终端是否有错误信息
4. 尝试手动处理：`python scripts/process_meeting.py file.mp3`

## 生产环境部署

### 使用 systemd 服务（Linux）

创建服务文件 `/etc/systemd/system/meeting-summarizer.service`：

```ini
[Unit]
Description=Meeting Summarizer Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/meeting-summarizer
ExecStart=/usr/bin/python3 /path/to/meeting-summarizer/scripts/monitor_meetings.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable meeting-summarizer
sudo systemctl start meeting-summarizer
sudo systemctl status meeting-summarizer
```

### 使用 Docker

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/monitor_meetings.py"]
```

构建并运行：

```bash
docker build -t meeting-summarizer .
docker run -d \
  -v ~/.meeting-summarizer:/root/.meeting-summarizer \
  -v ~/meeting-recordings:/root/meeting-recordings \
  --name meeting-summarizer \
  meeting-summarizer
```

### 使用 cron 定时任务（批量模式）

编辑 crontab：

```bash
crontab -e
```

添加定时任务（每天下午 6 点处理）：

```cron
0 18 * * * cd /path/to/meeting-summarizer && python scripts/process_all.py
```

## 高级配置

### 自定义分析提示词

编辑 `meeting_summarizer/analyzer.py`，修改 `_build_prompt` 方法：

```python
def _build_prompt(self, transcript: str, metadata: dict = None) -> str:
    return f"""
    [你的自定义提示词]

    转录文本：
    {transcript}
    """
```

### 支持多语言

Whisper API 自动检测语言，无需额外配置。

如需指定语言，修改 `meeting_summarizer/transcriber.py`：

```python
transcript = self.client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="zh",  # 指定中文
    response_format="verbose_json"
)
```

### 添加邮件通知

安装依赖：

```bash
pip install sendgrid
```

创建 `meeting_summarizer/email_notifier.py`：

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailNotifier:
    def __init__(self, api_key: str, from_email: str):
        self.client = SendGridAPIClient(api_key)
        self.from_email = from_email

    def send_summary(self, analysis: dict, to_email: str):
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=f"会议摘要: {analysis['metadata']['file']}",
            html_content=self._format_html(analysis)
        )
        self.client.send(message)
```

## 监控和日志

### 启用详细日志

修改脚本，添加日志配置：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('meeting-summarizer.log'),
        logging.StreamHandler()
    ]
)
```

### 监控 API 使用量

创建 `scripts/check_usage.py`：

```python
from openai import OpenAI
from anthropic import Anthropic

# 检查 OpenAI 使用量
openai_client = OpenAI(api_key="your-key")
# OpenAI 需要通过 dashboard 查看

# 检查 Anthropic 使用量
anthropic_client = Anthropic(api_key="your-key")
# Anthropic 需要通过 console 查看

print("请访问以下链接查看使用量：")
print("OpenAI: https://platform.openai.com/usage")
print("Anthropic: https://console.anthropic.com/settings/usage")
```

## 安全建议

1. **保护 API 密钥**
   - 不要将 config.yaml 提交到 git
   - 使用环境变量存储密钥
   - 定期轮换密钥

2. **限制文件访问**
   - 设置适当的文件权限：`chmod 600 ~/.meeting-summarizer/config.yaml`
   - 只允许授权用户访问监控文件夹

3. **监控异常活动**
   - 定期检查 API 使用量
   - 设置使用量告警
   - 记录所有处理日志

## 支持和反馈

如有问题或建议，请：
1. 查看 README.md 文档
2. 运行 `python scripts/test_setup.py` 诊断问题
3. 提交 Issue 到项目仓库

---

**预计总部署时间：30 分钟**

**月运营成本：$5-10（取决于使用频率）**

**维护成本：极低（自动化运行）**
