"""标记处理器 - 处理 ✅ 和 ⭐ 标记"""

import os
import re
import shutil
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class MarkProcessor:
    """处理文档中的阅读标记"""
    
    # 匹配标题行 (### [Title](url) ⭐⭐⭐)
    HEADING_PATTERN = re.compile(r"^(#{2,4})\s*\[(.+?)\]\((.+?)\)", re.MULTILINE)
    
    # 匹配操作行 (**操作**: [x] ✅ 已读  [ ] ❌ 跳过  [ ] ⭐ 收藏)
    ACTION_PATTERN = re.compile(r"\*\*操作\*\*:\s*\[([x ])\]\s*✅\s*已读\s*\[([x ])\]\s*❌\s*跳过\s*\[([x ])\]\s*⭐\s*收藏")
    
    # 标记类型
    MARK_READ = "✅"       # 已读删除
    MARK_SKIP = "❌"       # 跳过删除
    MARK_STAR = "⭐"       # 收藏归档
    
    def __init__(
        self,
        vault_path: str,
        digest_dir: str = "Daily Digest",
        archive_dir: str = "Daily Digest/Archive",
    ):
        self.vault_path = Path(vault_path).expanduser()
        self.digest_dir = self.vault_path / digest_dir
        self.archive_dir = self.vault_path / archive_dir
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def process_file(self, file_path: Path) -> Dict:
        """处理单个文件中的标记"""
        if not file_path.exists():
            return {"error": "File not found", "path": str(file_path)}
        
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        starred_items = []
        new_lines = []
        removed_count = 0
        starred_count = 0
        skipped_count = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 匹配标题行：### [Title](url)
            heading_match = self.HEADING_PATTERN.match(line)
            
            if heading_match:
                level, title, url = heading_match.groups()
                current_level = len(level)
                
                # 收集该条目的所有行（到下一个同级或更高级标题）
                item_lines = [line]
                i += 1
                action_mark = None
                
                while i < len(lines):
                    next_line = lines[i]
                    
                    # 检查是否遇到同级或更高级标题
                    if next_line.startswith("#"):
                        next_match = self.HEADING_PATTERN.match(next_line)
                        if next_match:
                            next_level = len(next_match.group(1))
                            if next_level <= current_level:
                                break
                    
                    # 检查操作行
                    action_match = self.ACTION_PATTERN.search(next_line)
                    if action_match:
                        read_checked, skip_checked, star_checked = action_match.groups()
                        if read_checked == "x":
                            action_mark = "read"
                        elif skip_checked == "x":
                            action_mark = "skip"
                        elif star_checked == "x":
                            action_mark = "star"
                    
                    item_lines.append(next_line)
                    i += 1
                
                # 根据操作处理
                if action_mark == "read":
                    # ✅ 已读 - 删除
                    removed_count += 1
                    continue
                
                elif action_mark == "skip":
                    # ❌ 跳过 - 删除
                    skipped_count += 1
                    removed_count += 1
                    continue
                
                elif action_mark == "star":
                    # ⭐ 收藏 - 归档并删除
                    starred_count += 1
                    starred_items.append({
                        "title": title,
                        "url": url,
                        "content": "\n".join(item_lines),
                    })
                    continue
                
                else:
                    # 无操作 - 保留
                    new_lines.extend(item_lines)
                    continue
            
            new_lines.append(line)
            i += 1
        
        # 归档收藏的内容
        if starred_items:
            self._archive_items(file_path.stem, starred_items)
        
        # 更新原文件
        if removed_count > 0 or starred_count > 0:
            new_content = "\n".join(new_lines)
            # 清理连续空行
            new_content = re.sub(r"\n{3,}", "\n\n", new_content)
            file_path.write_text(new_content, encoding="utf-8")
        
        return {
            "path": str(file_path),
            "removed": removed_count,
            "skipped": skipped_count,
            "starred": starred_count,
        }
    
    def _archive_items(self, date_str: str, items: List[Dict]) -> Path:
        """将收藏的内容归档"""
        archive_file = self.archive_dir / f"{date_str}-starred.md"
        
        # 追加到归档文件
        header = ""
        if not archive_file.exists():
            header = f"# ⭐ 收藏 - {date_str}\n\n"
            header += f"> 归档时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            header += "---\n\n"
        
        with archive_file.open("a", encoding="utf-8") as f:
            f.write(header)
            for item in items:
                title = item.get("title", "Untitled")
                url = item.get("url", "")
                content = item.get("content", "")
                
                # 移除标记符号，保留内容
                content = re.sub(r"\s*(✅|❌|⭐|👆)\s*$", "", content, flags=re.MULTILINE)
                f.write(content + "\n\n")
        
        return archive_file
    
    def process_all(self, days: int = 7) -> List[Dict]:
        """处理所有摘要文件"""
        results = []
        
        for file_path in sorted(self.digest_dir.glob("*.md")):
            # 跳过非日期文件
            if not re.match(r"\d{4}-\d{2}-\d{2}\.md", file_path.name):
                continue
            
            result = self.process_file(file_path)
            if result.get("removed", 0) > 0 or result.get("starred", 0) > 0:
                results.append(result)
        
        return results
    
    def cleanup_empty(self) -> List[Path]:
        """清理空的摘要文件（只剩 frontmatter 和说明）"""
        removed = []
        
        for file_path in self.digest_dir.glob("*.md"):
            content = file_path.read_text(encoding="utf-8")
            
            # 检查是否还有待处理的条目
            if "- [ ]" not in content and "- [✅]" not in content and "- [⭐]" not in content:
                # 更新状态为已完成
                if "status: unread" in content:
                    content = content.replace("status: unread", "status: completed")
                    file_path.write_text(content, encoding="utf-8")
                removed.append(file_path)
        
        return removed
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_files = 0
        total_unread = 0
        total_starred = 0
        
        for file_path in self.digest_dir.glob("*.md"):
            if not re.match(r"\d{4}-\d{2}-\d{2}\.md", file_path.name):
                continue
            
            total_files += 1
            content = file_path.read_text(encoding="utf-8")
            total_unread += content.count("- [ ]")
        
        # 统计归档数量
        for file_path in self.archive_dir.glob("*-starred.md"):
            content = file_path.read_text(encoding="utf-8")
            total_starred += content.count("- [ ]")
        
        return {
            "total_files": total_files,
            "unread_items": total_unread,
            "starred_items": total_starred,
        }


if __name__ == "__main__":
    # 测试
    processor = MarkProcessor("./test_vault")
    
    # 创建测试文件
    test_dir = Path("./test_vault/Daily Digest")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_content = """---
date: 2025-01-20
status: unread
---

# 📰 每日摘要

## 🔥 Hacker News

- [✅] **[已读文章](https://example.com)**
  > 这是已读的描述

- [⭐] **[收藏文章](https://example.com)**
  > 这是收藏的描述

- [ ] **[未处理文章](https://example.com)**
  > 这是未处理的描述
"""
    
    test_file = test_dir / "2025-01-20.md"
    test_file.write_text(test_content)
    
    result = processor.process_file(test_file)
    print(f"处理结果: {result}")
    print(f"\n处理后内容:\n{test_file.read_text()}")
