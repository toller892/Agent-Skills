#!/usr/bin/env python3
"""
Test script to verify the meeting summarizer setup
"""
import sys
from pathlib import Path

print("Meeting Summarizer - Setup Test")
print("=" * 60)

# Check Python version
print(f"\n✓ Python version: {sys.version.split()[0]}")

# Check dependencies
dependencies = [
    'openai',
    'anthropic',
    'watchdog',
    'requests',
    'yaml'
]

missing = []
for dep in dependencies:
    try:
        __import__(dep)
        print(f"✓ {dep} installed")
    except ImportError:
        print(f"✗ {dep} NOT installed")
        missing.append(dep)

if missing:
    print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Check configuration
config_path = Path.home() / '.meeting-summarizer' / 'config.yaml'
if config_path.exists():
    print(f"\n✓ Configuration file found: {config_path}")

    import yaml
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Check API keys
    if config.get('openai', {}).get('api_key', '').startswith('sk-'):
        print("✓ OpenAI API key configured")
    else:
        print("⚠ OpenAI API key not configured")

    if config.get('anthropic', {}).get('api_key', '').startswith('sk-ant-'):
        print("✓ Anthropic API key configured")
    else:
        print("⚠ Anthropic API key not configured")

    if config.get('slack', {}).get('webhook_url', '').startswith('https://'):
        print("✓ Slack webhook URL configured")
    else:
        print("⚠ Slack webhook URL not configured")
else:
    print(f"\n⚠ Configuration file not found: {config_path}")
    print("Run: python scripts/init_config.py")

# Check monitoring folder
monitoring_folder = Path.home() / 'meeting-recordings'
if monitoring_folder.exists():
    print(f"\n✓ Monitoring folder exists: {monitoring_folder}")
    mp3_files = list(monitoring_folder.glob('*.mp3'))
    print(f"  Found {len(mp3_files)} mp3 files")
else:
    print(f"\n⚠ Monitoring folder not found: {monitoring_folder}")
    print("Creating folder...")
    monitoring_folder.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {monitoring_folder}")

print("\n" + "=" * 60)
print("Setup test complete!")
print("\nNext steps:")
print("1. Configure API keys in ~/.meeting-summarizer/config.yaml")
print("2. Place mp3 files in ~/meeting-recordings")
print("3. Run: python scripts/monitor_meetings.py")
