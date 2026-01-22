"""Hacker News API 抓取模块"""

import requests
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class HackerNewsAPI:
    """Hacker News API 客户端"""
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
    
    def _get(self, endpoint: str) -> dict:
        """发送 GET 请求"""
        url = f"{self.BASE_URL}/{endpoint}.json"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
    
    def get_item(self, item_id: int) -> Optional[Dict]:
        """获取单个 item 详情"""
        try:
            return self._get(f"item/{item_id}")
        except Exception:
            return None
    
    def get_top_stories(self, limit: int = 20) -> List[Dict]:
        """获取 Top Stories"""
        ids = self._get("topstories")[:limit]
        return self._fetch_items(ids)
    
    def get_new_stories(self, limit: int = 20) -> List[Dict]:
        """获取 New Stories"""
        ids = self._get("newstories")[:limit]
        return self._fetch_items(ids)
    
    def get_best_stories(self, limit: int = 20) -> List[Dict]:
        """获取 Best Stories"""
        ids = self._get("beststories")[:limit]
        return self._fetch_items(ids)
    
    def get_ask_stories(self, limit: int = 20) -> List[Dict]:
        """获取 Ask HN"""
        ids = self._get("askstories")[:limit]
        return self._fetch_items(ids)
    
    def get_show_stories(self, limit: int = 20) -> List[Dict]:
        """获取 Show HN"""
        ids = self._get("showstories")[:limit]
        return self._fetch_items(ids)
    
    def _fetch_items(self, ids: List[int]) -> List[Dict]:
        """并发获取多个 items"""
        items = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.get_item, id_): id_ for id_ in ids}
            for future in as_completed(futures):
                item = future.result()
                if item and item.get("type") == "story":
                    items.append(self._format_item(item))
        
        # 按 score 排序
        items.sort(key=lambda x: x.get("score", 0), reverse=True)
        return items
    
    def _format_item(self, item: Dict) -> Dict:
        """格式化 item 数据"""
        return {
            "id": item.get("id"),
            "title": item.get("title", ""),
            "url": item.get("url", f"https://news.ycombinator.com/item?id={item.get('id')}"),
            "hn_url": f"https://news.ycombinator.com/item?id={item.get('id')}",
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "author": item.get("by", ""),
            "time": item.get("time", 0),
        }
    
    def get_stories_by_category(self, category: str, limit: int = 20) -> List[Dict]:
        """根据分类获取 stories"""
        category_map = {
            "top": self.get_top_stories,
            "new": self.get_new_stories,
            "best": self.get_best_stories,
            "ask": self.get_ask_stories,
            "show": self.get_show_stories,
        }
        func = category_map.get(category, self.get_top_stories)
        return func(limit=limit)


if __name__ == "__main__":
    # 测试
    hn = HackerNewsAPI()
    stories = hn.get_top_stories(limit=5)
    for s in stories:
        print(f"[{s['score']}] {s['title']}")
        print(f"    {s['url']}")
