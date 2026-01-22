"""Obsidian 文档生成器"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


def get_week_number(date: datetime) -> int:
    """获取年内周数"""
    return date.isocalendar()[1]


def get_week_range(date: datetime) -> tuple:
    """获取周的起止日期"""
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start, end


class DigestGenerator:
    """每日摘要文档生成器"""
    
    def __init__(self, vault_path: str, digest_dir: str = "Daily Digest"):
        self.vault_path = Path(vault_path).expanduser()
        self.digest_dir = self.vault_path / digest_dir
        self.digest_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录
        self.weekly_dir = self.digest_dir / "Weekly"
        self.weekly_dir.mkdir(exist_ok=True)
        self.archive_dir = self.digest_dir / "Archive"
        self.archive_dir.mkdir(exist_ok=True)
    
    def generate(
        self,
        hn_stories: List[Dict] = None,
        ph_posts: List[Dict] = None,
        newsletters: List[Dict] = None,
        date: Optional[datetime] = None,
    ) -> Path:
        """生成每日摘要文档"""
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        
        content = self._build_content(
            date_str=date_str,
            hn_stories=hn_stories or [],
            ph_posts=ph_posts or [],
            newsletters=newsletters or [],
        )
        
        # 写入文件
        file_path = self.digest_dir / f"{date_str}.md"
        file_path.write_text(content, encoding="utf-8")
        
        return file_path
    
    def _build_content(
        self,
        date_str: str,
        hn_stories: List[Dict],
        ph_posts: List[Dict],
        newsletters: List[Dict],
    ) -> str:
        """构建 Markdown 内容"""
        # 计算统计
        total_items = len(hn_stories) + len(ph_posts)
        for nl in newsletters:
            total_items += len(nl.get("articles", []))
        
        sources = []
        if hn_stories:
            sources.append("Hacker News")
        if ph_posts:
            sources.append("Product Hunt")
        for nl in newsletters:
            if nl.get("articles"):
                sources.append(nl.get("name", "Newsletter"))
        
        lines = [
            "---",
            f"date: {date_str}",
            "status: unread",
            f"total: {total_items}",
            "---",
            "",
            f"# 📰 每日摘要 - {date_str}",
            "",
            "> 💡 **Inbox模式**: 本索引只显示未处理的文章",
            ">",
            "> - ✅已读、❌跳过、⭐收藏的文章已自动移除",
            "> - 👆待写作的文章仍在此处",
            "> - 周末目标: 清空此索引 = 全部处理完",
            "",
            "---",
            "",
            f"📊 **待处理**: {total_items} 篇",
            f"📎 **来源**: {', '.join(sources)}",
            f"🕐 **更新时间**: {date_str}",
            "",
            "---",
            "",
        ]
        
        # Hacker News 部分
        if hn_stories:
            lines.extend(self._build_hn_section(hn_stories))
        
        # Product Hunt 部分
        if ph_posts:
            lines.extend(self._build_ph_section(ph_posts))
        
        # Newsletter 部分
        if newsletters:
            lines.extend(self._build_newsletter_section(newsletters))
        
        # 使用说明
        lines.extend([
            "",
            "---",
            "",
            "## 📋 标记说明",
            "",
            "| 标记 | 含义 | 处理 |",
            "|:---:|:---|:---|",
            "| ✅ | 已读 | 删除 |",
            "| ❌ | 跳过 | 删除 |",
            "| ⭐ | 收藏 | 归档 |",
            "| 👆 | 待写作 | 保留 |",
            "",
        ])
        
        return "\n".join(lines)
    
    def _build_hn_section(self, stories: List[Dict]) -> List[str]:
        """构建 Hacker News 部分"""
        lines = [
            "## 🔥 Hacker News",
            "",
        ]
        
        for story in stories:
            title = story.get("title", "Untitled")
            url = story.get("url", "")
            hn_url = story.get("hn_url", "")
            score = story.get("score", 0)
            comments = story.get("comments", 0)
            
            # 根据 score 生成星级
            stars = self._score_to_stars(score, max_score=500)
            
            lines.append(f"### [{title}]({url}) {stars}")
            lines.append("")
            lines.append(f"- **URL**: {url}")
            lines.append(f"- **讨论**: [HN 评论]({hn_url}) (👍 {score} | 💬 {comments})")
            lines.append("")
            # 添加操作选择
            lines.extend(self._build_action_buttons())
            lines.append("")
        
        return lines
    
    def _build_action_buttons(self) -> List[str]:
        """构建操作按钮"""
        return [
            "**操作**: [ ] ✅ 已读  [ ] ❌ 跳过  [ ] ⭐ 收藏",
        ]
    
    def _score_to_stars(self, score: int, max_score: int = 500) -> str:
        """将分数转换为星级评分"""
        if score >= max_score:
            filled = 5
        else:
            filled = min(5, max(1, int(score / max_score * 5) + 1))
        
        return "⭐" * filled + "☆" * (5 - filled)
    
    def _build_ph_section(self, posts: List[Dict]) -> List[str]:
        """构建 Product Hunt 部分"""
        lines = [
            "## 🚀 Product Hunt",
            "",
        ]
        
        for post in posts:
            name = post.get("name", "Untitled")
            tagline = post.get("tagline", "")
            url = post.get("url", "")
            votes = post.get("votes", 0)
            
            # 根据 votes 生成星级
            stars = self._score_to_stars(votes, max_score=300)
            
            lines.append(f"### [{name}]({url}) {stars}")
            lines.append("")
            if tagline:
                lines.append(f"> {tagline}")
                lines.append("")
            lines.append(f"- **URL**: {url}")
            lines.append(f"- **Votes**: ⬆️ {votes}")
            lines.append("")
            # 添加操作选择
            lines.extend(self._build_action_buttons())
            lines.append("")
        
        return lines
    
    def _build_newsletter_section(self, newsletters: List[Dict]) -> List[str]:
        """构建 Newsletter 部分"""
        lines = [
            "## 📧 Newsletters",
            "",
        ]
        
        for feed in newsletters:
            feed_name = feed.get("name", "Newsletter")
            articles = feed.get("articles", [])
            
            if not articles:
                continue
            
            lines.append(f"### 📰 {feed_name}")
            lines.append("")
            
            for article in articles:
                title = article.get("title", "Untitled")
                url = article.get("url", "")
                summary = article.get("summary", "")
                
                lines.append(f"#### [{title}]({url})")
                lines.append("")
                if summary:
                    # 截断过长的摘要
                    if len(summary) > 200:
                        summary = summary[:200] + "..."
                    lines.append(f"> {summary}")
                    lines.append("")
                lines.append(f"- **URL**: {url}")
                lines.append("")
                # 添加操作选择
                lines.extend(self._build_action_buttons())
                lines.append("")
        
        return lines
    
    def get_digest_path(self, date: Optional[datetime] = None) -> Path:
        """获取指定日期的摘要文件路径"""
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        return self.digest_dir / f"{date_str}.md"
    
    def list_digests(self, limit: int = 30) -> List[Path]:
        """列出最近的摘要文件"""
        files = sorted(self.digest_dir.glob("*.md"), reverse=True)
        return files[:limit]
    
    def generate_weekly_index(self, date: Optional[datetime] = None) -> Path:
        """生成周汇总索引页"""
        date = date or datetime.now()
        year = date.year
        week_num = get_week_number(date)
        week_start, week_end = get_week_range(date)
        
        # 统计本周数据
        total_items = 0
        processed_items = 0
        starred_items = 0
        sources = set()
        
        # 扫描本周的文件
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_file = self.digest_dir / f"{day.strftime('%Y-%m-%d')}.md"
            if day_file.exists():
                content = day_file.read_text(encoding="utf-8")
                # 简单统计
                total_items += content.count("###")
                if "Hacker News" in content:
                    sources.add("Hacker News")
                if "Product Hunt" in content:
                    sources.add("Product Hunt")
        
        # 统计归档数量
        for archive_file in self.archive_dir.glob("*-starred.md"):
            content = archive_file.read_text(encoding="utf-8")
            starred_items += content.count("- [ ]")
        
        lines = [
            "---",
            f"year: {year}",
            f"week: {week_num}",
            "type: weekly-index",
            "---",
            "",
            f"# {year}年第{week_num}周素材汇总 🗂️",
            "",
            "> 💡 **Inbox模式**: 本索引只显示未处理的文章",
            ">",
            "> - ✅已读、❌跳过、⭐收藏的文章已自动移除",
            "> - 👆待写作的文章仍在此处",
            "> - 周末目标: 清空此索引 = 全部处理完",
            "",
            "---",
            "",
            f"📅 **采集周次**: 第 {week_num} 周",
            f"📊 **待处理**: {total_items} 篇",
            f"📎 **来源**: {', '.join(sorted(sources)) if sources else '暂无'}",
            f"🕐 **最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC",
            "",
            "---",
            "",
            "## 📅 本周每日摘要",
            "",
        ]
        
        # 链接到每日摘要
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            day_file = self.digest_dir / f"{day_str}.md"
            
            if day_file.exists():
                lines.append(f"- [[{day_str}]] ({weekday_names[i]})")
            else:
                lines.append(f"- {day_str} ({weekday_names[i]}) - *未生成*")
        
        lines.extend([
            "",
            "---",
            "",
            "## 📋 标记说明",
            "",
            "| 标记 | 含义 | 处理 |",
            "|:---:|:---|:---|",
            "| ✅ | 已读 | 删除 |",
            "| ❌ | 跳过 | 删除 |",
            "| ⭐ | 收藏 | 归档 |",
            "| 👆 | 待写作 | 保留 |",
            "",
        ])
        
        # 写入文件
        file_path = self.weekly_dir / f"{year}-W{week_num:02d}.md"
        file_path.write_text("\n".join(lines), encoding="utf-8")
        
        return file_path


if __name__ == "__main__":
    # 测试
    gen = DigestGenerator("./test_vault")
    
    # 模拟数据
    hn_stories = [
        {"title": "Test Story", "url": "https://example.com", 
         "hn_url": "https://news.ycombinator.com/item?id=123",
         "score": 100, "comments": 50},
    ]
    
    ph_posts = [
        {"name": "Cool Product", "tagline": "A cool product", 
         "url": "https://producthunt.com/posts/cool", "votes": 200},
    ]
    
    path = gen.generate(hn_stories=hn_stories, ph_posts=ph_posts)
    print(f"Generated: {path}")
    print(path.read_text())
