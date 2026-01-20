// 自动生成的报告 - 独立版本
// 生成时间: 2026-01-20 07:32:34
// 可直接在 Typst 在线编辑器中使用

#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  numbering: "1",
  header: context {
    align(right)[
      #text(size: 9pt, fill: gray)[Agent-Skills 项目分析报告]
    ]
    line(length: 100%, stroke: 0.5pt + gray)
  },
  footer: context {
    line(length: 100%, stroke: 0.5pt + gray)
    v(0.25cm)
    align(center)[
      #text(size: 9pt, fill: gray)[第 #counter(page).display() 页]
    ]
  },
)

#set text(
  font: ("Noto Sans", "Noto Sans CJK SC"),
  size: 10.5pt,
  lang: "zh",
)

#set heading(numbering: "1.1")

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(1cm)
  text(size: 18pt, weight: "bold", fill: rgb("#0056b3"))[#it]
  v(0.5cm)
}

#show heading.where(level: 2): it => {
  v(0.5cm)
  text(size: 14pt, weight: "bold", fill: rgb("#343a40"))[#it]
  v(0.25cm)
}

#set par(justify: true, leading: 0.65em, first-line-indent: 2em)
#show heading: it => { it; par(first-line-indent: 0em)[] }

#set list(marker: [•], indent: 1em)
#set enum(numbering: "1.", indent: 1em)

#let styled-table(..args) = {
  table(
    stroke: (x, y) => {
      if y == 0 { (bottom: 2pt + rgb("#0056b3")) }
      else { (bottom: 0.5pt + gray) }
    },
    fill: (x, y) => {
      if y == 0 { rgb("#f8f9fa") }
      else if calc.rem(y, 2) == 0 { rgb("#f8f9fa").lighten(50%) }
    },
    inset: 0.5cm,
    ..args
  )
}

#let kpi-card(label, value, change) = {
  rect(
    width: 100%, fill: rgb("#f8f9fa"), stroke: 1pt + rgb("#dee2e6"),
    radius: 4pt, inset: 1cm,
  )[
    #text(size: 10pt, fill: rgb("#6c757d"), weight: "medium")[#label]
    #v(0.25cm)
    #text(size: 24pt, weight: "bold", fill: rgb("#0056b3"))[#value]
    #if change != none [
      #v(0.25cm)
      #let change-color = if change >= 0 { rgb("#28a745") } else { rgb("#dc3545") }
      #let change-icon = if change >= 0 { "↑" } else { "↓" }
      #let change-percent = calc.round(change * 100, digits: 0)
      #text(size: 12pt, fill: change-color, weight: "medium")[#change-icon #change-percent%]
    ]
  ]
}

#page(margin: 0cm, header: none, footer: none)[
  #place(top + center, dy: 30%)[
    #text(size: 28pt, weight: "bold", fill: rgb("#0056b3"))[Agent-Skills 项目分析报告]

    #v(0.5cm)
    
    #text(
      size: 16pt,
      fill: rgb("#6c757d"),
    )[OpenCode Agent Skills 集合项目]
    #v(2cm)
    #text(size: 14pt, fill: rgb("#495057"))[OpenCode Agent]
    #v(0.25cm)
    #text(size: 12pt, fill: rgb("#6c757d"))[
      #datetime.today().display("[year]年[month]月[day]日")
    ]
  ]
]

#page[
  #outline(
    title: [
      #text(size: 18pt, weight: "bold", fill: rgb("#0056b3"))[目录]
      #v(1cm)
    ],
    indent: auto,
    depth: 3,
  )
]

= 概览

Agent-Skills 是一个 OpenCode Agent Skills 集合项目，包含可复用的 AI 能力模块。本项目目前包含两个核心 skill：Typst 报告生成和论文解析器，旨在为 AI 助手提供专业的文档生成和学术论文解析能力。

== 关键指标

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 1cm,
  
  kpi-card("核心 Skills", "2", 0.0),
  kpi-card("代码文件", "15", 0.0),
  kpi-card("文档文件", "12", 0.0),
)

== 项目概述

