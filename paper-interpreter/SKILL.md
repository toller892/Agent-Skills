---
name: paper-interpreter
description: 论文→黄叔风格解读+纽约客插画+2026设计网页。五步搞定。
keywords: [论文, PDF, 解析, arxiv, 黄叔风格, 纽约客, 插画, HTML]
---

# 论文解析器

把学术论文变成人话。
配上纽约客插画。
输出精美网页+PDF。

五步走完。

---

## 工作流

### 1/ 抓信息 🔍

WebFetch 抓 arXiv 页面
WebSearch 补技术细节
WebFetch 找深度解读

搞定原材料。

### 2/ 写文章 ✍️

黄叔风格硬指标：

类比密度 ≥1个/400字
"你"字出现率 >30%
三层递进解释

输出 Markdown。

### 3/ 画插图 🎨

API: Nano Banana (Gemini 2.0)

纽约客极简风：
• 3-4色 muted 配色
• 中世纪现代美学
• 零文字标注

Base64 → PNG 保存。

### 4/ 做网页 💻

2026 前沿设计：

暖调配色 #FDFBF7
Noto Serif SC + Inter
滚动动画 (Intersection Observer)

输出完整 HTML。

### 5/ 生成PDF 📄

调用 generate_pdf.py
fpdf2 原生渲染
中文字体 STHeiti

搞定。

---

## 怎么用

直接说：

"解析这篇论文：https://arxiv.org/pdf/2301.12345.pdf"

或者

"黄叔风格解读这篇"

或者

"纽约客风格走一个"

---

## 输出啥

```
论文解读文件夹/
├── {名称}/
│   ├── index.html
│   ├── {名称}.pdf
│   ├── {名称}.md
│   ├── {名称}_log.txt
│   └── images/
│       ├── illustration_01.png
│       ├── illustration_02.png
│       └── ...
```

---

## 环境变量

`NANO_BANANA_TOKEN` 
必需。用于生成插画。

---

## 依赖

requests
fpdf2

装一下：
```
pip install requests fpdf2
```

完事。
