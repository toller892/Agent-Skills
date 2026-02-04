#!/bin/bash
# Meeting Summarizer - 一键运行脚本

echo "============================================================"
echo "Meeting Summarizer - 一键运行"
echo "============================================================"

# 检查 API keys
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  OPENAI_API_KEY 未设置"
    echo ""
    echo "请先设置你的中转站 API key:"
    echo "  export OPENAI_API_KEY='sk-xxx...'"
    echo ""
    exit 1
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY 未设置"
    echo ""
    echo "请先设置你的中转站 API key:"
    echo "  export ANTHROPIC_API_KEY='sk-ant-xxx...'"
    echo ""
    exit 1
fi

echo ""
echo "✓ API keys 已配置"
echo "  OPENAI_API_KEY: ${OPENAI_API_KEY:0:15}..."
echo "  ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:0:15}..."

# 进入目录
cd ~/.claude/skills/meeting-summarizer

# 激活虚拟环境
if [ ! -d "venv" ]; then
    echo ""
    echo "⚠️  虚拟环境不存在，正在创建..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "✓ 虚拟环境已激活"

# 检查音频文件
AUDIO_FILE="/mnt/d/Code/skills/2026_1_30 14_27_47.mp3"

if [ ! -f "$AUDIO_FILE" ]; then
    echo ""
    echo "⚠️  音频文件不存在: $AUDIO_FILE"
    echo ""
    echo "请提供音频文件路径:"
    read -p "Audio file: " AUDIO_FILE

    if [ ! -f "$AUDIO_FILE" ]; then
        echo "❌ 文件不存在: $AUDIO_FILE"
        exit 1
    fi
fi

echo "✓ 音频文件: $AUDIO_FILE"

# 运行处理
echo ""
echo "============================================================"
echo "开始处理..."
echo "============================================================"
echo ""

python quick_test.py

echo ""
echo "============================================================"
echo "完成！"
echo "============================================================"
