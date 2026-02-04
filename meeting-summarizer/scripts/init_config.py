#!/usr/bin/env python3
"""
Initialize configuration file for meeting summarizer
"""
import os
import yaml
from pathlib import Path


def create_config():
    """Create default configuration file"""
    config_path = Path.home() / '.meeting-summarizer' / 'config.yaml'
    config_path.parent.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        print(f"Configuration file already exists at: {config_path}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    config = {
        'openai': {
            'api_key': os.environ.get('OPENAI_API_KEY', 'your-openai-api-key')
        },
        'anthropic': {
            'api_key': os.environ.get('ANTHROPIC_API_KEY', 'your-anthropic-api-key')
        },
        'slack': {
            'webhook_url': os.environ.get('SLACK_WEBHOOK_URL', 'your-slack-webhook-url')
        },
        'monitoring': {
            'folder': '~/meeting-recordings',
            'check_interval': 60
        },
        'processing': {
            'cache_transcripts': True,
            'cache_dir': '~/.meeting-summarizer/cache'
        }
    }

    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

    print(f"Configuration file created at: {config_path}")
    print("\nPlease edit the file and add your API keys:")
    print(f"  - OpenAI API key")
    print(f"  - Anthropic API key")
    print(f"  - Slack webhook URL")
    print("\nOr set environment variables:")
    print(f"  export OPENAI_API_KEY='your-key'")
    print(f"  export ANTHROPIC_API_KEY='your-key'")
    print(f"  export SLACK_WEBHOOK_URL='your-webhook-url'")


if __name__ == '__main__':
    create_config()
