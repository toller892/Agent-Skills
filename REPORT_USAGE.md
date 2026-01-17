# Typst-Report Skill 使用示例

本示例展示了如何使用 typst-report skill 基于 Agent Skills 项目内容生成一份专业报告。

## 生成的报告内容

报告包含以下部分：

1. **项目概述** - Agent Skills 项目的整体介绍
2. **核心技能分析** - typst-report 和 paper-interpreter 技能详解
3. **项目结构** - 目录结构分析
4. **技术栈分析** - 使用的技术和工具
5. **文件统计** - 项目文件类型和数量统计
6. **使用场景** - 技能的应用场景
7. **优势分析** - 项目的优势特点
8. **改进建议** - 未来改进方向
9. **总结** - 项目综合评价

## 生成的文件

- `project-report-data.json` - 报告数据源文件（JSON格式）
- `agent-skills-report.pdf` - 生成的 PDF 报告
- `generate-report.sh` - 报告生成脚本

## 如何使用 typst-report skill

### 方法1：使用脚本生成
```bash
./generate-report.sh
```

### 方法2：手动生成
```bash
cd typst-report/typst-templates
typst compile --input payload="$(cat ../../project-report-data.json)" main.typ ../../report.pdf
```

### 方法3：在 GitHub Issue/PR 中使用
```
/oc 使用 typst-report skill 生成一份项目分析报告
```

## 数据格式说明

typst-report skill 接受 JSON 格式的数据，包含以下字段：

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

## 技能特点

1. **自动化生成** - 从结构化数据自动生成专业报告
2. **中文支持** - 完整的中文排版支持
3. **图表集成** - 内置图表组件（CeTZ）
4. **模板化** - 可定制的报告模板
5. **开源** - 基于 Typst 开源排版系统

## 扩展使用

你可以修改 `project-report-data.json` 文件来生成不同内容的报告，例如：

- 项目进度报告
- 代码质量分析报告
- 测试覆盖率报告
- 性能测试报告
- 用户需求分析报告

## 相关资源

- [Typst 官方文档](https://typst.app/docs/)
- [typst-report skill 文档](./typst-report/README.md)
- [Agent Skills 项目主页](./README.md)