#!/usr/bin/env python3
"""
Verify Vosk Setup - 验证 Vosk 环境配置
"""
import os
import sys
from pathlib import Path

def check_python_package(package_name):
    """Check if Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_command(command):
    """Check if command is available"""
    import shutil
    return shutil.which(command) is not None

def check_vosk_model():
    """Check if Vosk model is downloaded"""
    model_path = os.path.expanduser("~/.meeting-summarizer/vosk-model-cn")
    if not Path(model_path).exists():
        return False, "模型未下载"

    # Check for required files
    required_files = ['am', 'conf', 'graph']
    for file in required_files:
        if not Path(model_path, file).exists():
            return False, f"模型不完整（缺少 {file}）"

    return True, "模型已就绪"

def check_claude_api():
    """Check Claude API configuration"""
    import requests

    TOKEN = "your_claude_api_token_here"
    ANTHROPIC_BASE = "https://api.anthropic.com"

    try:
        response = requests.post(
            f"{ANTHROPIC_BASE}/v1/messages",
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "test"}]
            },
            timeout=10
        )
        return response.status_code == 200, f"状态码: {response.status_code}"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("Vosk Setup Verification")
    print("=" * 60)
    print()

    checks = []

    # Check Python packages
    print("📦 检查 Python 包...")
    packages = {
        'vosk': 'Vosk',
        'pydub': 'pydub',
        'requests': 'requests',
        'wave': 'wave'
    }

    for pkg, name in packages.items():
        installed = check_python_package(pkg)
        status = "✓" if installed else "✗"
        print(f"  {status} {name}")
        checks.append(installed)

    print()

    # Check system commands
    print("🔧 检查系统工具...")
    commands = ['ffmpeg']

    for cmd in commands:
        available = check_command(cmd)
        status = "✓" if available else "✗"
        print(f"  {status} {cmd}")
        checks.append(available)

    print()

    # Check Vosk model
    print("🤖 检查 Vosk 模型...")
    model_ok, model_msg = check_vosk_model()
    status = "✓" if model_ok else "✗"
    print(f"  {status} {model_msg}")
    checks.append(model_ok)

    print()

    # Check Claude API
    print("☁️  检查 Claude API...")
    api_ok, api_msg = check_claude_api()
    status = "✓" if api_ok else "✗"
    print(f"  {status} {api_msg}")
    checks.append(api_ok)

    print()
    print("=" * 60)

    if all(checks):
        print("🎉 所有依赖已就绪！")
        print()
        print("下一步：")
        print("  python vosk_summarizer.py <audio_file>")
        return 0
    else:
        print("⚠️  部分依赖缺失")
        print()
        print("修复步骤：")

        if not check_python_package('vosk'):
            print("  pip install vosk")
        if not check_python_package('pydub'):
            print("  pip install pydub")
        if not check_command('ffmpeg'):
            print("  sudo apt install ffmpeg  # Ubuntu/Debian")
            print("  brew install ffmpeg      # macOS")
        if not model_ok:
            print("  ./setup_vosk.sh")
            print("  # 或手动下载：")
            print("  wget https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip")
            print("  unzip vosk-model-cn-0.22.zip -d ~/.meeting-summarizer/")
            print("  mv ~/.meeting-summarizer/vosk-model-cn-0.22 ~/.meeting-summarizer/vosk-model-cn")

        return 1

if __name__ == '__main__':
    sys.exit(main())
