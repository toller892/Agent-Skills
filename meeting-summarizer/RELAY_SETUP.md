# Meeting Summarizer - 第三方中转站配置指南

## 使用第三方中转站的 API Keys

如果你使用的是第三方 API 中转站（如 OpenAI-SB、API2D 等），配置方法如下：

### 方法 1：临时设置（推荐用于测试）

```bash
# 在当前终端会话中设置
export OPENAI_API_KEY='sk-xxx...'  # 你的中转站 OpenAI key
export ANTHROPIC_API_KEY='sk-ant-xxx...'  # 你的中转站 Anthropic key

# 然后运行
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate
python quick_test.py
```

### 方法 2：永久设置（推荐用于长期使用）

编辑你的 shell 配置文件：

```bash
# 对于 bash
nano ~/.bashrc

# 对于 zsh
nano ~/.zshrc

# 添加以下内容：
export OPENAI_API_KEY='sk-xxx...'
export ANTHROPIC_API_KEY='sk-ant-xxx...'

# 保存后重新加载
source ~/.bashrc  # 或 source ~/.zshrc
```

### 方法 3：使用配置文件

```bash
# 1. 初始化配置
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate
python scripts/init_config.py

# 2. 编辑配置文件
nano ~/.meeting-summarizer/config.yaml

# 3. 填入你的中转站 API keys
openai:
  api_key: "sk-xxx..."  # 你的中转站 key

anthropic:
  api_key: "sk-ant-xxx..."  # 你的中转站 key

slack:
  webhook_url: ""  # 可选

# 4. 运行
python scripts/process_meeting.py "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"
```

## 第三方中转站注意事项

### 1. API Base URL 配置

如果你的中转站使用自定义 API endpoint，需要修改代码：

**修改 transcriber.py**:
```python
# 在 meeting_summarizer/transcriber.py 中
from openai import OpenAI

client = OpenAI(
    api_key=self.api_key,
    base_url="https://your-relay-url.com/v1"  # 添加这行
)
```

**修改 analyzer.py**:
```python
# 在 meeting_summarizer/analyzer.py 中
from anthropic import Anthropic

client = Anthropic(
    api_key=self.api_key,
    base_url="https://your-relay-url.com"  # 添加这行
)
```

### 2. 常见中转站配置

#### OpenAI-SB
```python
# transcriber.py
client = OpenAI(
    api_key=self.api_key,
    base_url="https://api.openai-sb.com/v1"
)
```

#### API2D
```python
# transcriber.py
client = OpenAI(
    api_key=self.api_key,
    base_url="https://openai.api2d.net/v1"
)
```

#### CloseAI
```python
# transcriber.py
client = OpenAI(
    api_key=self.api_key,
    base_url="https://api.closeai-proxy.xyz/v1"
)
```

### 3. 验证配置

运行测试脚本验证配置是否正确：

```bash
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate

# 设置 API keys
export OPENAI_API_KEY='your-key'
export ANTHROPIC_API_KEY='your-key'

# 运行测试
python quick_test.py
```

## 快速开始步骤

### 第 1 步：获取你的中转站 API Keys

从你使用的中转站获取：
- OpenAI API Key（用于 Whisper 转录）
- Anthropic API Key（用于 Claude 分析）

### 第 2 步：设置环境变量

```bash
export OPENAI_API_KEY='你的OpenAI中转站key'
export ANTHROPIC_API_KEY='你的Anthropic中转站key'
```

### 第 3 步：运行测试

```bash
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate
python quick_test.py
```

### 第 4 步：查看结果

处理完成后会显示：
- 会议摘要
- 关键决策点
- 行动项（任务 + 负责人 + 截止日期）

同时会生成 `2026_1_30 14_27_47_summary.txt` 文件。

## 故障排查

### 错误：API key not found
**解决方案**:
```bash
# 检查环境变量
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# 如果为空，重新设置
export OPENAI_API_KEY='your-key'
export ANTHROPIC_API_KEY='your-key'
```

### 错误：Connection refused / Timeout
**可能原因**:
- 中转站 base_url 配置错误
- 网络连接问题
- 中转站服务不可用

**解决方案**:
1. 检查中转站状态
2. 验证 base_url 是否正确
3. 测试网络连接

### 错误：Invalid API key
**可能原因**:
- API key 错误或过期
- 中转站账户余额不足
- API key 权限不足

**解决方案**:
1. 检查 API key 是否正确
2. 登录中转站查看余额
3. 确认 API key 有 Whisper 和 Claude 权限

### 错误：Rate limit exceeded
**可能原因**:
- 请求频率过高
- 中转站限流

**解决方案**:
1. 等待一段时间后重试
2. 联系中转站客服
3. 升级中转站套餐

## 成本估算（中转站）

不同中转站的定价可能不同，一般情况下：

- **Whisper 转录**: $0.006/分钟（官方价格）
- **Claude 分析**: $0.003/1k tokens（官方价格）

中转站通常会加价 10-30%，具体以你的中转站为准。

**1小时会议估算**:
- 转录: 60分钟 × $0.006 = $0.36
- 分析: ~10k tokens × $0.003 = $0.03
- **总计**: ~$0.39（官方价格）
- **中转站**: ~$0.45-0.50（加价后）

## 下一步

1. ✅ 从你的中转站获取 API keys
2. ✅ 设置环境变量
3. ✅ 运行 `python quick_test.py`
4. ✅ 查看生成的摘要文件
5. ✅ 开始处理实际的会议录音

## 需要帮助？

如果遇到问题：
1. 检查 API keys 是否正确设置
2. 验证中转站服务是否正常
3. 查看错误日志
4. 参考 USAGE_GUIDE.md 获取更多信息

## 文件位置

- **测试脚本**: `~/.claude/skills/meeting-summarizer/quick_test.py`
- **配置文件**: `~/.meeting-summarizer/config.yaml`
- **缓存目录**: `~/.meeting-summarizer/cache/`
- **测试录音**: `/mnt/d/Code/skills/2026_1_30 14_27_47.mp3`
