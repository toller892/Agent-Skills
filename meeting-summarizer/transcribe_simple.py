#!/usr/bin/env python3
"""
Meeting Transcriber - Simple Real-time Transcription
实时转录会议录音，按发言人分段，输出 Markdown
"""
import os
import sys
import time
import requests
from pathlib import Path
from datetime import datetime

# Configuration
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY', 'your_assemblyai_api_key_here')

def transcribe_audio(audio_file):
    """
    Transcribe audio with speaker labels using AssemblyAI
    """
    if not ASSEMBLYAI_API_KEY or ASSEMBLYAI_API_KEY == 'your_assemblyai_api_key_here':
        print("❌ ASSEMBLYAI_API_KEY not set")
        print("\n请设置 API Key：")
        print("  export ASSEMBLYAI_API_KEY='your_api_key'")
        return None

    print(f"\n[1/2] 上传音频文件...")

    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }

    try:
        # Upload audio file
        with open(audio_file, 'rb') as f:
            upload_response = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers={'authorization': ASSEMBLYAI_API_KEY},
                data=f,
                timeout=300
            )

        if upload_response.status_code != 200:
            print(f"  ✗ 上传失败: {upload_response.status_code}")
            return None

        audio_url = upload_response.json()['upload_url']
        print(f"  ✓ 上传完成")

        # Request transcription with speaker labels
        print(f"\n[2/2] 开始转录...")
        transcript_request = {
            "audio_url": audio_url,
            "speech_models": ["universal-2"],
            "language_code": "zh",
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
            print(f"  ✗ 转录请求失败: {transcript_response.status_code}")
            return None

        transcript_id = transcript_response.json()['id']
        print(f"  ✓ 转录任务已创建")

        # Poll for completion
        print(f"  ⏳ 处理中（这可能需要几分钟）...")
        polling_url = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'

        while True:
            polling_response = requests.get(polling_url, headers=headers, timeout=30)

            if polling_response.status_code != 200:
                print(f"  ✗ 查询失败: {polling_response.status_code}")
                return None

            result = polling_response.json()
            status = result['status']

            if status == 'completed':
                print(f"  ✓ 转录完成")

                # Get utterances (speaker-separated segments)
                utterances = result.get('utterances', [])
                confidence = result.get('confidence', 0)

                print(f"  ✓ 准确率: {confidence*100:.1f}%")
                print(f"  ✓ 发言段落: {len(utterances)} 段")

                return {
                    'utterances': utterances,
                    'confidence': confidence,
                    'audio_duration': result.get('audio_duration', 0)
                }

            elif status == 'error':
                print(f"  ✗ 转录失败: {result.get('error', 'Unknown error')}")
                return None

            time.sleep(3)

    except Exception as e:
        print(f"  ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_markdown(transcription_data, filename):
    """
    Generate Markdown transcript with speaker labels
    """
    utterances = transcription_data['utterances']
    confidence = transcription_data['confidence']
    duration = transcription_data['audio_duration']

    # Build markdown content
    md_content = f"""# 会议转录

**文件名**: {filename}
**转录时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
**音频时长**: {duration/1000:.1f} 秒
**准确率**: {confidence*100:.1f}%
**发言段落**: {len(utterances)} 段

---

## 转录内容

"""

    # Add each utterance with speaker label
    for i, utterance in enumerate(utterances, 1):
        speaker = utterance.get('speaker', 'Unknown')
        text = utterance.get('text', '')
        start = utterance.get('start', 0) / 1000  # Convert to seconds

        # Format timestamp
        minutes = int(start // 60)
        seconds = int(start % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"

        md_content += f"### [{timestamp}] 说话人 {speaker}\n\n"
        md_content += f"{text}\n\n"
        md_content += "---\n\n"

    return md_content

def main():
    print("="*60)
    print("Meeting Transcriber - 实时转录")
    print("="*60)

    if len(sys.argv) < 2:
        print("\n用法: python transcribe_simple.py <audio_file>")
        print("\n支持格式: mp3, wav, m4a, mp4")
        print("\n输出: Markdown 格式转录文档（按发言人分段）")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not Path(audio_file).exists():
        print(f"\n❌ 文件不存在: {audio_file}")
        sys.exit(1)

    print(f"\n📁 音频文件: {audio_file}")
    filename = Path(audio_file).name
    base_name = Path(audio_file).stem

    try:
        # Transcribe
        transcription_data = transcribe_audio(audio_file)

        if not transcription_data:
            print("\n✗ 转录失败")
            sys.exit(1)

        # Generate Markdown
        print(f"\n[3/3] 生成 Markdown 文档...")
        markdown_content = generate_markdown(transcription_data, filename)

        # Save Markdown
        md_file = f"{base_name}_transcript.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"  ✓ 已保存: {md_file}")

        # Print summary
        print(f"\n{'='*60}")
        print("✓ 转录完成！")
        print(f"{'='*60}")
        print(f"\n📝 输出文件: {md_file}")
        print(f"📊 发言段落: {len(transcription_data['utterances'])} 段")
        print(f"⏱️  音频时长: {transcription_data['audio_duration']/1000:.1f} 秒")
        print(f"✅ 准确率: {transcription_data['confidence']*100:.1f}%")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
