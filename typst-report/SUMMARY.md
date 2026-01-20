# Typst Report Skill - 功能总结

## 核心能力

这个 skill 提供 **完整的文档生成工作流**：

```
JSON 数据 → .typ 源文件 → PDF 文档
```

## 输出内容

### 1. .typ 源文件（Typst 源代码）

**特点：**
- 纯文本格式
- 可读、可编辑
- 可版本控制（Git）
- 可重复编译

**示例：**
```typst
#import "templates/business.typ": *

#show: report-conf.with(
  title: "月度报告",
)

= 概览
本月业绩良好...
```

**用途：**
- 查看生成逻辑
- 手动调整格式
- 学习 Typst 语法
- 作为模板复用

### 2. PDF 文档（最终输出）

**特点：**
- 专业排版
- 跨平台兼容
- 格式固定
- 可打印、可分享

**内容：**
- 封面页
- 目录页
- 正文（文本、表格、图表）
- 页眉页脚

## 使用方式

### 快速开始

```bash
# 1. 准备数据
cat > data.json << 'EOF'
{
  "title": "测试报告",
  "summary": "这是一个测试..."
}
EOF

# 2. 生成报告（同时生成 .typ 和 PDF）
python scripts/generate_report.py data.json

# 3. 查看输出
ls output/
# report_20260120_143000.typ  ← 源文件
# report_20260120_143000.pdf  ← PDF 文档
```

### 三种工作流

| 工作流 | 命令 | 输出 | 适用场景 |
|-------|------|------|---------|
| **完整流程** | `generate_report.py` | .typ + PDF | 生产环境 |
| **分步执行** | `generate.py` + `compile.py` | .typ + PDF | 开发调试 |
| **仅编译** | `compile.py` | PDF | 已有 .typ |

## 脚本说明

### 生成脚本

| 脚本 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `generate.py` | 生成 .typ 文件 | JSON | .typ |
| `generate_report.py` | 完整工作流 | JSON | .typ + PDF |

### 编译脚本

| 脚本 | 平台 | 功能 |
|------|------|------|
| `compile.py` | 跨平台 | 编译 .typ → PDF |
| `compile.sh` | Linux/macOS | 编译 .typ → PDF |
| `compile.bat` | Windows | 编译 .typ → PDF |

### 测试脚本

| 脚本 | 功能 |
|------|------|
| `test_compile.py` | 运行所有测试 |

## 模板类型

### 商业报告模板 (business.typ)

**特点：**
- 独立封面页
- 自动生成目录
- KPI 卡片
- 数据表格
- 图表组件

**适用：**
- 业务报告
- 数据分析
- 项目进展

### 学术论文模板 (academic.typ)

**特点：**
- 简洁封面
- 摘要和关键词
- 三线表
- 数学公式

**适用：**
- 学术论文
- 研究报告
- 技术文档

## 数据格式

### JSON 结构

```json
{
  "title": "报告标题",
  "subtitle": "副标题",
  "author": "作者",
  "summary": "概览内容",
  "metrics": [
    {
      "label": "指标名",
      "value": "数值",
      "change": 0.15
    }
  ],
  "sections": [
    {
      "heading": "章节标题",
      "level": 2,
      "type": "text|list|table|chart",
      "content": "内容..."
    }
  ]
}
```

### 支持的 section 类型

- `text` - 普通文本
- `list` - 无序列表
- `checklist` - 任务清单
- `table` - 数据表格
- `chart` - 图表（line/bar）

## 实际应用

### 1. 自动化周报

```python
# 每周五自动生成
from generate_report import generate_report_workflow

data = fetch_weekly_data()  # 从数据库获取
result = generate_report_workflow(
    json_file="weekly-data.json",
    output_dir="reports/weekly",
)
```

### 2. 批量生成客户报告

```python
for customer in customers:
    data = generate_customer_data(customer)
    generate_report_workflow(
        json_file=f"data/{customer}.json",
        output_dir=f"reports/{customer}",
        keep_typ=False,  # 只保留 PDF
    )
```

### 3. CI/CD 集成

```yaml
# GitHub Actions
- name: Generate Report
  run: |
    python scripts/generate_report.py data.json
    
- name: Upload PDF
  uses: actions/upload-artifact@v3
  with:
    name: report
    path: output/*.pdf
```

## 文件结构

```
typst-report/
├── scripts/                      # 脚本
│   ├── generate.py               # 生成 .typ
│   ├── generate_report.py        # 完整工作流
│   ├── compile.py                # 编译 PDF
│   └── test_compile.py           # 测试
├── typst-templates/              # 模板
│   ├── main.typ                  # 商业报告入口
│   ├── standard-example.typ      # 标准示例
│   ├── lib/                      # 库文件
│   │   ├── theme.typ             # 样式
│   │   ├── utils.typ             # 工具
│   │   └── charts.typ            # 图表
│   └── templates/                # 模板
│       ├── business.typ          # 商业模板
│       └── academic.typ          # 学术模板
└── output/                       # 输出目录
    ├── *.typ                     # 生成的源文件
    └── *.pdf                     # 生成的 PDF
```

## 优势对比

| 特性 | 传统方式 | Typst Skill |
|------|---------|-------------|
| 编写速度 | 慢（手动） | 快（自动） |
| 格式一致性 | 易出错 | 100% 一致 |
| 版本控制 | 困难 | Git 友好 |
| 自动化 | 难 | 完全可编程 |
| 数学公式 | 需插件 | 原生支持 |
| 中文支持 | 需配置 | 开箱即用 |
| 编译速度 | 慢 | 秒级 |
| 学习曲线 | 陡峭 | 平缓 |

## 快速参考

### 生成报告

```bash
# 完整工作流（推荐）
python scripts/generate_report.py data.json

# 仅生成 .typ
python scripts/generate.py data.json -o report.typ

# 生成并编译
python scripts/generate.py data.json -o report.typ --compile
```

### 编译文档

```bash
# 编译现有 .typ
python scripts/compile.py report.typ

# 传递 JSON 数据
python scripts/compile.py main.typ --json-file data.json
```

### 测试

```bash
# 运行所有测试
python scripts/test_compile.py
```

## 文档资源

- [README.md](README.md) - 项目概览
- [OUTPUTS.md](OUTPUTS.md) - 输出内容详解
- [USAGE.md](USAGE.md) - 详细使用指南
- [DEMO.md](DEMO.md) - 快速演示
- [SKILL.md](SKILL.md) - Typst 语法参考

## 获取帮助

```bash
# 查看帮助
python scripts/generate.py --help
python scripts/compile.py --help
python scripts/generate_report.py --help
```

## 总结

这个 skill 提供了：

✅ **完整的文档生成能力** - JSON → .typ → PDF  
✅ **双重输出** - 源文件 + 最终文档  
✅ **多种使用方式** - 脚本、CLI、自动化  
✅ **专业模板** - 商业报告、学术论文  
✅ **开箱即用** - 包含示例和测试  

**核心价值：让文档生成自动化、标准化、可编程化。**
