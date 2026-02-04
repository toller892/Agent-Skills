#!/usr/bin/env python3
"""
Process a single meeting file
"""
import sys
import yaml
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from meeting_summarizer.processor import MeetingProcessor


def load_config():
    """Load configuration from file"""
    config_path = Path.home() / '.meeting-summarizer' / 'config.yaml'

    if not config_path.exists():
        print(f"Configuration file not found: {config_path}")
        print("Please run: python scripts/init_config.py")
        sys.exit(1)

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/process_meeting.py <audio_file.mp3>")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not Path(audio_file).exists():
        print(f"File not found: {audio_file}")
        sys.exit(1)

    # Load configuration
    config = load_config()

    # Create processor
    processor = MeetingProcessor(config)

    # Process the file
    try:
        result = processor.process(audio_file)
        print("\n✓ Processing successful!")

        # Print summary
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
            print(f"  👤 {item['assignee']} | 📅 {item['deadline']}")

    except Exception as e:
        print(f"\n✗ Error processing file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
