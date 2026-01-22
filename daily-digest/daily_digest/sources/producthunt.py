"""Product Hunt API 抓取模块"""

import requests
from typing import List, Dict, Optional
from datetime import datetime, timezone


class ProductHuntAPI:
    """Product Hunt GraphQL API 客户端"""
    
    API_URL = "https://api.producthunt.com/v2/api/graphql"
    
    def __init__(self, token: Optional[str] = None, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        
        # 设置 headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.session.headers.update(headers)
    
    def _query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """发送 GraphQL 查询"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        resp = self.session.post(self.API_URL, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
    
    def get_today_posts(self, limit: int = 10) -> List[Dict]:
        """获取今日产品"""
        query = """
        query GetPosts($first: Int!) {
            posts(first: $first, order: VOTES) {
                edges {
                    node {
                        id
                        name
                        tagline
                        url
                        votesCount
                        website
                        createdAt
                        topics {
                            edges {
                                node {
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        
        try:
            result = self._query(query, {"first": limit})
            posts = result.get("data", {}).get("posts", {}).get("edges", [])
            return [self._format_post(edge["node"]) for edge in posts]
        except Exception as e:
            print(f"Product Hunt API error: {e}")
            return self._fallback_scrape(limit)
    
    def _format_post(self, post: Dict) -> Dict:
        """格式化产品数据"""
        topics = [
            t["node"]["name"] 
            for t in post.get("topics", {}).get("edges", [])
        ]
        
        return {
            "id": post.get("id"),
            "name": post.get("name", ""),
            "tagline": post.get("tagline", ""),
            "url": post.get("url", ""),
            "website": post.get("website", ""),
            "votes": post.get("votesCount", 0),
            "topics": topics,
            "created_at": post.get("createdAt", ""),
        }
    
    def _fallback_scrape(self, limit: int = 10) -> List[Dict]:
        """备用方案：从网页抓取（无需 API Token）"""
        try:
            # 使用公开的 JSON endpoint
            url = "https://www.producthunt.com/frontend/graphql"
            query = """
            query HomePage {
                homefeed(first: %d) {
                    edges {
                        node {
                            ... on Post {
                                id
                                name
                                tagline
                                slug
                                votesCount
                            }
                        }
                    }
                }
            }
            """ % limit
            
            resp = self.session.post(
                url,
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )
            
            if resp.status_code == 200:
                data = resp.json()
                edges = data.get("data", {}).get("homefeed", {}).get("edges", [])
                return [
                    {
                        "id": e["node"].get("id"),
                        "name": e["node"].get("name", ""),
                        "tagline": e["node"].get("tagline", ""),
                        "url": f"https://www.producthunt.com/posts/{e['node'].get('slug', '')}",
                        "votes": e["node"].get("votesCount", 0),
                        "topics": [],
                    }
                    for e in edges if e.get("node")
                ]
        except Exception:
            pass
        
        return []


if __name__ == "__main__":
    # 测试
    ph = ProductHuntAPI()
    posts = ph.get_today_posts(limit=5)
    for p in posts:
        print(f"[⬆️ {p['votes']}] {p['name']}")
        print(f"    {p['tagline']}")
        print(f"    {p['url']}")
