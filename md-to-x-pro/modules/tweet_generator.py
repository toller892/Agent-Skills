#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推文生成器模块
生成简短吸引人的Twitter推文
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TweetData:
    """推文数据类"""

    text: str
    card_number: int
    total_cards: int
    hashtags: List[str]
    is_thread: bool = True


class TweetGenerator:
    """推文生成器主类"""

    # Twitter 字符限制
    MAX_LENGTH = 280

    # 常见吸睛开头
    ENGAGING_OPENERS = [
        "🚀 探索{title}的奥秘",
        "💡 揭秘{title}",
        "🔥 {title}最新进展",
        "📚 关于{title}，你需要知道",
        "⚡ {title}深度解析",
        "🎯 {title}完全指南",
        "✨ {title}干货分享",
        "🔍 深入了解{title}",
        "💎 {title}精华总结",
        "📖 {title}一文读懂",
    ]

    # CTA（行动号召）短语
    CALL_TO_ACTIONS = [
        "阅读完整内容 →",
        "查看详情 →",
        "了解更多 →",
        "继续阅读 →",
        "点击查看 →",
        "探索更多 →",
        "完整版 →",
    ]

    # 话题标签模板
    HASHTAG_TEMPLATES = [
        "#{keyword}",
        "#{keyword}#{keyword2}",
        "#{keyword} #{keyword2} #{keyword3}",
    ]

    def __init__(self):
        """初始化推文生成器"""
        pass

    def generate_thread(
        self, document_data: Dict, card_data: List[Dict], keywords: List[str]
    ) -> List[TweetData]:
        """
        生成4张连贯的推文线程

        Args:
            document_data: 文档数据（标题、摘要等）
            card_data: 卡片数据列表
            keywords: 关键词列表

        Returns:
            List[TweetData]: 推文数据列表
        """
        tweets = []
        title = document_data.get("title", "精彩内容")

        # 生成开场推文
        intro_tweet = self._generate_intro_tweet(
            title, document_data.get("summary", ""), keywords
        )
        tweets.append(intro_tweet)

        # 生成每张卡片的推文
        for i, card in enumerate(card_data):
            tweet = self._generate_card_tweet(
                card_number=i + 1,
                total_cards=len(card_data),
                card_title=card["sections"][0]["title"]
                if card.get("sections")
                else f"第{i + 1}部分",
                card_content=card["sections"][0]["content"]
                if card.get("sections")
                else "",
                keywords=keywords,
                is_last=(i == len(card_data) - 1),
            )
            tweets.append(tweet)

        # 生成收尾推文
        outro_tweet = self._generate_outro_tweet(title, keywords)
        tweets.append(outro_tweet)

        return tweets

    def _generate_intro_tweet(
        self, title: str, summary: str, keywords: List[str]
    ) -> TweetData:
        """生成开场推文"""
        # 选择吸睛开头
        opener_template = self.ENGAGING_OPENERS[
            hash(title) % len(self.ENGAGING_OPENERS)
        ]
        opener = opener_template.format(title=self._truncate(title, 20))

        # 构建内容
        content_parts = [opener]

        if summary:
            # 截取摘要到合适长度
            remaining = self.MAX_LENGTH - len(opener) - 10  # 预留空间给hashtag和链接
            truncated_summary = self._truncate(summary, remaining - 60)
            content_parts.append(truncated_summary)

        # 添加hashtag
        hashtags = self._generate_hashtags(keywords)

        tweet_text = " ".join(content_parts)

        # 确保长度限制
        tweet_text = self._fit_to_limit(tweet_text, hashtags)

        return TweetData(
            text=tweet_text,
            card_number=0,
            total_cards=0,
            hashtags=hashtags,
            is_thread=True,
        )

    def _generate_card_tweet(
        self,
        card_number: int,
        total_cards: int,
        card_title: str,
        card_content: str,
        keywords: List[str],
        is_last: bool = False,
    ) -> TweetData:
        """生成单张卡片的推文"""
        # 构建开头
        if card_number == 1:
            opener = "🔔 第一部分"
        else:
            opener = f"📌 第{card_number}部分"

        content_parts = [opener]

        # 添加标题
        truncated_title = self._truncate(card_title, 40)
        content_parts.append(f"【{truncated_title}】")

        # 添加内容摘要
        remaining = self.MAX_LENGTH - len(" ".join(content_parts)) - 50
        if remaining > 50:
            truncated_content = self._truncate(card_content, remaining - 20)
            content_parts.append(truncated_content)

        # 添加进度指示
        progress = f"({card_number}/{total_cards})"

        # 添加CTA或进度
        if is_last:
            cta = self.CALL_TO_ACTIONS[0]
            tweet_text = f"{' '.join(content_parts)} {cta}"
        else:
            tweet_text = f"{' '.join(content_parts)} {progress}"

        # 添加hashtag
        hashtags = self._generate_hashtags(keywords, card_number)

        tweet_text = self._fit_to_limit(tweet_text, hashtags)

        return TweetData(
            text=tweet_text,
            card_number=card_number,
            total_cards=total_cards,
            hashtags=hashtags,
            is_thread=not is_last,
        )

    def _generate_outro_tweet(self, title: str, keywords: List[str]) -> TweetData:
        """生成收尾推文"""
        closers = [
            "🎉 完整内容已生成！",
            "✨ 希望对你有帮助！",
            "💪 持续学习，持续进步！",
            "🚀 更多内容，敬请期待！",
            "📈 感谢阅读！",
        ]

        closer = closers[hash(title) % len(closers)]

        # 添加邀请互动
        interaction = "有问题欢迎评论讨论 💬"

        tweet_text = f"{closer}\n\n{interaction}"

        # 生成hashtag
        hashtags = self._generate_hashtags(keywords)

        tweet_text = self._fit_to_limit(tweet_text, hashtags)

        return TweetData(
            text=tweet_text,
            card_number=999,
            total_cards=999,
            hashtags=hashtags,
            is_thread=False,
        )

    def _generate_hashtags(
        self, keywords: List[str], card_number: int = 0
    ) -> List[str]:
        """
        生成话题标签

        Args:
            keywords: 关键词列表
            card_number: 卡片编号（用于变化）

        Returns:
            List[str]: 话题标签列表
        """
        selected = []

        # 选择3-5个关键词作为hashtag
        count = 3 + (card_number % 3)  # 每张卡片略有不同

        for kw in keywords[:count]:
            # 清理关键词
            clean_kw = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", kw)
            if clean_kw and len(clean_kw) > 1:
                # 英文转小写
                if clean_kw.isascii():
                    clean_kw = clean_kw.lower()
                selected.append(f"#{clean_kw}")

        # 如果关键词不够，添加通用标签
        general_tags = ["AI", "科技", "干货", "分享"]
        general_tags_en = ["AI", "Tech", "Learn", "Share"]

        while len(selected) < 3 and general_tags:
            tag = (
                general_tags.pop(0)
                if selected
                else general_tags_en[len(selected) % len(general_tags_en)]
            )
            if tag not in selected:
                selected.append(f"#{tag}")

        return selected[:5]  # 最多5个

    def _truncate(self, text: str, max_length: int) -> str:
        """截断文本到指定长度"""
        if len(text) <= max_length:
            return text

        # 在单词边界截断
        truncated = text[:max_length]
        last_space = truncated.rfind(" ")
        last_newline = truncated.rfind("\n")
        cut_point = max(last_space, last_newline)

        if cut_point > max_length * 0.5:
            truncated = truncated[:cut_point]
        else:
            truncated = truncated.rstrip("，。！？、；：")

        return truncated + "..."

    def _fit_to_limit(self, text: str, hashtags: List[str]) -> str:
        """
        将文本调整到字符限制内

        Args:
            text: 原始文本
            hashtags: 话题标签列表

        Returns:
            str: 调整后的文本
        """
        hashtag_text = " " + " ".join(hashtags)

        # 如果超出限制，逐步截断
        while len(text + hashtag_text) > self.MAX_LENGTH:
            # 每次减少20个字符
            text = text[:-20].rstrip("，。！？、；：\n")

        return text + hashtag_text

    def generate_single_tweet(
        self, title: str, content: str, keywords: List[str], include_link: bool = False
    ) -> TweetData:
        """
        生成单条推文（不组成线程）

        Args:
            title: 内容标题
            content: 内容摘要
            keywords: 关键词列表
            include_link: 是否包含链接占位符

        Returns:
            TweetData: 推文数据
        """
        # 选择开头
        opener = self.ENGAGING_OPENERS[0].format(title=self._truncate(title, 15))

        # 构建内容
        available = self.MAX_LENGTH - len(opener) - len("🔥 \n\n→ ")

        if include_link:
            available -= 25  # 预留链接空间

        truncated_content = self._truncate(content, available)

        tweet_text = f"{opener}\n\n{truncated_content}"

        if include_link:
            tweet_text += "\n\n→ 阅读完整内容"

        # 添加hashtag
        hashtags = self._generate_hashtags(keywords)

        tweet_text = self._fit_to_limit(tweet_text, hashtags)

        return TweetData(
            text=tweet_text,
            card_number=1,
            total_cards=1,
            hashtags=hashtags,
            is_thread=False,
        )

    def format_thread_for_export(self, tweets: List[TweetData]) -> str:
        """
        格式化推文线程为可导出格式

        Args:
            tweets: 推文数据列表

        Returns:
            str: 格式化后的文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("🐦 Twitter 推文线程")
        lines.append("=" * 60)
        lines.append("")

        for i, tweet in enumerate(tweets):
            lines.append(f"--- 推文 {i + 1}/{len(tweets)} ---")
            lines.append("")
            lines.append(tweet.text)
            lines.append("")
            lines.append("-" * 40)
            lines.append("")

        lines.append("💡 使用提示:")
        lines.append("1. 按顺序发布这些推文")
        lines.append("2. 建议每条间隔2-5分钟")
        lines.append("3. 及时回复评论增加互动")
        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


# 测试代码
if __name__ == "__main__":
    # 测试推文生成器
    generator = TweetGenerator()

    # 模拟文档数据
    document_data = {
        "title": "人工智能的未来",
        "summary": "人工智能正在快速发展，改变我们的生活方式。本文探讨AI技术的最新进展和未来趋势，包括深度学习、自然语言处理等领域的突破。",
    }

    # 模拟卡片数据
    card_data = [
        {
            "sections": [
                {
                    "title": "当前发展",
                    "content": "深度学习和神经网络技术取得显著进展，大型语言模型将AI能力推向新高度。",
                }
            ]
        },
        {
            "sections": [
                {
                    "title": "应用场景",
                    "content": "AI广泛应用于医疗、金融、教育等行业，提高效率，创造价值。",
                }
            ]
        },
        {
            "sections": [
                {
                    "title": "技术突破",
                    "content": "自然语言处理和计算机视觉等领域实现重大突破，AI时代已经到来。",
                }
            ]
        },
        {
            "sections": [
                {
                    "title": "未来展望",
                    "content": "AI将继续朝着更智能、更安全、更可解释的方向发展，机遇与挑战并存。",
                }
            ]
        },
    ]

    keywords = [
        "AI",
        "人工智能",
        "机器学习",
        "深度学习",
        "技术",
        "未来",
        "创新",
        "科技",
    ]

    # 生成推文线程
    tweets = generator.generate_thread(document_data, card_data, keywords)

    # 打印结果
    print(generator.format_thread_for_export(tweets))

    # 单独测试单条推文
    print("\n" + "=" * 60)
    print("📝 单条推文示例:")
    print("=" * 60)
    single_tweet = generator.generate_single_tweet(
        title="Python编程指南",
        content="Python是一门优雅且强大的编程语言，适用于Web开发、数据科学、人工智能等多个领域。",
        keywords=["Python", "编程", "开发", "学习"],
    )
    print(single_tweet.text)
    print(f"\n字符数: {len(single_tweet.text)}")
