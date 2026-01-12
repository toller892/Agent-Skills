#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文解析器 - 五阶段工作流
将论文链接转换为图文并茂的PDF和HTML文档
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path
from datetime import datetime
from fpdf import FPDF
import re

# 尝试加载 .env 文件（如果存在）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # 如果没有安装 python-dotenv，跳过


class PaperInterpreter:
    """论文解析器 - 五阶段工作流"""
    
    def __init__(self, output_dir="paper_output"):
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.setup_directories()
        
        # 配置 Nano Banana API
        self.nano_banana_token = os.getenv("NANO_BANANA_TOKEN", "")
        
    def setup_directories(self):
        """创建必要的目录"""
        self.output_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
    
    # ========== 阶段1: 信息获取 ==========
    
    def fetch_paper_info(self, url):
        """
        阶段1: 信息获取
        - WebFetch: 抓取 arXiv 摘要页
        - WebSearch: 搜索补充技术细节
        - WebFetch: 获取技术博客深度解读
        """
        print("\n" + "="*60)
        print("阶段1: 信息获取")
        print("="*60)
        
        paper_info = {
            'url': url,
            'title': '',
            'abstract': '',
            'content': '',
            'sections': []
        }
        
        try:
            # 确保URL以.pdf结尾
            if not url.endswith('.pdf'):
                url = url + '.pdf'
                print(f"自动添加.pdf后缀: {url}")
            
            # 下载PDF
            print(f"正在下载论文: {url}")
            print("(这可能需要10-30秒，请耐心等待...)")
            
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()
            
            # 显示下载进度
            total_size = int(response.headers.get('content-length', 0))
            print(f"文件大小: {total_size / 1024 / 1024:.2f} MB")
            
            pdf_path = self.output_dir / "paper.pdf"
            downloaded = 0
            
            with open(pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r下载进度: {progress:.1f}%", end='', flush=True)
            
            print()  # 换行
            paper_info['pdf_path'] = str(pdf_path)
            print(f"✓ 论文已下载到: {pdf_path}")
            
            # 提取arXiv ID和标题（从URL）
            if 'arxiv.org' in url:
                arxiv_id = url.split('/')[-1].replace('.pdf', '')
                paper_info['arxiv_id'] = arxiv_id
                paper_info['title'] = f"arXiv:{arxiv_id}"
                print(f"✓ arXiv ID: {arxiv_id}")
            
        except Exception as e:
            print(f"✗ 下载失败: {e}")
            return None
        
        return paper_info

    # ========== 阶段2: 文章生成 ==========
    
    def generate_article(self, paper_info):
        """
        阶段2: 文章生成
        黄叔风格量化标准:
        - 类比密度 ≥1个/400字
        - 第二人称"你" >30%
        - 三层递进解释结构
        - Write: 输出 Markdown 文件
        """
        print("\n" + "="*60)
        print("阶段2: 文章生成 (黄叔风格)")
        print("="*60)
        
        # 这里应该调用Claude API或其他LLM来生成文章
        # 为了演示，我们创建一个模板
        
        title = paper_info.get('title', '论文解读')
        
        markdown = f"""# {title}

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📌 核心观点

你有没有想过，这篇论文到底在解决什么问题？

让我用一个类比来解释：就像你在黑暗中找钥匙，传统方法是一个个摸索，而这篇论文提出的方法，就像是打开了一盏灯。

## 🎯 三层递进解释

### 第一层：是什么？

这篇论文提出了一个新方法。简单来说，它就是...

### 第二层：为什么重要？

你可能会问，为什么我们需要这个方法？

想象一下，你在处理大量数据时...

### 第三层：怎么做到的？

具体实现上，论文采用了三个关键技术：

1. **技术点1**: 就像...
2. **技术点2**: 类似于...
3. **技术点3**: 可以理解为...

## 💡 关键洞察

你会发现，这个方法的精妙之处在于...

## 🔮 未来展望

这项研究为你打开了新的可能性...

---

*本文采用黄叔风格撰写，注重类比和第二人称叙述*
"""
        
        # 保存Markdown
        md_path = self.output_dir / f"{paper_info.get('arxiv_id', 'paper')}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"✓ Markdown已生成: {md_path}")
        
        paper_info['markdown'] = markdown
        paper_info['markdown_path'] = str(md_path)
        
        return paper_info

    # ========== 阶段3: 配图生成 ==========
    
    def generate_illustrations(self, paper_info):
        """
        阶段3: 配图生成
        API: Nano Banana (Gemini 2.0 Flash)
        风格: 纽约客杂志极简插画
        - 3-4色 muted 配色
        - 中世纪现代美学
        - 无文字标注
        - Base64解码保存PNG
        """
        print("\n" + "="*60)
        print("阶段3: 配图生成 (纽约客风格 - Nano Banana)")
        print("="*60)
        
        # 检查是否配置了Token
        if not self.nano_banana_token:
            print("⚠️  未配置 NANO_BANANA_TOKEN")
            print("跳过插画生成，继续后续流程...")
            paper_info['illustrations'] = []
            return paper_info
        
        # 从Markdown提取需要配图的章节
        markdown = paper_info.get('markdown', '')
        sections = re.findall(r'## (.+)', markdown)
        
        illustrations = []
        
        print(f"准备生成 {min(len(sections), 4)} 张插画...")
        print("(每张图片约需10-30秒，总计可能需要1-2分钟)")
        
        for i, section in enumerate(sections[:4], 1):  # 最多4张图
            print(f"\n[{i}/4] 正在生成插画: {section}")
            
            # 构建prompt - 纽约客风格
            prompt = f"""Create a minimalist New Yorker magazine style illustration for: {section}

Style requirements:
- Use only 3-4 muted colors: #FDFBF7 (cream), #7D9B76 (olive green), #C4785A (terracotta), #E8E4DD (light gray)
- Mid-century modern aesthetic with clean geometric shapes
- Simple, conceptual, and metaphorical representation
- Lots of negative space and clean lines
- NO text, labels, or annotations
- Flat design with subtle shadows
- Abstract and minimalist composition"""
            
            try:
                # 调用Nano Banana API
                image_data = self._call_nano_banana_api(prompt)
                if image_data:
                    # 保存图片
                    img_filename = f"illustration_{i:02d}.png"
                    img_path = self.images_dir / img_filename
                    
                    with open(img_path, 'wb') as f:
                        f.write(image_data)
                    
                    illustrations.append({
                        'section': section,
                        'filename': img_filename,
                        'path': str(img_path)
                    })
                    
                    print(f"  ✓ 插画已保存: {img_filename}")
                else:
                    print(f"  ⚠ 图片生成失败，跳过")
                    
            except Exception as e:
                print(f"  ✗ 生成失败: {e}")
        
        print(f"\n✓ 完成插画生成: {len(illustrations)}/4 张成功")
        paper_info['illustrations'] = illustrations
        return paper_info
    
    def _call_nano_banana_api(self, prompt):
        """调用Nano Banana API生成图片"""
        try:
            # Nano Banana API endpoint
            url = "https://api.nanobanana.ai/v1/images/generations"
            
            headers = {
                "Authorization": f"Bearer {self.nano_banana_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gemini-2.0-flash-exp",  # 或其他支持的模型
                "prompt": prompt,
                "n": 1,  # 生成1张图片
                "size": "1024x1024",  # 图片尺寸
                "response_format": "b64_json"  # Base64格式
            }
            
            print(f"  调用Nano Banana API...")
            print(f"  (图片生成可能需要10-30秒，请耐心等待...)")
            
            response = requests.post(url, headers=headers, json=payload, timeout=90)
            
            print(f"  API响应状态: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            
            # 从Base64解码图片
            if 'data' in result and len(result['data']) > 0:
                b64_image = result['data'][0].get('b64_json', '')
                if b64_image:
                    image_data = base64.b64decode(b64_image)
                    print(f"  ✓ 图片生成成功 ({len(image_data)} bytes)")
                    return image_data
                else:
                    print(f"  ⚠ 响应中没有b64_json字段")
            else:
                print(f"  ⚠ 响应中没有data字段")
            
            print(f"  API响应格式: {list(result.keys())}")
            return None
            
        except requests.exceptions.Timeout:
            print(f"  ✗ API请求超时（90秒）")
            return None
        except requests.exceptions.RequestException as e:
            print(f"  ✗ API请求失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"  错误详情: {error_detail}")
                except:
                    print(f"  响应内容: {e.response.text[:200]}")
            return None
        except Exception as e:
            print(f"  ✗ 处理失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    # ========== 阶段4: HTML生成 ==========
    
    def generate_html(self, paper_info):
        """
        阶段4: HTML生成
        2026前沿设计规范:
        - 暖调 Muted 配色 (#FDFBF7, #7D9B76, #C4785A...)
        - Noto Serif SC + Inter 字体
        - Intersection Observer 滚动动画
        Write: 输出完整 HTML 文件
        """
        print("\n" + "="*60)
        print("阶段4: HTML生成 (2026前沿设计)")
        print("="*60)
        
        markdown = paper_info.get('markdown', '')
        illustrations = paper_info.get('illustrations', [])
        title = paper_info.get('title', '论文解读')
        
        # 将Markdown转换为HTML内容
        html_content = self._markdown_to_html(markdown, illustrations)
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <!-- 2026前沿字体 -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            /* 2026 Muted 暖调配色 */
            --color-bg: #FDFBF7;
            --color-primary: #7D9B76;
            --color-accent: #C4785A;
            --color-text: #2C2C2C;
            --color-text-light: #6B6B6B;
            --color-border: #E8E4DD;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Serif SC', serif;
            background: var(--color-bg);
            color: var(--color-text);
            line-height: 1.8;
            font-size: 18px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 60px 40px;
        }}
        
        h1 {{
            font-family: 'Inter', sans-serif;
            font-size: 3em;
            font-weight: 700;
            color: var(--color-primary);
            margin-bottom: 0.5em;
            letter-spacing: -0.02em;
        }}
        
        h2 {{
            font-family: 'Inter', sans-serif;
            font-size: 2em;
            font-weight: 600;
            color: var(--color-accent);
            margin-top: 2em;
            margin-bottom: 0.8em;
            letter-spacing: -0.01em;
        }}
        
        h3 {{
            font-family: 'Inter', sans-serif;
            font-size: 1.5em;
            font-weight: 500;
            color: var(--color-primary);
            margin-top: 1.5em;
            margin-bottom: 0.6em;
        }}
        
        p {{
            margin-bottom: 1.2em;
            text-align: justify;
        }}
        
        blockquote {{
            border-left: 4px solid var(--color-primary);
            padding-left: 1.5em;
            margin: 2em 0;
            color: var(--color-text-light);
            font-style: italic;
        }}
        
        .illustration {{
            margin: 3em 0;
            text-align: center;
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }}
        
        .illustration.visible {{
            opacity: 1;
            transform: translateY(0);
        }}
        
        .illustration img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }}
        
        .meta {{
            font-family: 'Inter', sans-serif;
            font-size: 0.9em;
            color: var(--color-text-light);
            margin-bottom: 3em;
            padding-bottom: 1em;
            border-bottom: 1px solid var(--color-border);
        }}
        
        hr {{
            border: none;
            border-top: 1px solid var(--color-border);
            margin: 3em 0;
        }}
        
        ul, ol {{
            margin-left: 2em;
            margin-bottom: 1.2em;
        }}
        
        li {{
            margin-bottom: 0.5em;
        }}
        
        strong {{
            color: var(--color-accent);
            font-weight: 600;
        }}
        
        /* 滚动动画 */
        .fade-in {{
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }}
        
        .fade-in.visible {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
    
    <script>
        // Intersection Observer 滚动动画
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, observerOptions);
        
        // 观察所有插画和段落
        document.querySelectorAll('.illustration, .fade-in').forEach(el => {{
            observer.observe(el);
        }});
    </script>
