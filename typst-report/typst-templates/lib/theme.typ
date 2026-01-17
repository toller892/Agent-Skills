// theme.typ - 全局样式与企业识别系统

// ============================================
// 字体定义
// ============================================

// 中西文混排字体栈
#let font-stack-body = ("Noto Sans", "Noto Sans CJK SC", "Microsoft YaHei", "SimSun", "Arial")
#let font-stack-heading = ("Noto Sans", "Noto Sans CJK SC", "Microsoft YaHei", "SimSun", "Arial")
#let font-stack-mono = ("Noto Sans Mono", "Courier New", "Consolas", "monospace")

// ============================================
// 颜色系统
// ============================================

// 品牌主色
#let brand-primary = rgb("#0056b3")
#let brand-secondary = rgb("#6c757d")
#let brand-success = rgb("#28a745")
#let brand-warning = rgb("#ffc107")
#let brand-danger = rgb("#dc3545")
#let brand-info = rgb("#17a2b8")

// 灰度色阶
#let brand-gray-100 = rgb("#f8f9fa")
#let brand-gray-200 = rgb("#e9ecef")
#let brand-gray-300 = rgb("#dee2e6")
#let brand-gray-400 = rgb("#ced4da")
#let brand-gray-500 = rgb("#adb5bd")
#let brand-gray-600 = rgb("#6c757d")
#let brand-gray-700 = rgb("#495057")
#let brand-gray-800 = rgb("#343a40")
#let brand-gray-900 = rgb("#212529")

// 语义化颜色
#let color-text = brand-gray-900
#let color-text-muted = brand-gray-600
#let color-border = brand-gray-300
#let color-background = white

// ============================================
// 间距系统
// ============================================

#let spacing-xs = 0.25cm
#let spacing-sm = 0.5cm
#let spacing-md = 1cm
#let spacing-lg = 1.5cm
#let spacing-xl = 2cm

// ============================================
// 页面配置函数
// ============================================

/// 标准页面配置
#let setup-page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  header-content: none,
  footer-content: none,
) = {
  set page(
    paper: paper,
    margin: margin,
    
    // 页眉
    header: if header-content != none {
      header-content
    } else {
      context {
        align(right)[
          #text(size: 9pt, fill: brand-gray-600)[
            #datetime.today().display("[year]年[month]月[day]日")
          ]
        ]
        line(length: 100%, stroke: 0.5pt + brand-gray-300)
      }
    },
    
    // 页脚
    footer: if footer-content != none {
      footer-content
    } else {
      context {
        line(length: 100%, stroke: 0.5pt + brand-gray-300)
        v(spacing-xs)
        align(center)[
          #text(size: 9pt, fill: brand-gray-600)[
            第 #counter(page).display() 页
          ]
        ]
      }
    },
  )
}

// ============================================
// 文本样式
// ============================================

/// 标准文本配置
#let setup-text() = {
  set text(
    font: font-stack-body,
    size: 10.5pt,
    fill: color-text,
  )
}

/// 标题样式配置
#let setup-heading() = {
  set heading(numbering: "1.1")
  
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(spacing-lg)
    text(
      size: 18pt,
      weight: "bold",
      fill: brand-primary,
      font: font-stack-heading,
    )[#it]
    v(spacing-md)
  }
  
  show heading.where(level: 2): it => {
    v(spacing-md)
    text(
      size: 14pt,
      weight: "bold",
      fill: brand-gray-800,
      font: font-stack-heading,
    )[#it]
    v(spacing-sm)
  }
  
  show heading.where(level: 3): it => {
    v(spacing-sm)
    text(
      size: 12pt,
      weight: "bold",
      fill: brand-gray-700,
      font: font-stack-heading,
    )[#it]
    v(spacing-xs)
  }
}

// ============================================
// 段落样式
// ============================================

/// 段落配置
#let setup-paragraph() = {
  set par(
    justify: true,
    leading: 0.65em,
    first-line-indent: 2em,
  )
  
  // 标题后段落不缩进
  show heading: it => {
    it
    par(first-line-indent: 0em)[#v(0pt, weak: true)]
  }
}

// ============================================
// 列表样式
// ============================================

/// 列表配置
#let setup-list() = {
  set list(
    marker: [•],
    indent: 1em,
  )
  
  set enum(
    numbering: "1.",
    indent: 1em,
  )
}

// ============================================
// 代码块样式
// ============================================

/// 代码块配置
#let setup-code() = {
  show raw.where(block: true): it => {
    block(
      width: 100%,
      fill: brand-gray-100,
      inset: spacing-sm,
      radius: 4pt,
      stroke: 1pt + brand-gray-300,
    )[
      #set text(font: font-stack-mono, size: 9pt)
      #it
    ]
  }
  
  show raw.where(block: false): it => {
    box(
      fill: brand-gray-100,
      inset: (x: 4pt, y: 2pt),
      radius: 2pt,
    )[
      #set text(font: font-stack-mono, size: 9pt)
      #it
    ]
  }
}

// ============================================
// 表格样式
// ============================================

/// 标准表格样式
#let styled-table(..args) = {
  table(
    stroke: (x, y) => {
      if y == 0 {
        (bottom: 2pt + brand-primary)
      } else {
        (bottom: 0.5pt + brand-gray-300)
      }
    },
    fill: (x, y) => {
      if y == 0 {
        brand-gray-100
      } else if calc.rem(y, 2) == 0 {
        brand-gray-100.lighten(50%)
      }
    },
    inset: spacing-sm,
    ..args
  )
}

// ============================================
// 引用块样式
// ============================================

/// 引用块
#let quote-block(content, author: none) = {
  block(
    width: 100%,
    fill: brand-gray-100,
    inset: spacing-md,
    radius: 4pt,
    stroke: (left: 4pt + brand-primary),
  )[
    #set text(style: "italic", fill: brand-gray-700)
    #content
    
    #if author != none [
      #v(spacing-xs)
      #align(right)[
        #text(size: 9pt, weight: "bold")[— #author]
      ]
    ]
  ]
}

// ============================================
// 警告框样式
// ============================================

/// 信息框
#let info-box(content, title: "提示") = {
  block(
    width: 100%,
    fill: brand-info.lighten(90%),
    inset: spacing-sm,
    radius: 4pt,
    stroke: 1pt + brand-info,
  )[
    #text(weight: "bold", fill: brand-info)[#title]
    #v(spacing-xs)
    #content
  ]
}

/// 警告框
#let warning-box(content, title: "警告") = {
  block(
    width: 100%,
    fill: brand-warning.lighten(90%),
    inset: spacing-sm,
    radius: 4pt,
    stroke: 1pt + brand-warning,
  )[
    #text(weight: "bold", fill: brand-warning.darken(30%))[#title]
    #v(spacing-xs)
    #content
  ]
}

/// 错误框
#let error-box(content, title: "错误") = {
  block(
    width: 100%,
    fill: brand-danger.lighten(90%),
    inset: spacing-sm,
    radius: 4pt,
    stroke: 1pt + brand-danger,
  )[
    #text(weight: "bold", fill: brand-danger)[#title]
    #v(spacing-xs)
    #content
  ]
}
