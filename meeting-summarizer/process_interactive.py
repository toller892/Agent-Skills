#!/usr/bin/env python3
"""
Process meeting recording with API key prompts
"""
import os
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from meeting_summarizer.processor import MeetingProcessor


def get_api_key(name, env_var):
    """Get API key from environment or prompt"""
    key = os.getenv(env_var)
    if not key:
        print(f"\n{name} API key not found in environment.")
        print(f"Please enter your {name} API key:")
        key = input(f"{env_var}: ").strip()
        if not key:
            print(f"Error: {name} API key is required")
            sys.exit(1)
    return key


def main():
    print("="*60)
    print("Meeting Summarizer - Interactive Mode")
    print("="*60)

    # Get API keys
    openai_key = get_api_key("OpenAI", "OPENAI_API_KEY")
    anthropic_key = get_api_key("Anthropic", "ANTHROPIC_API_KEY")

    # Slack webhook is optional
    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    if not slack_webhook:
        print("\nSlack webhook not configured (optional)")
        use_slack = input("Do you want to enter Slack webhook URL? (y/n): ").strip().lower()
        if use_slack == 'y':
            slack_webhook = input("SLACK_WEBHOOK_URL: ").strip()
        else:
            slack_webhook = None

    # Get audio file path
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        print("\nEnter path to audio file:")
        audio_file = input("Audio file: ").strip()

    if not Path(audio_file).exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)

    # Create config
    config = {
        'openai': {'api_key': openai_key},
        'anthropic': {'api_key': anthropic_key},
        'slack': {'webhook_url': slack_webhook} if slack_webhook else {'webhook_url': 'disabled'},
        'processing': {
            'cache_dir': '~/.meeting-summarizer/cache',
            'cache_transcripts': True
        }
    }

    # Process
    print("\n" + "="*60)
    print("Starting processing...")
    print("="*60 + "\n")

    processor = MeetingProcessor(config)

    try:
        result = processor.process(audio_file)

        # Print results
        print("\n" + "="*60)
        print("MEETING SUMMARY")
        print("="*60)
        print(result['analysis']['summary'])

        print("\n" + "="*60)
        print("KEY DECISIONS")
        print("="*60)
        for i, decision in enumerate(result['analysis']['decisions'], 1):
            print(f"{i}. {decision}")

        print("\n" + "="*60)
        print("ACTION ITEMS")
        print("="*60)
        for i, item in enumerate(result['analysis']['action_items'], 1):
            print(f"\n{i}. {item['description']}")
            print(f"   Assignee: {item['assignee']}")
            print(f"   Deadline: {item['deadline']}")

        print("\n" + "="*60)
        print("Processing complete!")
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

        print(f"\nSummary saved to: {output_file}")

    except Exception as e:
        print(f"\nError processing file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
