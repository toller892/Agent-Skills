---
name: md-to-x-pro
description: 将本地文档转换为精美的图文并茂的HTML页面，支持Twitter分享的4张连贯内容卡片，以及带滚动动画的合并版长页面
author: Tony
version: 2.0.0
tags: [document, html, twitter, social-media, gemini, image-generation, scroll-animation]
requirements:
  - Python 3.8+
  - docling (文档解析)
  - requests (API调用)
  - base64 (图片编码)
capabilities:
  - 读取txt、md、docx格式的本地文档
  - 分析文档内容并提取关键信息
  - 生成精美的响应式HTML页面
  - 使用Gemini API生成配套图片
  - 自动将内容分割为4张连贯的Twitter卡片
  - 生成带滚动动画的合并版长页面
  - 支持API Key配置和提示
permissions:
  - file:read (读取本地文档)
  - file:write (生成HTML文件)
  - network:api (调用Gemini API)
---

# MD to X Pro Skill

这个技能可以将本地文档（txt、md、docx格式）转换为精美的图文并茂HTML页面，专门为Twitter分享优化，生成4张连贯的内容卡片，以及一个带滚动动画效果的合并版长页面。

## 功能特点

✨ **智能文档解析**
- 支持 txt、md、docx 格式
- 自动提取文档结构和关键信息
- 保持原有内容的逻辑层次

🎨 **精美视觉设计**
- 渐变背景和毛玻璃效果（backdrop-filter）
- 响应式布局适配各种屏幕
- 平滑动画和悬停效果
- Twitter卡片优化尺寸 (1200×630px)
- 深色主题配色方案

🖼️ **AI图片生成**
- 使用Gemini API生成配套图片
- 智能根据内容生成相关图像
- 无API Key时自动跳过图片生成
- 支持多种宽高比配置

📱 **Twitter友好**
- 自动分割为4张连贯内容卡片
- 每张卡片包含视觉焦点和吸引元素
- 保持整体叙事的连贯性

🎬 **滚动动画效果（合并版）**
- 卡片滚动进入视口时的淡入上滑动画
- 页面顶部进度条显示阅读进度
- 导航栏滚动时的收缩效果
- 返回顶部按钮（滚动超过500px时显示）
- 导航链接根据当前滚动位置自动高亮

## 使用方法

### 基本用法
```
请使用 md-to-x-pro 技能转换以下文档：
- 文档路径: /path/to/your/document.txt
```

### 高级用法（指定API Key和输出路径）
```
请使用 md-to-x-pro 技能：
- 文档路径: /path/to/your/document.md
- Gemini API Key: your_api_key_here
- 输出路径: /path/to/output
```

### 仅生成文字版本
```
请使用 md-to-x-pro 技能转换文档（不生成图片）：
- 文档路径: /path/to/your/document.docx
- 不需要图片生成
```

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| document_path | string | 是 | 要转换的文档路径 |
| api_key | string | 否 | Gemini API Key，不提供则跳过图片生成 |
| image_aspect_ratio | string | 否 | 图片宽高比，默认16:9，可选1:1、16:9、9:16、4:3 |
| output_dir | string | 否 | 输出目录，默认当前目录 |

## 输出结果

技能将生成：
1. `output/beautiful_content_1.html` - 第1张卡片（执行摘要/概述）
2. `output/beautiful_content_2.html` - 第2张卡片（技术架构/核心内容）
3. `output/beautiful_content_3.html` - 第3张卡片（生态系统/合作伙伴）
4. `output/beautiful_content_4.html` - 第4张卡片（风险展望/总结）
5. `output/beautiful_content_all.html` - **合并版长页面（带滚动动画）**
6. `output/images/` - 生成的图片文件目录（card1.png ~ card4.png）

## 工作流程

```
1. 文档解析
   ↓
2. 内容分析与关键信息提取
   ↓
3. 内容分割（4个部分）
   ↓
4. Gemini API 图片生成（如有API Key）
   ↓
5. 生成4张独立HTML卡片
   ↓
6. 生成合并版HTML（带滚动动画）
   ↓
7. Twitter卡片元数据渲染
```

## 依赖说明

- **docling**: IBM开发的文档解析库，支持多种格式
- **Gemini API**: Google的图像生成API
- **Python标准库**: base64、json、pathlib、re

