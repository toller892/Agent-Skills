# Meeting Summarizer - 最终配置方案

## 当前状态

✅ **Whisper 转录成功** - 你的中转站支持 OpenAI API
⚠️ **Claude 分析失败** - Anthropic API 认证问题

## 解决方案

### 方案 1：使用官方 Anthropic API（推荐）

Claude API 成本很低（~$0.03/小时会议），直接用官方的：

```bash
# 1. 注册 Anthropic 账号
https://console.anthropic.com/

# 2. 获取 API key
https://console.anthropic.com/settings/keys

# 3. 充值至少 $5

# 4. 设置环境变量
export ANTHROPIC_API_KEY='sk-ant-...'  # 官方 key，不是中转站的
```

### 方案 2：联系中转站客服

询问 colin1112.me 的 Anthropic API 正确使用方式：
- 是否需要特殊的 header？
- 是否需要不同的 endpoint？
- Token 格式是否正确？

## 推荐配置（混合方案）

使用中转站的 OpenAI + 官方的 Anthropic：

```bash
# OpenAI (中转站) - 用于 Whisper 转录
export OPENAI_API_KEY='你的中转站token'
export OPENAI_BASE_URL='https://any1.colin1112.me/openai/v1'

# Anthropic (官方) - 用于 Claude 分析
export ANTHROPIC_API_KEY='sk-ant-...'  # 官方 key
# 不设置 ANTHROPIC_BASE_URL，使用官方 API
```

## 成本分析（混合方案）

**1小时会议**:
- Whisper 转录（中转站）: ~$0.36
- Claude 分析（官方）: ~$0.03
- **总计**: ~$0.39

**20次会议/月**:
- **总成本**: ~$8/月
- 对比人工转录: 节省 96%

## 快速测试

创建测试脚本 `test_hybrid.py`:

```python
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from meeting_summarizer.transcriber import Transcriber
from meeting_summarizer.analyzer import MeetingAnalyzer

# 配置
openai_token = os.getenv('ANTHROPIC_AUTH_TOKEN')  # 中转站 token
anthropic_key = os.getenv('ANTHROPIC_API_KEY')  # 官方 key

if not openai_token:
    print("❌ ANTHROPIC_AUTH_TOKEN not set (for OpenAI relay)")
    sys.exit(1)

if not anthropic_key:
    print("❌ ANTHROPIC_API_KEY not set (for official Anthropic)")
    sys.exit(1)

# 初始化
transcriber = Transcriber(
    api_key=openai_token,
    cache_dir='~/.meeting-summarizer/cache',
    base_url='https://any1.colin1112.me/openai/v1'
)

analyzer = MeetingAnalyzer(
    api_key=anthropic_key
    # 不设置 base_url，使用官方 API
)

# 处理
audio_file = "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"
transcript_result = transcriber.transcribe(audio_file)
analysis = analyzer.analyze(transcript_result['text'], transcript_result['metadata'])

print("✓ Success!")
print(f"Summary: {analysis['summary'][:200]}...")
```

## 下一步

1. **获取官方 Anthropic API key**
   - 访问: https://console.anthropic.com/settings/keys
   - 创建新 key
   - 充值至少 $5

2. **设置环境变量**
   ```bash
   export ANTHROPIC_API_KEY='sk-ant-...'
   ```

3. **运行测试**
   ```bash
   cd ~/.claude/skills/meeting-summarizer
   source venv/bin/activate
   python test_hybrid.py
   ```

## 为什么推荐混合方案？

1. **成本最优**:
   - Whisper 转录占大头（$0.36），用中转站节省成本
   - Claude 分析很便宜（$0.03），用官方最稳定

2. **稳定性最好**:
   - 官方 Anthropic API 最稳定
   - 避免中转站的兼容性问题

3. **配置简单**:
   - 不需要研究中转站的特殊配置
   - 直接用官方 SDK

## 文件位置

- **测试脚本**: `~/.claude/skills/meeting-summarizer/test_hybrid.py`
- **配置文档**: `~/.claude/skills/meeting-summarizer/FINAL_SETUP.md`
- **转录缓存**: `~/.meeting-summarizer/cache/`

## 需要帮助？

如果遇到问题：
1. 确认 ANTHROPIC_API_KEY 是官方 key（sk-ant-开头）
2. 确认账户有余额
3. 查看错误日志
4. 参考 USAGE_GUIDE.md
