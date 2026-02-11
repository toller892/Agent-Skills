#!/usr/bin/env python3
"""
修复 Typst 语法问题
"""

import json
import re

def fix_typst_syntax(text):
    """修复 Typst 语法中的特殊字符"""
    if not text:
        return text
    
    # 转义 $ 符号
    text = re.sub(r'(?<!\\)\$', r'\\$', text)
    
    # 转义 % 符号
    text = re.sub(r'(?<!\\)%', r'\\%', text)
    
    # 转义 # 符号（不在行首时）
    text = re.sub(r'(?<!\\)#(?!\[)', r'\\#', text)
    
    # 转义 & 符号
    text = re.sub(r'(?<!\\)&', r'\\&', text)
    
    # 转义 _ 符号（不在 *...* 中时）
    text = re.sub(r'(?<!\\)_', r'\\_', text)
    
    # 转义 { 和 } 符号
    text = re.sub(r'(?<!\\)\{', r'\\{', text)
    text = re.sub(r'(?<!\\)\}', r'\\}', text)
    
    return text

def fix_json_data(json_file):
    """修复 JSON 数据中的 Typst 语法问题"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 修复标题和摘要
    if 'title' in data:
        data['title'] = fix_typst_syntax(data['title'])
    if 'subtitle' in data:
        data['subtitle'] = fix_typst_syntax(data['subtitle'])
    if 'summary' in data:
        data['summary'] = fix_typst_syntax(data['summary'])
    
    # 修复章节内容
    if 'sections' in data:
        for section in data['sections']:
            if 'heading' in section:
                section['heading'] = fix_typst_syntax(section['heading'])
            if 'content' in section:
                section['content'] = fix_typst_syntax(section['content'])
            
            # 修复表格数据
            if section.get('type') == 'table' and 'data' in section:
                fixed_data = []
                for row in section['data']:
                    fixed_row = [fix_typst_syntax(cell) for cell in row]
                    fixed_data.append(fixed_row)
                section['data'] = fixed_data
            
            # 修复列表项
            if section.get('type') in ['list', 'checklist'] and 'items' in section:
                section['items'] = [fix_typst_syntax(item) for item in section['items']]
    
    # 保存修复后的数据
    output_file = json_file.replace('.json', '_fixed.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 修复后的数据已保存到: {output_file}")
    return output_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "adcp_report_data.json"
    
    fixed_file = fix_json_data(json_file)
    print(f"原始文件: {json_file}")
    print(f"修复文件: {fixed_file}")