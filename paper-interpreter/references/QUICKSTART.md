# 快速开始指南 🚀

## 📋 前置要求

- Python 3.7+
- Nano Banana API Token
- 网络连接

## ⚡ 5分钟快速开始

### 1️⃣ 安装依赖

```bash
pip3 install requests fpdf2
```

### 2️⃣ 配置 Nano Banana Token

```bash
export NANO_BANANA_TOKEN="your_token_here"
```

### 3️⃣ 运行脚本

```bash
python3 paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf
```

### 4️⃣ 查看结果

```bash
cd paper_output
ls -la
```

你会看到：
- `{arxiv_id}.pdf` - 图文并茂的PDF
- `{arxiv_id}.md` - 黄叔风格Markdown
- `index.html` - 2026设计HTML
- `images/` - 纽约客风格插画

## 🎯 完整示例

```bash
# 1. 克隆或下载项目
cd /home/tony0523/.claude/skills/paper-interpreter

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 设置Token
export NANO_BANANA_TOKEN="nb_xxxxxxxxxxxxx"

# 4. 处理论文
python3 paper_interpreter.py https://arxiv.org/pdf/2401.00001.pdf

# 5. 查看输出
cd paper_output
ls -la

# 6. 在浏览器中打开HTML
# Windows: explorer.exe index.html
# Linux: xdg-open index.html
# Mac: open index.html
```

## 📝 在 Claude Code 中使用

### 方法1: 直接对话

```
你: 帮我解析这篇论文：https://arxiv.org/pdf/2401.00001.pdf

Claude: 好的，我来使用五阶段工作流为你解析这篇论文...
[自动调用 paper-interpreter skill]
```

### 方法2: Python 代码

```python
from paper_interpreter import PaperInterpreter

# 创建解析器
interpreter = PaperInterpreter()

# 处理论文
interpreter.process_paper("https://arxiv.org/pdf/2401.00001.pdf")
```

## 🎨 输出预览

### Markdown (黄叔风格)
```markdown
# 论文标题

你有没有想过，这篇论文到底在解决什么问题？

让我用一个类比来解释：就像你在黑暗中找钥匙...
```

### HTML (2026设计)
- 暖调 Muted 配色
- Noto Serif SC + Inter 字体
- 滚动动画效果
- 响应式设计

### PDF (图文并茂)
- 嵌入纽约客风格插画
- 原生PDF排版
- 中文支持

### 插画 (纽约客风格)
- 3-4色 muted 配色
- 中世纪现代美学
- 极简几何形状
- 无文字标注

## ⚙️ 配置选项

### 自定义输出目录

```python
interpreter = PaperInterpreter(output_dir="my_papers")
```

### 批量处理

```bash
for url in paper1.pdf paper2.pdf paper3.pdf; do
    python3 paper_interpreter.py "https://arxiv.org/pdf/$url"
done
```

## 🐛 常见问题

### Q: 提示"未设置 NANO_BANANA_TOKEN"

**A:** 设置环境变量
```bash
export NANO_BANANA_TOKEN="your_token_here"
```

### Q: 下载失败

**A:** 检查网络连接和URL是否正确
```bash
# 测试URL
curl -I https://arxiv.org/pdf/2401.00001.pdf
```

### Q: 插画生成失败

**A:** 检查Token是否有效
```bash
# 测试API
curl -X POST https://api.nanobanana.ai/v1/images/generations \
  -H "Authorization: Bearer $NANO_BANANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-2.0-flash-exp","prompt":"test","n":1}'
```

### Q: PDF中文显示问题

**A:** 当前使用内置字体，中文可能显示为问号。完整中文支持需要配置STHeiti字体。

## 📊 处理时间

- 阶段1 (信息获取): ~5-10秒
- 阶段2 (文章生成): ~1秒
- 阶段3 (配图生成): ~20-40秒 (4张图)
- 阶段4 (HTML生成): ~1秒
- 阶段5 (PDF生成): ~2-5秒

**总计**: 约 30-60秒

## 💡 最佳实践

1. **先测试**: 用一篇短论文测试完整流程
2. **监控Token**: 注意API使用量
3. **保存输出**: 及时备份生成的文件
4. **批量处理**: 使用脚本批量处理多篇论文

## 🔗 相关文档

- [完整文档](README.md)
- [工作流详解](WORKFLOW.md)
- [Nano Banana配置](NANO_BANANA_SETUP.md)
- [使用示例](example_usage.py)

## 🎉 开始使用

现在你已经准备好了！运行你的第一个论文解析：

```bash
export NANO_BANANA_TOKEN="your_token_here"
python3 paper_interpreter.py https://arxiv.org/pdf/2401.00001.pdf
```

享受五阶段工作流带来的高效体验！🚀
