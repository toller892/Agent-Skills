#!/usr/bin/env python3
"""
Quick test with actual audio file
"""
import os
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from meeting_summarizer.processor import MeetingProcessor


def main():
    # Get API keys from environment or prompt
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    slack_webhook = os.getenv('SLACK_WEBHOOK_URL', 'disabled')

    if not openai_key:
        print("Error: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY='sk-...'")
        sys.exit(1)

    if not anthropic_key:
        print("Error: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    # Audio file path
    audio_file = "/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"

    if not Path(audio_file).exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)

    # Create config
    config = {
        'openai': {'api_key': openai_key},
        'anthropic': {'api_key': anthropic_key},
        'slack': {'webhook_url': slack_webhook},
        'processing': {
            'cache_dir': '~/.meeting-summarizer/cache',
            'cache_transcripts': True
        }
    }

    # Process
    processor = MeetingProcessor(config)
    result = processor.process(audio_file)

    # Print results
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(result['analysis']['summary'])

    print("\n" + "="*60)
    print("DECISIONS")
    print("="*60)
    for decision in result['analysis']['decisions']:
        print(f"• {decision}")

    print("\n" + "="*60)
    print("ACTION ITEMS")
    print("="*60)
    for item in result['analysis']['action_items']:
        print(f"• {item['description']}")
        print(f"  Assignee: {item['assignee']} | Deadline: {item['deadline']}")


if __name__ == '__main__':
    main()
