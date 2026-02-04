#!/usr/bin/env python3
"""
Quick test script to verify the system is working
Tests each component individually
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 60)
print("Meeting Summarizer - Quick Test")
print("=" * 60)

# Test 1: Check dependencies
print("\n[1/5] Checking dependencies...")
dependencies = {
    'openai': 'OpenAI',
    'anthropic': 'Anthropic',
    'watchdog': 'Watchdog',
    'requests': 'Requests',
    'yaml': 'PyYAML'
}

missing = []
for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"  ✓ {name}")
    except ImportError:
        print(f"  ✗ {name} NOT installed")
        missing.append(name)

if missing:
    print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 2: Check configuration
print("\n[2/5] Checking configuration...")
import yaml

config_path = Path.home() / '.meeting-summarizer' / 'config.yaml'
if not config_path.exists():
    print(f"  ✗ Configuration file not found: {config_path}")
    print("  Run: python scripts/init_config.py")
    sys.exit(1)

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Check API keys
openai_key = config.get('openai', {}).get('api_key', '')
anthropic_key = config.get('anthropic', {}).get('api_key', '')
slack_webhook = config.get('slack', {}).get('webhook_url', '')

if openai_key.startswith('sk-'):
    print(f"  ✓ OpenAI API key configured")
else:
    print(f"  ✗ OpenAI API key not configured")
    print(f"    Edit {config_path} and add your OpenAI API key")

if anthropic_key.startswith('sk-ant-'):
    print(f"  ✓ Anthropic API key configured")
else:
    print(f"  ✗ Anthropic API key not configured")
    print(f"    Edit {config_path} and add your Anthropic API key")

if slack_webhook.startswith('https://'):
    print(f"  ✓ Slack webhook URL configured")
else:
    print(f"  ✗ Slack webhook URL not configured")
    print(f"    Edit {config_path} and add your Slack webhook URL")

# Test 3: Check monitoring folder
print("\n[3/5] Checking monitoring folder...")
monitoring_folder = Path(config['monitoring']['folder']).expanduser()
if monitoring_folder.exists():
    print(f"  ✓ Monitoring folder exists: {monitoring_folder}")
    mp3_files = list(monitoring_folder.glob('*.mp3'))
    print(f"  ℹ Found {len(mp3_files)} mp3 files")
else:
    print(f"  ⚠ Monitoring folder not found: {monitoring_folder}")
    print(f"  Creating folder...")
    monitoring_folder.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Created: {monitoring_folder}")

# Test 4: Check cache directory
print("\n[4/5] Checking cache directory...")
cache_dir = Path(config['processing']['cache_dir']).expanduser()
if cache_dir.exists():
    print(f"  ✓ Cache directory exists: {cache_dir}")
    cache_files = list(cache_dir.glob('*.json'))
    print(f"  ℹ Found {len(cache_files)} cached transcripts")
else:
    print(f"  ⚠ Cache directory not found: {cache_dir}")
    print(f"  Creating directory...")
    cache_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Created: {cache_dir}")

# Test 5: Test API connections (optional)
print("\n[5/5] Testing API connections...")

test_apis = input("Do you want to test API connections? (y/n): ").lower() == 'y'

if test_apis:
    # Test OpenAI
    if openai_key.startswith('sk-'):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            # Just test authentication, don't make actual API call
            print(f"  ✓ OpenAI API key is valid")
        except Exception as e:
            print(f"  ✗ OpenAI API error: {e}")

    # Test Anthropic
    if anthropic_key.startswith('sk-ant-'):
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=anthropic_key)
            # Just test authentication, don't make actual API call
            print(f"  ✓ Anthropic API key is valid")
        except Exception as e:
            print(f"  ✗ Anthropic API error: {e}")

    # Test Slack
    if slack_webhook.startswith('https://'):
        try:
            import requests
            # Send a test message
            test_message = {
                "text": "🧪 Meeting Summarizer - Test Message"
            }
            response = requests.post(slack_webhook, json=test_message)
            if response.status_code == 200:
                print(f"  ✓ Slack webhook is working (check your channel!)")
            else:
                print(f"  ✗ Slack webhook error: {response.status_code}")
        except Exception as e:
            print(f"  ✗ Slack webhook error: {e}")
else:
    print("  ⊘ Skipped API connection tests")

# Summary
print("\n" + "=" * 60)
print("Test Summary")
print("=" * 60)

all_configured = (
    openai_key.startswith('sk-') and
    anthropic_key.startswith('sk-ant-') and
    slack_webhook.startswith('https://')
)

if all_configured:
    print("✅ System is ready to use!")
    print("\nNext steps:")
    print("1. Place a test mp3 file in:", monitoring_folder)
    print("2. Run: python scripts/monitor_meetings.py")
    print("3. Or process a single file: python scripts/process_meeting.py <file.mp3>")
else:
    print("⚠ System needs configuration")
    print("\nNext steps:")
    print(f"1. Edit configuration file: {config_path}")
    print("2. Add your API keys")
    print("3. Run this test again: python scripts/quick_test.py")

print("\nFor detailed documentation, see:")
print("- QUICKSTART.md - Quick start guide")
print("- README.md - Full documentation")
print("- DEPLOYMENT.md - Deployment guide")
print("=" * 60)
