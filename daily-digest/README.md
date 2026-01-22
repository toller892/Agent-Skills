# 📰 Daily Digest

**每日信息摘要工具** - 告别信息过载，只看真正值得的内容

## ✨ 功能特点

- 🔥 **Hacker News** - 自动抓取热门技术文章
- 🚀 **Product Hunt** - 每日新产品发现
- 📧 **Newsletter** - RSS 订阅源聚合
- 📖 **Obsidian 集成** - 生成 Markdown 文档
- ⏰ **定时推送** - 每日 9 点通知
- ✅ **标记处理** - 已读删除，收藏归档

## 🚀 快速开始

### 1. 安装依赖

```bash
cd daily-digest
pip install -r requirements.txt
```

### 2. 初始化配置

```bash
python scripts/init_config.py --vault ~/Obsidian/MyVault
```

### 3. 生成今日摘要

```bash
python scripts/fetch_digest.py
```

### 4. 在 Obsidian 中查看

打开 `Daily Digest/2025-01-20.md`

## 📋 使用流程

```
┌─────────────────────────────────────────────────────┐
│  每日 9:00                                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │  HN     │  │   PH    │  │  RSS    │             │
│  └────┬────┘  └────┬────┘  └────┬────┘             │
│       │            │            │                   │
│       └────────────┼────────────┘                   │
│                    ▼                                │
│            ┌──────────────┐                        │
│            │  生成 .md    │                        │
│            └──────┬───────┘                        │
│                   ▼                                │
│            ┌──────────────┐                        │
│            │  推送通知    │ ──► 点击打开 Obsidian   │
│            └──────────────┘                        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  阅读时                                              │
│                                                     │
│  - [ ] 未读文章                                     │
│  - [✅] 已读 → 删除                                 │
│  - [⭐] 不错 → 归档到 Archive/                      │
│                                                     │
│  运行 process_marks.py 处理标记                     │
└─────────────────────────────────────────────────────┘
```

## 🔧 配置说明

编辑 `config.yaml`:

```yaml
# Obsidian Vault 路径
vault_path: ~/Obsidian/MyVault

# 输出目录
digest_dir: Daily Digest
archive_dir: Daily Digest/Archive

# 数据源
sources:
  hacker_news:
    enabled: true
    limit: 20
    categories: [top, show, ask]
  
  product_hunt:
    enabled: true
    limit: 10
  
  newsletters:
    enabled: true
    feeds:
      - name: "Hacker Newsletter"
        url: "https://hackernewsletter.com/rss.xml"
      - name: "TLDR"
        url: "https://tldr.tech/tech/rss.xml"

# 通知
notification:
  enabled: true
  time: "09:00"
  method: system  # system, slack, email
```

## ⏰ 定时任务

### Windows 任务计划程序

```powershell
# 创建每日 9:00 执行的任务
$action = New-ScheduledTaskAction -Execute "python" -Argument "scripts/fetch_digest.py" -WorkingDirectory "D:\Code\skills\daily-digest"
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
Register-ScheduledTask -TaskName "DailyDigest" -Action $action -Trigger $trigger
```

### macOS/Linux Cron

```bash
# 编辑 crontab
crontab -e

# 添加任务 (每日 9:00)
0 9 * * * cd /path/to/daily-digest && python scripts/fetch_digest.py
```

## 📁 项目结构

```
daily-digest/
├── SKILL.md              # Claude Code Skill 定义
├── README.md             # 本文件
├── config.example.yaml   # 配置示例
├── config.yaml           # 你的配置（git ignored）
├── requirements.txt      # Python 依赖
├── scripts/
│   ├── init_config.py    # 初始化配置
│   ├── fetch_digest.py   # 抓取生成摘要
│   └── process_marks.py  # 处理标记
└── daily_digest/
    ├── __init__.py
    ├── sources/
    │   ├── hackernews.py   # HN API
    │   ├── producthunt.py  # PH API
    │   └── newsletter.py   # RSS 抓取
    ├── generator.py        # 文档生成
    ├── processor.py        # 标记处理
    └── notifier.py         # 通知推送
```

## 🎯 Claude Code 使用

在 Claude Code 中可以直接使用：

```
/skill daily-digest

# 或者
生成今天的信息摘要
处理我的阅读标记
显示摘要统计
```

## ❓ 常见问题

### Q: Product Hunt API 需要 Token 吗？

不需要。使用公开 API，如需更高限额可申请 Developer Token。

### Q: 如何添加更多 RSS 源？

编辑 `config.yaml`，在 `newsletters.feeds` 下添加：

```yaml
- name: "My Feed"
  url: "https://example.com/feed.xml"
```

### Q: 推送的通知无法点击打开 Obsidian？

确保 Obsidian 已安装并注册了 `obsidian://` URL scheme。

### Q: 中文显示乱码？

确保终端支持 UTF-8 编码：

```bash
# Windows PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## 📜 License

MIT
