# 📄 Document to Beautiful HTML Skill

[![OpenCode Skill](https://img.shields.io/badge/OpenCode-Skill-blue)]()
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green)]()
[![License MIT](https://img.shields.io/badge/License-MIT-yellow)]()

将本地文档转换为精美的图文并茂HTML页面，专门为Twitter分享优化，生成4张连贯的内容卡片。

## ✨ 功能特点

- 📖 **智能文档解析** - 支持 txt、md、docx 格式
- 🎨 **精美视觉设计** - 渐变背景、阴影效果、响应式布局
- 🖼️ **AI图片生成** - 使用 Gemini API 生成配套图片
- 📱 **Twitter友好** - 自动分割为4张连贯内容卡片
- 🐦 **推文自动生成** - 生成吸引人的Twitter推文线程
- 🔐 **安全Key管理** - 支持环境变量和交互式输入

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 基本用法

```bash
# 只生成文字版本
python src/main.py document.txt

# 生成图片版本（需要API Key）
python src/main.py document.md --api-key YOUR_GEMINI_API_KEY

# 指定图片宽高比
python src/main.py document.docx -k YOUR_KEY --aspect-ratio 1:1
```

### 3. 交互式模式

```bash
python src/main.py --interactive
```

## 📖 使用示例

### 示例1: 转换 Markdown 文档

```bash
python src/main.py article.md -k YOUR_API_KEY -o my_output
```

### 示例2: 不生成图片

```bash
python src/main.py notes.txt --no-images
```

### 示例3: 自定义宽高比

```bash
python src/main.py report.docx -k YOUR_KEY -r 1:1
```

## 🎯 输出说明

转换完成后，您将获得：

```
output/
├── beautiful_content_1.html  # 第1张卡片
├── beautiful_content_2.html  # 第2张卡片
├── beautiful_content_3.html  # 第3张卡片
├── beautiful_content_4.html  # 第4张卡片
├── complete_content.html     # 完整页面
├── twitter_threads.txt       # Twitter推文线程
├── individual_tweets.txt     # 独立推文（可直接复制发布）
└── images/
    ├── card_1_image.png      # 配套图片
    ├── card_2_image.png
    ├── card_3_image.png
    └── card_4_image.png
```

### 🐦 推文内容

自动生成两种格式的推文：

1. **twitter_threads.txt** - 完整的推文线程，包含开场、4张卡片内容、收尾，共6条推文
2. **individual_tweets.txt** - 每条推文独立显示，方便逐条复制发布

#### 推文特点：
- ✅ 自动控制在280字符以内
- ✅ 吸睛开头（🚀💡🔥📚等）
- ✅ 智能摘要内容
- ✅ 自动添加相关话题标签
- ✅ 包含行动号召（CTA）

#### 推文示例：

```
🐦 Twitter 推文线程
============================================================

--- 开场推文 ---
🚀 探索人工智能的奥秘
深度学习和神经网络技术取得显著进展，大型语言模型将AI能力推向新高度...
#AI #人工智能 #机器学习 #深度学习 #Tech

--- 卡片1推文 ---
🔔 第一部分
【当前发展】
深度学习和神经网络技术取得显著进展...
(1/4)

============================================================
```

## 🔧 配置选项

### 命令行参数

| 参数 | 短格式 | 说明 | 默认值 |
|------|--------|------|--------|
| `document` | - | 要转换的文档路径 | 必填 |
| `--api-key` | `-k` | Gemini API Key | 可选 |
| `--output` | `-o` | 输出目录 | `output` |
| `--aspect-ratio` | `-r` | 图片宽高比 | `16:9` |
| `--no-images` | - | 不生成图片 | False |
| `--interactive` | `-i` | 交互式模式 | False |

### 支持的图片宽高比

- `16:9` - 横版（默认，Twitter标准）
- `1:1` - 方形（Instagram风格）
- `9:16` - 竖版（ Stories 风格）
- `4:3` - 标准4:3
- `3:4` - 竖版4:3

## 🔐 API Key 管理

### 方法1: 环境变量

```bash
export GEMINI_API_KEY="your_api_key_here"
python src/main.py document.txt
```

### 方法2: 命令行参数

```bash
python src/main.py document.txt -k your_api_key_here
```

### 方法3: 交互式输入

```bash
python src/main.py --interactive
```

## 📁 项目结构

```
document-to-beautiful-html/
├── SKILL.md                 # Skill 定义文件
├── README.md                # 使用说明
├── requirements.txt         # 依赖列表
├── src/
│   └── main.py             # 主程序入口
├── modules/
│   ├── document_parser.py   # 文档解析模块
│   ├── image_generator.py   # 图片生成模块
│   ├── html_generator.py    # HTML生成模块
│   └── api_key_manager.py   # API Key管理模块
└── assets/                  # 资源文件（可选）
```

## 🛠️ 技术栈

- **文档解析**: docling, python-docx
- **图片生成**: Gemini API (Google)
- **HTML/CSS**: 纯CSS实现，无外部依赖
- **Python**: 3.8+

## 📝 API 文档

本 Skill 使用的图片生成 API：

- **端点**: `https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent`
- **模型**: gemini-2.5-flash-image (快速) 或 gemini-3-pro-image-preview (高分辨率)
- **文档**: [Gemini Image Generation API](https://ai.google.dev/docs/gemini_image_generation)

## ⚠️ 注意事项

1. **API Key 安全**: 建议使用环境变量，不要在代码中硬编码
2. **图片生成**: 无 API Key 时只生成文字版本
3. **文件编码**: 确保文档编码为 UTF-8
4. **依赖安装**: 首次运行前请安装依赖

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**Made with ❤️ for OpenCode Agent Skills**
