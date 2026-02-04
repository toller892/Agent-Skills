#!/usr/bin/env python3
"""
Test if your relay supports both Anthropic and OpenAI APIs
"""
import os
import sys

print("="*60)
print("API Relay Configuration Test")
print("="*60)

# Check Anthropic configuration
anthropic_token = os.getenv('ANTHROPIC_AUTH_TOKEN')
anthropic_base = os.getenv('ANTHROPIC_BASE_URL')

print("\n[Anthropic Configuration]")
if anthropic_token:
    print(f"✓ ANTHROPIC_AUTH_TOKEN: {anthropic_token[:20]}...")
else:
    print("✗ ANTHROPIC_AUTH_TOKEN not set")

if anthropic_base:
    print(f"✓ ANTHROPIC_BASE_URL: {anthropic_base}")
else:
    print("✗ ANTHROPIC_BASE_URL not set")

# Check OpenAI configuration
openai_key = os.getenv('OPENAI_API_KEY')
openai_base = os.getenv('OPENAI_BASE_URL')

print("\n[OpenAI Configuration]")
if openai_key:
    print(f"✓ OPENAI_API_KEY: {openai_key[:20]}...")
else:
    print("✗ OPENAI_API_KEY not set")

if openai_base:
    print(f"✓ OPENAI_BASE_URL: {openai_base}")
else:
    print("✗ OPENAI_BASE_URL not set (will use official API)")

print("\n" + "="*60)
print("Configuration Summary")
print("="*60)

# Test if relay supports both
if anthropic_base and "mmkg.cloud" in anthropic_base:
    print("\n你使用的是 mmkg.cloud 中转站")
    print("\n需要确认的问题：")
    print("1. 这个中转站是否同时支持 OpenAI API？")
    print("2. 如果支持，OpenAI 的 base_url 是什么？")
    print("   - 可能是: https://api.mmkg.cloud/v1")
    print("   - 或者: https://openai.mmkg.cloud/v1")
    print("   - 或者需要单独的 OpenAI 中转站")

    print("\n建议方案：")
    print("方案 1: 如果 mmkg.cloud 支持 OpenAI")
    print("  export OPENAI_API_KEY='你的key'")
    print("  export OPENAI_BASE_URL='https://api.mmkg.cloud/v1'")

    print("\n方案 2: 使用官方 OpenAI API")
    print("  export OPENAI_API_KEY='sk-proj-...'  # 官方 key")
    print("  # 不设置 OPENAI_BASE_URL")

    print("\n方案 3: 使用其他 OpenAI 中转站")
    print("  export OPENAI_API_KEY='你的key'")
    print("  export OPENAI_BASE_URL='https://其他中转站/v1'")

print("\n" + "="*60)
print("Next Steps")
print("="*60)
print("\n1. 联系 mmkg.cloud 客服确认是否支持 OpenAI API")
print("2. 或者注册官方 OpenAI 账号获取 API key")
print("3. 配置好后运行: python test_apis.py")
