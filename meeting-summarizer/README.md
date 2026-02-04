# Meeting Summarizer

会议录音 → AI 转录 + 分析 → 3 种格式输出（TXT + MD + HTML）

---

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| **语音转录** | AssemblyAI API (universal-2 模型) |
| **AI 分析** | Claude Sonnet 4.5 |
| **输出格式** | Plain Text + Markdown + HTML |
| **语言** | Python 3 |

---

## 📥 输入

**支持格式**: mp3, wav, m4a, mp4

**示例**:
```
meeting.mp3
```

---

## 📤 输出

生成 3 个文件（同目录）：

| 文件 | 格式 | 特点 |
|------|------|------|
| `meeting_summary.txt` | 纯文本 | 基础摘要 |
| `meeting_summary.md` | Markdown | AI 优化，带表格/列表/优先级 |
| `meeting_summary.html` | HTML | 纽约客风格，精美排版 |

**内容包含**:
- 会议摘要
- 关键决策点
- 行动项（负责人 + 截止日期）
- 说话人识别

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API Keys

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API keys
# 或者设置环境变量：
export ASSEMBLYAI_API_KEY='your_api_key'
export ANTHROPIC_AUTH_TOKEN='your_claude_token'
```

**获取 API Keys**:
- AssemblyAI: https://www.assemblyai.com/dashboard/signup (免费 $50 额度)
- Claude API: https://console.anthropic.com/

### 3. 运行

```bash
# 生成 3 种格式（推荐）
python assemblyai_enhanced.py "/path/to/meeting.mp3"

# 或只生成基础文本
python assemblyai_summarizer.py "/path/to/meeting.mp3"
```

---

## 📋 启用方式

### 方法 1: Claude Code Skill

```bash
/meeting-summarizer "/path/to/meeting.mp3"
```

### 方法 2: 直接运行脚本

```bash
python assemblyai_enhanced.py "/path/to/meeting.mp3"
```

---

## 💰 成本

- **转录**: $0.25/小时 (AssemblyAI)
- **分析**: $0.03/小时 (Claude)
- **总计**: ~$0.28/会议

---

## ✅ 验证安装

```bash
python verify_assemblyai_setup.py
```

---

## 📊 示例输出

**输入**: 1 小时会议录音
**处理时间**: 2-3 分钟
**输出**:
- ✓ 转录准确率: 87%+
- ✓ 自动识别说话人
- ✓ 智能标点和格式化
- ✓ 3 种格式文件

---

## 📁 文件结构

```
meeting-summarizer/
├── assemblyai_enhanced.py      # 主脚本（推荐）
├── assemblyai_summarizer.py    # 基础版
├── verify_assemblyai_setup.py  # 验证工具
├── .env.example                 # 配置模板
├── SKILL.md                     # Skill 定义
└── README.md                    # 本文档
```

---

## 🔒 安全提示

- ⚠️ **不要**将 API keys 提交到 git
- ✅ 使用环境变量或 `.env` 文件
- ✅ 将 `.env` 添加到 `.gitignore`

---

## 📚 更多文档

- [AssemblyAI 注册指南](ASSEMBLYAI_SETUP.md)
- [Vosk 离线方案](VOSK_QUICK_START.md)
- [完整自动化指南](COMPLETE_AUTOMATION_GUIDE.md)

---

**快速开始**: `python assemblyai_enhanced.py meeting.mp3` 🚀
