#!/usr/bin/env python3
"""
Typst 文档生成器 - 从数据生成 .typ 文件

功能：
1. 从 JSON 数据生成 .typ 源文件
2. 支持多种模板（商业报告、学术论文）
3. 可选择是否自动编译为 PDF
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def generate_business_report(data: dict, output_file: str = None) -> str:
    """
    生成商业报告 .typ 文件
    
    参数：
        data: JSON 数据字典
        output_file: 输出文件路径（用于计算相对路径）
    
    返回：
        生成的 .typ 文件内容
    """
    title = data.get("title", "业务报告")
    subtitle = data.get("subtitle", "")
    author = data.get("author", "System")
    summary = data.get("summary", "")
    metrics = data.get("metrics", [])
    sections = data.get("sections", [])
    
    # 计算相对路径
    if output_file:
        from pathlib import Path
        output_path = Path(output_file).resolve()
        template_dir = Path("typst-report/typst-templates").resolve()
        
        try:
            # 计算相对路径
            rel_path = os.path.relpath(template_dir, output_path.parent)
            import_prefix = rel_path.replace("\\", "/")
        except ValueError:
            # 如果在不同驱动器，使用绝对路径
            import_prefix = "typst-report/typst-templates"
    else:
        import_prefix = "templates"
    
    # 生成 .typ 内容
    typ_content = f"""// 自动生成的商业报告
// 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

#import "{import_prefix}/templates/business.typ": *
#import "{import_prefix}/lib/utils.typ": *
#import "{import_prefix}/lib/charts.typ": *

// 报告配置
#show: report-conf.with(
  title: "{title}",
"""
    
    if subtitle:
        typ_content += f'  subtitle: "{subtitle}",\n'
    
    typ_content += f"""  author: "{author}",
  date: datetime.today(),
)

= 概览

{summary}

"""
    
    # 添加 KPI 指标
    if metrics:
        typ_content += """== 关键指标

#kpi-cards((
"""
        for metric in metrics:
            label = metric.get("label", "")
            value = metric.get("value", "")
            change = metric.get("change", 0)
            typ_content += f"""  (
    label: "{label}",
    value: "{value}",
    change: {change},
  ),
"""
        typ_content += """), columns: 3)

"""
    
    # 添加章节
    for section in sections:
        heading = section.get("heading", "未命名章节")
        level = section.get("level", 2)
        section_type = section.get("type", "text")
        
        # 生成标题
        heading_prefix = "=" * level
        typ_content += f"{heading_prefix} {heading}\n\n"
        
        # 根据类型生成内容
        if section_type == "text":
            content = section.get("content", "")
            typ_content += f"{content}\n\n"
        
        elif section_type == "list":
            items = section.get("items", [])
            for item in items:
                typ_content += f"- {item}\n"
            typ_content += "\n"
        
        elif section_type == "checklist":
            items = section.get("items", [])
            for item in items:
                typ_content += f"- [ ] {item}\n"
            typ_content += "\n"
        
        elif section_type == "table":
            headers = section.get("headers", [])
            data_rows = section.get("data", [])
            
            if headers and data_rows:
                typ_content += "#data-table(\n"
                typ_content += f"  ({', '.join([f'[*{h}*]' for h in headers])}),\n"
                typ_content += "  (\n"
                for row in data_rows:
                    typ_content += f"    ({', '.join([f'[{cell}]' for cell in row])}),\n"
                typ_content += "  )\n"
                typ_content += ")\n\n"
        
        elif section_type == "chart":
            chart_type = section.get("chart_type", "bar")
            chart_data = section.get("data", [])
            
            if chart_type == "bar":
                typ_content += "#simple-bar-chart((\n"
                for item in chart_data:
                    label = item.get("label", "")
                    value = item.get("value", 0)
                    typ_content += f'  (label: "{label}", value: {value}),\n'
                typ_content += "))\n\n"
            
            elif chart_type == "line":
                typ_content += "#line-chart(\n"
                typ_content += "  (\n"
                for item in chart_data:
                    x = item.get("x", 0)
                    y = item.get("y", 0)
                    typ_content += f"    ({x}, {y}),\n"
                typ_content += "  ),\n"
                typ_content += f'  title: "{heading}",\n'
                typ_content += ")\n\n"
    
    return typ_content


def generate_academic_paper(data: dict) -> str:
    """
    生成学术论文 .typ 文件
    
    参数：
        data: JSON 数据字典
    
    返回：
        生成的 .typ 文件内容
    """
    title = data.get("title", "学术论文")
    author = data.get("author", "作者")
    abstract = data.get("abstract", "")
    keywords = data.get("keywords", [])
    sections = data.get("sections", [])
    
    # 生成 .typ 内容
    typ_content = f"""// 自动生成的学术论文
// 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

#import "templates/academic.typ": *

#show: academic-conf.with(
  title: "{title}",
  author: "{author}",
  show-header: false,
"""
    
    if abstract:
        typ_content += f"""  abstract: [
    {abstract}
  ],
