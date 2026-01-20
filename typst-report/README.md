# Typst Report Generation Skill

**核心能力：将 Typst 源代码 (.typ) 编译为专业 PDF 文档**

```
┌──────────────┐                    ┌──────────────┐
│              │                    │              │
│  .typ 源码   │  ──[编译]──>       │  PDF 文档    │
│              │                    │              │
│ • 标题       │                    │ ✓ 排版精美   │
│ • 段落       │                    │ ✓ 自动分页   │
│ • 公式       │                    │ ✓ 页码目录   │
│ • 表格       │                    │ ✓ 中文支持   │
│ • 图表数据   │                    │ ✓ 图表渲染   │
└──────────────┘                    └──────────────┘
```

使用 Typst 排版系统生成专业 PDF 报告的 OpenCode skill。

## 功能特性

- 🔄 **完整工作流** - JSON → .typ → PDF
- 📄 **双重输出** - 生成 .typ 源文件和 PDF 文档
- 📊 **数据驱动** - 从 JSON/CSV 数据生成报告
- 🎨 **中文排版** - 支持中文字体和排版规范
- 📈 **图表组件** - 折线图、柱状图、KPI 卡片
- 📑 **自动化** - 封面、目录、页码自动生成
- 🎯 **多模板** - 商业报告、学术论文模板

## 目录结构

```
typst-report/
├── SKILL.md                          # Skill 定义文件
├── README.md                         # 本文件
├── scripts/                          # 编译脚本
│   ├── compile.py                    # Python 编译脚本（推荐）
│   ├── compile.sh                    # Shell 编译脚本
│   ├── compile.bat                   # Windows 批处理脚本
│   └── test_compile.py               # 测试脚本
└── typst-templates/                  # Typst 模板
    ├── main.typ                      # 商业报告入口
    ├── standard-example.typ          # 标准格式示例
    ├── academic-example.typ          # 学术论文示例
    ├── example-data.json             # 测试数据
    ├── lib/
    │   ├── utils.typ                 # 数据处理工具
    │   ├── theme.typ                 # 全局样式
    │   └── charts.typ                # 图表组件
    ├── templates/
    │   ├── business.typ              # 商业报告模板
    │   └── academic.typ              # 学术论文模板
    └── assets/
        ├── fonts/                    # 字体目录
        └── images/                   # 图片目录
```

## 使用方式

### 方式 1: 完整工作流（推荐）

**同时生成 .typ 源文件和 PDF 文档**

```bash
# 从 JSON 数据生成报告
python scripts/generate_report.py data.json

# 输出:
#   output/report_20260120_143000.typ  ← Typst 源文件
#   output/report_20260120_143000.pdf  ← PDF 文档
```

### 方式 2: 分步执行

**步骤 1: 生成 .typ 文件**
```bash
python scripts/generate.py data.json -o report.typ
```

**步骤 2: 编译为 PDF**
```bash
python scripts/compile.py report.typ
```

### 方式 3: 一步到位

**生成 .typ 并自动编译**
```bash
python scripts/generate.py data.json -o report.typ --compile
```

### 方式 4: 使用现有模板

**直接编译模板文件**
```bash
# 使用编译脚本（跨平台）
python scripts/compile.py typst-templates/standard-example.typ

# 传递 JSON 数据
python scripts/compile.py typst-templates/main.typ \
  --json-file typst-templates/example-data.json

# Shell 脚本（Linux/macOS）
bash scripts/compile.sh typst-templates/standard-example.typ

# 批处理脚本（Windows）
scripts\compile.bat typst-templates\standard-example.typ
```

### 方式 5: 直接使用 Typst CLI

```bash
# 基础编译
typst compile typst-templates/standard-example.typ output.pdf

# 使用示例数据
typst compile \
  --input payload="$(cat typst-templates/example-data.json)" \
  typst-templates/main.typ \
  test-report.pdf
```

### 方式 6: 在 GitHub Issue/PR 中

评论：
```
/oc 生成一份测试报告
```

### 快速测试

```bash
# 运行所有测试
python scripts/test_compile.py
```

## 数据格式

支持的输入格式：
- **JSON**（推荐）- 通过 `--input` 传递
- **CSV** - 从文件读取
- **Markdown** - 需要预处理为 JSON

### JSON 数据结构示例

```json
{
  "title": "报告标题",
  "subtitle": "副标题",
  "author": "作者",
  "summary": "概览内容",
  "metrics": [
    {"label": "指标名", "value": "1,234", "change": 0.15}
  ],
  "sections": [
    {
      "heading": "章节标题",
      "level": 2,
      "type": "text",
      "content": "章节内容"
    }
  ]
}
```

## Skill 输出内容

这个 skill 会生成以下文件：

### 1. .typ 源文件（可选保留）

Typst 源代码文件，包含：
- 文档结构和内容
- 格式化标记
- 数据引用
- 可读、可编辑、可版本控制

**示例：**
```typst
#import "templates/business.typ": *

#show: report-conf.with(
  title: "月度报告",
  author: "系统",
)

= 概览
本月业绩良好...

#kpi-cards((
  (label: "销售额", value: "¥1,234,567", change: 0.15),
))
```

### 2. PDF 文档（最终输出）

专业排版的 PDF 文件，包含：
- ✅ 封面页（标题、作者、日期）
- ✅ 目录页（自动生成）
- ✅ 正文内容（格式化文本、表格、图表）
- ✅ 页眉页脚（页码）
- ✅ 矢量图表（可缩放）

### 输出方式

**方式 1: 仅生成 .typ 文件**
```bash
python scripts/generate.py data.json -o report.typ
```

**方式 2: 生成 .typ 并编译为 PDF**
```bash
python scripts/generate.py data.json -o report.typ --compile
```

**方式 3: 完整工作流（推荐）**
```bash
# 同时生成 .typ 和 PDF
python scripts/generate_report.py data.json

# 输出:
#   output/report_20260120_143000.typ  ← 源文件
#   output/report_20260120_143000.pdf  ← PDF 文档
```

**方式 4: 仅保留 PDF**
```bash
# 不保留 .typ 源文件
python scripts/generate_report.py data.json --no-keep-typ
```

## 参考资源

- [输出内容详解](OUTPUTS.md) - 了解 .typ 和 PDF 文件
- [使用指南](USAGE.md) - 详细使用说明
- [快速演示](DEMO.md) - 实际示例演示
- [Typst 官方文档](https://typst.app/docs/)
- [CeTZ 图表库](https://typst.app/universe/package/cetz-plot/)
- [开发计划](../../doc/typst-skill-development-plan.md)
