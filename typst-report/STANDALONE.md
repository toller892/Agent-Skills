# 独立版本说明

## 什么是独立版本？

独立版本的 `.typ` 文件是指：
- ✅ **不依赖外部文件** - 所有样式定义都内联在文件中
- ✅ **可直接在线编译** - 可以直接在 Typst 在线编辑器中使用
- ✅ **完全自包含** - 无需上传模板文件或配置路径

## 为什么需要独立版本？

### 问题场景

使用模板导入方式生成的文件：

```typst
#import "typst-report/typst-templates/templates/business.typ": *
```

在 **Typst 在线编辑器**中会报错：
```
File not found (searched at typst-report/typst-templates/templates/business.typ)
```

### 解决方案

独立版本将所有样式定义内联：

```typst
// 所有样式定义都在文件内部
#set page(...)
#set text(...)
#let kpi-card(...) = {...}

// 直接使用，无需导入
#kpi-card("指标", "数值", 0.15)
```

## 使用方式

### 方式 1: 默认生成（推荐）

**从 v2.0 开始，skill 默认生成独立版本**

```bash
# 自动生成独立版本
python scripts/generate_report.py data.json

# 输出:
#   output/report_20260120_143000.typ  ← 独立版本，可直接在线编译
#   output/report_20260120_143000.pdf
```

### 方式 2: 显式指定

```bash
# 使用 generate.py
python scripts/generate.py data.json -o report.typ --standalone

# 使用 generate_standalone.py
python scripts/generate_standalone.py data.json -o report.typ
```

### 方式 3: 使用模板导入方式

如果你需要本地编译，可以使用模板导入方式：

```bash
python scripts/generate_report.py data.json --no-standalone
```

## 对比

| 特性 | 独立版本 | 模板导入版本 |
|------|---------|------------|
| **在线编辑器** | ✅ 可用 | ❌ 不可用 |
| **本地编译** | ✅ 可用 | ✅ 可用 |
| **文件大小** | 较大（~5-10KB） | 较小（~2-3KB） |
| **可读性** | 较差（样式定义多） | 较好（只有内容） |
| **可维护性** | 低（样式内联） | 高（样式集中管理） |
| **适用场景** | 在线编辑、分享 | 本地开发、团队协作 |

## 实际使用示例

### 示例 1: 在线编辑器使用

```bash
# 1. 生成独立版本
python scripts/generate_standalone.py data.json -o report.typ

# 2. 打开 Typst 在线编辑器
#    https://typst.app/

# 3. 复制 report.typ 的全部内容

# 4. 粘贴到在线编辑器

# 5. 点击编译 ✓
```

### 示例 2: 本地编译

```bash
# 生成独立版本
python scripts/generate_standalone.py data.json -o report.typ

# 本地编译
typst compile report.typ report.pdf
```

### 示例 3: 批量生成

```python
# batch_generate.py
from generate_standalone import generate_standalone_report
import json

customers = ["客户A", "客户B", "客户C"]

for customer in customers:
    # 准备数据
    data = {
        "title": f"{customer} 月度报告",
        "summary": f"为 {customer} 生成的报告...",
    }
    
    # 生成独立版本
    typ_content = generate_standalone_report(data)
    
    # 保存文件
    with open(f"reports/{customer}.typ", 'w') as f:
        f.write(typ_content)
    
    print(f"✓ 生成 {customer} 的报告")
```

## 文件结构对比

### 独立版本

```typst
// report-standalone.typ

// ============================================
// 页面设置（内联）
// ============================================
#set page(...)

// ============================================
// 文本设置（内联）
// ============================================
#set text(...)

// ============================================
// 组件定义（内联）
// ============================================
#let kpi-card(...) = {...}
#let styled-table(...) = {...}

// ============================================
// 正文内容
// ============================================
= 概览
...
```

### 模板导入版本

```typst
// report.typ

// 导入外部模板
#import "typst-report/typst-templates/templates/business.typ": *
#import "typst-report/typst-templates/lib/utils.typ": *

// 正文内容
= 概览
...
```

## 自定义样式

### 修改独立版本的样式

编辑生成的 `.typ` 文件：

```typst
// 修改主色调
#show heading.where(level: 1): it => {
  text(
    fill: rgb("#ff0000"),  // 改为红色
  )[#it]
}

// 修改字体大小
#set text(size: 12pt)  // 改为 12pt

// 修改页边距
#set page(margin: (x: 3cm, y: 3cm))
```

### 修改模板导入版本的样式

编辑 `typst-report/typst-templates/lib/theme.typ`：

```typst
// 修改主色调
#let brand-primary = rgb("#ff0000")

// 修改字体大小
#set text(size: 12pt)
```

## 性能对比

| 操作 | 独立版本 | 模板导入版本 |
|------|---------|------------|
| 生成速度 | 快（无需计算路径） | 较快 |
| 编译速度 | 快（无需加载外部文件） | 较快 |
| 文件大小 | 5-10 KB | 2-3 KB |
| 内存占用 | 相同 | 相同 |

## 最佳实践

### 推荐使用独立版本的场景

1. **在线编辑器使用** - 必须使用独立版本
2. **分享给他人** - 独立版本更方便
3. **一次性报告** - 不需要维护样式
4. **快速原型** - 快速生成和测试

### 推荐使用模板导入版本的场景

1. **团队协作** - 统一样式管理
2. **长期维护** - 样式集中更新
3. **大量报告** - 样式复用
4. **本地开发** - 更好的代码组织

## 常见问题

### Q: 独立版本可以修改样式吗？

A: 可以，直接编辑 `.typ` 文件中的样式定义部分。

### Q: 独立版本文件更大，会影响性能吗？

A: 不会。文件大小差异很小（几KB），对编译性能没有明显影响。

### Q: 可以将独立版本转换为模板导入版本吗？

A: 可以，但需要手动提取样式定义到模板文件中。

### Q: 默认生成哪种版本？

A: 从 v2.0 开始，默认生成独立版本。可以使用 `--no-standalone` 选项生成模板导入版本。

## 总结

**独立版本是 Typst 在线编辑器的最佳选择**

- ✅ 无需配置，开箱即用
- ✅ 可直接在线编译
- ✅ 方便分享和协作
- ✅ 适合快速原型和一次性报告

**从 v2.0 开始，skill 默认生成独立版本，确保最佳的在线编辑器兼容性。**
