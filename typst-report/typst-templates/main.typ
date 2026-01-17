// main.typ - 报告生成入口文件

#import "templates/business.typ": *
#import "lib/utils.typ": *
#import "lib/charts.typ": *

// ============================================
// 数据加载
// ============================================

// 从 CLI 输入解析 JSON 数据
#let payload = parse-payload()

// 提取报告元数据
#let report-title = safe-get(payload, "title", default: "自动化报告")
#let report-subtitle = safe-get(payload, "subtitle", default: none)
#let report-author = safe-get(payload, "author", default: "System")
#let report-date = datetime.today()

// ============================================
// 应用报告模板
// ============================================

#show: report-conf.with(
  title: report-title,
  subtitle: report-subtitle,
  author: report-author,
  date: report-date,
  // logo: "assets/images/logo.svg",  // 如果有 Logo
)

// ============================================
// 报告内容
// ============================================

= 概览

#let summary = safe-get(payload, "summary", default: "暂无概览信息")
#summary

// KPI 指标卡片
#let metrics = safe-get(payload, "metrics", default: ())
#if metrics.len() > 0 [
  == 关键指标
  
  #kpi-cards(metrics, columns: 3)
]

// ============================================
// 详细数据
// ============================================

#let sections = safe-get(payload, "sections", default: ())
#for section in sections [
  #let heading-text = safe-get(section, "heading", default: "未命名章节")
  #let level = safe-get(section, "level", default: 2)
  #let content-text = safe-get(section, "content", default: "")
  #let section-type = safe-get(section, "type", default: "text")
  
  // 根据 level 生成标题
  #if level == 1 [
    = #heading-text
  ] else if level == 2 [
    == #heading-text
  ] else [
    === #heading-text
  ]
  
  // 根据类型渲染内容
  #if section-type == "text" [
    // 使用 process-markdown 处理文本
    #process-markdown(content-text)
  ] else if section-type == "list" [
    #let items = safe-get(section, "items", default: ())
    #for item in items [
      - #item
    ]
  ] else if section-type == "checklist" [
    #let items = safe-get(section, "items", default: ())
    #for item in items [
      - [ ] #item
    ]
  ] else if section-type == "table" [
    // 兼容两种数据结构
    #let headers = safe-get(section, "headers", default: ())
    #let data = safe-get(section, "data", default: ())
    
    // 如果 headers 为空，尝试从 content 中获取
    #if headers.len() == 0 [
      #let content-obj = safe-get(section, "content", default: ())
      #headers = safe-get(content-obj, "headers", default: ())
      #let rows = safe-get(content-obj, "rows", default: ())
      #data = rows
    ]
    
    #if headers.len() > 0 and data.len() > 0 [
      #data-table(headers, data)
    ]
  ] else if section-type == "chart" [
    #let chart-data = safe-get(section, "data", default: ())
    #let chart-type = safe-get(section, "chart_type", default: "bar")
    
    #if chart-type == "line" [
      #line-chart(
        chart-data,
        title: heading-text,
        x-label: safe-get(section, "x_label", default: "X"),
        y-label: safe-get(section, "y_label", default: "Y"),
      )
    ] else if chart-type == "bar" [
      #simple-bar-chart(chart-data)
    ]
  ]
]

// ============================================
// 代码块渲染
// ============================================

#let code-blocks = safe-get(payload, "code_blocks", default: ())
#if code-blocks.len() > 0 [
  = 代码示例
  
  #for block in code-blocks [
    #let language = safe-get(block, "language", default: "text")
    #let code = safe-get(block, "code", default: "")
    
    ```#language
    #code
    ```
  ]
]

// ============================================
// 附录（可选）
// ============================================

#let appendix = safe-get(payload, "appendix", default: none)
#if appendix != none [
  #pagebreak()
  
  = 附录
  
  #appendix
]
