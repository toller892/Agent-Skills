#!/usr/bin/env python3
"""
解析 Markdown 文件并转换为 JSON 格式，用于 Typst 报告生成
"""

import json
import re
from datetime import datetime
from pathlib import Path

def parse_markdown_to_json(markdown_file):
    """将 Markdown 文件解析为 JSON 数据结构"""
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 初始化数据结构
    data = {
        "title": "",
        "subtitle": "",
        "author": "AI 生成",
        "summary": "",
        "sections": [],
        "metrics": [],
        "code_blocks": []
    }
    
    # 提取标题（第一个 # 开头的行）
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('# '):
            data["title"] = line[2:].strip()
            break
    
    # 提取副标题（第二个 # 开头的行或特殊标记）
    for i, line in enumerate(lines):
        if line.startswith('## ') and not data["subtitle"]:
            data["subtitle"] = line[3:].strip()
            break
    
    # 解析内容为章节
    sections = []
    current_section = None
    current_content = []
    
    for line in lines:
        # 检测章节标题
        if line.startswith('# '):
            if current_section:
                current_section["content"] = '\n'.join(current_content).strip()
                sections.append(current_section)
            current_section = {
                "heading": line[2:].strip(),
                "level": 1,
                "type": "text",
                "content": ""
            }
            current_content = []
        elif line.startswith('## '):
            if current_section:
                current_section["content"] = '\n'.join(current_content).strip()
                sections.append(current_section)
            current_section = {
                "heading": line[3:].strip(),
                "level": 2,
                "type": "text",
                "content": ""
            }
            current_content = []
        elif line.startswith('### '):
            if current_section:
                current_section["content"] = '\n'.join(current_content).strip()
                sections.append(current_section)
            current_section = {
                "heading": line[4:].strip(),
                "level": 3,
                "type": "text",
                "content": ""
            }
            current_content = []
        elif line.startswith('---') or line.startswith('***'):
            # 分隔符，结束当前章节
            if current_section:
                current_section["content"] = '\n'.join(current_content).strip()
                sections.append(current_section)
                current_section = None
                current_content = []
        else:
            if current_section:
                current_content.append(line)
            else:
                # 开头的摘要内容
                if line.strip() and not data["summary"]:
                    data["summary"] = line.strip()
    
    # 添加最后一个章节
    if current_section:
        current_section["content"] = '\n'.join(current_content).strip()
        sections.append(current_section)
    
    # 处理特殊格式
    processed_sections = []
    for section in sections:
        heading = section["heading"]
        content = section["content"]
        
        # 检查是否为表格
        if '|' in content and '---' in content:
            lines = content.split('\n')
            table_lines = []
            for line in lines:
                if '|' in line:
                    table_lines.append(line)
            
            if len(table_lines) >= 3:
                # 提取表头和数据
                headers = [h.strip() for h in table_lines[0].split('|')[1:-1]]
                data_rows = []
                for row_line in table_lines[2:]:
                    if '|' in row_line:
                        row_data = [d.strip() for d in row_line.split('|')[1:-1]]
                        data_rows.append(row_data)
                
                processed_sections.append({
                    "heading": heading,
                    "level": section["level"],
                    "type": "table",
                    "headers": headers,
                    "data": data_rows
                })
                continue
        
        # 检查是否为列表
        if any(line.strip().startswith(('-', '+', '*', '1.', '2.', '3.')) for line in content.split('\n')):
            items = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith(('- ', '+ ', '* ', '1. ', '2. ', '3. ')):
                    item = line[2:].strip()
                    if item:
                        items.append(item)
            
            if items:
                processed_sections.append({
                    "heading": heading,
                    "level": section["level"],
                    "type": "list",
                    "items": items
                })
                continue
        
        # 普通文本章节
        processed_sections.append({
            "heading": heading,
            "level": section["level"],
            "type": "text",
            "content": content
        })
    
    data["sections"] = processed_sections
    
    # 添加一些指标数据
    data["metrics"] = [
        {"label": "文档长度", "value": f"{len(content)} 字符", "change": 0},
        {"label": "章节数量", "value": f"{len(processed_sections)} 个", "change": 0},
        {"label": "表格数量", "value": f"{sum(1 for s in processed_sections if s['type'] == 'table')} 个", "change": 0},
    ]
    
    return data

def main():
    # 解析 AdCP 文件
    markdown_file = "AdCP_推特风格解读.md"
    output_file = "adcp_report_data.json"
    
    print(f"解析文件: {markdown_file}")
    
    try:
        data = parse_markdown_to_json(markdown_file)
        
        # 保存为 JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ JSON 数据已保存到: {output_file}")
        print(f"  标题: {data['title']}")
        print(f"  章节数: {len(data['sections'])}")
        print(f"  指标数: {len(data['metrics'])}")
        
        return data
        
    except Exception as e:
        print(f"✗ 解析失败: {e}")
        return None

if __name__ == "__main__":
    main()