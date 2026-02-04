#!/usr/bin/env python3
"""
Quick test script for meeting summarizer with third-party API relay
"""
import os
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from meeting_summarizer.processor import MeetingProcessor


def main():
    print("="*60)
    print("Meeting Summarizer - Quick Test")
    print("="*60)

    # Check for API keys in environment
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')

    if not openai_key:
        print("\n⚠️  OPENAI_API_KEY not found in environment")
        print("Please set it first:")
        print("  export OPENAI_API_KEY='your-key'")
        sys.exit(1)

    if not anthropic_key:
        print("\n⚠️  ANTHROPIC_API_KEY not found in environment")
        print("Please set it first:")
        print("  export ANTHROPIC_API_KEY='your-key'")
        sys.exit(1)

    # Audio file
    audio_file = "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"

    if not Path(audio_file).exists():
        print(f"\n⚠️  Audio file not found: {audio_file}")
        sys.exit(1)

    print(f"\n✓ OpenAI API key found: {openai_key[:10]}...")
    print(f"✓ Anthropic API key found: {anthropic_key[:10]}...")
    print(f"✓ Audio file found: {audio_file}")

    # Create config
    config = {
        'openai': {'api_key': openai_key},
        'anthropic': {'api_key': anthropic_key},
        'slack': {'webhook_url': None},  # Skip Slack for now
        'processing': {
            'cache_dir': os.path.expanduser('~/.meeting-summarizer/cache'),
            'cache_transcripts': True
        }
    }

    # Create cache directory
    os.makedirs(config['processing']['cache_dir'], exist_ok=True)

    print("\n" + "="*60)
    print("Starting processing...")
    print("="*60)

    processor = MeetingProcessor(config)

    try:
        result = processor.process(audio_file)

        # Print results
        print("\n" + "="*60)
        print("📝 MEETING SUMMARY")
        print("="*60)
        print(result['analysis']['summary'])

        print("\n" + "="*60)
        print("✅ KEY DECISIONS")
        print("="*60)
        for i, decision in enumerate(result['analysis']['decisions'], 1):
            print(f"{i}. {decision}")

        print("\n" + "="*60)
        print("🎯 ACTION ITEMS")
        print("="*60)
        for i, item in enumerate(result['analysis']['action_items'], 1):
            print(f"\n{i}. {item['description']}")
            print(f"   👤 Assignee: {item['assignee']}")
            print(f"   📅 Deadline: {item['deadline']}")

        print("\n" + "="*60)
        print("✓ Processing complete!")
        print("="*60)

        # Save to file
        output_file = Path(audio_file).stem + "_summary.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("MEETING SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(result['analysis']['summary'] + "\n\n")

            f.write("KEY DECISIONS\n")
            f.write("="*60 + "\n\n")
            for i, decision in enumerate(result['analysis']['decisions'], 1):
                f.write(f"{i}. {decision}\n")

            f.write("\n\nACTION ITEMS\n")
            f.write("="*60 + "\n\n")
            for i, item in enumerate(result['analysis']['action_items'], 1):
                f.write(f"{i}. {item['description']}\n")
                f.write(f"   Assignee: {item['assignee']}\n")
                f.write(f"   Deadline: {item['deadline']}\n\n")

        print(f"\n💾 Summary saved to: {output_file}")

        # Print cost estimate
        transcript_length = len(result['transcript']['text'])
        print(f"\n💰 Estimated cost:")
        print(f"   Transcription: ~$0.36 (60 min)")
        print(f"   Analysis: ~$0.03 ({transcript_length} chars)")
        print(f"   Total: ~$0.39")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
