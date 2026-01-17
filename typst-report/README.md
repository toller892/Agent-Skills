# Typst Report Generation Skill

使用 Typst 排版系统生成专业 PDF 报告的 OpenCode skill。

## 功能特性

- 📊 从 JSON/CSV 数据生成报告
- 🎨 支持中文排版
- 📈 内置图表组件（折线图、柱状图）
- 📑 自动生成封面、目录、页码
- 🎯 KPI 卡片、数据表格等业务组件

## 目录结构

```
typst-report/
├── SKILL.md                          # Skill 定义文件
├── README.md                         # 本文件
└── typst-templates/                  # Typst 模板
    ├── main.typ                      # 入口文件
    ├── example-data.json             # 测试数据
    ├── lib/
    │   ├── utils.typ                 # 数据处理工具
    │   ├── theme.typ                 # 全局样式
    │   └── charts.typ                # 图表组件
    ├── templates/
    │   └── business.typ              # 商业报告模板
    └── assets/
        ├── fonts/                    # 字体目录
        └── images/                   # 图片目录
```

## 使用方式

### 在 GitHub Issue/PR 中

评论：
```
/oc 生成一份测试报告
```

### 本地测试

```bash
cd typst-templates

# 使用示例数据
typst compile \
  --input payload="$(cat example-data.json)" \
  main.typ \
  test-report.pdf
```

## 数据格式

支持的输入格式：
- **JSON**（推荐）- 通过 `--input` 传递
- **CSV** - 从文件读取
- **Markdown** - 需要预处理为 JSON

### JSON 数据结构示例

```json
{
  "title": "报告标题",
  "subtitle": "副标题",
  "author": "作者",
  "summary": "概览内容",
  "metrics": [
    {"label": "指标名", "value": "1,234", "change": 0.15}
  ],
  "sections": [
    {
      "heading": "章节标题",
      "level": 2,
      "type": "text",
      "content": "章节内容"
    }
  ]
}
```

## 依赖

- Typst >= 0.11.0
- 中文字体（Noto Sans SC）

## 参考资源

- [Typst 官方文档](https://typst.app/docs/)
- [CeTZ 图表库](https://typst.app/universe/package/cetz-plot/)
- [开发计划](../../doc/typst-skill-development-plan.md)
