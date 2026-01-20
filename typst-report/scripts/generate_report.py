#!/usr/bin/env python3
"""
完整报告生成工作流

输入: JSON 数据
输出: 
  1. .typ 源文件
  2. PDF 文档
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 导入生成和编译模块
from generate import generate_typst_file
from compile import compile_typst, check_typst_installed


def generate_report_workflow(
    json_file: str,
    output_dir: str = "output",
    template: str = "business",
    keep_typ: bool = True,
) -> dict:
    """
    完整的报告生成工作流
    
    参数：
        json_file: JSON 数据文件
        output_dir: 输出目录
        template: 模板类型
        keep_typ: 是否保留 .typ 文件
    
    返回：
        生成的文件信息
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 读取 JSON 数据
    print("=" * 50)
    print("步骤 1: 读取数据")
    print("=" * 50)
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ 读取成功: {json_file}")
        
        # 显示数据摘要
        title = data.get("title", "未命名")
        print(f"  标题: {title}")
        
    except Exception as e:
        print(f"✗ 读取失败: {e}")
        return None
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"report_{timestamp}"
    typ_file = output_path / f"{base_name}.typ"
    pdf_file = output_path / f"{base_name}.pdf"
    
    # 步骤 2: 生成 .typ 文件
    print("\n" + "=" * 50)
    print("步骤 2: 生成 .typ 源文件")
    print("=" * 50)
    
    success = generate_typst_file(
        data=data,
        output_file=str(typ_file),
        template=template,
    )
    
    if not success:
        return None
    
    # 步骤 3: 编译为 PDF
    print("\n" + "=" * 50)
    print("步骤 3: 编译为 PDF")
    print("=" * 50)
    
    success = compile_typst(
        input_file=str(typ_file),
        output_file=str(pdf_file),
    )
    
    if not success:
        return None
    
    # 步骤 4: 清理（可选）
    if not keep_typ:
        print("\n" + "=" * 50)
        print("步骤 4: 清理临时文件")
        print("=" * 50)
        
        try:
            os.remove(typ_file)
            print(f"✓ 删除: {typ_file}")
        except Exception as e:
            print(f"⚠️ 删除失败: {e}")
    
    # 返回结果
    result = {
        "typ_file": str(typ_file) if keep_typ else None,
        "pdf_file": str(pdf_file),
        "timestamp": timestamp,
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="完整报告生成工作流（JSON → .typ → PDF）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础用法
  python generate_report.py data.json
  
  # 指定输出目录
  python generate_report.py data.json -o reports/
  
  # 使用学术模板
  python generate_report.py data.json --template academic
  
  # 不保留 .typ 文件
  python generate_report.py data.json --no-keep-typ
        """
    )
    
    parser.add_argument(
        "json_file",
        help="JSON 数据文件"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default="output",
        help="输出目录（默认: output）"
    )
    
    parser.add_argument(
        "-t", "--template",
        choices=["business", "academic"],
        default="business",
        help="模板类型（默认: business）"
    )
    
    parser.add_argument(
        "--no-keep-typ",
        action="store_true",
        help="不保留 .typ 源文件"
    )
    
    args = parser.parse_args()
    
    # 检查 Typst 是否安装
    print("检查环境...")
    if not check_typst_installed():
        sys.exit(1)
    
    print()
    
    # 执行工作流
    result = generate_report_workflow(
        json_file=args.json_file,
        output_dir=args.output_dir,
        template=args.template,
        keep_typ=not args.no_keep_typ,
    )
    
    if result is None:
        print("\n✗ 生成失败")
        sys.exit(1)
    
    # 显示结果
    print("\n" + "=" * 50)
    print("生成完成！")
    print("=" * 50)
    
    if result["typ_file"]:
        print(f"📄 .typ 源文件: {result['typ_file']}")
    
    print(f"📕 PDF 文档: {result['pdf_file']}")
    print(f"⏰ 生成时间: {result['timestamp']}")
    
    print("\n✓ 所有步骤完成！")


if __name__ == "__main__":
    main()
