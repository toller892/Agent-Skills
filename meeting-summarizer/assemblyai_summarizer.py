#!/usr/bin/env python3
"""
Meeting Summarizer - AssemblyAI Version
使用 AssemblyAI 进行高质量语音识别
"""
import os
import sys
import time
import requests
from pathlib import Path

# Configuration
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY', 'your_assemblyai_api_key_here')  # 从环境变量读取，或使用默认值
CLAUDE_TOKEN = "your_claude_api_token_here"
CLAUDE_BASE = "https://api.anthropic.com"

def transcribe_with_assemblyai(audio_file):
    """
    Transcribe audio using AssemblyAI
    高质量转录，支持说话人识别
    """
    if not ASSEMBLYAI_API_KEY:
        print("❌ ASSEMBLYAI_API_KEY not set")
        print("\n请设置 API Key：")
        print("  export ASSEMBLYAI_API_KEY='aai_...'")
        print("\n或在脚本中直接配置")
        return None

    print(f"\n[1/3] Transcribing with AssemblyAI...")

    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }

    try:
        # Step 1: Upload audio file
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
            print(f"  Response: {upload_response.text}")
            return None

        audio_url = upload_response.json()['upload_url']
        print(f"  ✓ Upload complete")

        # Step 2: Request transcription
        print(f"  Requesting transcription...")

        transcript_request = {
            "audio_url": audio_url,
            "speech_models": ["universal-2"],  # 使用 universal-2 模型
            "language_code": "zh",   # 中文
            "speaker_labels": True,  # 说话人识别
            "punctuate": True,       # 智能标点
            "format_text": True      # 格式化文本
        }

        transcript_response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers=headers,
            json=transcript_request,
            timeout=30
        )

        if transcript_response.status_code != 200:
            print(f"  ✗ Transcription request failed: {transcript_response.status_code}")
            print(f"  Response: {transcript_response.text}")
            return None

        transcript_id = transcript_response.json()['id']
        print(f"  ✓ Transcription started (ID: {transcript_id})")

        # Step 3: Poll for completion
        print(f"  Processing (this may take a few minutes)...")

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

                # Add speaker information if available
                if result.get('utterances'):
                    formatted_transcript = "\n\n".join([
                        f"说话人 {u['speaker']}: {u['text']}"
                        for u in result['utterances']
                    ])
                    transcript = formatted_transcript

                print(f"  ✓ Transcription complete ({len(transcript)} characters)")

                # Show confidence score
                if 'confidence' in result:
                    confidence = result['confidence'] * 100
                    print(f"  ✓ Confidence: {confidence:.1f}%")

                return transcript

            elif status == 'error':
                print(f"  ✗ Transcription failed: {result.get('error', 'Unknown error')}")
                return None

            # Still processing
            time.sleep(3)

    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_with_claude(transcript):
    """Analyze transcript with Claude"""
    print(f"\n[2/3] Analyzing with Claude...")

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

def main():
    print("="*60)
    print("Meeting Summarizer - AssemblyAI Version")
    print("="*60)

    if len(sys.argv) < 2:
        print("\nUsage: python assemblyai_summarizer.py <audio_file>")
        print("\nSupported formats: mp3, wav, m4a, mp4")
        print("\nFeatures:")
        print("  ✓ High accuracy transcription")
        print("  ✓ Speaker identification")
        print("  ✓ Smart punctuation")
        print("  ✓ Chinese language support")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not Path(audio_file).exists():
        print(f"\n❌ File not found: {audio_file}")
        sys.exit(1)

    print(f"\n📁 Audio file: {audio_file}")

    try:
        # Transcribe
        transcript = transcribe_with_assemblyai(audio_file)
        if not transcript:
            print("\n✗ Transcription failed")
            sys.exit(1)

        # Analyze
        analysis = analyze_with_claude(transcript)

        # Print results
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

        # Save
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
