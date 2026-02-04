#!/usr/bin/env python3
"""
Batch process all mp3 files in the monitoring folder
Useful for scheduled processing instead of real-time monitoring
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
    # Load configuration
    config = load_config()

    # Get monitoring folder
    watch_dir = Path(config['monitoring']['folder']).expanduser()

    if not watch_dir.exists():
        print(f"Monitoring folder not found: {watch_dir}")
        sys.exit(1)

    # Find all mp3 files
    mp3_files = list(watch_dir.glob('*.mp3'))

    if not mp3_files:
        print(f"No mp3 files found in {watch_dir}")
        sys.exit(0)

    print(f"Found {len(mp3_files)} mp3 files to process")
    print("=" * 60)

    # Create processor
    processor = MeetingProcessor(config)

    # Process each file
    success_count = 0
    error_count = 0

    for i, file_path in enumerate(mp3_files, 1):
        print(f"\n[{i}/{len(mp3_files)}] Processing: {file_path.name}")

        try:
            processor.process(str(file_path))
            success_count += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            error_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total files: {len(mp3_files)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {error_count}")


if __name__ == '__main__':
    main()
