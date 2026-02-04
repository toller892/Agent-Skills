#!/usr/bin/env python3
"""
Monitor meeting recordings folder and process new files automatically
"""
import sys
import yaml
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from meeting_summarizer.processor import MeetingProcessor
from meeting_summarizer.monitor import MeetingMonitor


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
    # Load configuration
    config = load_config()

    # Create processor
    processor = MeetingProcessor(config)

    # Get monitoring folder
    watch_dir = config['monitoring']['folder']

    print(f"""
╔══════════════════════════════════════════════════════════╗
║         Meeting Summarizer - Monitoring Mode             ║
╚══════════════════════════════════════════════════════════╝

Watching: {watch_dir}

The system will automatically:
  1. Detect new .mp3 files
  2. Transcribe using Whisper API
  3. Analyze using Claude API
  4. Send summary to Slack

Press Ctrl+C to stop monitoring.
""")

    # Create monitor
    monitor = MeetingMonitor(
        watch_dir=watch_dir,
        processor_callback=processor.process
    )

    # Process existing files first
    monitor.process_existing_files()

    # Start monitoring
    try:
        monitor.start()
    except KeyboardInterrupt:
        print("\n\nStopping monitor...")
        monitor.stop()
        print("Monitor stopped.")


if __name__ == '__main__':
    main()
