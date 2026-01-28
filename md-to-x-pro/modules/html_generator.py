#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML生成器模块
生成精美的响应式HTML页面，专门为Twitter分享优化
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def markdown_to_html(text: str) -> str:
    """
    将简单的Markdown格式转换为HTML

    支持的格式:
    - **加粗**: **text** -> <strong>text</strong>
    - *斜体*: *text* -> <em>text</em>
    - `代码`: `code` -> <code>code</code>
    - [链接](url): [text](url) -> <a href="url">text</a>
    - 换行符: \n -> <br>
    """
    if not text:
        return ""

    # 转义HTML特殊字符（除了我们要添加的标签）
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')

    # 处理代码块 `code`（在处理其他格式之前）
    def code_repl(match):
        code = match.group(1)
        return f'<code style="background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; color: #e83e8c;">{code}</code>'
    text = re.sub(r'`([^`]+)`', code_repl, text)

    # 处理加粗 **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # 处理斜体 *text*
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # 处理链接 [text](url)
    def link_repl(match):
        link_text = match.group(1)
        url = match.group(2)
        return f'<a href="{url}" target="_blank" style="color: #667eea; text-decoration: underline;">{link_text}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, text)

    # 处理换行符（将单个换行转换为<br>，但保留段落分隔）
    text = text.replace('\n\n', '</p><p>')
    text = text.replace('\n', '<br>')

    return text


@dataclass
class HTMLCardConfig:
    """HTML卡片配置类"""

    width: int = 1200
    height: int = 630
    title_color: str = "#1a1a2e"
    accent_color: str = "#e94560"
    gradient_start: str = "#667eea"
    gradient_end: str = "#764ba2"
    font_family: str = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    background_color: str = "#f8f9fa"


