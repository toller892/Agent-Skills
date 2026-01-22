# Daily Digest - 每日信息摘要

> 信息过载？每天只看真正值得的内容。

## 功能

- 🔥 抓取 Hacker News 热门文章
- 🚀 抓取 Product Hunt 新产品
- 📧 聚合 RSS Newsletter
- 📖 生成 Obsidian Markdown 文档
- ✅ 已读标记删除
- ⭐ 收藏标记归档

## 命令

### 生成每日摘要

```bash
cd d:\Code\skills\daily-digest
python scripts/fetch_digest.py
```

### 处理阅读标记

```bash
cd d:\Code\skills\daily-digest
python scripts/process_marks.py
```

### 初始化配置

```bash
cd d:\Code\skills\daily-digest
python scripts/init_config.py --vault <你的Obsidian路径>
```

## 使用示例

当用户说：
- "生成今日信息摘要" → 运行 `fetch_digest.py`
- "处理我的阅读标记" → 运行 `process_marks.py`
- "初始化摘要配置" → 运行 `init_config.py`

## 配置

配置文件：`config.yaml`

```yaml
vault_path: ~/Obsidian/MyVault  # Obsidian 路径
digest_dir: Daily Digest         # 输出目录
sources:
  hacker_news:
    enabled: true
    limit: 20
  product_hunt:
    enabled: true
    limit: 10
  newsletters:
    enabled: true
    feeds:
      - name: "TLDR"
        url: "https://tldr.tech/tech/rss.xml"
```

## 标记规则

在 Obsidian 中阅读时：

| 操作 | 标记 | 效果 |
|:---|:---:|:---|
| 已读 | `[✅]` | 从文档删除 |
| 收藏 | `[⭐]` | 归档到 Archive |

## 依赖

首次使用需安装：

```bash
pip install requests feedparser PyYAML rich python-dateutil
```
