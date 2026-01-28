#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI内容提炼模块
使用AI将文档内容提炼成吸引人的推文风格
"""

import json
import logging
from typing import Dict, List
import requests

logger = logging.getLogger(__name__)


class ContentRefiner:
    """内容提炼器 - 使用AI提炼精要并转化成推文风格"""

    def __init__(self, api_key: str = None):
        """
        初始化提炼器

        Args:
            api_key: Gemini API Key
        """
        self.api_key = api_key
        self.api_url = "https://cdn.12ai.org/v1beta/models/gemini-2.5-flash:generateContent"

    def refine_document_for_cards(
        self,
        document_title: str,
        document_content: str,
        sections: List[Dict],
        num_cards: int = 4
    ) -> List[Dict]:
        """
        将文档提炼成适合Twitter卡片的内容

        Args:
            document_title: 文档标题
            document_content: 文档完整内容
            sections: 文档章节列表
            num_cards: 需要生成的卡片数量

        Returns:
            List[Dict]: 提炼后的卡片数据
        """
        if not self.api_key:
            logger.warning("未提供API Key，使用基础提炼方法")
            return self._basic_refine(document_title, sections, num_cards)

        try:
            # 使用AI提炼内容
            return self._ai_refine(document_title, document_content, sections, num_cards)
        except Exception as e:
            logger.error(f"AI提炼失败，使用基础方法: {e}")
            return self._basic_refine(document_title, sections, num_cards)

    def _ai_refine(
        self,
        document_title: str,
        document_content: str,
        sections: List[Dict],
        num_cards: int
    ) -> List[Dict]:
        """使用AI提炼内容"""

        # 构建提示词
        prompt = f"""你是一位社交媒体内容专家，擅长将复杂的技术文档转化成吸引人的推文风格内容。

**原始文档标题：**
{document_title}

**文档内容片段：**
{document_content[:8000]}

**任务：**
请将这份文档提炼成 {num_cards} 张Twitter卡片的内容，每张卡片需要：

1. **吸引人的标题** - 使用emoji，简洁有力，引发好奇
2. **核心要点** - 3-5个bullet points，提炼最关键的信息
3. **金句/洞察** - 一个令人印象深刻的句子或洞察
4. **相关话题标签** - 3-5个相关的hashtag

**风格要求：**
- 使用emoji增加视觉吸引力
- 语言简洁、有力、口语化
- 避免过于技术化的术语，用通俗语言解释
- 每张卡片都要有独立的主题，但整体要有连贯性
- 制造悬念和吸引力，让读者想看下一张

**输出格式：**
请以JSON格式返回，格式如下：
{{
    "cards": [
        {{
            "card_number": 1,
            "title": "🔥 这里的标题要吸引眼球",
            "subtitle": "副标题（可选）",
            "key_points": [
                "📌 核心要点1",
                "📌 核心要点2",
                "📌 核心要点3"
            ],
            "insight": "💡 令人印象深刻的洞察或金句",
            "hashtags": ["#标签1", "#标签2", "#标签3"],
            "image_prompt": "用于AI生成图片的简短提示词（英文，20词以内）"
        }}
    ]
}}

注意：
- 卡片1应该制造悬念，介绍问题/痛点
- 卡片2-3应该提供核心解决方案和关键洞察
- 卡片4应该提供行动号召或未来展望
"""

        # 调用Gemini API
        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.8,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
                "responseMimeType": "application/json"
            }
        }

        url = f"{self.api_url}?key={self.api_key}"
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            raise Exception(f"API调用失败: {response.status_code} - {response.text}")

        result = response.json()

        # 提取生成的文本
        if "candidates" not in result or len(result["candidates"]) == 0:
            raise Exception("API响应中没有candidates")

        generated_text = result["candidates"][0]["content"]["parts"][0]["text"]

        # 解析JSON
        try:
            refined_data = json.loads(generated_text)
            cards = refined_data.get("cards", [])

            # 转换格式
            card_data = []
            for card in cards:
                card_data.append({
                    "card_number": card["card_number"],
                    "total_cards": num_cards,
                    "title": card["title"],
                    "subtitle": card.get("subtitle", ""),
                    "key_points": card["key_points"],
                    "insight": card["insight"],
                    "hashtags": card["hashtags"],
                    "image_prompt": card["image_prompt"],
                    "summary": card.get("summary", "")
                })

            return card_data

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            logger.error(f"生成的文本: {generated_text}")
            raise

    def _basic_refine(
        self,
        document_title: str,
        sections: List[Dict],
        num_cards: int
    ) -> List[Dict]:
        """基础提炼方法（不使用AI）"""

        cards = []
        sections_per_card = max(1, len(sections) // num_cards)

        for i in range(num_cards):
            start_idx = i * sections_per_card
            end_idx = min((i + 1) * sections_per_card, len(sections))
            card_sections = sections[start_idx:end_idx]

            # 提取关键内容
            key_points = []
            for section in card_sections[:3]:
                content = section.get("content", "")[:200]
                if content:
                    key_points.append(f"📌 {content[:100]}...")

            card = {
                "card_number": i + 1,
                "total_cards": num_cards,
                "title": f"📄 {document_title}",
                "subtitle": f"第 {i + 1} 部分 / 共 {num_cards} 部分",
                "key_points": key_points[:4] if key_points else ["📌 内容加载中..."],
                "insight": "💡 仔细阅读本文档，了解更多细节。",
                "hashtags": ["#文档", "#内容", "#学习"],
                "image_prompt": f"Professional illustration for part {i+1}",
                "summary": ""
            }

            cards.append(card)

        return cards


# 测试代码
if __name__ == "__main__":
    refiner = ContentRefiner(api_key="test_key")

    # 测试基础提炼
    test_sections = [
        {"title": "简介", "content": "这是测试内容"},
        {"title": "正文", "content": "这是正文内容"}
    ]

    cards = refiner._basic_refine("测试文档", test_sections, 2)
    print(json.dumps(cards, ensure_ascii=False, indent=2))
