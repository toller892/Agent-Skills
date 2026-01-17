// charts.typ - 图表组件封装（基于 CeTZ）

#import "@preview/cetz:0.3.1"
#import "@preview/cetz-plot:0.1.0": plot
#import "../lib/theme.typ": *

// ============================================
// 数据适配器
// ============================================

/// 将业务数据转换为 CeTZ 绘图格式
/// 输入：[{x, y}, ...] 或 [{label, value}, ...]
/// 输出：((x1, y1), (x2, y2), ...)
#let adapt-chart-data(data, x-key: "x", y-key: "y") = {
  if data == none or data.len() == 0 {
    return ()
  }
  
  data.map(item => {
    let x-val = if type(item) == dictionary {
      item.at(x-key, default: 0)
    } else {
      item.at(0)
    }
    
    let y-val = if type(item) == dictionary {
      item.at(y-key, default: 0)
    } else {
      item.at(1)
    }
    
    (x-val, y-val)
  })
}

// ============================================
// 折线图
// ============================================

/// 折线图
/// 
/// 参数：
/// - data: 数据数组 [{x, y}, ...]
/// - title: 图表标题
/// - x-label: X 轴标签
/// - y-label: Y 轴标签
/// - color: 线条颜色
/// - width: 图表宽度
/// - height: 图表高度
#let line-chart(
  data,
  title: none,
  x-label: "X",
  y-label: "Y",
  color: brand-primary,
  width: 12,
  height: 6,
) = {
  if data == none or data.len() == 0 {
    return [暂无数据]
  }
  
  let plot-data = adapt-chart-data(data)
  
  figure(
    cetz.canvas({
      import cetz.draw: *
      
      plot.plot(
        size: (width, height),
        x-label: x-label,
        y-label: y-label,
        x-tick-step: none,
        y-tick-step: none,
        {
          plot.add(
            plot-data,
            style: (stroke: 2pt + color),
            mark: "o",
            mark-style: (fill: color, stroke: none),
          )
        }
      )
    }),
    caption: if title != none { title },
  )
}

// ============================================
// 柱状图
// ============================================

/// 柱状图
/// 
/// 参数：
/// - data: 数据数组 [{label, value}, ...]
/// - title: 图表标题
/// - color: 柱子颜色
/// - width: 图表宽度
/// - height: 图表高度
#let bar-chart(
  data,
  title: none,
  color: brand-primary,
  width: 12,
  height: 6,
) = {
  if data == none or data.len() == 0 {
    return [暂无数据]
  }
  
  // 提取标签和数值
  let labels = data.map(item => item.at("label", default: ""))
  let values = data.map(item => {
    let val = item.at("value", default: 0)
    if type(val) == str { float(val) } else { val }
  })
  
  figure(
    cetz.canvas({
      import cetz.draw: *
      
      plot.plot(
        size: (width, height),
        x-tick-step: none,
        y-tick-step: none,
        {
          plot.add-bar(
            values.enumerate().map(((i, v)) => (i, v)),
            style: (fill: color),
          )
        }
      )
    }),
    caption: if title != none { title },
  )
}

// ============================================
// 简化版图表（不依赖 CeTZ）
// ============================================

/// 简单柱状图（纯 Typst 实现）
/// 适用于数据量小的场景
#let simple-bar-chart(data, max-height: 4cm, color: brand-primary) = {
  if data == none or data.len() == 0 {
    return [暂无数据]
  }
  
  let max-value = calc.max(..data.map(item => {
    let val = item.at("value", default: 0)
    if type(val) == str { float(val) } else { val }
  }))
  
  grid(
    columns: data.map(_ => 1fr),
    gutter: spacing-sm,
    
    ..data.map(item => {
      let label = item.at("label", default: "")
      let value = item.at("value", default: 0)
      let val-num = if type(value) == str { float(value) } else { value }
      let bar-height = (val-num / max-value) * max-height
      
      align(bottom + center)[
        // 柱子
        #box(
          width: 100%,
          height: bar-height,
          fill: color,
          radius: (top: 4pt),
        )
        
        #v(spacing-xs)
        
        // 数值
        #text(size: 10pt, weight: "bold")[#value]
        
        #v(spacing-xs)
        
        // 标签
        #text(size: 9pt, fill: brand-gray-600)[#label]
      ]
    })
  )
}

// ============================================
// 饼图（简化版）
// ============================================

/// 简单饼图（使用表格模拟）
/// 适用于数据量小的场景
#let simple-pie-chart(data, colors: (brand-primary, brand-secondary, brand-success, brand-warning, brand-info)) = {
  if data == none or data.len() == 0 {
    return [暂无数据]
  }
  
  let total = data.map(item => {
    let val = item.at("value", default: 0)
    if type(val) == str { float(val) } else { val }
  }).sum()
  
  // 图例
  grid(
    columns: (auto, 1fr, auto),
    gutter: spacing-sm,
    
    ..data.enumerate().map(((i, item)) => {
      let label = item.at("label", default: "")
      let value = item.at("value", default: 0)
      let val-num = if type(value) == str { float(value) } else { value }
      let percent = val-num / total
      let color = colors.at(calc.rem(i, colors.len()))
      
      (
        // 颜色块
        box(
          width: 1cm,
          height: 0.5cm,
          fill: color,
          radius: 2pt,
        ),
        
        // 标签
        text(size: 10pt)[#label],
        
        // 百分比
        text(size: 10pt, fill: brand-gray-600)[#format-percent(percent)]
      )
    }).flatten()
  )
}

// ============================================
// 趋势指示器
// ============================================

/// 趋势箭头
#let trend-indicator(value, threshold: 0) = {
  if value > threshold {
    text(fill: brand-success, size: 14pt)[↑]
  } else if value < threshold {
    text(fill: brand-danger, size: 14pt)[↓]
  } else {
    text(fill: brand-gray-500, size: 14pt)[→]
  }
}

// ============================================
// 迷你图表（Sparkline）
// ============================================

/// 迷你折线图
/// 适用于嵌入表格或卡片中
#let sparkline(data, width: 3cm, height: 1cm, color: brand-primary) = {
  if data == none or data.len() == 0 {
    return box(width: width, height: height)
  }
  
  let values = data.map(v => if type(v) == str { float(v) } else { v })
  let min-val = calc.min(..values)
  let max-val = calc.max(..values)
  let range = max-val - min-val
  
  if range == 0 {
    return box(width: width, height: height)[
      #place(center + horizon)[
        #line(length: width, stroke: 1pt + color)
      ]
    ]
  }
  
  box(width: width, height: height)[
    #place(left + bottom)[
      #for (i, val) in values.enumerate() {
        let x = (i / (values.len() - 1)) * width
        let y = ((val - min-val) / range) * height
        place(dx: x, dy: -y)[
          #circle(radius: 1pt, fill: color)
        ]
      }
    ]
  ]
}
