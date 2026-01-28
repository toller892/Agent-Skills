#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Key 管理器
安全管理和验证 API Key
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
import getpass

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class APIKeyConfig:
    """API Key配置类"""

    provider: str
    key: str = ""
    is_valid: bool = False
    last_checked: str = ""


class APIKeyManager:
    """API Key 管理器主类"""

    # 默认配置文件名
    DEFAULT_CONFIG_FILE = ".api_keys.json"

    # 环境变量名
    GEMINI_API_KEY_ENV = "GEMINI_API_KEY"

    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化 API Key 管理器

        Args:
            config_dir: 配置文件目录，默认当前目录
        """
        self.config_dir = Path(config_dir) if config_dir else Path.cwd()
        self.config_file = self.config_dir / self.DEFAULT_CONFIG_FILE
        self.keys: Dict[str, APIKeyConfig] = {}
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config_data = json.load(f)

                for provider, data in config_data.items():
                    self.keys[provider] = APIKeyConfig(
                        provider=provider,
                        key=data.get("key", ""),
                        is_valid=data.get("is_valid", False),
                        last_checked=data.get("last_checked", ""),
                    )

                logger.info(
                    f"从 {self.config_file} 加载了 {len(self.keys)} 个 API Key 配置"
                )

            except Exception as e:
                logger.warning(f"加载配置文件失败: {e}")

    def _save_config(self):
        """保存配置文件"""
        try:
            config_data = {}
            for provider, config in self.keys.items():
                config_data[provider] = {
                    "key": config.key,
                    "is_valid": config.is_valid,
                    "last_checked": config.last_checked,
                }

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)

            logger.info(f"配置已保存到 {self.config_file}")

        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")

    def set_api_key(self, provider: str, key: str, auto_validate: bool = True):
        """
        设置 API Key

        Args:
            provider: 服务提供商名称
            key: API Key
            auto_validate: 是否自动验证
        """
        # 清理 key（移除空格）
        cleaned_key = key.strip()

        self.keys[provider] = APIKeyConfig(
            provider=provider, key=cleaned_key, is_valid=False
        )

        logger.info(f"已设置 {provider} 的 API Key")

        if auto_validate:
            self.validate_key(provider)

        self._save_config()

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        获取 API Key

        Args:
            provider: 服务提供商名称

        Returns:
            Optional[str]: API Key，如果不存在则返回 None
        """
        # 首先检查内存中的配置
        if provider in self.keys:
            return self.keys[provider].key

        # 检查环境变量
        env_var = f"{provider.upper()}_API_KEY"
        env_key = os.environ.get(env_var)
        if env_key:
            return env_key

        # 检查通用环境变量
        if provider.lower() == "gemini":
            gemini_key = os.environ.get(self.GEMINI_API_KEY_ENV)
            if gemini_key:
                return gemini_key

        return None

    def validate_key(self, provider: str) -> bool:
        """
        验证 API Key 是否有效

        Args:
            provider: 服务提供商名称

        Returns:
            bool: 是否有效
        """
        key = self.get_api_key(provider)

        if not key:
            logger.warning(f"{provider} 的 API Key 不存在")
            return False

        # 基本的格式验证
        is_valid = self._basic_validation(provider, key)

        if provider in self.keys:
            from datetime import datetime

            self.keys[provider].is_valid = is_valid
            self.keys[provider].last_checked = datetime.now().isoformat()

        self._save_config()

        if is_valid:
            logger.info(f"{provider} 的 API Key 验证成功")
        else:
            logger.warning(f"{provider} 的 API Key 验证失败")

        return is_valid

    def _basic_validation(self, provider: str, key: str) -> bool:
        """
        基本格式验证

        Args:
            provider: 服务提供商
            key: API Key

        Returns:
            bool: 格式是否正确
        """
        if not key or len(key) < 10:
            return False

        # Gemini API Key 通常是 base64 编码的字符串
        if provider.lower() == "gemini":
            # Gemini Key 通常是 39 个字符的 base64 字符串
            return len(key) >= 20 and not any(c.isspace() for c in key)

        return True

    def remove_api_key(self, provider: str):
        """
        移除 API Key

        Args:
            provider: 服务提供商名称
        """
        if provider in self.keys:
            del self.keys[provider]
            self._save_config()
            logger.info(f"已移除 {provider} 的 API Key")

    def list_providers(self) -> list:
        """
        列出所有已配置的服务提供商

        Returns:
            list: 服务提供商列表
        """
        return list(self.keys.keys())

    def get_key_status(self, provider: str) -> Dict:
        """
        获取 API Key 状态

        Args:
            provider: 服务提供商名称

        Returns:
            Dict: 状态信息
        """
        key = self.get_api_key(provider)

        if provider in self.keys:
            config = self.keys[provider]
            return {
                "provider": provider,
                "has_key": bool(key),
                "is_valid": config.is_valid,
                "last_checked": config.last_checked,
                "key_length": len(key) if key else 0,
                "masked_key": self._mask_key(key) if key else None,
            }

        return {
            "provider": provider,
            "has_key": bool(key),
            "is_valid": False,
            "last_checked": None,
            "key_length": len(key) if key else 0,
            "masked_key": self._mask_key(key) if key else None,
        }

    def _mask_key(self, key: str) -> str:
        """
        遮盖 API Key（显示前后字符）

        Args:
            key: 原始 key

        Returns:
            str: 遮盖后的 key
        """
        if len(key) <= 8:
            return "*" * len(key)

        return f"{key[:4]}{'*' * (len(key) - 8)}{key[-4:]}"

    def interactive_setup(self, provider: str = "gemini"):
        """
        交互式设置 API Key

        Args:
            provider: 服务提供商名称
        """
        print(f"\n🔐 {provider.upper()} API Key 设置")
        print("-" * 40)

        # 检查是否已有 key
        existing_key = self.get_api_key(provider)
        if existing_key:
            status = self.get_key_status(provider)
            print(f"✓ 已配置 API Key")
            print(f"  状态: {'有效' if status['is_valid'] else '无效'}")
            print(f"  遮盖: {status['masked_key']}")

            change = input("\n是否更改? (y/n): ").strip().lower()
            if change != "y":
                print("取消设置")
                return

        # 输入新的 key
        print("\n请输入您的 API Key:")
        print("(Key 不会显示在屏幕上)")

        try:
            key = getpass.getpass("API Key: ")
        except:
            key = input("API Key: ")

        if not key.strip():
            print("✗ 未输入 API Key")
            return

        # 设置并验证
        self.set_api_key(provider, key)

        # 检查状态
        status = self.get_key_status(provider)
        if status["is_valid"]:
            print(f"\n✓ API Key 设置成功!")
            print(f"  Key: {status['masked_key']}")
        else:
            print(f"\n⚠ API Key 已设置，但验证失败")
            print("  请确保 Key 格式正确")

    def setup_from_environment(self, provider: str = "gemini"):
        """
        从环境变量设置 API Key

        Args:
            provider: 服务提供商名称
        """
        key = self.get_api_key(provider)

        if key:
            self.set_api_key(provider, key, auto_validate=True)
            logger.info(f"已从环境变量加载 {provider} 的 API Key")
        else:
            logger.warning(f"未找到 {provider} 的环境变量")


