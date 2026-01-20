# 故障排除指南

## 常见问题

### 问题 1: Typst 在线编辑器报错 "File not found"

**错误信息：**
```
File not found (searched at typst-report/typst-templates/templates/business.typ)
```

**原因：**
生成的 `.typ` 文件使用了相对路径导入模板，但在 Typst 在线编辑器中无法访问本地文件系统。

**解决方案 A: 使用独立版本（推荐）**

使用不依赖外部文件的独立版本：

```bash
# 生成独立版本（包含所有样式定义）
python scripts/generate.py data.json \
  -o report-standalone.typ \
  --standalone
```

或者直接使用已生成的独立版本：
- `agent-skills-report-standalone.typ`

**解决方案 B: 上传所有依赖文件**

在 Typst 在线编辑器中：

1. 上传主文件：`agent-skills-report.typ`
2. 创建目录结构并上传依赖文件：
   ```
   typst-report/
   └── typst-templates/
       ├── templates/
       │   ├── business.typ
       │   └── academic.typ
       └── lib/
           ├── theme.typ
           ├── utils.typ
           └── charts.typ
   ```

**解决方案 C: 本地编译**

安装 Typst 后本地编译：

```bash
# 安装 Typst
# macOS/Linux: curl -fsSL https://typst.app/install.sh | sh
# Windows: winget install --id Typst.Typst

# 编译
typst compile --root . agent-skills-report.typ agent-skills-report.pdf
```

### 问题 2: 中文显示为方块

**原因：**
缺少中文字体。

**解决方案：**

```bash
# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk

# macOS（通常已安装）
# 无需操作

# Windows（通常已安装）
# 无需操作
```

或在 `.typ` 文件中指定备用字体：

```typst
#set text(
  font: ("Noto Sans CJK SC", "Microsoft YaHei", "SimSun", "Arial"),
)
```

### 问题 3: 编译超时或内存不足

**原因：**
数据量过大或图表过多。

**解决方案：**

1. **减少数据量**
   ```json
   {
     "sections": [
       // 限制每个表格的行数
       {"type": "table", "data": [...]}  // 最多 100 行
     ]
   }
   ```

2. **预生成图表为图片**
   ```python
   import matplotlib.pyplot as plt
   
   # 生成图表
   plt.plot([1, 2, 3], [4, 5, 6])
   plt.savefig("chart.svg")
   ```
   
   然后在 `.typ` 中引用：
   ```typst
   #image("chart.svg")
   ```

3. **分页处理**
   将大报告拆分为多个小报告。

### 问题 4: 路径错误

**错误信息：**
```
error: file not found
```

**原因：**
相对路径计算错误。

**解决方案：**

确保在正确的目录运行命令：

```bash
# 错误：在子目录运行
cd typst-report
python scripts/generate.py data.json  # ✗ 路径错误

# 正确：在项目根目录运行
cd /path/to/project
python typst-report/scripts/generate.py data.json  # ✓ 正确
```

或使用绝对路径：

```bash
python /path/to/project/typst-report/scripts/generate.py \
  /path/to/data.json \
  -o /path/to/output/report.typ
```

### 问题 5: JSON 解析失败

**错误信息：**
```
JSONDecodeError: Expecting property name enclosed in double quotes
```

**原因：**
JSON 格式错误。

**解决方案：**

1. **检查 JSON 格式**
   ```bash
   # 使用 jq 验证
   jq . data.json
   
   # 或使用 Python
   python -m json.tool data.json
   ```

2. **常见错误**
   ```json
   {
     "title": "报告",
     "sections": [
       {
         "heading": "章节",
         "content": "内容"  // ✗ 最后一项不能有逗号
       },  // ✗ 删除这个逗号
     ]
   }
   ```
   
   正确格式：
   ```json
   {
     "title": "报告",
     "sections": [
       {
         "heading": "章节",
         "content": "内容"
       }
     ]
   }
   ```

### 问题 6: 生成的 PDF 格式不对

**原因：**
模板配置问题。

**解决方案：**

1. **检查模板类型**
   ```bash
   # 商业报告（默认）
   python scripts/generate.py data.json --template business
   
   # 学术论文
   python scripts/generate.py data.json --template academic
   ```

2. **自定义样式**
   修改 `typst-report/typst-templates/lib/theme.typ`：
   ```typst
   // 修改颜色
   #let brand-primary = rgb("#0056b3")  // 改为你的品牌色
   
   // 修改字体大小
   #set text(size: 11pt)  // 改为你需要的大小
   ```

## 调试技巧

### 1. 查看生成的 .typ 文件

```bash
# 生成但不编译
python scripts/generate.py data.json -o report.typ

# 查看内容
cat report.typ
```

### 2. 逐步调试

```bash
# 步骤 1: 生成 .typ
python scripts/generate.py data.json -o report.typ

# 步骤 2: 手动编译
typst compile report.typ

# 步骤 3: 查看错误信息
```

### 3. 使用示例数据测试

```bash
# 使用项目自带的示例数据
python scripts/generate_report.py \
  typst-report/typst-templates/example-data.json
```

### 4. 启用详细日志

```python
# 在脚本中添加调试信息
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 获取帮助

### 查看帮助信息

```bash
python scripts/generate.py --help
python scripts/compile.py --help
python scripts/generate_report.py --help
```

### 运行测试

```bash
# 运行所有测试
python scripts/test_compile.py

# 查看测试输出
```

### 查看文档

- [README.md](README.md) - 项目概览
- [USAGE.md](USAGE.md) - 详细使用指南
- [OUTPUTS.md](OUTPUTS.md) - 输出内容说明
- [DEMO.md](DEMO.md) - 快速演示

### 报告问题

如果以上方法都无法解决问题，请提供：

1. 错误信息（完整的错误堆栈）
2. 使用的命令
3. 输入的 JSON 数据
4. 系统环境（操作系统、Typst 版本）

## 快速参考

| 问题 | 解决方案 |
|------|---------|
| 在线编辑器报错 | 使用独立版本或上传所有依赖 |
| 中文方块 | 安装中文字体 |
| 编译超时 | 减少数据量或预生成图表 |
| 路径错误 | 在项目根目录运行 |
| JSON 错误 | 验证 JSON 格式 |
| 格式不对 | 检查模板类型 |
