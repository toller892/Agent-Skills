# Agent Skills

OpenCode Agent Skills 集合，包含可复用的 AI 能力模块。

## 已有 Skills

### [typst-report](./typst-report/)
使用 Typst 生成专业 PDF 报告

**功能：**
- 从 JSON/CSV 数据生成报告
- 支持图表、表格、KPI 卡片
- 中文排版支持

**使用：**
```
/oc 生成一份业务报告
```

## Skill 开发规范

每个 skill 应包含：
- `SKILL.md` - Skill 定义文件（必需）
- `README.md` - 使用说明
- `scripts/` - 可执行脚本（可选）
- `references/` - 参考文档（可选）

## 相关文档

- [Typst Skill 开发计划](../doc/typst-skill-development-plan.md)
- [任务清单](../doc/typst-skill-todo.md)
