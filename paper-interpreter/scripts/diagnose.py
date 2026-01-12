#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断脚本 - 检查环境和配置
"""

import os
import sys

def check_dependencies():
    """检查依赖"""
    print("检查Python依赖...")
    
    try:
        import requests
        print(f"  ✓ requests: {requests.__version__}")
    except ImportError:
        print("  ✗ requests 未安装")
        return False
    
    try:
        from fpdf import FPDF
        print(f"  ✓ fpdf2: 已安装")
    except ImportError:
        print("  ✗ fpdf2 未安装")
        return False
    
    try:
        from dotenv import load_dotenv
        print(f"  ✓ python-dotenv: 已安装（可选）")
    except ImportError:
        print("  ⚠ python-dotenv 未安装（可选）")
    
    return True

def check_token():
    """检查Token"""
    print("\n检查Nano Banana Token...")
    
    token = os.getenv("NANO_BANANA_TOKEN", "")
    
    if not token:
        print("  ✗ 未设置 NANO_BANANA_TOKEN")
        print("  提示: export NANO_BANANA_TOKEN='your_token_here'")
        return False
    
    if token.startswith("sk-"):
        print(f"  ✓ Token已设置: {token[:10]}...")
        return True
    elif token.startswith("nb_"):
        print(f"  ✓ Token已设置: {token[:10]}...")
        return True
    else:
        print(f"  ⚠ Token格式可能不正确: {token[:10]}...")
        return True

def test_network():
    """测试网络连接"""
    print("\n测试网络连接...")
    
    try:
        import requests
        
        # 测试arXiv
        print("  测试arXiv连接...")
        response = requests.head("https://arxiv.org", timeout=5)
        print(f"  ✓ arXiv可访问 ({response.status_code})")
        
        # 测试Nano Banana API
        print("  测试Nano Banana API...")
        response = requests.head("https://api.nanobanana.ai", timeout=5)
        print(f"  ✓ Nano Banana API可访问 ({response.status_code})")
        
        return True
    except Exception as e:
        print(f"  ✗ 网络测试失败: {e}")
        return False

def test_api():
    """测试API调用"""
    print("\n测试Nano Banana API...")
    
    token = os.getenv("NANO_BANANA_TOKEN", "")
    if not token:
        print("  ⚠ 跳过API测试（未设置Token）")
        return True
    
    try:
        import requests
        import json
        
        url = "https://api.nanobanana.ai/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gemini-2.0-flash-exp",
            "prompt": "A simple test image",
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json"
        }
        
        print("  发送测试请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"  响应状态: {response.status_code}")
        
        if response.status_code == 200:
            print("  ✓ API调用成功")
            return True
        else:
            print(f"  ✗ API返回错误: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"  ✗ API测试失败: {e}")
        return False

def main():
    print("=" * 60)
    print("论文解析器 - 环境诊断")
    print("=" * 60)
    
    results = []
    
    # 检查依赖
    results.append(("依赖检查", check_dependencies()))
    
    # 检查Token
    results.append(("Token检查", check_token()))
    
    # 测试网络
    results.append(("网络测试", test_network()))
    
    # 测试API
    results.append(("API测试", test_api()))
    
    # 总结
    print("\n" + "=" * 60)
    print("诊断结果")
    print("=" * 60)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    all_passed = all(r for _, r in results)
    
    if all_passed:
        print("\n✅ 所有检查通过！可以开始使用")
    else:
        print("\n⚠️  部分检查未通过，请根据上面的提示修复")
    
    print("\n提示:")
    print("  - 如果Token未设置: export NANO_BANANA_TOKEN='your_token'")
    print("  - 如果依赖未安装: pip3 install -r requirements.txt")
    print("  - 如果网络有问题: 检查防火墙和代理设置")

if __name__ == "__main__":
    main()
