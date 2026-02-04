#!/usr/bin/env python3
"""
Meeting Summarizer - Production Ready Version
Configured for mmkg.cloud relay
"""
import os
import sys
import requests
import json
from pathlib import Path

# Configuration from environment
TOKEN = os.getenv('ANTHROPIC_AUTH_TOKEN', 'your_claude_api_token_here')
ANTHROPIC_BASE = os.getenv('ANTHROPIC_BASE_URL', 'https://api.anthropic.com')
OPENAI_BASE = f"{ANTHROPIC_BASE}/openai/v1"

def analyze_transcript(transcript_text, metadata=None):
    """
    Analyze meeting transcript using Claude API

    Args:
        transcript_text: Meeting transcript text
        metadata: Optional metadata about the meeting

    Returns:
        dict with summary, decisions, and action_items
    """
    metadata_str = ""
    if metadata:
        metadata_str = f"\n\n**会议元数据：**\n"
        for key, value in metadata.items():
            metadata_str += f"- {key}: {value}\n"

    prompt = f"""请分析以下会议录音转录文本，并生成结构化摘要。

**转录文本：**
{transcript_text}
{metadata_str}

请按以下格式输出：

## 会议摘要
[用 2-3 段话概括会议的主要内容和讨论重点]

## 关键决策点
[列出会议中做出的重要决策，每个决策一行，使用 "- " 开头]

## 行动项
[列出需要执行的行动项，格式为：]
- [行动项描述] | 负责人: [姓名] | 截止日期: [日期]

请确保输出清晰、准确、可操作。如果某些信息在转录中不明确，请标注为 "待确认"。
"""

    print("  Calling Claude API...")

    response = requests.post(
        f"{ANTHROPIC_BASE}/v1/messages",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 4096,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Claude API Error: {response.status_code} - {response.text}")

    result = response.json()
    response_text = result['content'][0]['text']

    return parse_response(response_text)

def parse_response(response):
    """Parse Claude's structured response"""
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

def process_transcript_file(transcript_file):
    """Process a transcript text file"""
    print(f"\n{'='*60}")
    print(f"Processing transcript: {transcript_file}")
    print(f"{'='*60}\n")

    # Read transcript
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    print(f"✓ Transcript loaded ({len(transcript_text)} characters)")

    # Analyze
    print("\nAnalyzing with Claude...")
    analysis = analyze_transcript(transcript_text, {
        "file": Path(transcript_file).name
    })

    print(f"✓ Analysis complete")
    print(f"  - Summary: {len(analysis['summary'])} chars")
    print(f"  - Decisions: {len(analysis['decisions'])} items")
    print(f"  - Action items: {len(analysis['action_items'])} items")

    return analysis

def print_results(analysis):
    """Print formatted results"""
    print("\n" + "="*60)
    print("📝 MEETING SUMMARY")
    print("="*60)
    print(analysis['summary'])

    print("\n" + "="*60)
    print("✅ KEY DECISIONS")
    print("="*60)
    if analysis['decisions']:
        for i, decision in enumerate(analysis['decisions'], 1):
            print(f"{i}. {decision}")
    else:
        print("(无明确决策)")

    print("\n" + "="*60)
    print("🎯 ACTION ITEMS")
    print("="*60)
    if analysis['action_items']:
        for i, item in enumerate(analysis['action_items'], 1):
            print(f"\n{i}. {item['description']}")
            print(f"   👤 {item['assignee']}")
            print(f"   📅 {item['deadline']}")
    else:
        print("(无明确行动项)")

def save_results(analysis, output_file):
    """Save results to file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("MEETING SUMMARY\n")
        f.write("="*60 + "\n\n")
        f.write(analysis['summary'] + "\n\n")

        f.write("KEY DECISIONS\n")
        f.write("="*60 + "\n\n")
        if analysis['decisions']:
            for i, decision in enumerate(analysis['decisions'], 1):
                f.write(f"{i}. {decision}\n")
        else:
            f.write("(无明确决策)\n")

        f.write("\n\nACTION ITEMS\n")
        f.write("="*60 + "\n\n")
        if analysis['action_items']:
            for i, item in enumerate(analysis['action_items'], 1):
                f.write(f"{i}. {item['description']}\n")
                f.write(f"   Assignee: {item['assignee']}\n")
                f.write(f"   Deadline: {item['deadline']}\n\n")
        else:
            f.write("(无明确行动项)\n")

def main():
    print("="*60)
    print("Meeting Summarizer")
    print("="*60)

    if len(sys.argv) < 2:
        print("\nUsage: python summarize.py <transcript_file.txt>")
        print("\nNote: Due to Whisper API issues with the relay,")
        print("please provide a text transcript file instead of audio.")
        print("\nYou can:")
        print("1. Use Fireflies to export transcript as text")
        print("2. Use other transcription tools")
        print("3. Manually transcribe the audio")
        sys.exit(1)

    transcript_file = sys.argv[1]

    if not Path(transcript_file).exists():
        print(f"\n❌ File not found: {transcript_file}")
        sys.exit(1)

    try:
        # Process
        analysis = process_transcript_file(transcript_file)

        # Print
        print_results(analysis)

        # Save
        output_file = Path(transcript_file).stem + "_summary.txt"
        save_results(analysis, output_file)

        print("\n" + "="*60)
        print("✓ SUCCESS!")
        print("="*60)
        print(f"\n💾 Summary saved to: {output_file}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
