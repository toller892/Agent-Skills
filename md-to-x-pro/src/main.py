#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document to Beautiful HTML 主程序
将文档转换为精美的HTML页面
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DocumentToHTMLConverter:
    """文档转HTML转换器主类"""

    def __init__(self, api_key: Optional[str] = None):
        """初始化转换器"""
        # 导入模块
        from modules.document_parser import DocumentParser
        from modules.image_generator import GeminiImageGenerator, ImagePromptGenerator
        from modules.html_generator import HTMLGenerator
        from modules.api_key_manager import GeminiKeyManager
        from modules.tweet_generator import TweetGenerator
        from modules.content_refiner import ContentRefiner

        self.document_parser = DocumentParser()
        self.image_generator = GeminiImageGenerator()
        self.prompt_generator = ImagePromptGenerator()
        self.html_generator = HTMLGenerator()
        self.key_manager = GeminiKeyManager()
        self.tweet_generator = TweetGenerator()
        self.content_refiner = ContentRefiner(api_key=api_key)

    def convert(
        self,
        document_path: str,
        api_key: Optional[str] = None,
        output_dir: str = "output",
        aspect_ratio: str = "16:9",
        generate_images: bool = True,
    ) -> Dict:
        """
        执行文档到HTML的转换

        Args:
            document_path: 文档路径
            api_key: Gemini API Key
            output_dir: 输出目录
            aspect_ratio: 图片宽高比
            generate_images: 是否生成图片

        Returns:
            Dict: 转换结果
        """
        result = {
            "success": False,
            "document_path": document_path,
            "output_files": [],
            "images_generated": [],
            "error": None,
        }

        try:
            logger.info(f"开始转换文档: {document_path}")

            # 1. 设置 API Key
            if api_key:
                self.image_generator.set_api_key(api_key)
                self.key_manager.setup_gemini_key(api_key)
            else:
                # 尝试从环境变量或配置文件获取
                env_key = self.key_manager.get_gemini_key()
                if env_key:
                    self.image_generator.set_api_key(env_key)
                    logger.info("已从环境变量加载 API Key")
                else:
                    logger.info("未提供 API Key，将跳过图片生成")

            # 设置图片配置
            self.image_generator.set_config(aspect_ratio=aspect_ratio)

            # 2. 解析文档
            logger.info("解析文档...")
            document = self.document_parser.parse(document_path)
            logger.info(f"文档标题: {document.title}")
            logger.info(f"章节数: {len(document.sections)}")
            logger.info(f"关键词: {document.keywords}")

            # 3. AI提炼内容为推文风格的卡片
            logger.info("使用AI提炼内容为推文风格卡片...")
            # 将sections转换为字典格式
            sections_dict = [
                {"title": sec.title, "content": sec.content}
                for sec in document.sections
            ]
            refined_cards = self.content_refiner.refine_document_for_cards(
                document_title=document.title,
                document_content=document.full_text,
                sections=sections_dict,
                num_cards=4
            )
            logger.info(f"AI提炼完成，生成 {len(refined_cards)} 张卡片")

            # 4. 生成图片（如果需要）
            image_paths = []
            if generate_images and self.image_generator.api_key:
                logger.info("开始生成配套图片...")
                image_paths = self._generate_images_for_refined_cards(refined_cards, output_dir)
                result["images_generated"] = image_paths

            # 5. 生成HTML文件
            logger.info("生成推文风格HTML文件...")
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # 为每个卡片生成单独的HTML文件
            for i, card in enumerate(refined_cards):
                card_number = i + 1
                # 获取对应的图片路径
                image_path = image_paths[i] if i < len(image_paths) else None

                # 构建单张卡片的数据（推文风格）
                single_card_data = {
                    "card_number": card_number,
                    "total_cards": len(refined_cards),
                    "title": card.get("title", ""),
                    "subtitle": card.get("subtitle", ""),
                    "key_points": card.get("key_points", []),
                    "insight": card.get("insight", ""),
                    "hashtags": card.get("hashtags", []),
                    "image_path": image_path,
                    "has_images": bool(image_path),
                    "is_tweet_style": True  # 标记为推文风格
                }

                # 生成单张卡片的HTML
                html_content = self.html_generator._generate_tweet_style_card(single_card_data)
                output_file = output_path / f"beautiful_content_{card_number}.html"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(html_content)

                result["output_files"].append(str(output_file))
                logger.info(f"生成卡片 {card_number}: {output_file}")

            # 生成完整页面
            # 将DocumentSection对象转换为字典
            sections_dict = [
                {"title": sec.title, "content": sec.content, "level": sec.level}
                for sec in document.sections[:20]
            ]
            full_page_file = self.html_generator.generate_standalone_page(
                {
                    "title": document.title,
                    "summary": document.summary,
                    "sections": sections_dict,
                    "keywords": document.keywords,
                    "total_cards": 4,
                    "image_paths": result["images_generated"],
                },
                str(output_path / "complete_content.html"),
            )
            result["output_files"].append(full_page_file)

            # 6. 生成Twitter推文
            logger.info("生成Twitter推文...")
            tweet_file = self._generate_tweets_for_refined(
                refined_cards=refined_cards,
                output_dir=str(output_path),
            )
            result["output_files"].append(tweet_file)

            result["success"] = True
            logger.info("转换完成!")

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"转换失败: {e}")

        return result

    def _generate_images_for_cards(
        self, cards_data: List[Dict], output_dir: str
    ) -> List[str]:
        """
        为每张卡片生成配套图片

        Args:
            cards_data: 卡片数据列表
            output_dir: 输出目录

        Returns:
            List[str]: 生成的图片路径列表
        """
        image_paths = []
        images_dir = Path(output_dir) / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        for i, card in enumerate(cards_data):
            # 生成图片提示词
            prompt = self.prompt_generator.generate_for_section(
                card["sections"][0]["title"] if card["sections"] else card["title"],
                card["sections"][0]["content"] if card["sections"] else "",
                card["keywords"],
            )

            # 生成图片
            output_path = str(images_dir / f"card_{i + 1}_image.png")
            result = self.image_generator.generate_image(prompt, output_path)

            if result.success:
                image_paths.append(result.image_path)
                logger.info(f"卡片 {i + 1} 图片生成成功: {result.image_path}")
            else:
                logger.warning(f"卡片 {i + 1} 图片生成失败: {result.error_message}")
                image_paths.append("")

        return image_paths

    def _generate_images_for_refined_cards(
        self, refined_cards: List[Dict], output_dir: str
    ) -> List[str]:
        """
        为提炼后的卡片生成配套图片

        Args:
            refined_cards: AI提炼后的卡片数据列表
            output_dir: 输出目录

        Returns:
            List[str]: 生成的图片路径列表
        """
        image_paths = []
        images_dir = Path(output_dir) / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        for i, card in enumerate(refined_cards):
            # 使用卡片中自带的image_prompt
            prompt = card.get("image_prompt", f"Professional illustration for card {i+1}")

            # 生成图片
            output_path = str(images_dir / f"card_{i + 1}_image.png")
            result = self.image_generator.generate_image(prompt, output_path)

            if result.success:
                image_paths.append(result.image_path)
                logger.info(f"卡片 {i + 1} 图片生成成功: {result.image_path}")
            else:
                logger.warning(f"卡片 {i + 1} 图片生成失败: {result.error_message}")
                image_paths.append("")

        return image_paths

    def _generate_tweets(
        self,
        document_data: Dict,
        card_data: List[Dict],
        keywords: List[str],
        output_dir: str,
    ) -> str:
        """
        生成Twitter推文并保存

        Args:
            document_data: 文档数据
            card_data: 卡片数据列表
            keywords: 关键词列表
            output_dir: 输出目录

        Returns:
            str: 推文文件路径
        """
        # 生成推文线程
        tweets = self.tweet_generator.generate_thread(
            document_data, card_data, keywords
        )

        # 格式化输出
        tweet_content = self.tweet_generator.format_thread_for_export(tweets)

        # 保存文件
        output_file = Path(output_dir) / "twitter_threads.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(tweet_content)

        logger.info(f"推文已生成: {output_file}")

        # 同时生成每条单独推文的简短版本
        individual_tweets = []
        for i, tweet in enumerate(tweets):
            if tweet.card_number in [0, 999]:
                # 开场和收尾推文
                label = "开场" if tweet.card_number == 0 else "收尾"
                individual_tweets.append(f"\n=== {label}推文 ===\n{tweet.text}")
            else:
                individual_tweets.append(
                    f"\n=== 卡片{tweet.card_number}推文 ===\n{tweet.text}"
                )

        # 保存单独版本
        individual_file = Path(output_dir) / "individual_tweets.txt"
        with open(individual_file, "w", encoding="utf-8") as f:
            f.write("🐦 Twitter 推文 (每条独立)\n")
            f.write("=" * 40 + "\n")
            f.write("\n---\n".join(individual_tweets))
            f.write("\n\n💡 提示: 直接复制每条推文发布即可\n")

        logger.info(f"独立推文已生成: {individual_file}")

        return str(output_file)

    def _generate_tweets_for_refined(
        self,
        refined_cards: List[Dict],
        output_dir: str,
    ) -> str:
        """
        为提炼后的卡片生成Twitter推文

        Args:
            refined_cards: AI提炼后的卡片数据
            output_dir: 输出目录

        Returns:
            str: 推文文件路径
        """
        # 生成推文内容
        tweets = []

        # 开场推文
        if refined_cards:
            first_card = refined_cards[0]
            tweets.append(f"""🚀 {first_card.get('title', '')}

{first_card.get('insight', '')}

{' '.join(first_card.get('hashtags', []))}

👇 了解更多""")

        # 每张卡片的推文
        for card in refined_cards:
            tweet_content = f"""{card.get('title', '')}

{' '.join(card.get('key_points', [])[:3])}

💡 {card.get('insight', '')}

{' '.join(card.get('hashtags', []))}
{card['card_number']}/{len(refined_cards)}"""
            tweets.append(tweet_content)

        # 保存为线程
        output_file = Path(output_dir) / "twitter_threads.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("🐦 Twitter 推文线程\n")
            f.write("=" * 50 + "\n\n")
            for i, tweet in enumerate(tweets):
                f.write(f"【推文 {i+1}】\n{tweet}\n\n")
                f.write("-" * 50 + "\n\n")

        logger.info(f"推文已生成: {output_file}")

        # 保存独立推文
        individual_file = Path(output_dir) / "individual_tweets.txt"
        with open(individual_file, "w", encoding="utf-8") as f:
            f.write("🐦 Twitter 推文 (每条独立)\n")
            f.write("=" * 40 + "\n\n")
            for i, tweet in enumerate(tweets):
                f.write(f"=== 推文 {i+1} ===\n{tweet}\n\n")
            f.write("💡 提示: 直接复制每条推文发布即可\n")

        logger.info(f"独立推文已生成: {individual_file}")

        return str(output_file)

    def interactive_mode(self):
        """交互式模式"""
        print("\n" + "=" * 60)
        print("📄 Document to Beautiful HTML 转换器")
        print("=" * 60)
        print("\n将您的文档转换为精美的HTML页面，用于Twitter分享")

        # 1. 输入文档路径
        print("\n📁 步骤 1: 选择文档")
        document_path = input("请输入文档路径 (支持 txt, md, docx 格式): ").strip()

        if not Path(document_path).exists():
            print(f"✗ 文件不存在: {document_path}")
            return

        # 2. 输入 API Key
        print("\n🔑 步骤 2: 配置 Gemini API Key (可选)")
        api_key = input("请输入 Gemini API Key (直接回车跳过图片生成): ").strip()

        if api_key:
            print("✓ API Key 已设置，将生成配套图片")
        else:
            print("○ 跳过图片生成，将只生成文字版本")

        # 3. 选择宽高比
        print("\n🖼️ 步骤 3: 选择图片宽高比")
        aspect_ratios = ["16:9", "1:1", "9:16", "4:3", "3:4"]
        print("可选比例:", ", ".join(aspect_ratios))
        aspect_ratio = input("选择比例 (默认 16:9): ").strip() or "16:9"

        if aspect_ratio not in aspect_ratios:
            aspect_ratio = "16:9"

        # 4. 开始转换
        print("\n🚀 开始转换...")
        result = self.convert(
            document_path=document_path,
            api_key=api_key if api_key else None,
            aspect_ratio=aspect_ratio,
        )

        # 5. 显示结果
        self._display_results(result)

    def _display_results(self, result: Dict):
        """显示转换结果"""
        print("\n" + "=" * 60)
        print("📊 转换结果")
        print("=" * 60)

        if result["success"]:
            print("✅ 转换成功!")
            print(f"\n📄 生成的HTML文件:")
            for i, file in enumerate(result["output_files"], 1):
                print(f"   {i}. {file}")

            if result["images_generated"]:
                print(f"\n🖼️ 生成的图片:")
                for i, img in enumerate(result["images_generated"], 1):
                    if img:
                        print(f"   {i}. {img}")
                    else:
                        print(f"   {i}. (图片生成失败)")

            print("\n💡 提示:")
            print("   - 4张卡片可以用于Twitter连续分享")
            print("   - 完整页面包含所有内容的综合版本")
            print("   - 生成的HTML文件可以直接在浏览器中打开")
            print("   - twitter_threads.txt 包含完整的推文线程")
            print("   - individual_tweets.txt 可以逐条复制发布")

        else:
            print(f"❌ 转换失败!")
            print(f"错误信息: {result['error']}")

    def run_cli(self):
        """运行命令行界面"""
        parser = argparse.ArgumentParser(
            description="将文档转换为精美的HTML页面",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例:
  python main.py document.txt
  python main.py document.md --api-key YOUR_KEY
  python main.py document.docx --aspect-ratio 1:1
  python main.py document.txt --no-images
            """,
        )

        parser.add_argument("document", help="要转换的文档路径")
        parser.add_argument("--api-key", "-k", help="Gemini API Key")
        parser.add_argument(
            "--output", "-o", default="output", help="输出目录 (默认: output)"
        )
        parser.add_argument(
            "--aspect-ratio", "-r", default="16:9", help="图片宽高比 (默认: 16:9)"
        )
        parser.add_argument("--no-images", action="store_true", help="不生成图片")
        parser.add_argument(
            "--interactive", "-i", action="store_true", help="交互式模式"
        )

        args = parser.parse_args()

        if args.interactive:
            self.interactive_mode()
        else:
            result = self.convert(
                document_path=args.document,
                api_key=args.api_key,
                output_dir=args.output,
                aspect_ratio=args.aspect_ratio,
                generate_images=not args.no_images,
            )
            self._display_results(result)


def main():
    """主函数"""
    # 从命令行参数获取API key（如果提供）
    import sys
    api_key = None
    if "--api-key" in sys.argv or "-k" in sys.argv:
        parser = argparse.ArgumentParser()
        parser.add_argument("--api-key", "-k")
        args, _ = parser.parse_known_args()
        api_key = args.api_key

    converter = DocumentToHTMLConverter(api_key=api_key)
    converter.run_cli()


if __name__ == "__main__":
    main()