class HTMLGenerator:
    """HTML生成器主类"""

    def __init__(self):
        self.config = HTMLCardConfig()
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """加载HTML模板"""
        return {
            "base": self._get_base_template(),
            "card": self._get_card_template(),
            "styles": self._get_css_styles(),
            "script": self._get_javascript(),
        }

    def generate_twitter_cards(
        self, card_data: Dict, output_dir: str = "output"
    ) -> List[str]:
        """
        生成4张Twitter卡片

        Args:
            card_data: 卡片数据
            output_dir: 输出目录

        Returns:
            List[str]: 生成的HTML文件路径列表
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        generated_files = []
        total_cards = card_data.get("total_cards", 4)

        for i in range(total_cards):
            card_number = i + 1

            # 安全获取图片路径
            image_paths = card_data.get("image_paths") or []
            image_path = image_paths[i] if i < len(image_paths) else None

            # 构建单张卡片的数据
            single_card_data = {
                "card_number": card_number,
                "total_cards": total_cards,
                "title": card_data.get("title", ""),
                "subtitle": f"第 {card_number} 部分 / 共 {total_cards} 部分"
                if total_cards > 1
                else None,
                "sections": card_data.get("sections", []),
                "keywords": card_data.get("keywords", []),
                "summary": card_data.get("summary") if card_number == 1 else None,
                "image_path": image_path,
                "has_images": bool(image_path),
            }

            # 生成HTML
            html_content = self._generate_card_html(single_card_data)

            # 保存文件
            output_file = output_path / f"beautiful_content_{card_number}.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            generated_files.append(str(output_file))
            logger.info(f"生成卡片 {card_number}: {output_file}")

        return generated_files

    def _generate_card_html(self, card_data: Dict) -> str:
        """生成单张卡片的HTML"""
        # 转换标题的Markdown格式
        title_html = markdown_to_html(card_data.get("title", ""))

        # 安全获取描述内容
        desc_content = card_data.get("summary")
        if not desc_content and card_data.get("sections"):
            desc_content = card_data["sections"][0].get("content", "")[:150]
        if not desc_content:
            desc_content = card_data.get("title", "")[:150]

        # 转换摘要（如果存在）
        summary_html = markdown_to_html(card_data.get("summary", "")) if card_data.get("summary") else ""

        # 处理图片路径 - 使用相对路径
        image_path = card_data.get("image_path", "")
        if image_path:
            # 如果是绝对路径，转换为相对路径
            from pathlib import Path as Pathlib
            path_obj = Pathlib(image_path)
            if path_obj.is_absolute():
                # 提取文件名并使用相对路径
                image_path = f"images/{path_obj.name}"

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{card_data["title"]} - 第 {card_data["card_number"]} 部分">
    <meta property="og:description" content="{desc_content}...">
    <meta property="og:image" content="{image_path}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{card_data["title"]} - 第 {card_data["card_number"]} 部分">
    <meta name="twitter:description" content="{desc_content}...">
    <meta name="twitter:image" content="{image_path}">
    <title>{card_data["title"]} - 第 {card_data["card_number"]} 部分</title>
    <style>
{self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <div class="brand">
                    <span class="brand-icon">✨</span>
                    <span class="brand-text">内容精选</span>
                </div>
                <div class="card-badge">{card_data["card_number"]} / {card_data["total_cards"]}</div>
            </div>

            <div class="card-body">
                <h1 class="card-title">{title_html}</h1>
                {f'<p class="card-subtitle">{card_data["subtitle"]}</p>' if card_data.get("subtitle") else ""}

                {f'<div class="summary-box">{summary_html}</div>' if summary_html else ""}
"""

        # 添加图片（如果有）
        if image_path and card_data["has_images"]:
            html += f"""
                <div class="image-container">
                    <img src="{image_path}" alt="配图" class="card-image" onerror="this.style.display='none'">
                </div>
"""

        # 添加章节内容
        for section in card_data.get("sections", []):
            # 转换Markdown格式为HTML
            title_html = markdown_to_html(section["title"])
            content_html = markdown_to_html(section["content"])

            html += f"""
                <div class="content-section">
                    <h2 class="section-title">{title_html}</h2>
                    <div class="section-content">{content_html}</div>
                </div>
"""

        # 添加关键词标签
        if card_data.get("keywords"):
            keywords_html = "".join(
                [
                    f'<span class="keyword-tag">{kw}</span>'
                    for kw in card_data["keywords"][:5]
                ]
            )
            html += f"""
                <div class="keywords-section">
                    {keywords_html}
                </div>
"""

        html += f"""
            </div>
            
            <div class="card-footer">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {(card_data["card_number"] / card_data["total_cards"]) * 100}%"></div>
                </div>
                <div class="footer-text">
                    {card_data["card_number"]} / {card_data["total_cards"]} 部分完成
                </div>
            </div>
        </div>
    </div>
    
    <script>
{self._get_javascript()}
    </script>
</body>
</html>
"""
        return html

    def _generate_tweet_style_card(self, card_data: Dict) -> str:
        """生成推文风格的卡片HTML"""

        # 处理图片路径 - 使用相对路径
        image_path = card_data.get("image_path", "")
        if image_path:
            from pathlib import Path as Pathlib
            path_obj = Pathlib(image_path)
            if path_obj.is_absolute():
                image_path = f"images/{path_obj.name}"

        # 获取key_points并转为HTML
        key_points_html = ""
        for point in card_data.get("key_points", []):
            key_points_html += f'<li class="key-point">{point}</li>\n'

        # 获取hashtags
        hashtags_html = " ".join(card_data.get("hashtags", []))

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{card_data.get('title', '')}">
    <meta property="og:description" content="{card_data.get('insight', '')[:200]}">
    <meta property="og:image" content="{image_path}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{card_data.get('title', '')}">
    <meta name="twitter:description" content="{card_data.get('insight', '')[:200]}">
    <meta name="twitter:image" content="{image_path}">
    <title>{card_data.get('title', '')}</title>
    <style>
{self._get_tweet_style_css()}
    </style>
