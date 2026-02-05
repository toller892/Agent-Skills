# Meeting Transcriber - 多模型安装指南

## 📦 支持的模型

### 1. AssemblyAI (云端)
- **准确率**: 87%+
- **成本**: $0.25/小时
- **特点**: 说话人识别、云端处理
- **安装**: 无需安装，仅需 API Key

### 2. SenseVoice (本地)
- **准确率**: 95%+
- **成本**: 免费
- **特点**: 50+语言、情感识别、超低延迟
- **安装**: 需要安装 FunASR

### 3. Paraformer (本地)
- **准确率**: 94%+
- **成本**: 免费
- **特点**: 热词定制、说话人识别
- **安装**: 需要安装 FunASR

---

## 🚀 安装步骤

### 方法 1: 只使用 AssemblyAI (最简单)

```bash
# 只需要 requests
pip install requests

# 设置 API Key
export ASSEMBLYAI_API_KEY='your_api_key'
```

### 方法 2: 安装本地模型 (SenseVoice + Paraformer)

```bash
# 安装 FunASR 和依赖
pip install funasr modelscope torch torchaudio

# 首次运行会自动下载模型（约 1-2 GB）
```

### 方法 3: 安装所有模型

```bash
# 安装所有依赖
pip install requests funasr modelscope torch torchaudio

# 设置 AssemblyAI API Key (可选)
export ASSEMBLYAI_API_KEY='your_api_key'
```

---

## 📋 使用方法

### 交互式选择模型

```bash
python transcribe_multi_model.py meeting.mp3
```

会显示菜单让你选择：
```
请选择语音识别模型
============================================================

[1] AssemblyAI
    描述: 云端 API，准确率 87%+，支持说话人识别
    成本: $0.25/小时
    要求: API Key

[2] SenseVoice
    描述: 阿里开源，准确率 95%+，50+语言，情感识别
    成本: 免费
    要求: 本地模型

[3] Paraformer
    描述: 阿里 FunASR，准确率 94%+，热词定制
    成本: 免费
    要求: 本地模型

请输入选项 (1-3):
```

### 直接指定模型

```bash
# 使用 AssemblyAI
python transcribe_multi_model.py meeting.mp3 1

# 使用 SenseVoice
python transcribe_multi_model.py meeting.mp3 2

# 使用 Paraformer
python transcribe_multi_model.py meeting.mp3 3
```

---

## 📊 模型对比

| 特性 | AssemblyAI | SenseVoice | Paraformer |
|------|-----------|------------|------------|
| **准确率** | 87%+ | 95%+ | 94%+ |
| **成本** | $0.25/小时 | 免费 | 免费 |
| **部署** | 云端 | 本地 | 本地 |
| **说话人识别** | ✓ | ✗ | ✓ |
| **多语言** | ✓ | ✓ (50+) | ✓ |
| **离线使用** | ✗ | ✓ | ✓ |
| **首次下载** | 无需 | ~1GB | ~1GB |

---

## 💡 选择建议

### 使用 AssemblyAI 如果：
- ✓ 需要快速开始（无需安装模型）
- ✓ 需要说话人识别
- ✓ 不介意付费
- ✓ 有稳定网络连接

### 使用 SenseVoice 如果：
- ✓ 需要最高准确率
- ✓ 需要多语言支持
- ✓ 需要情感识别
- ✓ 完全免费

### 使用 Paraformer 如果：
- ✓ 需要说话人识别
- ✓ 需要热词定制
- ✓ 需要离线使用
- ✓ 完全免费

---

## 🔧 故障排查

### 问题 1: FunASR 安装失败

```bash
# 尝试使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple funasr modelscope
```

### 问题 2: 模型下载慢

```bash
# 设置 ModelScope 镜像
export MODELSCOPE_CACHE=~/.cache/modelscope
```

### 问题 3: 内存不足

```bash
# 使用较小的 batch_size
# 编辑脚本，修改 batch_size_s=60 为 batch_size_s=30
```

---

## 📁 输出文件

不同模型会生成不同后缀的文件：

- `meeting_transcript_assemblyai.md` - AssemblyAI 转录
- `meeting_transcript_sensevoice.md` - SenseVoice 转录
- `meeting_transcript_paraformer.md` - Paraformer 转录

---

## 🎯 快速开始

```bash
# 1. 安装依赖（选择一种）
pip install requests  # 仅 AssemblyAI
# 或
pip install funasr modelscope  # 本地模型

# 2. 运行转录
python transcribe_multi_model.py meeting.mp3

# 3. 选择模型并等待完成
```

完成！🚀
