#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 跳过图片生成，快速验证流程
"""

import os
import sys

# 临时清空Token，跳过图片生成
os.environ['NANO_BANANA_TOKEN'] = ''

from paper_interpreter import PaperInterpreter

def main():
    if len(sys.argv) < 2:
        print("使用方法: python quick_test.py <论文URL>")
        print("示例: python quick_test.py https://arxiv.org/pdf/2301.00001.pdf")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print("🚀 快速测试模式")
    print("=" * 60)
    print("注意: 跳过图片生成，只测试其他阶段")
    print("=" * 60)
    
    interpreter = PaperInterpreter(output_dir="quick_test_output")
    success = interpreter.process_paper(url)
    
    if success:
        print("\n✅ 测试成功！")
        print("如需生成图片，请设置 NANO_BANANA_TOKEN 并运行完整版本")
    else:
        print("\n❌ 测试失败")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
