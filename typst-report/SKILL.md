---
name: typst-report
description: 使用 Typst 生成专业 PDF 报告，支持图表、表格、多栏布局，适用于业务分析、需求文档等场景
---

# Typst Report Generation Skill

## 概述

这个 skill 帮助你使用 Typst 排版系统生成专业的 PDF 报告。Typst 是一个现代化的标记型排版系统，比 LaTeX 更简单，比 Markdown 转 PDF 更专业。

## 核心能力

- 从 JSON/CSV 数据生成报告
- 支持中文排版
- 包含表格、图表、封面、目录
- 矢量图表（CeTZ）
- 自动分页和页码

## Typst 基础语法速查

### 标题
```typst
= 一级标题
== 二级标题
=== 三级标题
```

### 文本样式
```typst
*粗体* _斜体_ `代码`
```

### 列表
```typst
- 无序列表项
- 另一项

+ 有序列表项
+ 另一项
```

### 表格
```typst
#table(
  columns: (1fr, 1fr, 1fr),
  [*列1*], [*列2*], [*列3*],
  [数据1], [数据2], [数据3],
)
```

### 图片
```typst
#image("path/to/image.png", width: 80%)
```

## 支持的数据格式

### 1. JSON（主要，推荐）

**通过 CLI 传递：**
```bash
typst compile \
  --input payload='{"title": "报告标题", "data": [...]}' \
  main.typ output.pdf
```

**在模板中解析：**
```typst
#let raw-payload = sys.inputs.at("payload", default: "{}")
#let data = json.decode(raw-payload)
#let title = data.at("title", default: "未命名报告")
```

**从文件读取：**
```typst
#let data = json("data.json")
```

### 2. CSV（表格数据）

```typst
#let data = csv("data.csv")
// 返回二维数组：[["列1", "列2"], ["值1", "值2"]]
```

### 3. YAML / TOML / XML

```typst
#let config = yaml("config.yaml")
#let settings = toml("settings.toml")
#let xml_data = xml("data.xml")
```

### 4. Markdown（需要预处理）

Typst 不直接解析 Markdown，需要先转换为 JSON：

**推荐流程（适用于 Issue/PR 内容）：**
```
Markdown (Issue body)
  ↓
OpenCode Agent 解析
  ↓
JSON {title, sections, tasks, code_blocks}
  ↓
Typst 渲染
  ↓
PDF
```

**示例 JSON 结构：**
```json
{
  "title": "需求分析",
  "sections": [
    {
      "heading": "背景",
      "content": "项目需要...",
      "level": 2
    },
    {
      "heading": "任务清单",
      "items": ["任务1", "任务2"],
      "type": "checklist"
    }
  ],
  "code_blocks": [
    {
      "language": "python",
      "code": "def hello():\n    pass"
    }
  ]
}
```

**在 Typst 中渲染：**
```typst
#for section in data.sections [
  #heading(level: section.level)[#section.heading]
  
  #if section.type == "checklist" [
    #for item in section.items [
      - [ ] #item
    ]
  ] else [
    #section.content
  ]
]
```

## 编译命令参考

### 基础编译
```bash
typst compile main.typ output.pdf
```

### 指定字体路径
```bash
typst compile \
  --font-path ./assets/fonts \
  main.typ output.pdf
```

### 指定根目录（安全）
```bash
typst compile \
  --root . \
  --font-path ./assets/fonts \
  main.typ output.pdf
```

## 常见报告类型示例

### 业务报告模板

```typst
#import "templates/business.typ": report-conf

#let payload = json.decode(sys.inputs.at("payload", default: "{}"))

#show: report-conf.with(
  title: payload.at("title", default: "业务报告"),
  author: "System",
)

= 概览
#payload.at("summary", default: "无数据")

= 详细数据
#table(
  columns: (1fr, auto, auto),
  [*指标*], [*数值*], [*环比*],
  ..payload.at("metrics", default: ()).map(m => (
    m.name, str(m.value), m.change
  )).flatten()
)
```

### KPI 卡片网格

```typst
#let kpi-cards(metrics) = {
  let cells = metrics.map(m => {
    rect(width: 100%, fill: luma(240), inset: 10pt)[
      #text(size: 10pt, fill: gray)[#m.label] \
      #text(size: 18pt, weight: "bold")[#m.value]
    ]
  })
  grid(columns: (1fr, 1fr, 1fr), gutter: 10pt, ..cells)
}
```

## 错误处理

### 字体缺失
如果中文显示为方块，需要安装中文字体：
```bash
# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk

# 或在模板中指定字体
#set text(font: ("Noto Sans SC", "SimSun"))
```

### JSON 解析失败
使用防御性编程：
```typst
#let data = json.decode(raw-payload)
#let title = data.at("title", default: "默认标题")
```

### 编译超时
对于大数据量图表，考虑预处理为 SVG：
```python
# 用 matplotlib 生成 SVG
import matplotlib.pyplot as plt
plt.savefig("chart.svg")
```

然后在 Typst 中引用：
```typst
#image("chart.svg")
```

## 项目结构

```
typst-templates/
├── assets/
│   ├── fonts/           # 中文字体
│   └── images/          # Logo 等
├── lib/
│   ├── theme.typ        # 样式定义
│   ├── charts.typ       # 图表组件
│   └── utils.typ        # 工具函数
├── templates/
│   └── business.typ     # 报告模板
└── main.typ             # 入口文件
```

## 使用示例

在 Issue 中评论：
```
/oc 根据这个 issue 生成需求分析报告 PDF
```

OpenCode 会：
1. 分析 issue 内容
2. 生成 `.typ` 文件
3. 编译为 PDF
4. 上传为 artifact

## 参考资源

- [Typst 官方文档](https://typst.app/docs/)
- [CeTZ 图表库](https://typst.app/universe/package/cetz-plot/)
- [Typst Universe 包管理](https://typst.app/universe/)
