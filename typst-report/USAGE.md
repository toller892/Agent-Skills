# Typst Report - 使用指南

## 核心能力

这个 skill 提供 **Typst 源码 → PDF 文档** 的完整编译能力。

```
┌─────────────┐
│  .typ 文件  │  ← 左边：Typst 源代码
│  (源代码)   │
└─────────────┘
       ↓
   [编译脚本]
       ↓
┌─────────────┐
│  PDF 文档   │  ← 右边：排版好的文档
│  (最终输出) │
└─────────────┘
```

## 快速开始

### 1. 安装 Typst

```bash
# macOS/Linux
curl -fsSL https://typst.app/install.sh | sh

# Windows
winget install --id Typst.Typst

# 或从 GitHub 下载
# https://github.com/typst/typst/releases
```

### 2. 编译示例文档

```bash
# 方式 1: 使用 Python 脚本（推荐）
python scripts/compile.py typst-templates/standard-example.typ

# 方式 2: 直接使用 Typst
typst compile typst-templates/standard-example.typ output.pdf
```

### 3. 查看输出

编译成功后，会在同目录生成 `standard-example.pdf`

## 使用场景

### 场景 1: 编译静态文档

**适用于：** 学术论文、技术文档

```bash
# 编写 .typ 文件
cat > my-paper.typ << 'EOF'
#import "templates/academic.typ": *

#show: academic-conf.with(
  title: "我的论文",
  author: "张三",
)

= 引言
这是论文内容...

$E = m c^2$
EOF

# 编译
python scripts/compile.py my-paper.typ
```

### 场景 2: 数据驱动报告

**适用于：** 业务报告、数据分析

```bash
# 准备数据
cat > data.json << 'EOF'
{
  "title": "月度报告",
  "metrics": [
    {"label": "销售额", "value": "¥1,234,567", "change": 0.15}
  ],
  "sections": [
    {
      "heading": "概览",
      "type": "text",
      "content": "本月业绩良好..."
    }
  ]
}
EOF

# 编译（传递数据）
python scripts/compile.py typst-templates/main.typ \
  --json-file data.json \
  -o report.pdf
```

### 场景 3: 自动化生成

**适用于：** CI/CD、定时任务

```python
# generate_report.py
import json
from compile import compile_typst

# 从数据库获取数据
data = fetch_data_from_database()

# 生成报告
payload = {
    "title": "自动化报告",
    "metrics": data["metrics"],
    "sections": data["sections"],
}

# 编译
compile_typst(
    input_file="typst-templates/main.typ",
    output_file=f"reports/report-{date}.pdf",
    payload=payload
)
```

## 编译脚本详解

### Python 脚本 (compile.py)

**优势：** 跨平台、功能完整、易于集成

```bash
# 基础用法
python scripts/compile.py input.typ

# 指定输出文件
python scripts/compile.py input.typ -o output.pdf

# 传递 JSON 数据（字符串）
python scripts/compile.py input.typ --json '{"title": "报告"}'

# 传递 JSON 数据（文件）
python scripts/compile.py input.typ --json-file data.json

# 指定字体路径
python scripts/compile.py input.typ --font-path ./fonts

# 指定根目录
python scripts/compile.py input.typ --root .

# 查看帮助
python scripts/compile.py --help
```

### Shell 脚本 (compile.sh)

**适用于：** Linux/macOS

```bash
# 基础用法
bash scripts/compile.sh input.typ

# 指定输出
bash scripts/compile.sh input.typ -o output.pdf

# 传递 JSON
bash scripts/compile.sh input.typ -j '{"title": "报告"}'

# 从文件读取 JSON
bash scripts/compile.sh input.typ -f data.json
```

### 批处理脚本 (compile.bat)

**适用于：** Windows

```cmd
REM 基础用法
scripts\compile.bat input.typ

REM 指定输出
scripts\compile.bat input.typ output.pdf
```

## 模板选择

### 商业报告模板 (business.typ)

**特点：**
- 独立封面页
- 自动生成目录
- KPI 卡片、数据表格
- 现代商务风格

**使用：**
```typst
#import "templates/business.typ": *

#show: report-conf.with(
  title: "业务报告",
  author: "公司名",
)

= 概览
...
```

### 学术论文模板 (academic.typ)

**特点：**
- 简洁封面
- 摘要和关键词
- 三线表
- 学术风格

**使用：**
```typst
#import "templates/academic.typ": *

#show: academic-conf.with(
  title: "论文标题",
  author: "作者",
  abstract: [摘要内容],
  keywords: ("关键词1", "关键词2"),
)

= 引言
...
```

## 测试

运行完整测试套件：

```bash
python scripts/test_compile.py
```

测试包括：
1. 基础编译测试
2. JSON 数据传递测试
3. JSON 文件读取测试

## 常见问题

### Q: 中文显示为方块？

**A:** 需要安装中文字体

```bash
# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk

# macOS（通常已安装）
# Windows（通常已安装）
```

### Q: 编译失败？

**A:** 检查：
1. Typst 是否安装：`typst --version`
2. 输入文件是否存在
3. 语法是否正确（查看错误信息）

### Q: 如何自定义样式？

**A:** 修改 `lib/theme.typ` 中的颜色、字体、间距等配置

### Q: 如何添加图片？

**A:** 
```typst
#image("assets/images/logo.png", width: 80%)
```

### Q: 如何生成图表？

**A:** 使用内置图表组件：
```typst
#import "lib/charts.typ": *

#line-chart(
  data: ((1, 100), (2, 150), (3, 200)),
  title: "趋势图",
)
```

## 进阶用法

### 批量生成报告

```python
# batch_generate.py
import json
from pathlib import Path
from compile import compile_typst

# 读取多个数据文件
data_dir = Path("data")
for json_file in data_dir.glob("*.json"):
    with open(json_file) as f:
        payload = json.load(f)
    
    output_file = f"reports/{json_file.stem}.pdf"
    compile_typst(
        "typst-templates/main.typ",
        output_file,
        payload=payload
    )
    print(f"✓ 生成: {output_file}")
```

### 集成到 CI/CD

```yaml
# .github/workflows/generate-report.yml
name: Generate Report

on:
  schedule:
    - cron: '0 0 * * 1'  # 每周一

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Typst
        run: |
          curl -fsSL https://typst.app/install.sh | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      
      - name: Generate Report
        run: |
          python scripts/compile.py \
            typst-templates/main.typ \
            --json-file data/weekly-report.json \
            -o weekly-report.pdf
      
      - name: Upload PDF
        uses: actions/upload-artifact@v3
        with:
          name: weekly-report
          path: weekly-report.pdf
```

## 参考资源

- [Typst 官方文档](https://typst.app/docs/)
- [Typst 语法速查](https://typst.app/docs/reference/)
- [CeTZ 图表库](https://typst.app/universe/package/cetz-plot/)
- [Typst Universe](https://typst.app/universe/)
