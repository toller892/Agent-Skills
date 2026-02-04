#!/usr/bin/env python3
"""
Verify AssemblyAI Setup - 验证 AssemblyAI 环境配置
"""
import os
import sys

def check_python_package(package_name):
    """Check if Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_assemblyai_api():
    """Check AssemblyAI API configuration"""
    import requests

    api_key = os.getenv('ASSEMBLYAI_API_KEY', '')

    if not api_key:
        return False, "API Key 未设置"

    # Note: Some API keys may not start with 'aai_', test directly
    try:
        # Test API key validity
        response = requests.get(
            'https://api.assemblyai.com/v2/transcript',
            headers={'authorization': api_key},
            timeout=10
        )

        # 200 or 404 means API key is valid (404 just means no transcript ID provided)
        if response.status_code in [200, 404]:
            return True, "API Key 有效"
        elif response.status_code == 401:
            return False, "API Key 无效或已过期"
        else:
            return False, f"状态码: {response.status_code}"

    except Exception as e:
        return False, f"连接失败: {str(e)}"

def check_claude_api():
    """Check Claude API configuration"""
    import requests

    TOKEN = "your_claude_api_token_here"
    CLAUDE_BASE = "https://api.anthropic.com"

    try:
        response = requests.post(
            f"{CLAUDE_BASE}/v1/messages",
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
    print("AssemblyAI Setup Verification")
    print("=" * 60)
    print()

    checks = []

    # Check Python packages
    print("📦 检查 Python 包...")
    packages = {
        'requests': 'requests'
    }

    for pkg, name in packages.items():
        installed = check_python_package(pkg)
        status = "✓" if installed else "✗"
        print(f"  {status} {name}")
        checks.append(installed)

    print()

    # Check AssemblyAI API
    print("🎙️  检查 AssemblyAI API...")
    api_key = os.getenv('ASSEMBLYAI_API_KEY', '')

    if not api_key:
        print("  ✗ API Key 未设置")
        print("    请设置环境变量：")
        print("    export ASSEMBLYAI_API_KEY='aai_...'")
        checks.append(False)
    else:
        api_ok, api_msg = check_assemblyai_api()
        status = "✓" if api_ok else "✗"
        print(f"  {status} {api_msg}")
        checks.append(api_ok)

    print()

    # Check Claude API
    print("☁️  检查 Claude API...")
    claude_ok, claude_msg = check_claude_api()
    status = "✓" if claude_ok else "✗"
    print(f"  {status} {claude_msg}")
    checks.append(claude_ok)

    print()
    print("=" * 60)

    if all(checks):
        print("🎉 所有配置已就绪！")
        print()
        print("下一步：")
        print("  python assemblyai_summarizer.py <audio_file>")
        print()
        print("功能：")
        print("  ✓ 高质量转录")
        print("  ✓ 说话人识别")
        print("  ✓ 智能标点")
        print("  ✓ 中文支持")
        return 0
    else:
        print("⚠️  部分配置缺失")
        print()
        print("修复步骤：")

        if not check_python_package('requests'):
            print("  pip install requests")

        if not api_key:
            print("\n  1. 注册 AssemblyAI 账号：")
            print("     https://www.assemblyai.com/dashboard/signup")
            print("\n  2. 获取 API Key：")
            print("     Dashboard → API Keys → Create New API Key")
            print("\n  3. 设置环境变量：")
            print("     export ASSEMBLYAI_API_KEY='aai_...'")
            print("\n  或在脚本中直接配置：")
            print("     编辑 assemblyai_summarizer.py")
            print("     ASSEMBLYAI_API_KEY = 'aai_...'")

        return 1

if __name__ == '__main__':
    sys.exit(main())
