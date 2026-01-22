#!/usr/bin/env python3
"""
标记处理脚本 - 处理文档中的 ✅ 和 ⭐ 标记

使用方法:
    python process_marks.py              # 处理所有摘要文件
    python process_marks.py --stats      # 显示统计信息
    python process_marks.py --cleanup    # 清理空文件
"""

import sys
import argparse
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml
from rich.console import Console
from rich.table import Table

from daily_digest.processor import MarkProcessor


console = Console()


def load_config(config_path: Path = None) -> dict:
    """加载配置文件"""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    
    if not config_path.exists():
        return {
            "vault_path": "~/Obsidian/MyVault",
            "digest_dir": "Daily Digest",
            "archive_dir": "Daily Digest/Archive",
        }
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def show_stats(processor: MarkProcessor):
    """显示统计信息"""
    stats = processor.get_stats()
    
    table = Table(title="📊 Daily Digest 统计")
    table.add_column("指标", style="cyan")
    table.add_column("数值", style="green")
    
    table.add_row("摘要文件数", str(stats["total_files"]))
    table.add_row("未读条目", str(stats["unread_items"]))
    table.add_row("已归档收藏", str(stats["starred_items"]))
    
    console.print(table)


def process_all(processor: MarkProcessor):
    """处理所有文件"""
    results = processor.process_all()
    
    if not results:
        console.print("[dim]没有需要处理的标记[/dim]")
        return
    
    table = Table(title="✅ 处理结果")
    table.add_column("文件", style="cyan")
    table.add_column("已读删除", style="red")
    table.add_column("收藏归档", style="yellow")
    
    total_removed = 0
    total_starred = 0
    
    for result in results:
        path = Path(result["path"]).name
        removed = result.get("removed", 0)
        starred = result.get("starred", 0)
        
        table.add_row(path, str(removed), str(starred))
        total_removed += removed
        total_starred += starred
    
    table.add_section()
    table.add_row("[bold]总计[/bold]", f"[bold]{total_removed}[/bold]", f"[bold]{total_starred}[/bold]")
    
    console.print(table)


def cleanup(processor: MarkProcessor):
    """清理空文件"""
    completed = processor.cleanup_empty()
    
    if completed:
        console.print(f"\n[green]已标记 {len(completed)} 个文件为已完成:[/green]")
        for f in completed:
            console.print(f"  - {f.name}")
    else:
        console.print("[dim]没有需要清理的文件[/dim]")


def main():
    parser = argparse.ArgumentParser(description="处理 Daily Digest 标记")
    parser.add_argument("--config", type=str, help="配置文件路径")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--cleanup", action="store_true", help="清理空文件")
    parser.add_argument("--file", type=str, help="处理指定文件")
    args = parser.parse_args()
    
    console.print("\n[bold blue]📋 Daily Digest 标记处理器[/bold blue]\n")
    
    # 加载配置
    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)
    
    # 创建处理器
    processor = MarkProcessor(
        vault_path=config.get("vault_path", "~/Obsidian/MyVault"),
        digest_dir=config.get("digest_dir", "Daily Digest"),
        archive_dir=config.get("archive_dir", "Daily Digest/Archive"),
    )
    
    if args.stats:
        show_stats(processor)
    elif args.cleanup:
        cleanup(processor)
    elif args.file:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = processor.digest_dir / args.file
        
        result = processor.process_file(file_path)
        console.print(f"处理结果: 删除 {result.get('removed', 0)} 条, 归档 {result.get('starred', 0)} 条")
    else:
        process_all(processor)
        console.print()
        show_stats(processor)
    
    console.print()


if __name__ == "__main__":
    main()
