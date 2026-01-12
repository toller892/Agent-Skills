# 论文解析器 - 五阶段工作流 📄

将论文链接转换为图文并茂的PDF和HTML文档，采用黄叔风格写作+纽约客插画+2026前沿设计。

## 🎯 五阶段工作流

### 阶段1: 信息获取 🔍
- WebFetch: 抓取 arXiv 摘要页
- WebSearch: 搜索补充技术细节
- WebFetch: 获取技术博客深度解读

### 阶段2: 文章生成 ✍️
**黄叔风格量化标准:**
- 类比密度 ≥1个/400字
- 第二人称"你" >30%
- 三层递进解释结构
- Write: 输出 Markdown 文件

### 阶段3: 配图生成
**API:** Nano Banana (Gemini 2.0 Flash)

**风格:** 纽约客杂志极简插画
- 3-4色 muted 配色
- 中世纪现代美学
- 无文字标注
- Base64解码保存PNG

### 阶段4: HTML生成 🌐
**2026前沿设计规范:**
- 暖调 Muted 配色 (#FDFBF7, #7D9B76, #C4785A...)
- Noto Serif SC + Inter 字体
- Intersection Observer 滚动动画
- Write: 输出完整 HTML 文件

### 阶段5: PDF生成 📑
- 调用 generate_pdf.py 脚本
- fpdf2 库生成原生 PDF (非 HTML 转换)
- 中文字体: STHeiti

## 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install requests fpdf2
```

## 使用方法

### 方法1: 从URL下载并解析

```bash
python paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf
```

### 方法2: 解析本地PDF文件

```bash
python paper_interpreter.py /path/to/paper.pdf
```

## 输出结构

运行后会在 `paper_output` 目录下生成以下文件：

```
paper_output/
├── {arxiv_id}.pdf          # 图文并茂的PDF文档
├── {arxiv_id}.md           # 黄叔风格Markdown
├── {arxiv_id}_log.txt      # 执行日志
├── index.html              # 2026设计风格HTML
├── paper.pdf               # 原始PDF
└── images/                 # 纽约客风格插画
    ├── illustration_01.png
    ├── illustration_02.png
    ├── illustration_03.png
    └── illustration_04.png
```

## 环境变量

```bash
# 必需：配置Nano Banana API Token以生成插画
export NANO_BANANA_TOKEN="your_token_here"
```

如果不配置Token，将跳过插画生成，但仍会生成Markdown、HTML和PDF。

## 使用方法

### 方法1: 命令行使用

```bash
# 设置Token
export NANO_BANANA_TOKEN="your_token_here"

# 运行
python3 paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf
```

### 方法2: 在Claude Code中使用

直接对话：
```
你：帮我解析这篇论文：https://arxiv.org/pdf/2301.12345.pdf
Claude：好的，我来使用五阶段工作流为你解析...
```

## 在Claude Code中使用

### 作为Python脚本

直接在Claude Code中运行：

```python
from paper_interpreter import PaperInterpreter

# 创建解析器实例
interpreter = PaperInterpreter(output_dir="my_paper_output")

# 处理论文
interpreter.process_paper("https://arxiv.org/pdf/2301.12345.pdf")
```

### 集成到工作流

```python
# 批量处理多篇论文
papers = [
    "https://arxiv.org/pdf/2301.12345.pdf",
    "https://arxiv.org/pdf/2302.67890.pdf",
]

for i, paper_url in enumerate(papers):
    interpreter = PaperInterpreter(output_dir=f"paper_{i+1}")
    interpreter.process_paper(paper_url)
```

## 示例输出

### HTML页面预览

生成的HTML页面包含：
- 清晰的页面标题和时间戳
- 按页码组织的内容
- 嵌入的图片展示
- 响应式设计，适配各种屏幕

### Markdown文档

```markdown
# 论文解读

生成时间: 2026-01-08 10:30:00

---

## 第 1 页

[论文第一页的文字内容...]

![图片](images/image_01_001.png)

---

## 第 2 页

[论文第二页的文字内容...]

![图片](images/image_02_001.png)

---
```

## 高级用法

### 自定义输出目录

```python
interpreter = PaperInterpreter(output_dir="custom_output")
```

### 只提取特定内容

```python
# 只提取文字
text_content, _ = interpreter.extract_content("paper.pdf")

# 只生成HTML
interpreter.generate_html(text_content, images_info)
```

## 注意事项

⚠️ **PDF格式**: 某些加密或扫描版PDF可能无法正确提取内容
⚠️ **网络连接**: 从URL下载需要稳定的网络连接
⚠️ **文件大小**: 大型PDF文件处理时间较长
⚠️ **中文支持**: 完全支持中文内容的提取和显示

## 故障排除

### 问题1: 无法下载PDF

```
解决方案: 检查URL是否正确，或尝试手动下载后使用本地文件
```

### 问题2: 图片提取失败

```
解决方案: 某些PDF的图片格式可能不支持，这是正常现象
```

### 问题3: 中文乱码

```
解决方案: 确保使用UTF-8编码保存文件
```

## 技术栈

- **PyMuPDF (fitz)**: PDF解析和内容提取
- **requests**: HTTP请求和文件下载
- **Python 3.7+**: 核心语言

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
