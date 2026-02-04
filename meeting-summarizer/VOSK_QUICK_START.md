# Meeting Summarizer - Vosk 快速开始指南

## 🎯 推荐方案：Vosk（免费离线）

**优势**：
- ✅ 完全免费
- ✅ 离线运行，无需网络
- ✅ 支持中文
- ✅ 无 API 限制
- ✅ 隐私安全（数据不上传）

**成本**：仅 Claude 分析 ~$0.03/会议

---

## 📦 第 1 步：安装依赖

```bash
cd ~/.claude/skills/meeting-summarizer
source venv/bin/activate  # 如果有虚拟环境

# 安装 Python 包
pip install vosk pydub requests

# 安装 ffmpeg（音频转换）
sudo apt install ffmpeg  # Ubuntu/Debian
# 或
brew install ffmpeg      # macOS
```

---

## 📥 第 2 步：下载 Vosk 中文模型

### 方法 A：自动下载（推荐）

```bash
cd ~/.claude/skills/meeting-summarizer
./setup_vosk.sh
```

### 方法 B：手动下载

```bash
# 1. 下载模型（约 42MB）
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip

# 2. 创建目录
mkdir -p ~/.meeting-summarizer

# 3. 解压
unzip vosk-model-cn-0.22.zip -d ~/.meeting-summarizer/

# 4. 重命名
mv ~/.meeting-summarizer/vosk-model-cn-0.22 ~/.meeting-summarizer/vosk-model-cn

# 5. 验证
ls ~/.meeting-summarizer/vosk-model-cn/
# 应该看到：am/  conf/  graph/  ivector/  README
```

---

## ✅ 第 3 步：验证安装

```bash
python verify_vosk_setup.py
```

**预期输出**：
```
✓ Vosk 已安装
✓ pydub 已安装
✓ ffmpeg 已安装
✓ Vosk 中文模型已下载
✓ Claude API 配置正确

🎉 所有依赖已就绪！
```

---

## 🚀 第 4 步：测试转录

### 单文件处理

```bash
# 处理 Fireflies 导出的 mp3
python vosk_summarizer.py "/path/to/meeting.mp3"
```

**完整流程**：
1. 自动转换音频格式（mp3 → wav）
2. Vosk 离线转录
3. Claude 分析生成摘要
4. 提取关键决策和行动项
5. 保存结果到 `meeting_summary.txt`

---

## 🔄 第 5 步：启动自动监控（可选）

如果想要完全自动化：

```bash
# 1. 安装监控依赖
pip install watchdog

# 2. 修改 auto_monitor.py 使用 Vosk
# （已在 vosk_auto_monitor.py 中实现）

# 3. 启动监控
python vosk_auto_monitor.py
```

**使用方式**：
```bash
# 从 Fireflies 下载 mp3 后，直接放入监控文件夹
cp ~/Downloads/meeting.mp3 ~/meeting-recordings/

# 系统自动：
# ✓ 检测新文件
# ✓ Vosk 转录
# ✓ Claude 分析
# ✓ 保存摘要
```

---

## 📊 处理示例

### 输入
```bash
python vosk_summarizer.py "2026_1_30 14_27_47.mp3"
```

### 输出
```
============================================================
Meeting Summarizer - Vosk Version (Free)
============================================================

📁 Audio file: 2026_1_30 14_27_47.mp3

[1/3] Transcribing with Vosk (offline)...
  Loading Vosk model...
  Transcribing...
  ✓ Transcription complete (4521 characters)

[2/3] Analyzing with Claude...
  ✓ Analysis complete

============================================================
📝 MEETING SUMMARY
============================================================
本次会议主要围绕项目进度和技术优化展开讨论...

============================================================
✅ KEY DECISIONS
============================================================
1. 采用Redis缓存方案优化数据库查询性能
2. 增加2名开发人员以加快项目进度

============================================================
🎯 ACTION ITEMS
============================================================

1. 优化数据库查询性能
   👤 张三
   📅 2026-02-10

2. 完成Redis缓存集成
   👤 李四
   📅 2026-02-12

============================================================
✓ SUCCESS!
============================================================

💾 Summary saved to: 2026_1_30 14_27_47_summary.txt
```

---

## 🔧 故障排查

### 问题 1：Vosk 模型未找到

**症状**：
```
⚠️  Vosk 中文模型未找到
```

**解决**：
```bash
# 检查模型路径
ls ~/.meeting-summarizer/vosk-model-cn/

# 如果不存在，重新下载
wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
unzip vosk-model-cn-0.22.zip -d ~/.meeting-summarizer/
mv ~/.meeting-summarizer/vosk-model-cn-0.22 ~/.meeting-summarizer/vosk-model-cn
```

### 问题 2：音频转换失败

**症状**：
```
✗ Conversion failed: FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**解决**：
```bash
# 安装 ffmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

### 问题 3：Claude API 错误

**症状**：
```
❌ Error: Claude API Error: 401
```

**解决**：
```bash
# 检查环境变量（如果使用）
echo $ANTHROPIC_AUTH_TOKEN
echo $ANTHROPIC_BASE_URL

# 或者直接在脚本中使用硬编码配置（已配置）
# TOKEN = "your_claude_api_token_here"
# ANTHROPIC_BASE = "https://api.anthropic.com"
```

---

## 📈 性能对比

| 方案 | 成本/会议 | 优势 | 劣势 |
|------|----------|------|------|
| **Vosk（推荐）** | $0.03 | 免费、离线、隐私 | 准确率略低 |
| OpenAI Whisper | $0.39 | 准确率高 | 需付费、需网络 |
| AssemblyAI | $0.28 | 准确率高 | 需付费、需网络 |

**1小时会议，20次/月**：
- Vosk: $0.60/月（仅 Claude）
- Whisper: $7.80/月

---

## 🎯 下一步

### 立即可用
1. ✅ 单文件处理：`python vosk_summarizer.py meeting.mp3`
2. ✅ 批量处理：循环调用脚本
3. ✅ 查看摘要：`cat meeting_summary.txt`

### 可选增强
1. 🔄 自动监控：`python vosk_auto_monitor.py`
2. 📱 Slack 通知：配置 SLACK_WEBHOOK_URL
3. 🤖 Gemini 对比：添加双 AI 分析

---

## 📁 文件位置

- **转录脚本**：`~/.claude/skills/meeting-summarizer/vosk_summarizer.py`
- **验证脚本**：`~/.claude/skills/meeting-summarizer/verify_vosk_setup.py`
- **自动监控**：`~/.claude/skills/meeting-summarizer/vosk_auto_monitor.py`
- **Vosk 模型**：`~/.meeting-summarizer/vosk-model-cn/`
- **输出文件**：与输入文件同目录

---

## 🎉 开始使用

```bash
# 1. 安装依赖
pip install vosk pydub requests
sudo apt install ffmpeg

# 2. 下载模型
./setup_vosk.sh

# 3. 验证安装
python verify_vosk_setup.py

# 4. 处理会议录音
python vosk_summarizer.py "meeting.mp3"

# 完成！🚀
```
