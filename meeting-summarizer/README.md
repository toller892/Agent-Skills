# Meeting Transcriber

自动转录会议录音，识别说话人，生成带时间戳的 Markdown 文档。支持 Gemini 和 Paraformer 两种模型，在 Claude Code 中自动生成会议总结。

## 特性

✅ **智能模型选择** - 自动检测 API key，优先使用 Gemini，无 key 时自动回退到 Paraformer

✅ **自动说话人识别** - 区分不同发言人

✅ **AI 会议总结** - 在 Claude Code 中自动生成精炼总结

✅ **多语言支持** - Gemini 支持 100+ 语言

✅ **离线可用** - Paraformer 本地模型无需网络

## 快速开始

### 1. 安装依赖

```bash
# 基础依赖（必需）
pip install requests

# 本地模型依赖（Paraformer，可选）
pip install funasr modelscope torch torchaudio
```

### 2. 设置 API Key（推荐）

```bash
export GEMINI_API_KEY='your_api_key'
```

获取免费 API key：https://aistudio.google.com/app/apikey

**如果不设置 API key，将自动使用 Paraformer 本地模型（免费，离线）**

### 3. 转录音频

```bash
# 自动选择模型（有 key 用 Gemini，无 key 用 Paraformer）
python transcribe_only.py "meeting.mp3"

# 手动指定 Gemini
python transcribe_only.py "meeting.mp3" 1

# 手动指定 Paraformer
python transcribe_only.py "meeting.mp3" 2
```

## 模型对比

| 模型 | 准确率 | 速度 | 成本 | 说话人识别 | 发言段落 | 推荐场景 |
|------|--------|------|------|-----------|---------|---------|
| **Gemini 2.5** ⭐ | 90% | 10-30秒 | 免费配额 | ✅ | 126段 | 默认选择，快速零配置 |
| **Paraformer** | 94% | ~3分钟 | 完全免费 | ✅ | 179段 | 离线使用，最佳分段 |

详细对比见 [MODEL_COMPARISON.md](MODEL_COMPARISON.md)

## 输出示例

生成的 Markdown 文件包含：

```markdown
## 会议精要

### 整体总结
本次会议是团队工作同步会议...

### 关键要点
1. 技术开发任务...
2. 配置调整...

### 发言人总结
**说话人 1**: 主持会议开场
**说话人 2**: 汇报技术任务...

### 行动项
- [ ] 调整配置并测试
- [ ] 更新文档...

---

## 原始转录内容

### [00:03] 说话人 1
咱们开始吧...
```

## 在 Claude Code 中使用

当作为 Claude Code skill 使用时：

1. **转录**：运行脚本生成带时间戳的转录
2. **AI 总结**：Claude 自动读取转录并生成会议精要
3. **无需额外 API key**：Claude 直接处理总结生成

详见 [SKILL.md](SKILL.md)

## 文件说明

- `transcribe_only.py` - 推荐使用（在 Claude Code 中）
- `transcribe_multi_model.py` - 完整功能版本
- `SKILL.md` - Claude Code skill 定义
- `MODEL_COMPARISON.md` - 详细模型对比
- `requirements.txt` - Python 依赖

## 常见问题

**Q: 不设置 API key 可以用吗？**
A: 可以！会自动使用 Paraformer 本地模型，完全免费且离线可用。

**Q: Gemini 配额用完了怎么办？**
A: 自动回退到 Paraformer 本地模型，或者手动指定：`python transcribe_only.py meeting.mp3 2`

**Q: 哪个模型分段更精细？**
A: Paraformer（179段）比 Gemini（126段）多 42%，但 Gemini 速度快 6-18 倍。

**Q: 支持哪些音频格式？**
A: 支持 mp3, wav, m4a, mp4 等常见格式。

**Q: 需要多少内存？**
A: Gemini 无需本地资源。Paraformer 需要 4GB+ RAM。

## 许可证

MIT License

## 更新日志

- **2026-02-06**: 简化为 Gemini + Paraformer 双模型，自动回退机制
- **2026-02-05**: 添加 Gemini 2.5 Flash 支持，优化说话人识别
- **2026-02-04**: 初始版本
