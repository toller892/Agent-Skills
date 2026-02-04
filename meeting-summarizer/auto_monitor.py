#!/usr/bin/env python3
"""
Meeting Summarizer - Complete Automation
完整自动化版本：监控文件夹 → 转录 → 分析 → 通知
"""
import os
import sys
import time
import requests
import hashlib
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
TOKEN = "your_claude_api_token_here"
ANTHROPIC_BASE = "https://api.anthropic.com"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # 需要设置
SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK_URL')  # 需要设置

WATCH_FOLDER = os.path.expanduser("~/meeting-recordings")
CACHE_DIR = os.path.expanduser("~/.meeting-summarizer/cache")
PROCESSED_FILE = os.path.expanduser("~/.meeting-summarizer/processed.json")

# Ensure directories exist
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

def load_processed():
    """Load list of processed files"""
    if Path(PROCESSED_FILE).exists():
        with open(PROCESSED_FILE, 'r') as f:
            return json.load(f)
    return []

def save_processed(file_hash):
    """Save processed file hash"""
    processed = load_processed()
    if file_hash not in processed:
        processed.append(file_hash)
        with open(PROCESSED_FILE, 'w') as f:
            json.dump(processed, f)

def get_file_hash(file_path):
    """Calculate file hash"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def transcribe_audio(audio_file):
    """
    Transcribe audio using Whisper API
    需要 OPENAI_API_KEY
    """
    if not OPENAI_API_KEY:
        print("⚠️  OPENAI_API_KEY not set, skipping transcription")
        print("   Please set: export OPENAI_API_KEY='sk-...'")
        return None

    print(f"  [1/3] Transcribing audio...")

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        with open(audio_file, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )

        print(f"  ✓ Transcription complete ({len(transcript)} characters)")
        return transcript

    except Exception as e:
        print(f"  ✗ Transcription failed: {e}")
        return None

def analyze_with_claude(transcript):
    """Analyze transcript with Claude"""
    print(f"  [2/3] Analyzing with Claude...")

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
        f"{ANTHROPIC_BASE}/v1/messages",
        headers={
            "Authorization": f"Bearer {TOKEN}",
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

    print(f"  ✓ Claude analysis complete")
    return parse_response(response_text)

def parse_response(response):
    """Parse Claude's response"""
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

def send_to_slack(analysis, filename):
    """Send summary to Slack"""
    if not SLACK_WEBHOOK:
        print("  ⚠️  SLACK_WEBHOOK_URL not set, skipping notification")
        return False

    print(f"  [3/3] Sending to Slack...")

    # Format decisions
    decisions_text = "\n".join([f"• {d}" for d in analysis['decisions']]) if analysis['decisions'] else "(无明确决策)"

    # Format action items
    action_items_text = ""
    if analysis['action_items']:
        for item in analysis['action_items']:
            action_items_text += f"• {item['description']}\n"
            action_items_text += f"  👤 {item['assignee']} | 📅 {item['deadline']}\n"
    else:
        action_items_text = "(无明确行动项)"

    message = {
        "text": f"📝 会议摘要已生成: {filename}",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"📝 会议摘要: {filename}"}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*会议摘要*\n{analysis['summary']}"}
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*✅ 关键决策点*\n{decisions_text}"}
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*🎯 行动项*\n{action_items_text}"}
            }
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK, json=message, timeout=10)
        if response.status_code == 200:
            print(f"  ✓ Slack notification sent")
            return True
        else:
            print(f"  ✗ Slack notification failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Slack notification error: {e}")
        return False

def process_audio_file(audio_file):
    """Process a single audio file"""
    print(f"\n{'='*60}")
    print(f"Processing: {Path(audio_file).name}")
    print(f"{'='*60}")

    # Check if already processed
    file_hash = get_file_hash(audio_file)
    if file_hash in load_processed():
        print("  ⚠️  File already processed, skipping")
        return

    try:
        # Step 1: Transcribe
        transcript = transcribe_audio(audio_file)
        if not transcript:
            print("  ✗ Skipping analysis (no transcript)")
            return

        # Step 2: Analyze with Claude
        analysis = analyze_with_claude(transcript)

        # Step 3: Send to Slack
        send_to_slack(analysis, Path(audio_file).name)

        # Save results
        output_file = Path(audio_file).stem + "_summary.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"MEETING SUMMARY: {Path(audio_file).name}\n")
            f.write("="*60 + "\n\n")
            f.write(analysis['summary'] + "\n\n")
            f.write("KEY DECISIONS\n")
            f.write("="*60 + "\n\n")
            for i, decision in enumerate(analysis['decisions'], 1):
                f.write(f"{i}. {decision}\n")
            f.write("\n\nACTION ITEMS\n")
            f.write("="*60 + "\n\n")
            for i, item in enumerate(analysis['action_items'], 1):
                f.write(f"{i}. {item['description']}\n")
                f.write(f"   Assignee: {item['assignee']}\n")
                f.write(f"   Deadline: {item['deadline']}\n\n")

        print(f"\n  ✓ Summary saved to: {output_file}")

        # Mark as processed
        save_processed(file_hash)

        print(f"\n{'='*60}")
        print("✓ Processing complete!")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n  ✗ Error: {e}")
        import traceback
        traceback.print_exc()

class MeetingFileHandler(FileSystemEventHandler):
    """Handle new audio files"""

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path

        # Check if it's an audio file
        if file_path.endswith(('.mp3', '.m4a', '.wav', '.mp4')):
            print(f"\n🔔 New file detected: {Path(file_path).name}")

            # Wait a bit to ensure file is fully written
            time.sleep(2)

            # Process the file
            process_audio_file(file_path)

def main():
    print("="*60)
    print("Meeting Summarizer - Auto Monitor")
    print("="*60)

    print(f"\n📁 Monitoring folder: {WATCH_FOLDER}")
    print(f"💾 Cache directory: {CACHE_DIR}")

    # Check configuration
    if not OPENAI_API_KEY:
        print("\n⚠️  WARNING: OPENAI_API_KEY not set")
        print("   Transcription will be skipped")
        print("   Set with: export OPENAI_API_KEY='sk-...'")

    if not SLACK_WEBHOOK:
        print("\n⚠️  WARNING: SLACK_WEBHOOK_URL not set")
        print("   Slack notifications will be skipped")
        print("   Set with: export SLACK_WEBHOOK_URL='https://hooks.slack.com/...'")

    print(f"\n✓ Ready! Drop audio files into: {WATCH_FOLDER}")
    print("  Press Ctrl+C to stop\n")

    # Set up file system observer
    event_handler = MeetingFileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping monitor...")
        observer.stop()

    observer.join()
    print("✓ Monitor stopped")


if __name__ == '__main__':
    main()
