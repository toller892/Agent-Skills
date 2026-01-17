// utils.typ - 数据处理工具函数

// ============================================
// 数据解析
// ============================================

/// 安全解析 JSON payload
/// 从 sys.inputs 获取数据，带默认值处理
#let parse-payload() = {
  let raw-payload = sys.inputs.at("payload", default: "{}")
  json.decode(raw-payload)
}

/// 安全获取字典值，带默认值
#let safe-get(dict, key, default: none) = {
  dict.at(key, default: default)
}

// ============================================
// 数字格式化
// ============================================

/// 格式化货币（人民币）
/// 示例：format-money(1234567.89) => "¥1,234,567.89"
#let format-money(value, currency: "¥") = {
  if value == none { return "N/A" }
  
  let num = if type(value) == str {
    float(value)
  } else {
    value
  }
  
  // 分离整数和小数部分
  let int-part = calc.floor(num)
  let dec-part = calc.rem(num * 100, 100)
  
  // 整数部分添加千分位
  let int-str = str(int-part)
  let result = ""
  let count = 0
  
  for char in int-str.rev() {
    if count > 0 and calc.rem(count, 3) == 0 {
      result = "," + result
    }
    result = char + result
    count += 1
  }
  
  // 组合结果
  if dec-part > 0 {
    currency + result + "." + str(calc.round(dec-part)).pad(2, with: "0")
  } else {
    currency + result
  }
}

/// 格式化百分比
/// 示例：format-percent(0.1234) => "12.34%"
#let format-percent(value, decimals: 2) = {
  if value == none { return "N/A" }
  
  let num = if type(value) == str {
    float(value)
  } else {
    value
  }
  
  let percent = num * 100
  let rounded = calc.round(percent, digits: decimals)
  str(rounded) + "%"
}

/// 格式化大数字（K/M/B）
/// 示例：format-large-number(1234567) => "1.23M"
#let format-large-number(value, decimals: 2) = {
  if value == none { return "N/A" }
  
  let num = if type(value) == str {
    float(value)
  } else {
    value
  }
  
  if num >= 1000000000 {
    str(calc.round(num / 1000000000, digits: decimals)) + "B"
  } else if num >= 1000000 {
    str(calc.round(num / 1000000, digits: decimals)) + "M"
  } else if num >= 1000 {
    str(calc.round(num / 1000, digits: decimals)) + "K"
  } else {
    str(num)
  }
}

// ============================================
// 日期格式化
// ============================================

/// 格式化日期（中文）
/// 示例：format-date(datetime.today()) => "2026年1月17日"
#let format-date(date, format: "zh") = {
  if date == none { return "N/A" }
  
  if format == "zh" {
    str(date.year()) + "年" + str(date.month()) + "月" + str(date.day()) + "日"
  } else if format == "iso" {
    date.display("[year]-[month]-[day]")
  } else {
    date.display()
  }
}

/// 格式化日期时间（中文）
/// 示例：format-datetime(datetime.today()) => "2026年1月17日 14:30"
#let format-datetime(date, format: "zh") = {
  if date == none { return "N/A" }
  
  if format == "zh" {
    format-date(date, format: "zh") + " " + str(date.hour()).pad(2, with: "0") + ":" + str(date.minute()).pad(2, with: "0")
  } else {
    date.display("[year]-[month]-[day] [hour]:[minute]")
  }
}

// ============================================
// 数组处理
// ============================================

/// 过滤空值
/// 示例：safe-filter((1, none, 2, none, 3)) => (1, 2, 3)
#let safe-filter(arr) = {
  if arr == none { return () }
  arr.filter(it => it != none)
}

/// 安全获取数组元素
#let safe-at(arr, index, default: none) = {
  if arr == none or index >= arr.len() {
    default
  } else {
    arr.at(index)
  }
}

// ============================================
// CSV 处理
// ============================================

/// CSV 数据类型转换
/// 将 CSV 字符串数组转换为数值
#let csv-to-typed(data, columns: ()) = {
  if data == none or data.len() == 0 { return () }
  
  // 跳过表头
  let rows = data.slice(1)
  
  rows.map(row => {
    row.enumerate().map(((i, cell)) => {
      // 如果指定了列类型
      if i < columns.len() {
        let col-type = columns.at(i)
        if col-type == "int" {
          int(cell)
        } else if col-type == "float" {
          float(cell)
        } else {
          cell
        }
      } else {
        // 尝试自动转换
        if cell.match(regex("^-?\d+$")) != none {
          int(cell)
        } else if cell.match(regex("^-?\d+\.\d+$")) != none {
          float(cell)
        } else {
          cell
        }
      }
    })
  })
}

// ============================================
// 文本处理
// ============================================

/// 截断文本
/// 示例：truncate("很长的文本...", 10) => "很长的文本..."
#let truncate(text, max-len, suffix: "...") = {
  if text == none { return "" }
  
  let str-text = str(text)
  if str-text.len() <= max-len {
    str-text
  } else {
    str-text.slice(0, max-len) + suffix
  }
}

/// 首字母大写
#let capitalize(text) = {
  if text == none or text == "" { return "" }
  
  let str-text = str(text)
  upper(str-text.at(0)) + str-text.slice(1)
}
