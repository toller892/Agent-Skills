// 自动生成的商业报告
// 生成时间: 2026-01-20 06:37:58

#import "typst-report/typst-templates/templates/business.typ": *
#import "typst-report/typst-templates/lib/utils.typ": *
#import "typst-report/typst-templates/lib/charts.typ": *

// 报告配置
#show: report-conf.with(
  title: "Agent-Skills 项目分析报告",
  subtitle: "OpenCode Agent Skills 集合项目",
  author: "OpenCode Agent",
  date: datetime.today(),
)

= 概览

Agent-Skills 是一个 OpenCode Agent 技能集合项目，包含可复用的 AI 能力模块。本项目旨在为 AI 助手提供标准化的技能开发框架和实用工具。

== 关键指标

#kpi-cards((
  (
    label: "技能数量",
    value: "2",
    change: 1.0,
  ),
  (
    label: "文档文件",
    value: "15+",
    change: 0.5,
  ),
  (
    label: "代码文件",
    value: "20+",
    change: 0.4,
  ),
), columns: 3)

== 项目概述

Agent-Skills 项目是一个 OpenCode Agent 技能集合，包含可复用的 AI 能力模块。项目采用模块化设计，每个技能都有完整的文档和示例代码。

== 核心技能

- typst-report: 使用 Typst 生成专业 PDF 报告
- paper-interpreter: 论文→黄叔风格解读+纽约客插画+2026设计网页

== Typst Report Skill 功能

- [ ] 完整工作流: JSON → .typ → PDF
- [ ] 双重输出: 生成 .typ 源文件和 PDF 文档
- [ ] 数据驱动: 从 JSON/CSV 数据生成报告
- [ ] 中文排版: 支持中文字体和排版规范
- [ ] 图表组件: 折线图、柱状图、KPI 卡片
- [ ] 自动化: 封面、目录、页码自动生成
- [ ] 多模板: 商业报告、学术论文模板

== Paper Interpreter Skill 功能

- [ ] 论文解析: 自动解析学术论文内容
- [ ] 黄叔风格: 以黄叔风格解读复杂内容
- [ ] 纽约客插画: 生成纽约客风格插画
- [ ] 2026设计: 现代网页设计风格
- [ ] 多格式输出: 支持多种输出格式

== 项目结构

#table(
  columns: (1fr, 2fr, 1fr),
  [*目录*], [*描述*], [*文件数量*],
  [typst-report/], [Typst 报告生成技能], [15+],
  [paper-interpreter/], [论文解析技能], [10+],
  [.github/], [GitHub Actions 配置], [1],
  [typst-x86_64-unknown-linux-musl/], [Typst 二进制文件], [2],
)

=== Typst Report 文件结构

#table(
  columns: (2fr, 2fr, 1fr),
  [*文件*], [*用途*], [*状态*],
  [SKILL.md], [技能定义文件], [✅ 完成],
  [README.md], [使用说明文档], [✅ 完成],
  [SUMMARY.md], [功能总结], [✅ 完成],
  [USAGE.md], [详细使用指南], [✅ 完成],
  [OUTPUTS.md], [输出内容详解], [✅ 完成],
  [DEMO.md], [快速演示], [✅ 完成],
  [typst-templates/main.typ], [商业报告入口], [✅ 完成],
  [typst-templates/standard-example.typ], [标准格式示例], [✅ 完成],
  [typst-templates/academic-example.typ], [学术论文示例], [✅ 完成],
  [typst-templates/example-data.json], [测试数据], [✅ 完成],
)

== 技术架构

项目采用模块化架构，每个技能独立开发，通过标准化的接口与 OpenCode Agent 集成。Typst Report 技能使用 Python 脚本进行数据处理和编译，Paper Interpreter 技能使用 API 调用进行内容解析。

== 开发规范

- 每个技能必须包含 SKILL.md 定义文件
- 提供完整的 README.md 使用说明
- 包含示例代码和测试数据
- 支持中文文档和国际化
- 遵循统一的代码风格规范

== 使用场景

- 自动化报告生成: 定期业务报告、数据分析报告
- 学术论文解析: 快速理解论文核心内容
- 文档转换: 将 Markdown、JSON 等格式转换为专业 PDF
- 内容创作: 生成风格化的内容解读
- 团队协作: 标准化的文档输出格式

== 项目优势

- [ ] 标准化: 统一的技能开发框架
- [ ] 可复用: 技能模块可跨项目使用
- [ ] 文档完善: 完整的文档和示例
- [ ] 自动化: 支持 CI/CD 集成
- [ ] 开源: MIT 许可证，可自由使用和修改

== 未来规划

- 增加更多实用技能模块
- 优化技能间的协作机制
- 提供 Web 界面管理工具
- 支持更多数据格式输入
- 集成更多 AI 模型能力

