# Typst Report - 快速演示

## 演示：从源码到 PDF

### 步骤 1: 创建 Typst 源文件

创建 `demo.typ`：

```typst
#import "templates/academic.typ": *

#show: academic-conf.with(
  title: "快速演示文档",
  author: "演示用户",
  show-header: false,
)

= 简介

这是一个 *快速演示* 文档，展示 Typst 的基本功能。

== 文本格式

- *加粗文本*
- _斜体文本_
- `代码文本`

= 数学公式

行内公式：爱因斯坦方程 $E = m c^2$

块级公式：
$ F(x) = integral_0^x sin(t) dif t $

= 表格

#table(
  columns: (auto, 1fr, 1fr),
  [*序号*], [*项目*], [*数值*],
  [1], [项目 A], [100],
  [2], [项目 B], [200],
  [3], [项目 C], [300],
)

= 结论

Typst 让文档编写变得简单高效！
```

### 步骤 2: 编译为 PDF

```bash
# 使用 Python 脚本
python scripts/compile.py demo.typ

# 或直接使用 Typst
typst compile demo.typ
```

### 步骤 3: 查看结果

打开生成的 `demo.pdf`，你会看到：

```
┌─────────────────────────────┐
│   快速演示文档               │  ← 标题居中
│   演示用户                   │
│   2026年1月20日             │
├─────────────────────────────┤
│                              │
│ 1 简介                       │  ← 自动编号
│                              │
│ 这是一个快速演示文档，展示   │
│ Typst 的基本功能。           │
│                              │
│ 1.1 文本格式                 │
│                              │
│ • 加粗文本                   │  ← 格式化
│ • 斜体文本                   │
│ • 代码文本                   │
│                              │
│ 2 数学公式                   │
│                              │
│ 行内公式：爱因斯坦方程 E=mc² │  ← 公式渲染
│                              │
│ 块级公式：                   │
│     ∫₀ˣ sin(t) dt           │
│                              │
│ 3 表格                       │
│                              │
│ ┌────┬────────┬──────┐      │  ← 表格
│ │序号│ 项目   │ 数值 │      │
│ ├────┼────────┼──────┤      │
│ │ 1  │ 项目 A │ 100  │      │
│ │ 2  │ 项目 B │ 200  │      │
│ │ 3  │ 项目 C │ 300  │      │
│ └────┴────────┴──────┘      │
│                              │
│ 4 结论                       │
│                              │
│ Typst 让文档编写变得简单高效！│
│                              │
└─────────────────────────────┘
         1 / 1                    ← 页码
```

## 演示：数据驱动报告

### 步骤 1: 准备数据

创建 `report-data.json`：

```json
{
  "title": "2026年1月销售报告",
  "subtitle": "华东区域",
  "author": "销售部",
  "summary": "本月销售业绩创历史新高，同比增长 25%。",
  "metrics": [
    {
      "label": "总销售额",
      "value": "¥1,234,567",
      "change": 0.25
    },
    {
      "label": "新客户",
      "value": "156",
      "change": 0.18
    },
    {
      "label": "订单数",
      "value": "892",
      "change": 0.12
    }
  ],
  "sections": [
    {
      "heading": "销售分析",
      "level": 2,
      "type": "text",
      "content": "本月销售主要增长来自企业客户，占比达到 65%。"
    },
    {
      "heading": "区域分布",
      "level": 2,
      "type": "table",
      "headers": ["区域", "销售额", "占比"],
      "data": [
        ["上海", "¥456,789", "37%"],
        ["杭州", "¥345,678", "28%"],
        ["南京", "¥234,567", "19%"],
        ["其他", "¥197,533", "16%"]
      ]
    }
  ]
}
```

### 步骤 2: 编译报告

```bash
python scripts/compile.py typst-templates/main.typ \
  --json-file report-data.json \
  -o sales-report.pdf
```

### 步骤 3: 查看结果

生成的 `sales-report.pdf` 包含：

