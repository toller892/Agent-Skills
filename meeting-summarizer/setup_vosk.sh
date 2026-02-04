#!/bin/bash
# Vosk 中文模型自动下载脚本

set -e

echo "============================================================"
echo "Vosk 中文模型安装"
echo "============================================================"
echo

MODEL_URL="https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip"
MODEL_DIR="$HOME/.meeting-summarizer"
MODEL_NAME="vosk-model-cn"
TEMP_ZIP="/tmp/vosk-model-cn-0.22.zip"

# 检查是否已安装
if [ -d "$MODEL_DIR/$MODEL_NAME" ]; then
    echo "✓ Vosk 模型已存在: $MODEL_DIR/$MODEL_NAME"
    echo
    echo "如需重新安装，请先删除："
    echo "  rm -rf $MODEL_DIR/$MODEL_NAME"
    exit 0
fi

# 创建目录
echo "📁 创建目录..."
mkdir -p "$MODEL_DIR"

# 下载模型
echo "📥 下载 Vosk 中文模型（约 42MB）..."
echo "   URL: $MODEL_URL"
echo

if command -v wget &> /dev/null; then
    wget -O "$TEMP_ZIP" "$MODEL_URL"
elif command -v curl &> /dev/null; then
    curl -L -o "$TEMP_ZIP" "$MODEL_URL"
else
    echo "❌ 错误：需要 wget 或 curl"
    echo "   安装方法："
    echo "     sudo apt install wget  # Ubuntu/Debian"
    echo "     brew install wget      # macOS"
    exit 1
fi

# 解压
echo
echo "📦 解压模型..."
unzip -q "$TEMP_ZIP" -d "$MODEL_DIR/"

# 重命名
echo "📝 重命名..."
mv "$MODEL_DIR/vosk-model-cn-0.22" "$MODEL_DIR/$MODEL_NAME"

# 清理
echo "🧹 清理临时文件..."
rm "$TEMP_ZIP"

# 验证
echo
echo "✅ 验证安装..."
if [ -d "$MODEL_DIR/$MODEL_NAME/am" ] && \
   [ -d "$MODEL_DIR/$MODEL_NAME/conf" ] && \
   [ -d "$MODEL_DIR/$MODEL_NAME/graph" ]; then
    echo "✓ 模型安装成功！"
    echo
    echo "模型位置: $MODEL_DIR/$MODEL_NAME"
    echo
    echo "下一步："
    echo "  python verify_vosk_setup.py"
else
    echo "❌ 模型安装失败（文件不完整）"
    exit 1
fi
