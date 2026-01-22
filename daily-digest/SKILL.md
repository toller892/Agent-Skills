---
name: daily-digest
description: 每日信息摘要工具，自动抓取 Hacker News、Product Hunt、Newsletter 内容，生成 Obsidian 文档，支持阅读标记和归档
---

# Daily Digest Skill

## 概述

信息过载？这个 skill 帮助你每天只看真正值得的内容。

- 🕘 每日 9 点推送整理好的文档
- 📖 点击用 Obsidian 查看
- ✅ 阅读完成后标记删除
- ⭐️ 优质内容自动归档

## 核心能力

### 1. 内容抓取
- **Hacker News**: Top stories, Show HN, Ask HN
- **Product Hunt**: 每日新产品
- **Newsletter**: RSS 订阅源

### 2. 文档生成
- 生成 Markdown 格式，兼容 Obsidian
- 按来源分类，带摘要和链接
- 自动添加标记复选框

### 3. 标记处理
- `✅` 标记 → 已读，删除该条目
- `⭐️` 标记 → 收藏，归档到 `archive/` 目录

## 使用方法

### 初始化配置

```bash
# 在 Obsidian vault 目录下创建配置
python scripts/init_config.py --vault ~/Obsidian/MyVault
```

### 生成每日摘要

```bash
# 抓取并生成今日摘要
python scripts/fetch_digest.py

# 指定日期
python scripts/fetch_digest.py --date 2025-01-20
```

### 处理标记

```bash
# 扫描文档中的标记并处理
python scripts/process_marks.py
```

### 定时任务（可选）

Windows 任务计划程序或 cron：

```bash
# 每日 9:00 执行
0 9 * * * cd /path/to/daily-digest && python scripts/fetch_digest.py
```

## 配置文件

`config.yaml`:

```yaml
# Obsidian Vault 路径
vault_path: ~/Obsidian/MyVault

# 摘要输出目录（相对于 vault）
digest_dir: Daily Digest
archive_dir: Daily Digest/Archive

# 数据源配置
sources:
  hacker_news:
    enabled: true
    limit: 20  # 最多抓取条数
    categories:
      - top
      - show
      - ask
  
  product_hunt:
    enabled: true
    limit: 10
  
  newsletters:
    enabled: true
    feeds:
      - name: "Hacker Newsletter"
        url: "https://hackernewsletter.com/rss"
      - name: "TLDR"
        url: "https://tldr.tech/rss"

# 推送设置
notification:
  enabled: true
  time: "09:00"
  # 可选: slack, email, system
  method: system
```

## 文档格式示例

生成的 `2025-01-20.md`:

```markdown
---
date: 2025-01-20
status: unread
total: 30
---

# 📰 每日摘要 - 2025-01-20

> 💡 **Inbox模式**: 本索引只显示未处理的文章
>
> - ✅已读、❌跳过、⭐收藏的文章已自动移除
> - 👆待写作的文章仍在此处
> - 周末目标: 清空此索引 = 全部处理完

---

📊 **待处理**: 30 篇
📎 **来源**: Hacker News, Product Hunt, TLDR
🕐 **更新时间**: 2025-01-20

---

## 🔥 Hacker News

### [Show HN: I built a tool for X](https://example.com) ⭐⭐⭐⭐☆ ✅

- **URL**: https://example.com
- **讨论**: [HN 评论](https://news.ycombinator.com/item?id=xxx) (👍 256 | 💬 89)

### [Why Rust is the future](https://example.com/rust) ⭐⭐⭐☆☆

- **URL**: https://example.com/rust
- **讨论**: [HN 评论](https://news.ycombinator.com/item?id=yyy) (👍 189 | 💬 234)

## 🚀 Product Hunt

### [ProductName](https://producthunt.com/posts/xxx) ⭐⭐⭐⭐⭐ 👆

> 一句话描述这个产品

- **URL**: https://producthunt.com/posts/xxx
- **Votes**: ⬆️ 456

---

## 📋 标记说明

| 标记 | 含义 | 处理 |
|:---:|:---|:---|
| ✅ | 已读 | 删除 |
| ❌ | 跳过 | 删除 |
| ⭐ | 收藏 | 归档 |
| 👆 | 待写作 | 保留 |

## API 说明

### HackerNewsAPI

```python
from daily_digest import HackerNewsAPI

hn = HackerNewsAPI()
stories = hn.get_top_stories(limit=20)
# [{'id': 123, 'title': '...', 'url': '...', 'score': 256, 'comments': 89}]
```

### ProductHuntAPI

```python
from daily_digest import ProductHuntAPI

ph = ProductHuntAPI(token="your_token")  # 可选
posts = ph.get_today_posts(limit=10)
```

### NewsletterFetcher

```python
from daily_digest import NewsletterFetcher

nf = NewsletterFetcher()
nf.add_feed("https://example.com/rss")
articles = nf.fetch_all()
```

## 项目结构

```
daily-digest/
├── SKILL.md              # Skill 定义
├── README.md             # 使用说明
├── config.example.yaml   # 配置示例
├── requirements.txt      # Python 依赖
├── scripts/
│   ├── init_config.py    # 初始化配置
│   ├── fetch_digest.py   # 抓取并生成摘要
│   └── process_marks.py  # 处理标记
└── daily_digest/
    ├── __init__.py
    ├── sources/
    │   ├── __init__.py
    │   ├── hackernews.py
    │   ├── producthunt.py
    │   └── newsletter.py
    ├── generator.py       # 文档生成器
    ├── processor.py       # 标记处理器
    └── notifier.py        # 通知推送
```

## 常见问题

### Product Hunt 需要 API Token 吗？

不需要，使用公开 GraphQL API。如需更高限额，可申请 Developer Token。

### 如何添加自定义 RSS 源？

编辑 `config.yaml`，在 `newsletters.feeds` 下添加：

```yaml
- name: "My Feed"
  url: "https://example.com/feed.xml"
```

### 支持哪些 Newsletter 格式？

支持标准 RSS 2.0 和 Atom 格式。

## 依赖

- Python 3.9+
- requests
- feedparser
- PyYAML
- rich (可选，美化输出)
