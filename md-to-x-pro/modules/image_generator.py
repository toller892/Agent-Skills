#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片生成器模块
使用 Gemini API 生成配套图片
"""

import base64
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import requests
from requests.exceptions import RequestException

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ImageGenerationResult:
    """图片生成结果类"""

    success: bool
    image_path: Optional[str] = None
    base64_data: Optional[str] = None
    error_message: Optional[str] = None
    prompt_used: str = ""


@dataclass
class ImageConfig:
    """图片配置类"""

    aspect_ratio: str = "16:9"
    image_size: str = "1K"
    response_modalities: List[str] = None

    def __post_init__(self):
        if self.response_modalities is None:
            self.response_modalities = ["IMAGE"]


class GeminiImageGenerator:
    """Gemini 图片生成器主类"""

    # API 端点
    API_ENDPOINT = (
        "https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent"
    )
    PRO_ENDPOINT = (
        "https://cdn.12ai.org/v1beta/models/gemini-3-pro-image-preview:generateContent"
    )

    # 支持的宽高比
    SUPPORTED_ASPECT_RATIOS = [
        "1:1",
        "16:9",
        "9:16",
        "4:3",
        "3:4",
        "3:2",
        "2:3",
        "5:4",
        "4:5",
        "21:9",
    ]

    # 支持的图片尺寸
    SUPPORTED_SIZES = ["1K", "2K", "4K"]

    def __init__(self, api_key: Optional[str] = None, use_pro_model: bool = False):
        """
        初始化图片生成器

        Args:
            api_key: Gemini API Key，如果不提供则无法生成图片
            use_pro_model: 是否使用pro模型（支持4K分辨率）
        """
        self.api_key = api_key
        self.config = ImageConfig()
        self.use_pro_model = use_pro_model

    def set_api_key(self, api_key: str):
        """设置 API Key"""
        self.api_key = api_key
        logger.info("API Key 已设置")

    def set_config(self, aspect_ratio: str = "16:9", image_size: str = "1K"):
        """
        设置图片生成配置

        Args:
            aspect_ratio: 宽高比
            image_size: 图片尺寸
        """
        if aspect_ratio not in self.SUPPORTED_ASPECT_RATIOS:
            logger.warning(f"不支持的宽高比 {aspect_ratio}，使用默认值 16:9")
            aspect_ratio = "16:9"

        if image_size not in self.SUPPORTED_SIZES:
            logger.warning(f"不支持的图片尺寸 {image_size}，使用默认值 1K")
            image_size = "1K"

        self.config.aspect_ratio = aspect_ratio
        self.config.image_size = image_size

        logger.info(f"图片配置已更新: {aspect_ratio}, {image_size}")

    def generate_image(
        self, prompt: str, output_path: Optional[str] = None
    ) -> ImageGenerationResult:
        """
        根据提示词生成图片

        Args:
            prompt: 图片描述提示词
            output_path: 可选的输出路径

        Returns:
            ImageGenerationResult: 生成结果
        """
        if not self.api_key:
            logger.warning("未提供 API Key，跳过图片生成")
            return ImageGenerationResult(
                success=False,
                error_message="未提供 Gemini API Key，无法生成图片",
                prompt_used=prompt,
            )

        logger.info(f"开始生成图片，提示词: {prompt[:100]}...")

        try:
            # 构建请求体
            payload = self._build_payload(prompt)

            # 发送 API 请求
            response = self._send_request(payload)

            # 解析响应
            result = self._parse_response(response, output_path)

            if result.success:
                logger.info(f"图片生成成功: {result.image_path}")
            else:
                logger.error(f"图片生成失败: {result.error_message}")

            return result

        except RequestException as e:
            error_msg = f"API 请求失败: {str(e)}"
            logger.error(error_msg)
            return ImageGenerationResult(
                success=False, error_message=error_msg, prompt_used=prompt
            )
        except Exception as e:
            error_msg = f"图片生成过程出错: {str(e)}"
            logger.error(error_msg)
            return ImageGenerationResult(
                success=False, error_message=error_msg, prompt_used=prompt
            )

    def _build_payload(self, prompt: str) -> Dict:
        """构建 API 请求体"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": self.config.response_modalities,
                "imageConfig": {
                    "aspectRatio": self.config.aspect_ratio,
                },
            },
        }

        # 只有pro模型才支持imageSize参数
        if self.use_pro_model:
            payload["generationConfig"]["imageConfig"]["imageSize"] = self.config.image_size

        return payload

    def _send_request(self, payload: Dict) -> Dict:
        """发送 API 请求"""
        # 根据模型类型选择端点
        endpoint = self.PRO_ENDPOINT if self.use_pro_model else self.API_ENDPOINT
        url = f"{endpoint}?key={self.api_key}"

        headers = {"Content-Type": "application/json"}

        logger.info(f"使用{'Pro' if self.use_pro_model else 'Flash'}模型生成图片")

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=60,  # 60秒超时
        )

        response.raise_for_status()
        return response.json()

    def _parse_response(
        self, response: Dict, output_path: Optional[str]
    ) -> ImageGenerationResult:
        """解析 API 响应"""
        try:
            # 调试：打印完整响应
            logger.debug(f"API响应: {json.dumps(response, indent=2)[:500]}...")

            # 检查响应结构
            if "candidates" not in response:
                return ImageGenerationResult(
                    success=False,
                    error_message=f"API 响应中没有 candidates 字段。响应: {str(response)[:200]}",
                    prompt_used="",
                )

            candidates = response["candidates"]
            if not candidates:
                return ImageGenerationResult(
                    success=False,
                    error_message="API 响应中 candidates 为空",
                    prompt_used="",
                )

            # 提取图片数据
            candidate = candidates[0]
            content = candidate.get("content", {})
            parts = content.get("parts", [])

            if not parts:
                return ImageGenerationResult(
                    success=False,
                    error_message="API 响应中没有 parts 字段",
                    prompt_used="",
                )

            part = parts[0]

            # 检查是否有 inline_data (支持驼峰和蛇形两种命名)
            inline_data = part.get("inlineData") or part.get("inline_data")

            if not inline_data:
                # 尝试查找其他位置的图片数据
                for p in parts:
                    inline_data = p.get("inlineData") or p.get("inline_data")
                    if inline_data:
                        part = p
                        break
                else:
                    # 打印实际的parts结构用于调试
                    logger.error(f"Parts结构: {json.dumps(parts, indent=2)[:500]}")
                    return ImageGenerationResult(
                        success=False,
                        error_message=f"API 响应中没有找到图片数据。Parts: {str(parts)[:200]}",
                        prompt_used="",
                    )

            image_data = inline_data.get("data", "")
            mime_type = inline_data.get("mimeType") or inline_data.get("mime_type", "image/png")

            # 解码 base64 数据
            try:
                image_bytes = base64.b64decode(image_data)
            except Exception as e:
                return ImageGenerationResult(
                    success=False,
                    error_message=f"Base64 解码失败: {str(e)}",
                    prompt_used="",
                )

            # 确定输出路径
            if output_path is None:
                output_path = self._generate_output_path()

            # 保存图片
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            with open(output_path, "wb") as f:
                f.write(image_bytes)

            return ImageGenerationResult(
                success=True,
                image_path=output_path,
                base64_data=image_data,
                error_message=None,
            )

        except (KeyError, IndexError) as e:
            return ImageGenerationResult(
                success=False,
                error_message=f"解析响应数据失败: {str(e)}",
                prompt_used="",
            )

    def _generate_output_path(self) -> str:
        """生成默认输出路径"""
        import time

        timestamp = int(time.time())
        return f"output/images/image_{timestamp}.png"

    def generate_batch(
        self, prompts: List[str], output_dir: str = "output/images"
    ) -> List[ImageGenerationResult]:
        """
        批量生成图片

        Args:
            prompts: 提示词列表
            output_dir: 输出目录

        Returns:
            List[ImageGenerationResult]: 生成结果列表
        """
        results = []
        output_path_dir = Path(output_dir)
        output_path_dir.mkdir(parents=True, exist_ok=True)

        for i, prompt in enumerate(prompts):
            output_path = str(output_path_dir / f"image_{i + 1}.png")
            result = self.generate_image(prompt, output_path)
            results.append(result)

        return results

    def edit_image(
        self, input_image_path: str, edit_prompt: str, output_path: Optional[str] = None
    ) -> ImageGenerationResult:
        """
        编辑现有图片

        Args:
            input_image_path: 输入图片路径
            edit_prompt: 编辑提示词
            output_path: 输出路径

        Returns:
            ImageGenerationResult: 生成结果
        """
        if not self.api_key:
            return ImageGenerationResult(
                success=False,
                error_message="未提供 API Key，无法编辑图片",
                prompt_used="",
            )

        logger.info(f"开始编辑图片: {input_image_path}")

        try:
            # 读取图片并编码为 base64
            with open(input_image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")

            # 构建请求体（包含图片）
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": edit_prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": image_data,
                                }
                            },
                        ]
                    }
                ]
            }

            # 发送请求
            response = self._send_request(payload)

            # 解析响应
            result = self._parse_response(response, output_path)

            if result.success:
                logger.info(f"图片编辑成功: {result.image_path}")
            else:
                logger.error(f"图片编辑失败: {result.error_message}")

            return result

        except Exception as e:
            error_msg = f"图片编辑过程出错: {str(e)}"
            logger.error(error_msg)
            return ImageGenerationResult(
                success=False, error_message=error_msg, prompt_used=edit_prompt
            )

    def get_model_info(self) -> Dict:
        """获取模型信息"""
        return {
            "fast_model": "gemini-2.5-flash-image",
            "pro_model": "gemini-3-pro-image-preview",
            "supported_aspect_ratios": self.SUPPORTED_ASPECT_RATIOS,
            "supported_sizes": self.SUPPORTED_SIZES,
        }


