# Meeting Transcriber

音频文件 → 实时转录 → Markdown 文档（按发言人分段）

---

## 🎯 功能

- ✅ 实时转录音频
- ✅ 自动识别发言人
- ✅ 按时间戳分段
- ✅ 输出 Markdown 文档
- ❌ 不做任何总结或分析

---

## 🔧 技术栈

- **转录**: AssemblyAI API (universal-2 模型)
- **语言**: Python 3
- **输出**: Markdown

---

## 📥 输入

**支持格式**: mp3, wav, m4a, mp4

---

## 📤 输出

**单个 Markdown 文件**: `filename_transcript.md`

**内容格式**:
```markdown
# 会议转录

**文件名**: meeting.mp3
**转录时间**: 2026年02月04日
**音频时长**: 60.0 秒
**准确率**: 87.5%
**发言段落**: 35 段

---

## 转录内容

### [00:03] 说话人 A

这是说话人 A 的发言内容...

---

### [00:22] 说话人 B

这是说话人 B 的发言内容...

---
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API Key

```bash
# 方法 1: 环境变量
export ASSEMBLYAI_API_KEY='your_api_key'

# 方法 2: 编辑脚本
# 修改 transcribe_simple.py 第 12 行
ASSEMBLYAI_API_KEY = 'your_api_key'
```

**获取 API Key**: https://www.assemblyai.com/dashboard/signup (免费 $50 额度)

### 3. 运行

```bash
python transcribe_simple.py meeting.mp3
```

---

## 📋 使用方式

### 方法 1: 直接运行

```bash
python transcribe_simple.py "/path/to/meeting.mp3"
```

### 方法 2: Claude Code Skill

```bash
/meeting-summarizer "/path/to/meeting.mp3"
```

---

## 💰 成本

- **转录**: $0.25/小时 (AssemblyAI)
- **总计**: $0.25/小时（无其他费用）

---

## 📊 输出示例

**输入**: 1 小时会议录音

**输出**:
- ✓ 转录准确率: 87%+
- ✓ 自动识别说话人 (A, B, C, D...)
- ✓ 时间戳标记 ([00:03], [00:22]...)
- ✓ Markdown 格式，易于阅读和编辑

---

## 📁 文件结构

```
meeting-summarizer/
├── transcribe_simple.py        # 主脚本（极简版）
├── .env.example                # 配置模板
├── SKILL.md                    # Skill 定义
└── README.md                   # 本文档
```

---

## 🔒 安全提示

- ⚠️ **不要**将 API key 提交到 git
- ✅ 使用环境变量
- ✅ 将 `.env` 添加到 `.gitignore`

---

**快速开始**: `python transcribe_simple.py meeting.mp3` 🚀