"""
    
    if keywords:
        keywords_str = '", "'.join(keywords)
        typ_content += f'  keywords: ("{keywords_str}"),\n'
    
    typ_content += ")\n\n"
    
    # 添加章节
    for section in sections:
        heading = section.get("heading", "未命名章节")
        level = section.get("level", 1)
        section_type = section.get("type", "text")
        
        # 生成标题
        heading_prefix = "=" * level
        typ_content += f"{heading_prefix} {heading}\n\n"
        
        # 根据类型生成内容
        if section_type == "text":
            content = section.get("content", "")
            typ_content += f"{content}\n\n"
        
        elif section_type == "list":
            items = section.get("items", [])
            for item in items:
                typ_content += f"- {item}\n"
            typ_content += "\n"
        
        elif section_type == "table":
            headers = section.get("headers", [])
            data_rows = section.get("data", [])
            
            if headers and data_rows:
                typ_content += "#three-line-table(\n"
                typ_content += f"  columns: ({', '.join(['auto'] * len(headers))}),\n"
                typ_content += f"  {', '.join([f'[*{h}*]' for h in headers])},\n"
                for row in data_rows:
                    typ_content += f"  {', '.join([f'[{cell}]' for cell in row])},\n"
                typ_content += ")\n\n"
    
    return typ_content


def generate_typst_file(
    data: dict,
    output_file: str,
    template: str = "business",
) -> bool:
    """
    生成 .typ 文件
    
    参数：
        data: JSON 数据
        output_file: 输出文件路径
        template: 模板类型（business/academic）
    
    返回：
        是否成功
    """
    try:
        # 根据模板类型生成内容
        if template == "business":
            typ_content = generate_business_report(data, output_file)
        elif template == "academic":
            typ_content = generate_academic_paper(data, output_file)
        else:
            print(f"✗ 不支持的模板类型: {template}")
            return False
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(typ_content)
        
        print(f"✓ 生成 .typ 文件: {output_file}")
        
        # 显示文件大小
        size = os.path.getsize(output_file)
        print(f"  文件大小: {size} 字节")
        
        return True
        
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="从 JSON 数据生成 Typst 文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 JSON 文件生成
  python generate.py data.json -o report.typ
  
  # 指定模板类型
  python generate.py data.json -o paper.typ --template academic
  
  # 生成后自动编译
  python generate.py data.json -o report.typ --compile
        """
    )
    
    parser.add_argument(
        "json_file",
        help="JSON 数据文件"
    )
    
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="输出的 .typ 文件路径"
    )
    
    parser.add_argument(
        "-t", "--template",
        choices=["business", "academic"],
        default="business",
        help="模板类型（默认: business）"
    )
    
    parser.add_argument(
        "-c", "--compile",
        action="store_true",
        help="生成后自动编译为 PDF"
    )
    
    parser.add_argument(
        "-s", "--standalone",
        action="store_true",
        help="生成独立版本（无需外部依赖，可直接在在线编辑器使用）"
    )
    
    args = parser.parse_args()
    
    # 如果是独立版本，使用专门的生成器
    if args.standalone:
        from generate_standalone import generate_standalone_report
        
        # 读取 JSON 数据
        try:
            with open(args.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"✗ 读取 JSON 文件失败: {e}")
            sys.exit(1)
        
        # 生成独立版本
        print("生成独立版本 .typ 文件...")
        typ_content = generate_standalone_report(data)
        
        # 写入文件
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(typ_content)
            print(f"✓ 生成成功: {args.output}")
            print(f"  可直接在 Typst 在线编辑器中使用")
        except Exception as e:
            print(f"✗ 写入文件失败: {e}")
            sys.exit(1)
        
        # 如果需要编译
        if args.compile:
            print("\n开始编译...")
            from compile import compile_typst
            pdf_file = Path(args.output).with_suffix('.pdf')
            compile_typst(args.output, str(pdf_file))
        
        sys.exit(0)
    
    args = parser.parse_args()
    
    # 读取 JSON 数据
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"✗ 读取 JSON 文件失败: {e}")
        sys.exit(1)
    
    # 生成 .typ 文件
    success = generate_typst_file(
        data=data,
        output_file=args.output,
        template=args.template,
    )
    
    if not success:
        sys.exit(1)
    
    # 如果需要编译
    if args.compile:
        print("\n开始编译...")
        
        # 导入编译模块
        try:
            from compile import compile_typst
            
            pdf_file = Path(args.output).with_suffix('.pdf')
            compile_success = compile_typst(
                input_file=args.output,
                output_file=str(pdf_file),
            )
            
            if not compile_success:
                sys.exit(1)
                
        except ImportError:
            print("✗ 无法导入编译模块，请手动编译")
            print(f"  命令: typst compile {args.output}")
            sys.exit(1)
    
    print("\n✓ 完成！")
    
    if not args.compile:
        print(f"\n编译命令:")
        print(f"  typst compile {args.output}")


if __name__ == "__main__":
    main()