class GeminiKeyManager(APIKeyManager):
    """专门管理 Gemini API Key 的类"""

    def __init__(self):
        """初始化 Gemini Key 管理器"""
        super().__init__()
        self.provider = "gemini"

    def get_gemini_key(self) -> Optional[str]:
        """
        获取 Gemini API Key

        Returns:
            Optional[str]: API Key
        """
        return self.get_api_key(self.provider)

    def setup_gemini_key(self, key: str):
        """设置 Gemini API Key"""
        self.set_api_key(self.provider, key)

    def validate_gemini_key(self) -> bool:
        """验证 Gemini API Key"""
        return self.validate_key(self.provider)

    def check_gemini_key_status(self) -> Dict:
        """检查 Gemini Key 状态"""
        return self.get_key_status(self.provider)

    def interactive_gemini_setup(self):
        """交互式设置 Gemini Key"""
        self.interactive_setup(self.provider)


# 测试代码
if __name__ == "__main__":
    # 测试 API Key 管理器
    manager = APIKeyManager()

    # 交互式设置
    print("API Key 管理器测试")
    print("=" * 40)

    # 检查状态
    status = manager.get_key_status("gemini")
    print(f"Gemini Key 状态:")
    print(f"  是否有 Key: {status['has_key']}")
    print(f"  是否有效: {status['is_valid']}")
    print(f"  Key 遮盖: {status['masked_key']}")

    # 列出所有提供商
    providers = manager.list_providers()
    print(f"\n已配置的提供商: {providers}")
