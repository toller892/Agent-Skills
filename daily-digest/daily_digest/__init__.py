"""Daily Digest - 每日信息摘要工具"""

from .sources.hackernews import HackerNewsAPI
from .sources.producthunt import ProductHuntAPI
from .sources.newsletter import NewsletterFetcher
from .generator import DigestGenerator
from .processor import MarkProcessor

__version__ = "1.0.0"
__all__ = [
    "HackerNewsAPI",
    "ProductHuntAPI",
    "NewsletterFetcher",
    "DigestGenerator",
    "MarkProcessor",
]