## 注意事项

⚠️ **API Key安全**
- 建议使用环境变量或安全的密钥管理
- 不要在公开场合分享您的API Key

⚠️ **图片生成**
- 无API Key时只生成文字版本
- 图片生成可能需要几秒钟
- 建议使用16:9或1:1的宽高比

⚠️ **文档格式**
- 确保文档编码为UTF-8
- docx文件需要正确安装python-docx
- 复杂的docx格式可能需要额外处理

## 示例输出

生成的HTML页面包含：
- 精美的渐变标题和毛玻璃效果
- 内容摘要和关键点
- AI生成的配套图片
- 社交媒体优化标签
- 响应式设计适配移动端

### 合并版页面特性
- **固定导航栏**：带毛玻璃效果，滚动时收缩
- **Hero区域**：大标题、副标题、关键数据统计
- **滚动动画**：卡片淡入上滑效果（Intersection Observer）
- **进度条**：页面顶部显示阅读进度
- **返回顶部**：滚动超过500px时显示
- **导航高亮**：根据滚动位置自动高亮当前章节

## 技术实现

### 文档解析
```python
from docling import Document
doc = Document(document_path)
content = doc.get_text()
```

### Gemini API 调用
```python
import requests
import base64

url = f"https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseModalities": ["IMAGE"],
        "imageConfig": {"aspectRatio": "16:9"}
    }
}
```

### 核心CSS样式
```css
/* 深色渐变背景 */
body {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    background-attachment: fixed;
}

/* 毛玻璃卡片 */
.card {
    background: linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    backdrop-filter: blur(10px);
    border-radius: 28px;
}

/* 滚动动画 */
.card {
    opacity: 0;
    transform: translateY(60px);
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.card.visible {
    opacity: 1;
    transform: translateY(0);
}

/* 进度条 */
.progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4, #f472b6);
    z-index: 1001;
}
```

### 核心JavaScript
```javascript
// 滚动动画
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

cards.forEach(card => observer.observe(card));

// 进度条
window.addEventListener('scroll', () => {
    const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.width = scrollPercent + '%';
});

// 导航高亮
window.addEventListener('scroll', () => {
    sections.forEach(section => {
        if (window.scrollY >= section.offsetTop - 200) {
            current = section.getAttribute('id');
        }
    });
    navLinks.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === '#' + current);
    });
});
```

### 配色方案
| 颜色 | 用途 | 色值 |
|------|------|------|
| 紫色 | 主色调/徽章 | #7c3aed |
| 青色 | 强调色/链接 | #06b6d4 |
| 粉色 | 装饰色/徽章 | #f472b6 |
| 绿色 | 成功/正面 | #4ade80 |
| 黄色 | 警告/注意 | #fbbf24 |
| 红色 | 风险/错误 | #ef4444 |

## 故障排除

❓ **问题：文档无法解析**
- 检查文件是否存在
- 确认文件格式是否支持
- 尝试转换为UTF-8编码

❓ **问题：图片生成失败**
- 检查API Key是否正确
- 确认网络连接正常
- 查看API调用限制

❓ **问题：HTML显示异常**
- 检查CSS是否正确加载
- 确认图片路径是否正确
- 尝试在不同浏览器中测试

## 扩展定制

### 自定义CSS样式
可自定义的样式元素：
- **颜色方案**：修改渐变背景和主题色
- **字体设置**：更换字体族和大小
- **动画效果**：调整过渡时间和缓动函数
- **响应式断点**：适配不同屏幕尺寸

### 合并版页面定制
- **导航栏**：修改 `.nav` 样式调整导航外观
- **Hero区域**：修改 `.hero` 样式调整首屏布局
- **卡片动画**：修改 `.card` 的 `transition` 属性调整动画效果
- **进度条**：修改 `.progress-bar` 的 `background` 调整颜色

### 内容布局组件
| 组件 | 用途 | CSS类名 |
|------|------|---------|
| info-box | 信息卡片 | `.info-box` |
| stat-card | 数据统计 | `.stat-card` |
| timeline | 时间线 | `.timeline` |
| badge | 标签徽章 | `.badge` |

### 集成其他API
可扩展支持其他图片生成服务：
- OpenAI DALL-E
- Stability AI
- Midjourney API
