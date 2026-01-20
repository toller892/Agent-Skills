#!/usr/bin/env python3
"""
Typst 编译脚本 - 将 .typ 文件编译为 PDF

功能：
1. 检查 Typst 是否安装
2. 编译 .typ 文件为 PDF
3. 支持传递 JSON 数据
4. 支持指定字体路径
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path


def check_typst_installed():
    """检查 Typst 是否已安装"""
    try:
        result = subprocess.run(
            ["typst", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ Typst 已安装: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Typst 未安装")
        print("\n安装方法：")
        print("  macOS/Linux: curl -fsSL https://typst.app/install.sh | sh")
        print("  Windows: winget install --id Typst.Typst")
        print("  或访问: https://github.com/typst/typst/releases")
        return False


def compile_typst(
    input_file: str,
    output_file: str = None,
    payload: dict = None,
    font_path: str = None,
    root: str = None,
):
    """
    编译 Typst 文件为 PDF
    
    参数：
        input_file: 输入的 .typ 文件路径
        output_file: 输出的 PDF 文件路径（可选，默认同名）
        payload: JSON 数据（可选）
        font_path: 字体路径（可选）
        root: 根目录（可选）
    """
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"✗ 输入文件不存在: {input_file}")
        return False
    
    # 确定输出文件名
    if output_file is None:
        output_file = Path(input_file).with_suffix('.pdf')
    
    # 构建命令
    cmd = ["typst", "compile"]
    
    # 添加根目录
    if root:
        cmd.extend(["--root", root])
    
    # 添加字体路径
    if font_path:
        cmd.extend(["--font-path", font_path])
    
    # 添加 JSON 数据
    if payload:
        payload_str = json.dumps(payload, ensure_ascii=False)
        cmd.extend(["--input", f"payload={payload_str}"])
    
    # 添加输入输出文件
    cmd.extend([input_file, output_file])
    
    # 执行编译
    print(f"\n编译中: {input_file} -> {output_file}")
    print(f"命令: {' '.join(cmd[:3])} ...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"✓ 编译成功: {output_file}")
        
        # 显示文件大小
        size = os.path.getsize(output_file)
        size_kb = size / 1024
        print(f"  文件大小: {size_kb:.1f} KB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 编译失败")
        print(f"\n错误信息:")
        print(e.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="编译 Typst 文件为 PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础编译
  python compile.py main.typ
  
  # 指定输出文件
  python compile.py main.typ -o report.pdf
  
  # 传递 JSON 数据
  python compile.py main.typ --json '{"title": "报告"}'
  
  # 从文件读取 JSON
  python compile.py main.typ --json-file data.json
  
  # 指定字体路径
  python compile.py main.typ --font-path ./assets/fonts
        """
    )
    
    parser.add_argument(
        "input",
        help="输入的 .typ 文件"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="输出的 PDF 文件（默认同名）"
    )
    
    parser.add_argument(
        "--json",
        help="JSON 数据字符串"
    )
    
    parser.add_argument(
        "--json-file",
        help="JSON 数据文件路径"
    )
    
    parser.add_argument(
        "--font-path",
        help="字体目录路径"
    )
    
    parser.add_argument(
        "--root",
        help="根目录路径"
    )
    
    args = parser.parse_args()
    
    # 检查 Typst 是否安装
    if not check_typst_installed():
        sys.exit(1)
    
    # 解析 JSON 数据
    payload = None
    if args.json:
        try:
            payload = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"✗ JSON 解析失败: {e}")
            sys.exit(1)
    elif args.json_file:
        try:
            with open(args.json_file, 'r', encoding='utf-8') as f:
                payload = json.load(f)
        except Exception as e:
            print(f"✗ 读取 JSON 文件失败: {e}")
            sys.exit(1)
    
    # 编译
    success = compile_typst(
        input_file=args.input,
        output_file=args.output,
        payload=payload,
        font_path=args.font_path,
        root=args.root,
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