Agent-Skills 项目是一个 OpenCode Agent Skills 集合，旨在提供可复用的 AI 能力模块。项目遵循标准的 skill 开发规范，每个 skill 包含完整的文档、脚本和模板。

**项目结构：**
- typst-report: Typst 报告生成 skill
- paper-interpreter: 论文解析器 skill
- 文档: README.md, opencode.json 等配置文件

== Typst 报告生成 Skill

Typst 报告生成 skill 是一个专业的 PDF 报告生成工具，使用 Typst 排版系统。它支持从 JSON/CSV 数据生成报告，包含图表、表格、封面、目录等功能。

**核心特性：**
- 完整工作流：JSON → .typ → PDF
- 双重输出：生成 .typ 源文件和 PDF 文档
- 中文排版支持
- 数据驱动：从 JSON/CSV 数据生成报告
- 图表组件：折线图、柱状图、KPI 卡片
- 自动化：封面、目录、页码自动生成

== Typst Skill 文件结构

#styled-table(
  columns: (1fr, 1fr, 1fr),
  [*目录*], [*文件*], [*描述*],
  [typst-report/], [SKILL.md], [Skill 定义文件],
  [typst-report/], [README.md], [使用说明文档],
  [typst-report/scripts/], [compile.py], [Python 编译脚本],
  [typst-report/scripts/], [generate.py], [生成脚本],
  [typst-report/typst-templates/], [main.typ], [报告入口文件],
  [typst-report/typst-templates/], [standard-example.typ], [标准格式示例],
  [typst-report/typst-templates/], [academic-example.typ], [学术论文示例],
  [typst-report/typst-templates/lib/], [utils.typ], [数据处理工具],
  [typst-report/typst-templates/lib/], [theme.typ], [全局样式],
  [typst-report/typst-templates/lib/], [charts.typ], [图表组件],
)

== 论文解析器 Skill

论文解析器 skill 采用五阶段工作流，将论文链接转换为图文并茂的 PDF 和 HTML 文档，采用黄叔风格写作 + 纽约客插画 + 2026 前沿设计。

**五阶段工作流：**
1. 信息获取：抓取 arXiv 摘要页，搜索补充技术细节
2. 文章生成：黄叔风格量化标准，输出 Markdown 文件
3. 配图生成：使用 Nano Banana API 生成纽约客风格插画
4. HTML 生成：2026 前沿设计规范
5. PDF 生成：调用 generate_pdf.py 脚本生成原生 PDF

== 论文解析器文件结构

#styled-table(
  columns: (1fr, 1fr, 1fr),
  [*目录*], [*文件*], [*描述*],
  [paper-interpreter/], [SKILL.md], [Skill 定义文件],
  [paper-interpreter/], [README.md], [使用说明文档],
  [paper-interpreter/scripts/], [paper_interpreter.py], [主解析脚本],
  [paper-interpreter/scripts/], [diagnose.py], [诊断脚本],
  [paper-interpreter/scripts/], [example_usage.py], [使用示例],
  [paper-interpreter/references/], [README.md], [详细文档],
  [paper-interpreter/references/], [WORKFLOW.md], [工作流说明],
  [paper-interpreter/references/], [QUICKSTART.md], [快速开始指南],
)

== 技术架构

**Typst 报告生成技术栈：**
- Typst 排版系统：现代化的标记型排版系统
- Python 脚本：数据预处理和编译自动化
- JSON/CSV 数据格式：结构化数据输入
- CeTZ 图表库：矢量图表渲染

**论文解析器技术栈：**
- PyMuPDF (fitz)：PDF 解析和内容提取
- requests：HTTP 请求和文件下载
- fpdf2：PDF 生成库
- Nano Banana API：AI 图像生成

== 使用场景

- 自动化业务报告生成
- 学术论文解析和摘要
- CI/CD 集成文档生成
- 批量客户报告生成
- 技术文档自动化排版

== 项目状态

== 未来规划

- 增加更多 skill 模块
- 优化 Typst 模板样式
- 增强论文解析的准确性
- 添加更多数据源支持
- 优化编译性能

