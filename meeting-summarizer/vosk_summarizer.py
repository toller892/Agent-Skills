#!/usr/bin/env python3
"""
Meeting Summarizer - Vosk Version (Free, Offline)
使用 Vosk 进行免费离线语音识别
"""
import os
import sys
import json
import wave
from pathlib import Path
from vosk import Model, KaldiRecognizer, SetLogLevel

# Configuration
TOKEN = "your_claude_api_token_here"
ANTHROPIC_BASE = "https://api.anthropic.com"
VOSK_MODEL_PATH = os.path.expanduser("~/.meeting-summarizer/vosk-model-cn")

SetLogLevel(-1)  # Disable Vosk logs

def download_vosk_model():
    """Download Vosk Chinese model if not exists"""
    if Path(VOSK_MODEL_PATH).exists():
        return True

    print("\n⚠️  Vosk 中文模型未找到")
    print("\n请下载模型：")
    print("1. 访问：https://alphacephei.com/vosk/models")
    print("2. 下载：vosk-model-cn-0.22.zip（中文模型）")
    print("3. 解压到：~/.meeting-summarizer/vosk-model-cn/")
    print("\n或运行：")
    print("  wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip")
    print("  unzip vosk-model-cn-0.22.zip -d ~/.meeting-summarizer/")
    print("  mv ~/.meeting-summarizer/vosk-model-cn-0.22 ~/.meeting-summarizer/vosk-model-cn")

    return False

def convert_to_wav(audio_file):
    """Convert audio to WAV format for Vosk"""
    from pydub import AudioSegment

    output_file = Path(audio_file).stem + "_converted.wav"

    print(f"  Converting to WAV format...")

    # Load audio
    audio = AudioSegment.from_file(audio_file)

    # Convert to mono, 16kHz, 16-bit
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio = audio.set_sample_width(2)

    # Export
    audio.export(output_file, format="wav")

    print(f"  ✓ Converted to: {output_file}")
    return output_file

def transcribe_with_vosk(audio_file):
    """
    Transcribe audio using Vosk (Free, Offline)
    """
    print(f"\n[1/3] Transcribing with Vosk (offline)...")

    # Check model
    if not download_vosk_model():
        return None

    # Convert to WAV if needed
    if not audio_file.endswith('.wav'):
        try:
            audio_file = convert_to_wav(audio_file)
        except Exception as e:
            print(f"  ✗ Conversion failed: {e}")
            print("  Please install: pip install pydub")
            print("  And install ffmpeg: sudo apt install ffmpeg")
            return None

    # Load model
    print(f"  Loading Vosk model...")
    model = Model(VOSK_MODEL_PATH)

    # Open audio file
    wf = wave.open(audio_file, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 48000]:
        print("  ✗ Audio file must be WAV format mono PCM.")
        return None

    # Create recognizer
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # Transcribe
    print(f"  Transcribing...")
    transcript = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if 'text' in result:
                transcript += result['text'] + " "

    # Final result
    final_result = json.loads(rec.FinalResult())
    if 'text' in final_result:
        transcript += final_result['text']

    transcript = transcript.strip()

    print(f"  ✓ Transcription complete ({len(transcript)} characters)")

    return transcript

def analyze_with_claude(transcript):
    """Analyze transcript with Claude"""
    import requests

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
    print("Meeting Summarizer - Vosk Version (Free)")
    print("="*60)

    if len(sys.argv) < 2:
        print("\nUsage: python vosk_summarizer.py <audio_file>")
        print("\nSupported formats: mp3, wav, m4a, mp4")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not Path(audio_file).exists():
        print(f"\n❌ File not found: {audio_file}")
        sys.exit(1)

    print(f"\n📁 Audio file: {audio_file}")

    try:
        # Transcribe
        transcript = transcribe_with_vosk(audio_file)
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
