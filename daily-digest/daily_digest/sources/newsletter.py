"""Newsletter/RSS 抓取模块"""

import feedparser
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from concurrent.futures import ThreadPoolExecutor, as_completed


class NewsletterFetcher:
    """RSS/Atom Feed 抓取器"""
    
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.feeds: List[Dict] = []
    
    def add_feed(self, url: str, name: Optional[str] = None) -> None:
        """添加 RSS 源"""
        self.feeds.append({
            "url": url,
            "name": name or url,
        })
    
    def add_feeds(self, feeds: List[Dict]) -> None:
        """批量添加 RSS 源"""
        for feed in feeds:
            self.add_feed(
                url=feed.get("url", ""),
                name=feed.get("name"),
            )
    
    def fetch_feed(self, feed_info: Dict, days: int = 1) -> Dict:
        """抓取单个 feed"""
        url = feed_info.get("url", "")
        name = feed_info.get("name", url)
        
        try:
            parsed = feedparser.parse(url)
            
            if parsed.bozo and not parsed.entries:
                return {"name": name, "url": url, "articles": [], "error": str(parsed.bozo_exception)}
            
            # 过滤最近 N 天的文章
            cutoff = datetime.now() - timedelta(days=days)
            articles = []
            
            for entry in parsed.entries[:20]:  # 最多 20 篇
                pub_date = self._parse_date(entry)
                
                # 如果有日期且超过截止时间，跳过
                if pub_date and pub_date < cutoff:
                    continue
                
                articles.append({
                    "title": entry.get("title", "Untitled"),
                    "url": entry.get("link", ""),
                    "summary": self._clean_summary(entry.get("summary", "")),
                    "published": pub_date.isoformat() if pub_date else None,
                    "author": entry.get("author", ""),
                })
            
            return {
                "name": name,
                "url": url,
                "articles": articles,
            }
        
        except Exception as e:
            return {"name": name, "url": url, "articles": [], "error": str(e)}
    
    def fetch_all(self, days: int = 1) -> List[Dict]:
        """并发抓取所有 feeds"""
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self.fetch_feed, feed, days): feed 
                for feed in self.feeds
            }
            
            for future in as_completed(futures):
                result = future.result()
                if result.get("articles"):
                    results.append(result)
        
        return results
    
    def _parse_date(self, entry: Dict) -> Optional[datetime]:
        """解析发布日期"""
        for field in ["published", "updated", "created"]:
            date_str = entry.get(field) or entry.get(f"{field}_parsed")
            if date_str:
                try:
                    if isinstance(date_str, str):
                        return date_parser.parse(date_str)
                    elif hasattr(date_str, "tm_year"):
                        # struct_time
                        return datetime(*date_str[:6])
                except Exception:
                    continue
        return None
    
    def _clean_summary(self, summary: str, max_length: int = 200) -> str:
        """清理摘要文本"""
        import re
        
        # 移除 HTML 标签
        clean = re.sub(r"<[^>]+>", "", summary)
        # 移除多余空白
        clean = re.sub(r"\s+", " ", clean).strip()
        # 截断
        if len(clean) > max_length:
            clean = clean[:max_length].rsplit(" ", 1)[0] + "..."
        
        return clean


# 预设的优质 Newsletter 源
POPULAR_FEEDS = [
    {"name": "Hacker Newsletter", "url": "https://hackernewsletter.com/rss.xml"},
    {"name": "TLDR", "url": "https://tldr.tech/tech/rss.xml"},
    {"name": "Morning Brew", "url": "https://www.morningbrew.com/daily/rss"},
    {"name": "The Pragmatic Engineer", "url": "https://newsletter.pragmaticengineer.com/feed"},
    {"name": "ByteByteGo", "url": "https://blog.bytebytego.com/feed"},
]


if __name__ == "__main__":
    # 测试
    nf = NewsletterFetcher()
    nf.add_feeds(POPULAR_FEEDS[:2])
    
    results = nf.fetch_all(days=7)
    for feed in results:
        print(f"\n=== {feed['name']} ===")
        for article in feed.get("articles", [])[:3]:
            print(f"  - {article['title']}")
            print(f"    {article['url']}")
