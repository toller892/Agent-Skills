#!/usr/bin/env python3
"""
快速测试 Typst 编译功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from compile import check_typst_installed, compile_typst


def test_basic_compile():
    """测试基础编译"""
    print("=" * 50)
    print("测试 1: 基础编译")
    print("=" * 50)
    
    input_file = "../typst-templates/standard-example.typ"
    output_file = "../typst-templates/test-output.pdf"
    
    success = compile_typst(input_file, output_file)
    
    if success:
        print("\n✓ 测试 1 通过")
    else:
        print("\n✗ 测试 1 失败")
    
    return success


def test_json_compile():
    """测试 JSON 数据编译"""
    print("\n" + "=" * 50)
    print("测试 2: JSON 数据编译")
    print("=" * 50)
    
    input_file = "../typst-templates/main.typ"
    output_file = "../typst-templates/test-json-output.pdf"
    
    payload = {
        "title": "测试报告",
        "subtitle": "自动化生成",
        "author": "测试脚本",
        "summary": "这是一个测试报告，用于验证 JSON 数据传递功能。",
        "metrics": [
            {"label": "测试指标 1", "value": "100", "change": 0.15},
            {"label": "测试指标 2", "value": "200", "change": -0.05},
            {"label": "测试指标 3", "value": "300", "change": 0.25},
        ],
        "sections": [
            {
                "heading": "测试章节",
                "level": 2,
                "type": "text",
                "content": "这是一个测试章节的内容。"
            },
            {
                "heading": "测试列表",
                "level": 2,
                "type": "list",
                "items": ["项目 1", "项目 2", "项目 3"]
            },
            {
                "heading": "测试表格",
                "level": 2,
                "type": "table",
                "headers": ["列1", "列2", "列3"],
                "data": [
                    ["数据1", "数据2", "数据3"],
                    ["数据4", "数据5", "数据6"],
                ]
            }
        ]
    }
    
    success = compile_typst(input_file, output_file, payload=payload)
    
    if success:
        print("\n✓ 测试 2 通过")
    else:
        print("\n✗ 测试 2 失败")
    
    return success


def test_json_file_compile():
    """测试从 JSON 文件编译"""
    print("\n" + "=" * 50)
    print("测试 3: JSON 文件编译")
    print("=" * 50)
    
    import json
    
    input_file = "../typst-templates/main.typ"
    json_file = "../typst-templates/example-data.json"
    output_file = "../typst-templates/test-json-file-output.pdf"
    
    # 读取 JSON 文件
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except Exception as e:
        print(f"✗ 读取 JSON 文件失败: {e}")
        return False
    
    success = compile_typst(input_file, output_file, payload=payload)
    
    if success:
        print("\n✓ 测试 3 通过")
    else:
        print("\n✗ 测试 3 失败")
    
    return success


def main():
    print("Typst 编译功能测试")
    print("=" * 50)
    
    # 检查 Typst 是否安装
    if not check_typst_installed():
        print("\n请先安装 Typst 后再运行测试")
        sys.exit(1)
    
    # 切换到脚本目录
    os.chdir(Path(__file__).parent)
    
    # 运行测试
    results = []
    
    results.append(("基础编译", test_basic_compile()))
    results.append(("JSON 数据编译", test_json_compile()))
    results.append(("JSON 文件编译", test_json_file_compile()))
    
    # 显示结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{name}: {status}")
    
    # 统计
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("\n⚠️ 部分测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