</body>
</html>
"""
        
        # 保存HTML
        html_path = self.output_dir / "index.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ HTML已生成: {html_path}")
        
        paper_info['html_path'] = str(html_path)
        return paper_info
    
    def _markdown_to_html(self, markdown, illustrations):
        """将Markdown转换为HTML，并插入插画"""
        lines = markdown.split('\n')
        html_lines = []
        illustration_index = 0
        
        for line in lines:
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                # 在每个二级标题前插入插画
                if illustration_index < len(illustrations):
                    ill = illustrations[illustration_index]
                    if not ill.get('placeholder'):
                        html_lines.append(f'<div class="illustration"><img src="images/{ill["filename"]}" alt="{ill["section"]}"></div>')
                    illustration_index += 1
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('> '):
                html_lines.append(f'<blockquote>{line[2:]}</blockquote>')
            elif line.startswith('- ') or line.startswith('* '):
                html_lines.append(f'<li>{line[2:]}</li>')
            elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
                html_lines.append(f'<li>{line[3:]}</li>')
            elif line.strip() == '':
                html_lines.append('<br>')
            elif line.strip() == '---':
                html_lines.append('<hr>')
            else:
                # 处理粗体
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                html_lines.append(f'<p class="fade-in">{line}</p>')
        
        return '\n'.join(html_lines)

    # ========== 阶段5: PDF生成 ==========
    
    def generate_pdf(self, paper_info):
        """
        阶段5: PDF生成
        - 调用 generate_pdf.py 脚本
        - fpdf2 库生成原生 PDF (非 HTML 转换)
        - 中文字体: STHeiti
        """
        print("\n" + "="*60)
        print("阶段5: PDF生成 (fpdf2原生)")
        print("="*60)
        
        try:
            markdown = paper_info.get('markdown', '')
            illustrations = paper_info.get('illustrations', [])
            title = paper_info.get('title', '论文解读')
            
            # 创建PDF
            pdf = FPDF()
            pdf.add_page()
            
            # 设置中文字体（需要先下载STHeiti字体）
            # pdf.add_font('STHeiti', '', 'STHeiti.ttf', uni=True)
            # pdf.set_font('STHeiti', '', 12)
            
            # 使用内置字体作为fallback
            pdf.set_font('Arial', 'B', 24)
            
            # 标题
            pdf.cell(0, 20, title.encode('latin-1', 'ignore').decode('latin-1'), ln=True, align='C')
            
            pdf.set_font('Arial', '', 12)
            pdf.ln(10)
            
            # 处理Markdown内容
            lines = markdown.split('\n')
            illustration_index = 0
            
            for line in lines:
                if line.startswith('# '):
                    pdf.set_font('Arial', 'B', 20)
                    pdf.multi_cell(0, 10, line[2:].encode('latin-1', 'ignore').decode('latin-1'))
                    pdf.ln(5)
                elif line.startswith('## '):
                    # 插入插画
                    if illustration_index < len(illustrations):
                        ill = illustrations[illustration_index]
                        if not ill.get('placeholder') and Path(ill['path']).exists():
                            try:
                                pdf.image(ill['path'], x=30, w=150)
                                pdf.ln(5)
                            except:
                                pass
                        illustration_index += 1
                    
                    pdf.set_font('Arial', 'B', 16)
                    pdf.multi_cell(0, 10, line[3:].encode('latin-1', 'ignore').decode('latin-1'))
                    pdf.ln(3)
                elif line.startswith('### '):
                    pdf.set_font('Arial', 'B', 14)
                    pdf.multi_cell(0, 8, line[4:].encode('latin-1', 'ignore').decode('latin-1'))
                    pdf.ln(2)
                elif line.strip() and not line.startswith('>') and not line.startswith('*'):
                    pdf.set_font('Arial', '', 11)
                    # 移除Markdown格式
                    clean_line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
                    pdf.multi_cell(0, 6, clean_line.encode('latin-1', 'ignore').decode('latin-1'))
                    pdf.ln(2)
            
            # 保存PDF
            pdf_filename = f"{paper_info.get('arxiv_id', 'paper')}.pdf"
            pdf_path = self.output_dir / pdf_filename
            pdf.output(str(pdf_path))
            
            print(f"✓ PDF已生成: {pdf_path}")
            
            paper_info['output_pdf_path'] = str(pdf_path)
            
        except Exception as e:
            print(f"✗ PDF生成失败: {e}")
            print("提示: 如需完整中文支持，请配置STHeiti字体")
        
        return paper_info

    # ========== 主流程 ==========
    
    def process_paper(self, url):
        """完整的五阶段工作流"""
        print("\n" + "🚀 "*20)
        print("论文解析器 - 五阶段工作流启动")
        print("🚀 "*20)
        
        # 阶段1: 信息获取
        paper_info = self.fetch_paper_info(url)
        if not paper_info:
            print("\n❌ 信息获取失败")
            return False
        
        # 阶段2: 文章生成
        paper_info = self.generate_article(paper_info)
        
        # 阶段3: 配图生成
        paper_info = self.generate_illustrations(paper_info)
        
        # 阶段4: HTML生成
        paper_info = self.generate_html(paper_info)
        
        # 阶段5: PDF生成
        paper_info = self.generate_pdf(paper_info)
        
        # 生成日志
        self._save_log(paper_info)
        
        print("\n" + "="*60)
        print("✅ 所有阶段完成!")
        print("="*60)
        print(f"\n📁 输出目录: {self.output_dir.absolute()}")
        print(f"\n生成文件:")
        print(f"  - {paper_info.get('markdown_path', 'N/A')}")
        print(f"  - {paper_info.get('html_path', 'N/A')}")
        print(f"  - {paper_info.get('output_pdf_path', 'N/A')}")
        print(f"  - {len(paper_info.get('illustrations', []))} 张插画")
        print()
        
        return True
    
    def _save_log(self, paper_info):
        """保存处理日志"""
        log_content = f"""论文解析日志
{'='*60}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
论文URL: {paper_info.get('url', 'N/A')}
arXiv ID: {paper_info.get('arxiv_id', 'N/A')}

