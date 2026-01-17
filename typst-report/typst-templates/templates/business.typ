// business.typ - 商业报告模板

#import "../lib/theme.typ": *
#import "../lib/utils.typ": *

// ============================================
// 报告配置函数
// ============================================

/// 商业报告配置
/// 
/// 参数：
/// - title: 报告标题
/// - subtitle: 副标题（可选）
/// - author: 作者
/// - date: 日期（默认今天）
/// - logo: Logo 路径（可选）
/// - body: 报告内容
#let report-conf(
  title: "",
  subtitle: none,
  author: "System",
  date: datetime.today(),
  logo: none,
  body
) = {
  // 文档元数据
  set document(title: title, author: author)
  
  // 设置中文字体支持
  set text(
    font: ("Linux Libertine", "Noto Sans CJK SC", "Microsoft YaHei", "SimSun"),
    lang: "zh",
  )
  
  // 应用全局样式
  setup-page()
  setup-text()
  setup-heading()
  setup-paragraph()
  setup-list()
  setup-code()
  
  // ============================================
  // 封面页
  // ============================================
  
  page(
    margin: 0cm,
    header: none,
    footer: none,
  )[
    #place(
      top + center,
      dy: 30%,
    )[
      // Logo
      #if logo != none [
        #image(logo, width: 4cm)
        #v(spacing-xl)
      ]
      
      // 标题
      #text(
        size: 28pt,
        weight: "bold",
        fill: brand-primary,
        font: font-stack-heading,
      )[#title]
      
      // 副标题
      #if subtitle != none [
        #v(spacing-sm)
        #text(
          size: 16pt,
          fill: brand-gray-600,
          font: font-stack-heading,
        )[#subtitle]
      ]
      
      #v(spacing-xl)
      
      // 作者和日期
      #text(size: 14pt, fill: brand-gray-700)[
        #author
      ]
      
      #v(spacing-xs)
      
      #text(size: 12pt, fill: brand-gray-600)[
        #format-date(date)
      ]
    ]
  ]
  
  // ============================================
  // 目录页
  // ============================================
  
  page[
    #outline(
      title: [
        #text(size: 18pt, weight: "bold", fill: brand-primary)[目录]
        #v(spacing-md)
      ],
      indent: auto,
      depth: 3,
    )
  ]
  
  // ============================================
  // 正文内容
  // ============================================
  
  body
}

// ============================================
// KPI 卡片组件
// ============================================

/// KPI 卡片网格
/// 
/// 参数：
/// - metrics: 指标数组 [{label, value, change}, ...]
/// - columns: 列数（默认 3）
#let kpi-cards(metrics, columns: 3) = {
  if metrics == none or metrics.len() == 0 {
    return [暂无数据]
  }
  
  let cells = metrics.map(m => {
    let label = safe-get(m, "label", default: "未命名")
    let value = safe-get(m, "value", default: "N/A")
    let change = safe-get(m, "change", default: none)
    
    rect(
      width: 100%,
      fill: brand-gray-100,
      stroke: 1pt + brand-gray-300,
      radius: 4pt,
      inset: spacing-md,
    )[
      // 标签
      #text(
        size: 10pt,
        fill: brand-gray-600,
        weight: "medium",
      )[#label]
      
      #v(spacing-xs)
      
      // 数值
      #text(
        size: 24pt,
        weight: "bold",
        fill: brand-primary,
      )[#value]
      
      // 变化率
      #if change != none [
        #v(spacing-xs)
        #let change-color = if change >= 0 { brand-success } else { brand-danger }
        #let change-icon = if change >= 0 { "↑" } else { "↓" }
        #text(
          size: 12pt,
          fill: change-color,
          weight: "medium",
        )[#change-icon #format-percent(change)]
      ]
    ]
  })
  
  grid(
    columns: (1fr,) * columns,
    gutter: spacing-md,
    ..cells
  )
}

// ============================================
// 数据表格组件
// ============================================

