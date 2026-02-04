# Meeting Summarizer - 使用指南

## ✅ 已验证可用

- **Claude 分析**: 完美工作
- **中文支持**: 完美
- **结构化输出**: 完美
- **中转站**: mmkg.cloud 完全兼容

## 🚀 快速开始

### 方法 1：从 Fireflies 导出文本转录

```bash
# 1. 在 Fireflies 中导出会议转录为文本文件
# 2. 运行分析
cd ~/.claude/skills/meeting-summarizer
python summarize.py /path/to/transcript.txt
```

### 方法 2：手动创建转录文本

创建一个文本文件 `meeting.txt`：

```
会议时间：2026-02-04
参会人员：张三、李四、王五

会议内容：
讨论了项目进度和下一步计划...
[你的会议内容]
```

然后运行：

```bash
python summarize.py meeting.txt
```

## 📋 输出示例

运行后会生成：

```
============================================================
📝 MEETING SUMMARY
============================================================
[2-3段会议概述]

============================================================
✅ KEY DECISIONS
============================================================
1. [决策1]
2. [决策2]

============================================================
🎯 ACTION ITEMS
============================================================

1. [任务描述]
   👤 [负责人]
   📅 [截止日期]
```

同时生成 `*_summary.txt` 文件。

## 🔧 配置

脚本会自动使用环境变量：

```bash
# 已配置（从 Claude Code）
ANTHROPIC_AUTH_TOKEN=your_claude_api_token_here
ANTHROPIC_BASE_URL=https://api.anthropic.com
```

无需额外配置！

## 💡 工作流程建议

### 选项 A：Fireflies + Meeting Summarizer

```
1. Fireflies 录制会议
2. Fireflies 导出转录文本
3. 运行 summarize.py 分析
4. 获得结构化摘要
```

### 选项 B：其他工具 + Meeting Summarizer

```
1. 使用任何录音工具
2. 使用任何转录工具（Whisper、讯飞等）
3. 运行 summarize.py 分析
4. 获得结构化摘要
```

### 选项 C：直接输入

```
1. 手动整理会议笔记
2. 保存为文本文件
3. 运行 summarize.py 分析
4. 获得结构化摘要
```

## 📊 成本

- **Claude 分析**: ~$0.03/小时会议
- **总成本**: ~$0.60/月（20次会议）

非常便宜！

## ⚠️ 关于 Whisper API

由于中转站的 Whisper API 返回格式问题，当前版本：
- ✅ 支持文本转录输入
- ⚠️ 暂不支持直接处理音频文件

**解决方案**：
1. 使用 Fireflies 等工具先转录
2. 或注册官方 OpenAI 账号使用 Whisper API（$0.36/小时）

## 🎯 实际使用示例

```bash
# 示例 1：处理 Fireflies 导出
python summarize.py ~/Downloads/fireflies_transcript.txt

# 示例 2：处理会议笔记
python summarize.py ~/Documents/meeting_notes.txt

# 示例 3：批量处理
for file in ~/meetings/*.txt; do
    python summarize.py "$file"
done
```

## 📁 文件位置

- **主脚本**: `~/.claude/skills/meeting-summarizer/summarize.py`
- **输出文件**: 与输入文件同目录，后缀 `_summary.txt`

## 🆘 故障排查

### 错误：ANTHROPIC_AUTH_TOKEN not set
**解决方案**: 环境变量应该已经设置，检查：
```bash
echo $ANTHROPIC_AUTH_TOKEN
```

### 错误：File not found
**解决方案**: 使用绝对路径或确认文件存在

### 错误：API Error 401
**解决方案**: Token 可能过期，联系中转站客服

## ✨ 特性

- ✅ 自动提取会议摘要
- ✅ 识别关键决策点
- ✅ 提取行动项（任务+负责人+截止日期）
- ✅ 中文完美支持
- ✅ 结构化输出
- ✅ 保存为文本文件

## 🎉 开始使用

```bash
cd ~/.claude/skills/meeting-summarizer
python summarize.py your_transcript.txt
```

就这么简单！
