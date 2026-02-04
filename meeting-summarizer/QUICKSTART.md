# 会议录音自动总结系统 - 30 分钟快速上线

## 系统已完成！

你的会议录音自动总结系统已经完全实现，包含所有核心功能：

✅ 自动监控 ~/meeting-recordings 文件夹
✅ Whisper API 音频转录
✅ Claude API 智能分析
✅ Slack 自动通知
✅ 成本优化（缓存、去重）

---

## 立即开始（3 步）

### 第 1 步：安装依赖（2 分钟）

```bash
cd /mnt/d/Code/skills/meeting-summarizer
pip install -r requirements.txt
```

### 第 2 步：配置 API 密钥（5 分钟）

```bash
# 初始化配置文件
python scripts/init_config.py

# 编辑配置文件
nano ~/.meeting-summarizer/config.yaml
```

填入你的 API 密钥：

```yaml
openai:
  api_key: "sk-..."  # https://platform.openai.com/api-keys

anthropic:
  api_key: "sk-ant-..."  # https://console.anthropic.com/settings/keys

slack:
  webhook_url: "https://hooks.slack.com/services/..."  # https://api.slack.com/apps
```

### 第 3 步：启动系统（1 分钟）

```bash
# 测试配置
python scripts/test_setup.py

# 启动监控
python scripts/monitor_meetings.py
```

---

## 使用方式

### 自动模式（推荐）
将 mp3 文件放入 `~/meeting-recordings` 文件夹，系统自动处理。

### 手动模式
```bash
python scripts/process_meeting.py /path/to/meeting.mp3
```

### 批量处理
```bash
python scripts/process_all.py
```

---

## 成本估算

### 单次会议（1 小时）
- Whisper 转录: $0.36
- Claude 分析: $0.03
- **总计: ~$0.39**

### 每月（20 次会议）
- **约 $8/月**

### 成本优化
✅ 自动缓存转录结果
✅ 文件哈希去重
✅ 批量处理模式

---

## 输出示例

系统会在 Slack 发送以下格式的消息：

```
📝 会议摘要: meeting_2024-02-04.mp3
⏰ 处理时间: 2024-02-04 14:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 会议摘要
本次会议讨论了产品路线图和 Q1 目标...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 关键决策点
• 确定使用 Claude API 进行分析
• 预算控制在 $10/月以内
• 优先实现自动监控功能

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 行动项
• 完成 API 集成测试
  👤 张三 | 📅 2024-02-10

• 部署到生产环境
  👤 李四 | 📅 2024-02-15
```

---

## 故障排查

### 问题：转录失败
```bash
# 检查 OpenAI API key
# 访问 https://platform.openai.com/account/billing 检查余额
```

### 问题：分析失败
```bash
# 检查 Anthropic API key
# 访问 https://console.anthropic.com/settings/limits 检查配额
```

### 问题：Slack 通知失败
```bash
# 检查 Webhook URL 是否正确
# 在 Slack 应用设置中重新生成 Webhook
```

---

## 项目结构

```
meeting-summarizer/
├── meeting_summarizer/         # 核心模块
│   ├── transcriber.py         # Whisper 转录
│   ├── analyzer.py            # Claude 分析
│   ├── notifier.py            # Slack 通知
│   ├── monitor.py             # 文件监控
│   └── processor.py           # 主流程
├── scripts/                    # 可执行脚本
│   ├── init_config.py         # 初始化配置
│   ├── monitor_meetings.py    # 监控模式
│   ├── process_meeting.py     # 处理单个文件
│   ├── process_all.py         # 批量处理
│   └── test_setup.py          # 测试设置
├── README.md                   # 详细文档
├── DEPLOYMENT.md               # 部署指南
├── ARCHITECTURE.md             # 架构说明
└── SKILL.md                    # Skill 定义
```

---

## 高级功能

### 生产环境部署（systemd）
```bash
# 创建服务文件
sudo nano /etc/systemd/system/meeting-summarizer.service

# 启动服务
sudo systemctl enable meeting-summarizer
sudo systemctl start meeting-summarizer
```

### Docker 部署
```bash
docker build -t meeting-summarizer .
docker run -d \
  -v ~/.meeting-summarizer:/root/.meeting-summarizer \
  -v ~/meeting-recordings:/root/meeting-recordings \
  meeting-summarizer
```

### 定时批量处理（cron）
```bash
# 每天下午 6 点处理
0 18 * * * cd /path/to/meeting-summarizer && python scripts/process_all.py
```

---

## 获取 API 密钥

### OpenAI API Key
1. 访问 https://platform.openai.com/api-keys
2. 点击 "Create new secret key"
3. 复制密钥（格式：sk-...）

### Anthropic API Key
1. 访问 https://console.anthropic.com/settings/keys
2. 点击 "Create Key"
3. 复制密钥（格式：sk-ant-...）

### Slack Webhook URL
1. 访问 https://api.slack.com/apps
2. 创建新应用 → "From scratch"
3. 启用 "Incoming Webhooks"
4. 添加 Webhook 到工作区
5. 复制 Webhook URL

---

## 技术栈

- **转录**: OpenAI Whisper API
- **分析**: Anthropic Claude Sonnet 4.5
- **通知**: Slack Webhook
- **监控**: watchdog
- **语言**: Python 3.11+

---

## 为什么选择这个方案？

### ✅ 成本低
- 比 Fireflies 便宜 90%
- 按使用量付费
- 无月费

### ✅ 速度快
- 30 分钟完成开发
- 即刻上线使用
- 无需复杂配置

### ✅ 可控性强
- 完全掌控代码
- 自定义分析逻辑
- 数据本地缓存

### ✅ 质量高
- Whisper 业界最佳转录
- Claude 最强分析能力
- 结构化输出

---

## 下一步

1. **立即测试**: 放一个测试 mp3 文件到 ~/meeting-recordings
2. **查看结果**: 检查 Slack 频道
3. **调整提示词**: 根据需要修改 analyzer.py
4. **生产部署**: 使用 systemd 或 Docker

---

**预计总时间: 30 分钟**
**月运营成本: $5-10**
**维护成本: 极低**

🎉 **系统已就绪，开始使用吧！**