阶段1: 信息获取 ✓
阶段2: 文章生成 ✓
阶段3: 配图生成 ✓ ({len(paper_info.get('illustrations', []))} 张)
阶段4: HTML生成 ✓
阶段5: PDF生成 ✓

输出文件:
- Markdown: {paper_info.get('markdown_path', 'N/A')}
- HTML: {paper_info.get('html_path', 'N/A')}
- PDF: {paper_info.get('output_pdf_path', 'N/A')}

插画列表:
"""
        for ill in paper_info.get('illustrations', []):
            log_content += f"  - {ill['filename']}: {ill['section']}\n"
        
        log_path = self.output_dir / f"{paper_info.get('arxiv_id', 'paper')}_log.txt"
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        print(f"✓ 日志已保存: {log_path}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python paper_interpreter.py <论文URL>")
        print("示例: python paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf")
        print("\n环境变量:")
        print("  NANO_BANANA_TOKEN - Nano Banana API Token（必需，用于生成插画）")
        print("\n配置方法:")
        print("  export NANO_BANANA_TOKEN='your_token_here'")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 检查Token
    if not os.getenv("NANO_BANANA_TOKEN"):
        print("\n⚠️  警告: 未设置 NANO_BANANA_TOKEN")
        print("将跳过插画生成，只生成Markdown、HTML和PDF")
        print("\n如需生成插画，请设置环境变量:")
        print("  export NANO_BANANA_TOKEN='your_token_here'")
        print()
    
    # 创建解析器
    interpreter = PaperInterpreter()
    
    # 处理论文
    success = interpreter.process_paper(url)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
