#!/usr/bin/env python3
"""
每日摘要抓取脚本

使用方法:
    python fetch_digest.py                    # 生成今日摘要
    python fetch_digest.py --date 2025-01-20  # 指定日期
    python fetch_digest.py --no-notify        # 不发送通知
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from daily_digest.sources import HackerNewsAPI, ProductHuntAPI, NewsletterFetcher
from daily_digest.generator import DigestGenerator
from daily_digest.notifier import send_daily_notification


console = Console()


def load_config(config_path: Path = None) -> dict:
    """加载配置文件"""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    
    if not config_path.exists():
        # 使用默认配置
        console.print("[yellow]config.yaml not found, using defaults[/yellow]")
        return {
            "vault_path": "~/Obsidian/MyVault",
            "digest_dir": "Daily Digest",
            "archive_dir": "Daily Digest/Archive",
            "sources": {
                "hacker_news": {"enabled": True, "limit": 20, "categories": ["top"]},
                "product_hunt": {"enabled": True, "limit": 10},
                "newsletters": {"enabled": False, "feeds": []},
            },
            "notification": {"enabled": True, "method": "system"},
        }
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_hacker_news(config: dict) -> list:
    """抓取 Hacker News"""
    hn_config = config.get("sources", {}).get("hacker_news", {})
    
    if not hn_config.get("enabled", True):
        return []
    
    limit = hn_config.get("limit", 20)
    categories = hn_config.get("categories", ["top"])
    
    hn = HackerNewsAPI()
    all_stories = []
    
    for category in categories:
        stories = hn.get_stories_by_category(category, limit=limit // len(categories))
        all_stories.extend(stories)
    
    # 去重并按 score 排序
    seen = set()
    unique_stories = []
    for s in sorted(all_stories, key=lambda x: x.get("score", 0), reverse=True):
        if s["id"] not in seen:
            seen.add(s["id"])
            unique_stories.append(s)
    
    return unique_stories[:limit]


def fetch_product_hunt(config: dict) -> list:
    """抓取 Product Hunt"""
    ph_config = config.get("sources", {}).get("product_hunt", {})
    
    if not ph_config.get("enabled", True):
        return []
    
    limit = ph_config.get("limit", 10)
    token = ph_config.get("token")  # 可选
    
    ph = ProductHuntAPI(token=token)
    return ph.get_today_posts(limit=limit)


def fetch_newsletters(config: dict) -> list:
    """抓取 Newsletters"""
    nl_config = config.get("sources", {}).get("newsletters", {})
    
    if not nl_config.get("enabled", False):
        return []
    
    feeds = nl_config.get("feeds", [])
    if not feeds:
        return []
    
    nf = NewsletterFetcher()
    nf.add_feeds(feeds)
    return nf.fetch_all(days=1)


def main():
    parser = argparse.ArgumentParser(description="生成每日信息摘要")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--config", type=str, help="配置文件路径")
    parser.add_argument("--no-notify", action="store_true", help="不发送通知")
    parser.add_argument("--open", action="store_true", help="生成后立即打开")
    parser.add_argument("--weekly", action="store_true", help="同时生成周汇总")
    args = parser.parse_args()
    
    # 解析日期
    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        target_date = datetime.now()
    
    date_str = target_date.strftime("%Y-%m-%d")
    
    console.print(f"\n[bold blue]📰 Daily Digest - {date_str}[/bold blue]\n")
    
    # 加载配置
    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)
    
    # 创建生成器
    generator = DigestGenerator(
        vault_path=config.get("vault_path", "~/Obsidian/MyVault"),
        digest_dir=config.get("digest_dir", "Daily Digest"),
    )
    
    hn_stories = []
    ph_posts = []
    newsletters = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # 抓取 Hacker News
        task = progress.add_task("抓取 Hacker News...", total=None)
        try:
            hn_stories = fetch_hacker_news(config)
            progress.update(task, description=f"[green]✓ Hacker News ({len(hn_stories)} 条)[/green]")
        except Exception as e:
            progress.update(task, description=f"[red]✗ Hacker News: {e}[/red]")
        progress.remove_task(task)
        
        # 抓取 Product Hunt
        task = progress.add_task("抓取 Product Hunt...", total=None)
        try:
            ph_posts = fetch_product_hunt(config)
            progress.update(task, description=f"[green]✓ Product Hunt ({len(ph_posts)} 条)[/green]")
        except Exception as e:
            progress.update(task, description=f"[red]✗ Product Hunt: {e}[/red]")
        progress.remove_task(task)
        
        # 抓取 Newsletters
        task = progress.add_task("抓取 Newsletters...", total=None)
        try:
            newsletters = fetch_newsletters(config)
            article_count = sum(len(f.get("articles", [])) for f in newsletters)
            progress.update(task, description=f"[green]✓ Newsletters ({article_count} 篇)[/green]")
        except Exception as e:
            progress.update(task, description=f"[red]✗ Newsletters: {e}[/red]")
        progress.remove_task(task)
        
        # 生成文档
        task = progress.add_task("生成文档...", total=None)
        file_path = generator.generate(
            hn_stories=hn_stories,
            ph_posts=ph_posts,
            newsletters=newsletters,
            date=target_date,
        )
        progress.update(task, description=f"[green]✓ 文档已生成[/green]")
        progress.remove_task(task)
    
    console.print(f"\n[bold green]✅ 摘要已保存到:[/bold green] {file_path}")
    
    # 发送通知
    notify_config = config.get("notification", {})
    if notify_config.get("enabled", True) and not args.no_notify:
        method = notify_config.get("method", "system")
        send_daily_notification(file_path, method=method)
        console.print("[dim]📬 通知已发送[/dim]")
    
    # 生成周汇总
    if args.weekly:
        weekly_path = generator.generate_weekly_index(target_date)
        console.print(f"[bold green]📅 周汇总已保存到:[/bold green] {weekly_path}")
    
    # 打开文件
    if args.open:
        from daily_digest.notifier import Notifier
        notifier = Notifier()
        notifier.open_in_obsidian(file_path)
    
    console.print()


if __name__ == "__main__":
    main()
