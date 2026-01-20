#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成独立版本的 Typst 文件"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def get_standalone_header(title, subtitle, author):
    """获取独立版本的文件头部"""
    
    subtitle_block = ""
    if subtitle:
        subtitle_block = "\n    #v(0.5cm)\n    \n    #text(\n"
        subtitle_block += "      size: 16pt,\n      fill: rgb(\"#6c757d\"),\n"
        subtitle_block += "    )[" + subtitle + "]\n"
    
    header = '// 自动生成的报告 - 独立版本\n'
    header += '// 生成时间: {}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    header += '// 可直接在 Typst 在线编辑器中使用\n\n'
    header += '#set page(\n'
    header += '  paper: "a4",\n'
    header += '  margin: (x: 2.5cm, y: 2.5cm),\n'
    header += '  numbering: "1",\n'
    header += '  header: context {\n'
    header += '    align(right)[\n'
    header += '      #text(size: 9pt, fill: gray)[{}]\n'.format(title)
    header += '    ]\n'
    header += '    line(length: 100%, stroke: 0.5pt + gray)\n'
    header += '  },\n'
    header += '  footer: context {\n'
    header += '    line(length: 100%, stroke: 0.5pt + gray)\n'
    header += '    v(0.25cm)\n'
    header += '    align(center)[\n'
    header += '      #text(size: 9pt, fill: gray)[第 #counter(page).display() 页]\n'
    header += '    ]\n'
    header += '  },\n'
    header += ')\n\n'
    header += '#set text(\n'
    header += '  font: ("Noto Sans", "Noto Sans CJK SC"),\n'
    header += '  size: 10.5pt,\n'
    header += '  lang: "zh",\n'
    header += ')\n\n'
    header += '#set heading(numbering: "1.1")\n\n'
    header += '#show heading.where(level: 1): it => {\n'
    header += '  pagebreak(weak: true)\n'
    header += '  v(1cm)\n'
    header += '  text(size: 18pt, weight: "bold", fill: rgb("#0056b3"))[#it]\n'
    header += '  v(0.5cm)\n'
    header += '}\n\n'
    header += '#show heading.where(level: 2): it => {\n'
    header += '  v(0.5cm)\n'
    header += '  text(size: 14pt, weight: "bold", fill: rgb("#343a40"))[#it]\n'
    header += '  v(0.25cm)\n'
    header += '}\n\n'
    header += '#set par(justify: true, leading: 0.65em, first-line-indent: 2em)\n'
    header += '#show heading: it => { it; par(first-line-indent: 0em)[] }\n\n'
    header += '#set list(marker: [•], indent: 1em)\n'
    header += '#set enum(numbering: "1.", indent: 1em)\n\n'
    header += '#let styled-table(..args) = {\n'
    header += '  table(\n'
    header += '    stroke: (x, y) => {\n'
    header += '      if y == 0 { (bottom: 2pt + rgb("#0056b3")) }\n'
    header += '      else { (bottom: 0.5pt + gray) }\n'
    header += '    },\n'
    header += '    fill: (x, y) => {\n'
    header += '      if y == 0 { rgb("#f8f9fa") }\n'
    header += '      else if calc.rem(y, 2) == 0 { rgb("#f8f9fa").lighten(50%) }\n'
    header += '    },\n'
    header += '    inset: 0.5cm,\n'
    header += '    ..args\n'
    header += '  )\n'
    header += '}\n\n'
    header += '#let kpi-card(label, value, change) = {\n'
    header += '  rect(\n'
    header += '    width: 100%, fill: rgb("#f8f9fa"), stroke: 1pt + rgb("#dee2e6"),\n'
    header += '    radius: 4pt, inset: 1cm,\n'
    header += '  )[\n'
    header += '    #text(size: 10pt, fill: rgb("#6c757d"), weight: "medium")[#label]\n'
    header += '    #v(0.25cm)\n'
    header += '    #text(size: 24pt, weight: "bold", fill: rgb("#0056b3"))[#value]\n'
    header += '    #if change != none [\n'
    header += '      #v(0.25cm)\n'
    header += '      #let change-color = if change >= 0 { rgb("#28a745") } else { rgb("#dc3545") }\n'
    header += '      #let change-icon = if change >= 0 { "↑" } else { "↓" }\n'
    header += '      #let change-percent = calc.round(change * 100, digits: 0)\n'
    header += '      #text(size: 12pt, fill: change-color, weight: "medium")[#change-icon #change-percent%]\n'
    header += '    ]\n'
    header += '  ]\n'
    header += '}\n\n'
    header += '#page(margin: 0cm, header: none, footer: none)[\n'
    header += '  #place(top + center, dy: 30%)[\n'
    header += '    #text(size: 28pt, weight: "bold", fill: rgb("#0056b3"))[{}]\n'.format(title)
    header += subtitle_block
    header += '    #v(2cm)\n'
    header += '    #text(size: 14pt, fill: rgb("#495057"))[{}]\n'.format(author)
    header += '    #v(0.25cm)\n'
    header += '    #text(size: 12pt, fill: rgb("#6c757d"))[\n'
    header += '      #datetime.today().display("[year]年[month]月[day]日")\n'
    header += '    ]\n'
    header += '  ]\n'
    header += ']\n\n'
    header += '#page[\n'
    header += '  #outline(\n'
    header += '    title: [\n'
    header += '      #text(size: 18pt, weight: "bold", fill: rgb("#0056b3"))[目录]\n'
    header += '      #v(1cm)\n'
    header += '    ],\n'
    header += '    indent: auto,\n'
    header += '    depth: 3,\n'
    header += '  )\n'
    header += ']\n\n'
    return header