</head>
<body>
    <div class="tweet-container">
        <div class="tweet-card">
            <!-- 卡片头部 -->
            <div class="tweet-header">
                <div class="tweet-number">{card_data["card_number"]}/{card_data["total_cards"]}</div>
                <div class="tweet-badge">📱 精选内容</div>
            </div>

            <!-- 主标题 -->
            <div class="tweet-title-section">
                <h1 class="tweet-title">{card_data.get('title', '')}</h1>
                {f'<p class="tweet-subtitle">{card_data.get("subtitle", "")}</p>' if card_data.get("subtitle") else ""}
            </div>

            <!-- 配图 -->
            {f'''<div class="tweet-image">
                <img src="{image_path}" alt="配图" onerror="this.parentElement.style.display='none'">
            </div>''' if image_path and card_data.get("has_images") else ""}

            <!-- 核心要点 -->
            <div class="tweet-content">
                <ul class="key-points-list">
                    {key_points_html}
                </ul>
            </div>

            <!-- 洞察金句 -->
            <div class="tweet-insight">
                <span class="insight-icon">💡</span>
                <span class="insight-text">{card_data.get('insight', '')}</span>
            </div>

            <!-- 话题标签 -->
            <div class="tweet-footer">
                <div class="tweet-hashtags">{hashtags_html}</div>
            </div>
        </div>
    </div>

    <script>
{self._get_tweet_style_js()}
    </script>