class ImagePromptGenerator:
    """图片提示词生成器"""

    @staticmethod
    def generate_for_section(
        section_title: str, section_content: str, keywords: List[str]
    ) -> str:
        """
        根据章节内容生成图片提示词

        Args:
            section_title: 章节标题
            section_content: 章节内容
            keywords: 关键词列表

        Returns:
            str: 图片提示词
        """
        # 提取内容概要
        content_snippet = section_content[:200].replace("\n", " ")

        # 结合标题和关键词
        combined_keywords = " ".join(keywords[:5])

        prompt = f"""
        Create a visually stunning, modern illustration representing: {section_title}
        
        Visual concept: {content_snippet}
        
        Style requirements:
        - Professional and modern design
        - Vivid colors with gradient effects
        - Clean and minimal aesthetic
        - Suitable for social media sharing
        - High resolution (16:9 aspect ratio)
        - Captivating visual storytelling
        
        Key visual elements: {combined_keywords}
        
        Do not include any text in the image.
        """

        return prompt.strip()

    @staticmethod
    def generate_cover(title: str, summary: str, keywords: List[str]) -> str:
        """
        生成封面图片提示词

        Args:
            title: 文档标题
            summary: 文档摘要
            keywords: 关键词列表

        Returns:
            str: 封面图片提示词
        """
        combined_keywords = " ".join(keywords[:8])

        prompt = f"""
        Create a breathtaking, professional cover image for: {title}
        
        Theme and concept: {summary}
        
        Style requirements:
        - Epic and inspiring visual design
        - Modern corporate/professional aesthetic
        - Dynamic gradient color scheme
        - Clean and sophisticated look
        - Perfect for title screen or cover page
        - High impact visual storytelling
        - 16:9 aspect ratio, high resolution
        
        Visual elements to incorporate: {combined_keywords}
        
        No text or typography in the image.
        """

        return prompt.strip()

    @staticmethod
    def generate_summary(keyword: str) -> str:
        """生成简单关键词图片提示词"""
        return f"""
        Create a modern, minimalist icon or illustration representing: {keyword}
        
        Style: Clean, professional, suitable for social media.
        Color scheme: Vibrant but professional.
        Background: Solid or subtle gradient.
        """


# 测试代码
if __name__ == "__main__":
    # 测试图片生成器
    generator = GeminiImageGenerator()

    # 获取模型信息
    info = generator.get_model_info()
    print("支持的宽高比:", info["supported_aspect_ratios"])
    print("支持的尺寸:", info["supported_sizes"])

    # 测试提示词生成
    prompt_gen = ImagePromptGenerator()

    test_prompt = prompt_gen.generate_for_section(
        "人工智能的未来",
        "人工智能正在快速发展，改变我们的生活方式...",
        ["AI", "技术", "未来", "创新", "智能"],
    )

    print("\n生成的提示词:")
    print(test_prompt)
