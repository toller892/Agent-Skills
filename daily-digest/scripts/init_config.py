#!/usr/bin/env python3
"""
初始化配置脚本

使用方法:
    python init_config.py --vault ~/Obsidian/MyVault
"""

import sys
import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="初始化 Daily Digest 配置")
    parser.add_argument("--vault", type=str, required=True, help="Obsidian Vault 路径")
    parser.add_argument("--force", action="store_true", help="覆盖现有配置")
    args = parser.parse_args()
    
    vault_path = Path(args.vault).expanduser().absolute()
    
    # 检查 vault 是否存在
    if not vault_path.exists():
        print(f"❌ Vault 路径不存在: {vault_path}")
        print("请确认 Obsidian Vault 路径正确")
        sys.exit(1)
    
    # 检查是否是 Obsidian vault
    obsidian_dir = vault_path / ".obsidian"
    if not obsidian_dir.exists():
        print(f"⚠️ 警告: {vault_path} 可能不是 Obsidian Vault（未找到 .obsidian 目录）")
        response = input("是否继续? [y/N] ")
        if response.lower() != "y":
            sys.exit(0)
    
    # 复制配置文件
    script_dir = Path(__file__).parent.parent
    example_config = script_dir / "config.example.yaml"
    target_config = script_dir / "config.yaml"
    
    if target_config.exists() and not args.force:
        print(f"⚠️ 配置文件已存在: {target_config}")
        print("使用 --force 覆盖")
        sys.exit(1)
    
    # 读取示例配置并替换路径
    with open(example_config, "r", encoding="utf-8") as f:
        config_content = f.read()
    
    # 替换 vault 路径
    config_content = config_content.replace(
        "vault_path: ~/Obsidian/MyVault",
        f"vault_path: {vault_path}"
    )
    
    # 写入配置
    with open(target_config, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print(f"✅ 配置文件已创建: {target_config}")
    
    # 创建目录结构
    digest_dir = vault_path / "Daily Digest"
    archive_dir = digest_dir / "Archive"
    
    digest_dir.mkdir(exist_ok=True)
    archive_dir.mkdir(exist_ok=True)
    
    print(f"✅ 已创建目录: {digest_dir}")
    print(f"✅ 已创建目录: {archive_dir}")
    
    print("\n🎉 初始化完成!")
    print("\n下一步:")
    print("  1. 编辑 config.yaml 添加你的 Newsletter 订阅源")
    print("  2. 运行 python scripts/fetch_digest.py 生成第一份摘要")
    print("  3. 在 Obsidian 中打开查看")


if __name__ == "__main__":
    main()