</body>
</html>
"""
        return html

    def _get_css_styles(self) -> str:
        """获取CSS样式"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            color: white;
            font-weight: 600;
        }
        
        .brand-icon {
            font-size: 24px;
        }
        
        .card-badge {
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            color: white;
            font-weight: 600;
            font-size: 14px;
        }
        
        .card-body {
            padding: 40px;
        }
        
        .card-title {
            font-size: 2.5em;
            color: #1a1a2e;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .card-subtitle {
            font-size: 1.2em;
            color: #666;
            margin-bottom: 30px;
        }
        
        .summary-box {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
            font-size: 1.1em;
            color: #333;
            line-height: 1.8;
        }
        
        .image-container {
            margin: 30px 0;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .card-image {
            width: 100%;
            height: auto;
            display: block;
        }
        
        .content-section {
            margin: 30px 0;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 15px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .content-section:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .section-title {
            font-size: 1.5em;
            color: #e94560;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-title::before {
            content: '📌';
            font-size: 0.8em;
        }
        
        .section-content {
            color: #444;
            line-height: 1.9;
            font-size: 1.05em;
        }
        
        .keywords-section {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
        }
        
        .keyword-tag {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
            transition: transform 0.3s ease;
        }
        
        .keyword-tag:hover {
            transform: scale(1.05);
        }
        
        .card-footer {
            padding: 20px 40px;
            background: #f8f9fa;
        }
        
        .progress-bar {
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
            transition: width 0.5s ease;
        }
        
        .footer-text {
            text-align: right;
            color: #888;
            font-size: 0.9em;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .card-body {
                padding: 25px;
            }
            
            .card-title {
                font-size: 1.8em;
            }
            
            .section-title {
                font-size: 1.3em;
            }
            
            .content-section {
                padding: 20px;
            }
        }
        
        /* 动画效果 */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .content-section {
            animation: fadeIn 0.5s ease-out;
        }
        
        .content-section:nth-child(2) { animation-delay: 0.1s; }
        .content-section:nth-child(3) { animation-delay: 0.2s; }
        .content-section:nth-child(4) { animation-delay: 0.3s; }
        """

    def _get_base_template(self) -> str:
        """获取基础HTML模板"""
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
            {styles}
            </style>
        </head>
        <body>
            {content}
        </body>
        </html>
        """

    def _get_card_template(self) -> str:
        """获取卡片模板"""
        return """
        <div class="card">
            <div class="card-header">
                <div class="brand">
                    <span class="brand-icon">✨</span>
                    <span class="brand-text">内容精选</span>
                </div>
                <div class="card-badge">{card_number} / {total_cards}</div>
            </div>
            <div class="card-body">
                {body_content}
            </div>
            <div class="card-footer">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
            </div>
        </div>
        """

    def _get_javascript(self) -> str:
        """获取JavaScript代码"""
        return """
        // 添加交互效果
        document.addEventListener('DOMContentLoaded', function() {
            // 为所有内容区块添加悬停效果
            const sections = document.querySelectorAll('.content-section');
            sections.forEach((section, index) => {
                section.style.animationDelay = `${index * 0.1}s`;
            });
            
            // 添加滚动动画
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, {
                threshold: 0.1
            });
            
            sections.forEach(section => {
                observer.observe(section);
            });
        });
        
        // 分享功能
        function shareCard() {
            if (navigator.share) {
                navigator.share({
                    title: document.title,
                    url: window.location.href
                });
            } else {
                // 复制链接到剪贴板
                navigator.clipboard.writeText(window.location.href);
                alert('链接已复制到剪贴板！');
            }
        }
        """

    def generate_standalone_page(
        self, card_data: Dict, output_path: str = "beautiful_content.html"
    ):
        """
        生成独立HTML页面

        Args:
            card_data: 卡片数据
            output_path: 输出路径
        """
        # 合并所有卡片内容
        full_content = []

        for i in range(card_data.get("total_cards", 1)):
            single_card_data = {
                "card_number": i + 1,
                "total_cards": card_data.get("total_cards", 1),
                "title": card_data.get("title", ""),
                "subtitle": f"第 {i + 1} 部分 / 共 {card_data.get('total_cards', 1)} 部分",
                "sections": card_data.get("sections", []),
                "keywords": card_data.get("keywords", []),
                "summary": card_data.get("summary") if i == 0 else None,
                "image_path": card_data.get("image_paths", [])[i]
                if card_data.get("image_paths")
                else None,
                "has_images": bool(card_data.get("image_paths")),
            }

            full_content.append(self._generate_card_html(single_card_data))

        # 生成完整页面
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{card_data.get("title", "精美内容")}</title>
    <style>
{self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        {" ".join(full_content)}
    </div>
    
    <script>
{self._get_javascript()}
    </script>
</body>
</html>
"""
        # 保存文件
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        logger.info(f"生成完整页面: {output_file}")
        return str(output_file)

    def _get_tweet_style_css(self) -> str:
        """获取推文风格的CSS样式"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            min-height: 100vh;
            padding: 40px 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .tweet-container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }

        .tweet-card {
            background: #ffffff;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .tweet-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .tweet-number {
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 14px;
            backdrop-filter: blur(10px);
        }

        .tweet-badge {
            background: rgba(255, 255, 255, 0.25);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
            backdrop-filter: blur(10px);
        }

        .tweet-title-section {
            padding: 32px 28px 24px;
        }

        .tweet-title {
            font-size: 28px;
            font-weight: 800;
            color: #1a1a2e;
            line-height: 1.3;
            margin-bottom: 12px;
        }

        .tweet-subtitle {
            font-size: 16px;
            color: #6b7280;
            font-weight: 500;
        }

        .tweet-image {
            width: 100%;
            height: 320px;
            overflow: hidden;
            background: #f3f4f6;
        }

        .tweet-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .tweet-image:hover img {
            transform: scale(1.05);
        }

        .tweet-content {
            padding: 28px;
        }

        .key-points-list {
            list-style: none;
        }

        .key-point {
            font-size: 17px;
            line-height: 1.7;
            color: #374151;
            margin-bottom: 14px;
            padding-left: 28px;
            position: relative;
        }

        .key-point:before {
            content: "▸";
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
            font-size: 20px;
        }

        .tweet-insight {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 20px 24px;
            margin: 0 28px 24px;
            border-radius: 16px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            border-left: 4px solid #f59e0b;
        }

        .insight-icon {
            font-size: 24px;
            flex-shrink: 0;
        }

        .insight-text {
            font-size: 16px;
            font-weight: 600;
            color: #92400e;
            line-height: 1.5;
        }

        .tweet-footer {
            background: #f9fafb;
            padding: 20px 28px;
            border-top: 1px solid #e5e7eb;
        }

        .tweet-hashtags {
            font-size: 15px;
            color: #667eea;
            font-weight: 600;
        }

        @media (max-width: 768px) {
            body {
                padding: 20px 12px;
            }

            .tweet-title {
                font-size: 24px;
            }

            .key-point {
                font-size: 16px;
            }

            .tweet-image {
                height: 240px;
            }
        }
        """

    def _get_tweet_style_js(self) -> str:
        """获取推文风格的JavaScript"""
        return """
        document.addEventListener('DOMContentLoaded', function() {
            // 添加滚动效果
            const tweetCard = document.querySelector('.tweet-card');
            tweetCard.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px)';
                this.style.transition = 'transform 0.3s ease';
            });

            tweetCard.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });

            // 为关键点添加淡入动画
            const keyPoints = document.querySelectorAll('.key-point');
            keyPoints.forEach((point, index) => {
                point.style.opacity = '0';
                point.style.animation = `fadeInUp 0.5s ease ${index * 0.1}s forwards`;
            });
        });

        // 添加淡入动画
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(style);
        """


class SocialMediaOptimizer:
    """社交媒体优化器"""

    @staticmethod
    def generate_twitter_meta(card_data: Dict, base_url: str = "") -> Dict:
        """
        生成Twitter分享所需的Meta标签

        Args:
            card_data: 卡片数据
            base_url: 基础URL

        Returns:
            Dict: Meta标签字典
        """
        return {
            "twitter:card": "summary_large_image",
            "twitter:title": f"{card_data.get('title', '内容')} - 第 {card_data.get('card_number', 1)} 部分",
            "twitter:description": card_data.get(
                "summary", card_data.get("sections", [{}])[0].get("content", "")[:200]
            ),
            "twitter:image": f"{base_url}/images/{card_data.get('card_number', 1)}.png",
            "og:title": f"{card_data.get('title', '内容')} - 第 {card_data.get('card_number', 1)} 部分",
            "og:description": card_data.get(
                "summary", card_data.get("sections", [{}])[0].get("content", "")[:200]
            ),
            "og:image": f"{base_url}/images/{card_data.get('card_number', 1)}.png",
            "og:type": "article",
        }

    @staticmethod
    def generate_hashtags(keywords: List[str]) -> str:
        """
        生成话题标签

        Args:
            keywords: 关键词列表

        Returns:
            str: 话题标签字符串
        """
        hashtags = [f"#{kw.replace(' ', '')}" for kw in keywords[:5]]
        return " ".join(hashtags)


# 测试代码
if __name__ == "__main__":
    # 测试HTML生成器
    generator = HTMLGenerator()

    # 模拟卡片数据
    test_card_data = {
        "card_number": 1,
        "total_cards": 4,
        "title": "人工智能的未来发展",
        "subtitle": "第 1 部分 / 共 4 部分",
        "summary": "人工智能正在快速发展，改变我们的生活方式。本文探讨AI技术的最新进展和未来趋势。",
        "sections": [
            {
                "title": "引言",
                "content": "人工智能（AI）已经成为了当今科技领域最热门的话题之一。从自动驾驶汽车到智能助手，AI正在以前所未有的速度改变着我们的世界。",
            },
            {
                "title": "当前发展",
                "content": "近年来，深度学习和神经网络技术的突破使得AI在图像识别、自然语言处理等领域取得了显著进展。大型语言模型的出现更是将AI的能力推向了一个新的高度。",
            },
        ],
        "keywords": ["AI", "人工智能", "机器学习", "深度学习", "技术"],
        "image_paths": ["output/images/image_1.png"],
        "has_images": True,
    }

    # 生成测试卡片
    output_files = generator.generate_twitter_cards(test_card_data)

    print("生成的HTML文件:")
    for file in output_files:
        print(f"  - {file}")

    # 生成完整页面
    full_page = generator.generate_standalone_page(
        {**test_card_data, "sections": test_card_data["sections"] * 4},
        "test_full_page.html",
    )
    print(f"完整页面: {full_page}")