/// 动态数据表格
/// 
/// 参数：
/// - headers: 表头数组 ["列1", "列2", ...]
/// - data: 数据数组 [[值1, 值2], ...]
/// - formatters: 格式化函数数组（可选）
#let data-table(headers, data, formatters: none) = {
  if data == none or data.len() == 0 {
    return [暂无数据]
  }
  
  let col-count = headers.len()
  
  styled-table(
    columns: (1fr,) * col-count,
    
    // 表头
    ..headers.map(h => [*#h*]),
    
    // 数据行
    ..data.map(row => {
      row.enumerate().map(((i, cell)) => {
        // 应用格式化函数
        if formatters != none and i < formatters.len() and formatters.at(i) != none {
          formatters.at(i)(cell)
        } else {
          str(cell)
        }
      })
    }).flatten()
  )
}

// ============================================
// 分节组件
// ============================================

/// 带标题的内容块
#let section-block(title, content, icon: none) = {
  block(
    width: 100%,
    breakable: false,
  )[
    // 标题栏
    #block(
      width: 100%,
      fill: brand-primary.lighten(90%),
      inset: spacing-sm,
      radius: (top: 4pt),
      stroke: (bottom: 2pt + brand-primary),
    )[
      #text(
        size: 14pt,
        weight: "bold",
        fill: brand-primary,
      )[
        #if icon != none [#icon ]
        #title
      ]
    ]
    
    // 内容区
    #block(
      width: 100%,
      inset: spacing-md,
      stroke: (
        left: 1pt + brand-gray-300,
        right: 1pt + brand-gray-300,
        bottom: 1pt + brand-gray-300,
      ),
      radius: (bottom: 4pt),
    )[
      #content
    ]
  ]
}

// ============================================
// 时间线组件
// ============================================

/// 时间线
/// 
/// 参数：
/// - events: 事件数组 [{date, title, description}, ...]
#let timeline(events) = {
  if events == none or events.len() == 0 {
    return [暂无事件]
  }
  
  for event in events {
    let date = safe-get(event, "date", default: "")
    let title = safe-get(event, "title", default: "未命名事件")
    let description = safe-get(event, "description", default: "")
    
    grid(
      columns: (auto, 1fr),
      gutter: spacing-md,
      
      // 日期标记
      [
        #block(
          fill: brand-primary,
          inset: (x: spacing-sm, y: spacing-xs),
          radius: 4pt,
        )[
          #text(size: 9pt, fill: white, weight: "bold")[#date]
        ]
      ],
      
      // 事件内容
      [
        #text(weight: "bold", size: 11pt)[#title]
        #if description != "" [
          #v(spacing-xs)
          #text(size: 10pt, fill: brand-gray-700)[#description]
        ]
      ]
    )
    
    v(spacing-sm)
  }
}

// ============================================
// 进度条组件
// ============================================

/// 进度条
/// 
/// 参数：
/// - label: 标签
/// - value: 当前值
/// - max: 最大值
/// - color: 颜色（可选）
#let progress-bar(label, value, max, color: brand-primary) = {
  let percent = calc.min(value / max * 100, 100)
  
  block(width: 100%)[
    // 标签和百分比
    #grid(
      columns: (1fr, auto),
      [#text(size: 10pt, weight: "medium")[#label]],
      [#text(size: 10pt, fill: brand-gray-600)[#format-percent(value / max)]]
    )
    
    #v(spacing-xs)
    
    // 进度条
    #box(
      width: 100%,
      height: 8pt,
      fill: brand-gray-200,
      radius: 4pt,
    )[
      #place(
        left,
        box(
          width: percent * 1%,
          height: 8pt,
          fill: color,
          radius: 4pt,
        )
      )
    ]
  ]
}

// ============================================
// 统计卡片组件
// ============================================

/// 统计卡片（带图标）
#let stat-card(label, value, icon: "📊", color: brand-primary) = {
  rect(
    width: 100%,
    fill: color.lighten(95%),
    stroke: 1pt + color.lighten(50%),
    radius: 4pt,
    inset: spacing-md,
  )[
    #grid(
      columns: (auto, 1fr),
      gutter: spacing-md,
      
      // 图标
      [
        #text(size: 32pt)[#icon]
      ],
      
      // 内容
      [
        #text(size: 10pt, fill: brand-gray-600)[#label]
        #v(spacing-xs)
        #text(size: 20pt, weight: "bold", fill: color)[#value]
      ]
    )
  ]
}
