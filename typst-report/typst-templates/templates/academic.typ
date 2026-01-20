// academic.typ - 学术论文模板（符合标准格式）

#import "../lib/theme.typ": *
#import "../lib/utils.typ": *

// ============================================
// 学术论文配置函数
// ============================================

/// 学术论文配置
/// 
/// 参数：
/// - title: 论文标题
/// - author: 作者
/// - date: 日期（默认今天）
/// - abstract: 摘要（可选）
/// - keywords: 关键词数组（可选）
/// - body: 论文内容
#let academic-conf(
  title: "",
  author: "作者",
  date: datetime.today(),
  abstract: none,
  keywords: (),
  body
) = {
  // 文档元数据
  set document(title: title, author: author)
  
  // ============================================
  // 页面设置（符合标准格式）
  // ============================================
  
  set page(
    paper: "a4",
    margin: (x: 2cm, y: 2.5cm),
    numbering: "1 / 1",  // 当前页 / 总页数
    
    // 页眉
    header: context {
      align(right)[
        #text(size: 9pt, fill: brand-gray-600)[
          #title
        ]
      ]
      line(length: 100%, stroke: 0.5pt + brand-gray-300)
    },
    
    // 页脚
    footer: context {
      line(length: 100%, stroke: 0.5pt + brand-gray-300)
      v(spacing-xs)
      align(center)[
        #text(size: 9pt, fill: brand-gray-600)[
          #counter(page).display("1 / 1", both: true)
        ]
      ]
    },
  )
  
  // ============================================
  // 文本设置（使用衬线字体）
  // ============================================
  
  set text(
    font: ("Linux Libertine", "Noto Serif CJK SC", "SimSun"),
    size: 11pt,
    lang: "zh",
  )
  
  // ============================================
  // 标题设置
  // ============================================
  
  set heading(numbering: "1.1")
  
  show heading.where(level: 1): it => {
    v(spacing-md)
    text(
      size: 16pt,
      weight: "bold",
      font: ("Linux Libertine", "Noto Serif CJK SC"),
    )[#it]
    v(spacing-sm)
  }
  
  show heading.where(level: 2): it => {
    v(spacing-sm)
    text(
      size: 13pt,
      weight: "bold",
      font: ("Linux Libertine", "Noto Serif CJK SC"),
    )[#it]
    v(spacing-xs)
  }
  
  // ============================================
  // 段落设置（学术风格：无首行缩进）
  // ============================================
  
  set par(
    justify: true,
    leading: 0.65em,
    first-line-indent: 0em,  // 学术论文通常不缩进
  )
  
  // ============================================
  // 列表设置
  // ============================================
  
  set list(
    marker: [•],
    indent: 1em,
  )
  
  set enum(
    numbering: "1.",
    indent: 1em,
  )
  
  // ============================================
  // 代码块设置
  // ============================================
  
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
  
  // ============================================
  // 封面（简洁版）
  // ============================================
  
  align(center)[
    #text(1.5em, weight: "bold")[#title]
    #v(0.5em)
    作者：#author \
    日期：#format-date(date)
  ]
  
  #line(length: 100%)
  
  // ============================================
  // 摘要（如果有）
  // ============================================
  
  #if abstract != none [
    #v(spacing-md)
    
    #align(center)[
      #text(weight: "bold")[摘要]
    ]
    
    #v(spacing-xs)
    
    #block(
      width: 100%,
      inset: (x: 2em),
    )[
      #abstract
    ]
    
    #if keywords.len() > 0 [
      #v(spacing-xs)
      #text(weight: "bold")[关键词：] #keywords.join("；")
    ]
    
    #v(spacing-md)
    #line(length: 100%)
  ]
  
  // ============================================
  // 正文内容
  // ============================================
  
  #v(spacing-md)
  
  body
}

// ============================================
// 学术表格样式
// ============================================

/// 三线表（学术论文常用）
#let three-line-table(..args) = {
  table(
    stroke: (x, y) => {
      if y == 0 {
        (top: 1.5pt + black, bottom: 1pt + black)
      } else if y == 1 {
        none
      } else {
        (bottom: 0.5pt + brand-gray-400)
      }
    },
    inset: (x: spacing-sm, y: spacing-xs),
    ..args
  )
}

// ============================================
// 图表标题
// ============================================

/// 图表标题（带编号）
#let figure-caption(content, kind: "图") = {
  context {
    let num = counter(figure.where(kind: kind)).display()
    [#kind #num：#content]
  }
}
