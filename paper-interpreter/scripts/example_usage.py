#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例 - 演示如何使用论文解析器（五阶段工作流）
"""

import os
from paper_interpreter import PaperInterpreter

def example_1_basic_usage():
    """示例1: 基本使用"""
    print("\n" + "="*60)
    print("示例1: 基本使用")
    print("="*60)
    
    # 设置 Nano Banana Token（如果还没设置）
    if not os.getenv("NANO_BANANA_TOKEN"):
        print("\n⚠️  提示: 未设置 NANO_BANANA_TOKEN")
        print("将跳过插画生成，只生成 Markdown、HTML 和 PDF")
        print("\n如需生成插画，请先设置:")
        print("  export NANO_BANANA_TOKEN='your_token_here'")
        print()
    
    # 创建解析器
    interpreter = PaperInterpreter(output_dir="example_output_1")
    
    # 处理论文
    paper_url = "https://arxiv.org/pdf/2301.00001.pdf"
    print(f"\n正在处理论文: {paper_url}")
    
    # 注意: 这会实际下载和处理论文，取消注释以运行
    # interpreter.process_paper(paper_url)
    
    print("\n(示例代码，实际运行请取消注释)")


def example_2_with_token():
    """示例2: 配置Token后使用"""
    print("\n" + "="*60)
    print("示例2: 配置Token后使用")
    print("="*60)
    
    # 在代码中设置 Token（不推荐，仅用于演示）
    # 实际使用时应该用环境变量
    # os.environ['NANO_BANANA_TOKEN'] = 'your_token_here'
    
    interpreter = PaperInterpreter(output_dir="example_output_2")
    
    paper_url = "https://arxiv.org/pdf/2302.00001.pdf"
    print(f"\n正在处理论文: {paper_url}")
    
    # interpreter.process_paper(paper_url)
    
    print("\n(示例代码，实际运行请取消注释)")


def example_3_custom_output():
    """示例3: 自定义输出目录"""
    print("\n" + "="*60)
    print("示例3: 自定义输出目录")
    print("="*60)
    
    # 为每篇论文创建独立目录
    paper_id = "2303.12345"
    output_dir = f"papers/{paper_id}"
    
    interpreter = PaperInterpreter(output_dir=output_dir)
    
    paper_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    print(f"\n输出目录: {output_dir}")
    print(f"论文URL: {paper_url}")
    
    # interpreter.process_paper(paper_url)
    
    print("\n(示例代码，实际运行请取消注释)")


def example_4_batch_processing():
    """示例4: 批量处理多篇论文"""
    print("\n" + "="*60)
    print("示例4: 批量处理多篇论文")
    print("="*60)
    
    papers = [
        "https://arxiv.org/pdf/2301.00001.pdf",
        "https://arxiv.org/pdf/2302.00001.pdf",
        "https://arxiv.org/pdf/2303.00001.pdf",
    ]
    
    for i, paper_url in enumerate(papers, 1):
        print(f"\n处理第 {i}/{len(papers)} 篇论文...")
        
        # 为每篇论文创建独立目录
        arxiv_id = paper_url.split('/')[-1].replace('.pdf', '')
        interpreter = PaperInterpreter(output_dir=f"batch_output/{arxiv_id}")
        
        # interpreter.process_paper(paper_url)
        
        print(f"论文 {i} 处理完成")
    
    print("\n(示例代码，实际运行请取消注释)")


def show_workflow():
    """显示五阶段工作流"""
    print("\n" + "="*60)
    print("五阶段工作流说明")
    print("="*60)
    
    workflow = """
    阶段1: 信息获取 🔍
      └─ 下载PDF + 提取arXiv ID
    
    阶段2: 文章生成 ✍️ (黄叔风格)
      └─ 类比密度 + 第二人称 + 三层递进
    
    阶段3: 配图生成 🎨 (纽约客风格)
      └─ Nano Banana API + 3-4色muted + 极简插画
    
    阶段4: HTML生成 🌐 (2026设计)
      └─ 暖调配色 + Inter/Noto字体 + 滚动动画
    
    阶段5: PDF生成 📑
      └─ fpdf2原生 + 嵌入插画 + 中文支持
    
    输出文件:
      - {arxiv_id}.pdf          # 图文并茂PDF
      - {arxiv_id}.md           # 黄叔风格Markdown
      - {arxiv_id}_log.txt      # 执行日志
      - index.html              # 2026设计HTML
      - images/                 # 纽约客插画
    """
    
    print(workflow)


def main():
    """主函数 - 运行所有示例"""
    print("\n" + "🚀 "*20)
    print("论文解析器 - 使用示例")
    print("🚀 "*20)
    
    # 显示工作流
    show_workflow()
    
    # 选择要运行的示例
    print("\n请选择要运行的示例:")
    print("1. 基本使用")
    print("2. 配置Token后使用")
    print("3. 自定义输出目录")
    print("4. 批量处理多篇论文")
    print("5. 显示工作流说明")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-5): ").strip()
    
    if choice == "1":
        example_1_basic_usage()
    elif choice == "2":
        example_2_with_token()
    elif choice == "3":
        example_3_custom_output()
    elif choice == "4":
        example_4_batch_processing()
    elif choice == "5":
        show_workflow()
    elif choice == "0":
        print("再见!")
    else:
        print("无效选项，请重新运行程序")
    
    print("\n" + "="*60)
    print("提示: 实际运行需要取消示例代码中的注释")
    print("提示: 记得设置 NANO_BANANA_TOKEN 环境变量")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