def convert_markdown_to_typst(text):
    """将 Markdown 格式转换为 Typst 格式"""
    import re
    # 将 **text** 转换为 *text* (粗体)
    text = re.sub(r'\*\*([^*]+)\*\*', r'*\1*', text)
    return text


def generate_standalone_report(data):
    """生成独立版本的报告"""
    title = data.get("title", "报告")
    subtitle = data.get("subtitle", "")
    author = data.get("author", "System")
    summary = data.get("summary", "")
    metrics = data.get("metrics", [])
    sections = data.get("sections", [])
    
    # 生成文件头部
    content = get_standalone_header(title, subtitle, author)
    
    # 添加概览（转换格式）
    content += "= 概览\n\n{}\n\n".format(convert_markdown_to_typst(summary))
    
    # 添加 KPI 指标
    if metrics:
        content += "== 关键指标\n\n#grid(\n  columns: (1fr, 1fr, 1fr),\n  gutter: 1cm,\n  \n"
        for m in metrics:
            label = m.get("label", "")
            value = m.get("value", "")
            change = m.get("change", None)
            content += '  kpi-card("{}", "{}", {}),\n'.format(label, value, change)
        content += ")\n\n"
    
    # 添加章节
    for section in sections:
        heading = section.get("heading", "未命名章节")
        level = section.get("level", 2)
        section_type = section.get("type", "text")
        
        content += "{} {}\n\n".format('=' * level, heading)
        
        if section_type == "text":
            content += "{}\n\n".format(convert_markdown_to_typst(section.get('content', '')))
        elif section_type == "list":
            for item in section.get("items", []):
                content += "- {}\n".format(convert_markdown_to_typst(item))
            content += "\n"
        elif section_type == "table":
            headers = section.get("headers", [])
            data_rows = section.get("data", [])
            if headers and data_rows:
                content += "#styled-table(\n"
                content += "  columns: ({}),\n".format(', '.join(['1fr'] * len(headers)))
                content += "  {},\n".format(', '.join(['[*{}*]'.format(convert_markdown_to_typst(h)) for h in headers]))
                for row in data_rows:
                    content += "  {},\n".format(', '.join(['[{}]'.format(convert_markdown_to_typst(str(cell))) for cell in row]))
                content += ")\n\n"
    
    return content


def main():
    parser = argparse.ArgumentParser(description="生成独立版本的 Typst 文件")
    parser.add_argument("json_file", help="JSON 数据文件")
    parser.add_argument("-o", "--output", required=True, help="输出文件")
    parser.add_argument("-c", "--compile", action="store_true", help="自动编译")
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print("✗ 读取失败: {}".format(e))
        sys.exit(1)
    
    # 生成内容
    print("生成独立版本 .typ 文件...")
    content = generate_standalone_report(data)
    
    # 写入文件
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ 生成成功: {}".format(args.output))
        print("  可直接在 Typst 在线编辑器中使用")
    except Exception as e:
        print("✗ 写入失败: {}".format(e))
        sys.exit(1)
    
    # 编译
    if args.compile:
        print("\n开始编译...")
        try:
            from compile import compile_typst
            pdf_file = Path(args.output).with_suffix('.pdf')
            compile_typst(args.output, str(pdf_file))
        except ImportError:
            print("✗ 无法导入编译模块")
            sys.exit(1)


if __name__ == "__main__":
    main()