```
┌─────────────────────────────┐
│                              │
│   2026年1月销售报告          │  ← 封面页
│   华东区域                   │
│                              │
│   销售部                     │
│   2026年1月20日             │
│                              │
└─────────────────────────────┘

┌─────────────────────────────┐
│   目录                       │  ← 自动生成
│                              │
│   1. 概览 ............... 3  │
│   2. 销售分析 ........... 4  │
│   3. 区域分布 ........... 4  │
│                              │
└─────────────────────────────┘

┌─────────────────────────────┐
│ 1 概览                       │  ← 正文
│                              │
│ 本月销售业绩创历史新高，     │
│ 同比增长 25%。               │
│                              │
│ ┌──────────┬──────────┬─────┐│
│ │ 总销售额 │ 新客户   │订单数││  ← KPI 卡片
│ │          │          │     ││
│ │¥1,234,567│   156    │ 892 ││
│ │  ↑25%    │  ↑18%    │↑12% ││
│ └──────────┴──────────┴─────┘│
│                              │
│ 2 销售分析                   │
│                              │
│ 本月销售主要增长来自企业客户，│
│ 占比达到 65%。               │
│                              │
│ 3 区域分布                   │
│                              │
│ ┌────────┬──────────┬──────┐│
│ │ 区域   │ 销售额   │ 占比 ││
│ ├────────┼──────────┼──────┤│
│ │ 上海   │ ¥456,789 │ 37%  ││
│ │ 杭州   │ ¥345,678 │ 28%  ││
│ │ 南京   │ ¥234,567 │ 19%  ││
│ │ 其他   │ ¥197,533 │ 16%  ││
│ └────────┴──────────┴──────┘│
│                              │
└─────────────────────────────┘
         3 / 3
```

## 对比：传统方式 vs Typst

### 传统方式（Word/LaTeX）

```
1. 打开 Word/编写 LaTeX
2. 手动设置字体、边距、页眉页脚
3. 手动插入表格、调整格式
4. 手动生成目录
5. 手动更新页码
6. 导出 PDF
⏱️ 耗时：30-60 分钟
```

### Typst 方式

```
1. 编写 .typ 文件（或准备 JSON 数据）
2. 运行编译命令
⏱️ 耗时：10 秒
```

## 核心优势

| 特性 | 传统方式 | Typst |
|------|---------|-------|
| **编写速度** | 慢 | 快 |
| **格式一致性** | 手动调整，易出错 | 自动化，100% 一致 |
| **版本控制** | 二进制文件，难以 diff | 纯文本，Git 友好 |
| **自动化** | 难以自动化 | 完全可编程 |
| **数学公式** | 需要插件 | 原生支持 |
| **中文支持** | 需要配置 | 开箱即用 |
| **编译速度** | 慢（LaTeX） | 秒级 |
| **学习曲线** | 陡峭（LaTeX） | 平缓 |

## 实际应用场景

### 1. 自动化周报

```python
# 每周五自动生成
import requests
from compile import compile_typst

# 从 API 获取数据
data = requests.get("https://api.example.com/weekly-stats").json()

# 生成报告
compile_typst(
    "typst-templates/main.typ",
    f"reports/week-{week_num}.pdf",
    payload=data
)
```

### 2. 批量生成客户报告

```python
# 为每个客户生成定制报告
for customer in customers:
    data = generate_customer_data(customer)
    compile_typst(
        "typst-templates/main.typ",
        f"reports/{customer.name}.pdf",
        payload=data
    )
```

### 3. CI/CD 集成

```yaml
# 每次发版自动生成 Release Notes
- name: Generate Release Notes
  run: |
    python scripts/compile.py \
      release-notes.typ \
      -o release-notes-v${{ github.ref_name }}.pdf
```

## 下一步

1. **安装 Typst**：参考 [USAGE.md](USAGE.md)
2. **运行测试**：`python scripts/test_compile.py`
3. **查看示例**：编译 `standard-example.typ`
4. **创建自己的文档**：参考模板开始编写

## 获取帮助

- 查看 [USAGE.md](USAGE.md) 了解详细用法
- 查看 [SKILL.md](SKILL.md) 了解 Typst 语法
- 访问 [Typst 官方文档](https://typst.app/docs/)
