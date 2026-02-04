#!/bin/bash
# Quick setup script for Meeting Summarizer
# Run this to set up everything in one go

set -e

echo "=========================================="
echo "Meeting Summarizer - Quick Setup"
echo "=========================================="

# Check Python version
echo ""
echo "[1/6] Checking Python version..."
python3 --version || { echo "Error: Python 3 not found"; exit 1; }

# Install dependencies
echo ""
echo "[2/6] Installing dependencies..."
pip install -r requirements.txt

# Initialize config
echo ""
echo "[3/6] Initializing configuration..."
python3 scripts/init_config.py

# Create monitoring folder
echo ""
echo "[4/6] Creating monitoring folder..."
mkdir -p ~/meeting-recordings
echo "Created: ~/meeting-recordings"

# Create cache folder
echo ""
echo "[5/6] Creating cache folder..."
mkdir -p ~/.meeting-summarizer/cache
echo "Created: ~/.meeting-summarizer/cache"

# Run test
echo ""
echo "[6/6] Running system test..."
python3 scripts/test_setup.py

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit configuration: nano ~/.meeting-summarizer/config.yaml"
echo "2. Add your API keys:"
echo "   - OpenAI API key: https://platform.openai.com/api-keys"
echo "   - Anthropic API key: https://console.anthropic.com/settings/keys"
echo "   - Slack webhook: https://api.slack.com/apps"
echo "3. Run quick test: python3 scripts/quick_test.py"
echo "4. Start monitoring: python3 scripts/monitor_meetings.py"
echo ""
echo "For detailed instructions, see QUICKSTART.md"
echo "=========================================="
