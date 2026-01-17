#!/bin/bash

# Agent Skills 项目报告生成脚本
# 使用 typst-report skill 生成项目分析报告

echo "=== Agent Skills 项目报告生成 ==="
echo ""

# 检查依赖
if ! command -v typst &> /dev/null; then
    echo "错误: Typst 未安装"
    echo "请安装 Typst: https://github.com/typst/typst"
    exit 1
fi

# 检查数据文件
if [ ! -f "project-report-data.json" ]; then
    echo "错误: 数据文件 project-report-data.json 不存在"
    exit 1
fi

# 生成报告
echo "正在生成报告..."
cd typst-report/typst-templates

typst compile \
    --input payload="$(cat ../../project-report-data.json)" \
    main.typ \
    ../../agent-skills-report.pdf

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 报告生成成功!"
    echo "📄 报告文件: agent-skills-report.pdf"
    echo "📊 文件大小: $(ls -lh ../../agent-skills-report.pdf | awk '{print $5}')"
else
    echo ""
    echo "❌ 报告生成失败"
    exit 1
fi