#!/usr/bin/env python3
"""
Meeting Summarizer - Enhanced Version with HTML & MD Output
生成纽约客风格 HTML 和优化的 Markdown 格式
"""
import os
import sys
import time
import requests
from pathlib import Path
from datetime import datetime

# Configuration
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY', 'your_assemblyai_api_key_here')
CLAUDE_TOKEN = "your_claude_api_token_here"
CLAUDE_BASE = "https://api.anthropic.com"

def transcribe_with_assemblyai(audio_file):
    """Transcribe audio using AssemblyAI"""
    if not ASSEMBLYAI_API_KEY:
        print("❌ ASSEMBLYAI_API_KEY not set")
        return None

    print(f"\n[1/4] Transcribing with AssemblyAI...")

    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }

    try:
        # Upload audio file
        print(f"  Uploading audio file...")
        with open(audio_file, 'rb') as f:
            upload_response = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers={'authorization': ASSEMBLYAI_API_KEY},
                data=f,
                timeout=300
            )

        if upload_response.status_code != 200:
            print(f"  ✗ Upload failed: {upload_response.status_code}")
            return None

        audio_url = upload_response.json()['upload_url']
        print(f"  ✓ Upload complete")

        # Request transcription
        print(f"  Requesting transcription...")
        transcript_request = {
            "audio_url": audio_url,
            "speech_models": ["universal-2"],
            "language_code": "zh",
            "speaker_labels": True,
            "punctuate": True,
            "format_text": True
        }

        transcript_response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers=headers,
            json=transcript_request,
            timeout=30
        )

        if transcript_response.status_code != 200:
            print(f"  ✗ Transcription request failed: {transcript_response.status_code}")
            return None

        transcript_id = transcript_response.json()['id']
        print(f"  ✓ Transcription started (ID: {transcript_id})")

        # Poll for completion
        print(f"  Processing...")
        polling_url = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'

        while True:
            polling_response = requests.get(polling_url, headers=headers, timeout=30)
            if polling_response.status_code != 200:
                print(f"  ✗ Polling failed: {polling_response.status_code}")
                return None

            result = polling_response.json()
            status = result['status']

            if status == 'completed':
                transcript = result['text']
                if result.get('utterances'):
                    formatted_transcript = "\n\n".join([
                        f"说话人 {u['speaker']}: {u['text']}"
                        for u in result['utterances']
                    ])
                    transcript = formatted_transcript

                print(f"  ✓ Transcription complete ({len(transcript)} characters)")
                if 'confidence' in result:
                    print(f"  ✓ Confidence: {result['confidence']*100:.1f}%")

                return transcript
            elif status == 'error':
                print(f"  ✗ Transcription failed: {result.get('error', 'Unknown error')}")
                return None

            time.sleep(3)

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def analyze_with_claude(transcript):
    """Analyze transcript with Claude - structured format"""
    print(f"\n[2/4] Analyzing with Claude...")

    prompt = f"""请分析以下会议录音转录文本，并生成结构化摘要。

**转录文本：**
{transcript}

请按以下格式输出：

## 会议摘要
[用 2-3 段话概括会议的主要内容和讨论重点]

## 关键决策点
[列出会议中做出的重要决策，每个决策一行，使用 "- " 开头]

## 行动项
[列出需要执行的行动项，格式为：]
- [行动项描述] | 负责人: [姓名] | 截止日期: [日期]

请确保输出清晰、准确、可操作。"""

    response = requests.post(
        f"{CLAUDE_BASE}/v1/messages",
        headers={
            "Authorization": f"Bearer {CLAUDE_TOKEN}",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Claude API Error: {response.status_code}")

    result = response.json()
    response_text = result['content'][0]['text']
    print(f"  ✓ Analysis complete")

    return parse_response(response_text), response_text

def parse_response(response):
    """Parse Claude's response into structured data"""
    sections = {
        "summary": "",
        "decisions": [],
        "action_items": []
    }

    current_section = None
    lines = response.split('\n')

    for line in lines:
        line = line.strip()

        if line.startswith('## 会议摘要'):
            current_section = 'summary'
            continue
        elif line.startswith('## 关键决策点'):
            current_section = 'decisions'
            continue
        elif line.startswith('## 行动项'):
            current_section = 'action_items'
            continue

        if not line or line.startswith('#'):
            continue

        if current_section == 'summary':
            sections['summary'] += line + '\n'
        elif current_section == 'decisions' and line.startswith('-'):
            sections['decisions'].append(line[1:].strip())
        elif current_section == 'action_items' and line.startswith('-'):
            parts = line[1:].split('|')
            action_item = {
                "description": parts[0].strip() if len(parts) > 0 else "",
                "assignee": parts[1].replace('负责人:', '').strip() if len(parts) > 1 else "待确认",
                "deadline": parts[2].replace('截止日期:', '').strip() if len(parts) > 2 else "待确认"
            }
            sections['action_items'].append(action_item)

    sections['summary'] = sections['summary'].strip()
    return sections

def generate_markdown_with_claude(analysis, filename):
    """Generate enhanced Markdown with Claude"""
    print(f"\n[3/4] Generating enhanced Markdown...")

    prompt = f"""请将以下会议摘要转换为优化的 Markdown 格式。

**会议文件**: {filename}
**日期**: {datetime.now().strftime('%Y年%m月%d日')}

**会议摘要**:
{analysis['summary']}

**关键决策点**:
{chr(10).join([f"- {d}" for d in analysis['decisions']])}

**行动项**:
{chr(10).join([f"- {item['description']} (负责人: {item['assignee']}, 截止: {item['deadline']})" for item in analysis['action_items']])}

请生成一个专业、清晰、易读的 Markdown 文档，包含：
1. 标题和元信息
2. 执行摘要（Executive Summary）
3. 详细的会议内容
4. 关键决策点（带编号）
5. 行动项清单（带复选框）
6. 下一步计划

使用适当的 Markdown 格式：标题、列表、引用、表格等。"""

    response = requests.post(
        f"{CLAUDE_BASE}/v1/messages",
        headers={
            "Authorization": f"Bearer {CLAUDE_TOKEN}",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Claude API Error: {response.status_code}")

    result = response.json()
    markdown_content = result['content'][0]['text']
    print(f"  ✓ Markdown generated")

    return markdown_content

def generate_html_with_claude(analysis, filename):
    """Generate New Yorker style HTML with Claude"""
    print(f"\n[4/4] Generating New Yorker style HTML...")

    prompt = f"""请将以下会议摘要转换为纽约客（New Yorker）风格的精美 HTML 页面。

**会议文件**: {filename}
**日期**: {datetime.now().strftime('%Y年%m月%d日')}

**会议摘要**:
{analysis['summary']}

**关键决策点**:
{chr(10).join([f"- {d}" for d in analysis['decisions']])}

**行动项**:
{chr(10).join([f"- {item['description']} (负责人: {item['assignee']}, 截止: {item['deadline']})" for item in analysis['action_items']])}

请生成一个完整的 HTML 页面，要求：

1. **设计风格**：
   - 纽约客杂志风格：优雅、专业、易读
   - 使用衬线字体（如 Georgia, Garamond）
   - 宽松的行距和留白
   - 精致的排版

2. **组件丰富**：
   - 页面头部：标题、日期、元信息
   - 执行摘要卡片（带背景色）
   - 会议内容区域（多栏布局）
   - 决策点时间线（带图标）
   - 行动项看板（卡片式）
   - 页脚：生成信息

3. **交互元素**：
   - 平滑滚动
   - 悬停效果
   - 响应式设计
   - 打印友好

4. **颜色方案**：
   - 主色：深灰色 (#2c3e50)
   - 强调色：深蓝色 (#3498db)
   - 背景：米白色 (#f8f9fa)
   - 卡片：白色带阴影

请生成完整的 HTML 代码（包含 CSS 和少量 JavaScript），可以直接在浏览器中打开。"""

    response = requests.post(
        f"{CLAUDE_BASE}/v1/messages",
        headers={
            "Authorization": f"Bearer {CLAUDE_TOKEN}",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 8192,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=90
    )

    if response.status_code != 200:
        raise Exception(f"Claude API Error: {response.status_code}")

    result = response.json()
    html_content = result['content'][0]['text']

    # Remove markdown code blocks if present
    if html_content.startswith('```html'):
        html_content = html_content.split('```html')[1].split('```')[0].strip()
    elif html_content.startswith('```'):
        html_content = html_content.split('```')[1].split('```')[0].strip()

    print(f"  ✓ HTML generated")

    return html_content

def main():
    print("="*60)
    print("Meeting Summarizer - Enhanced Version")
    print("="*60)

    if len(sys.argv) < 2:
        print("\nUsage: python assemblyai_enhanced.py <audio_file>")
        print("\nOutputs:")
        print("  1. Plain text summary (.txt)")
        print("  2. Enhanced Markdown (.md)")
        print("  3. New Yorker style HTML (.html)")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not Path(audio_file).exists():
        print(f"\n❌ File not found: {audio_file}")
        sys.exit(1)

    print(f"\n📁 Audio file: {audio_file}")
    filename = Path(audio_file).name
    base_name = Path(audio_file).stem

    try:
        # Step 1: Transcribe
        transcript = transcribe_with_assemblyai(audio_file)
        if not transcript:
            print("\n✗ Transcription failed")
            sys.exit(1)

        # Step 2: Analyze
        analysis, raw_analysis = analyze_with_claude(transcript)

        # Step 3: Generate Markdown
        markdown_content = generate_markdown_with_claude(analysis, filename)

        # Step 4: Generate HTML
        html_content = generate_html_with_claude(analysis, filename)

        # Save all formats
        print(f"\n{'='*60}")
        print("💾 Saving files...")
        print(f"{'='*60}")

        # 1. Plain text
        txt_file = f"{base_name}_summary.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"MEETING SUMMARY: {filename}\n")
            f.write("="*60 + "\n\n")
            f.write(raw_analysis)
        print(f"  ✓ Plain text: {txt_file}")

        # 2. Markdown
        md_file = f"{base_name}_summary.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"  ✓ Markdown: {md_file}")

        # 3. HTML
        html_file = f"{base_name}_summary.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  ✓ HTML: {html_file}")

        # Print summary
        print(f"\n{'='*60}")
        print("✓ SUCCESS!")
        print(f"{'='*60}")
        print(f"\n📝 Generated 3 formats:")
        print(f"  1. {txt_file} - Plain text summary")
        print(f"  2. {md_file} - Enhanced Markdown")
        print(f"  3. {html_file} - New Yorker style HTML")
        print(f"\n💡 Open HTML in browser:")
        print(f"  open {html_file}  # macOS")
        print(f"  xdg-open {html_file}  # Linux")
        print(f"  start {html_file}  # Windows")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
