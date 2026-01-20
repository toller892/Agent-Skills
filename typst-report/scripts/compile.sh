#!/bin/bash
# Typst 编译脚本 - Shell 版本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Typst 是否安装
check_typst() {
    if ! command -v typst &> /dev/null; then
        echo -e "${RED}✗ Typst 未安装${NC}"
        echo ""
        echo "安装方法："
        echo "  macOS/Linux: curl -fsSL https://typst.app/install.sh | sh"
        echo "  Windows: winget install --id Typst.Typst"
        echo "  或访问: https://github.com/typst/typst/releases"
        exit 1
    fi
    
    version=$(typst --version)
    echo -e "${GREEN}✓ Typst 已安装: $version${NC}"
}

# 显示帮助
show_help() {
    cat << EOF
用法: $0 [选项] <输入文件.typ>

选项:
  -o, --output FILE       输出 PDF 文件路径
  -j, --json STRING       JSON 数据字符串
  -f, --json-file FILE    JSON 数据文件
  --font-path PATH        字体目录路径
  --root PATH             根目录路径
  -h, --help              显示帮助信息

示例:
  # 基础编译
  $0 main.typ

  # 指定输出文件
  $0 main.typ -o report.pdf

  # 传递 JSON 数据
  $0 main.typ -j '{"title": "报告"}'

  # 从文件读取 JSON
  $0 main.typ -f data.json

  # 指定字体路径
  $0 main.typ --font-path ./assets/fonts
EOF
}

# 解析参数
INPUT_FILE=""
OUTPUT_FILE=""
JSON_DATA=""
JSON_FILE=""
FONT_PATH=""
ROOT_PATH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -j|--json)
            JSON_DATA="$2"
            shift 2
            ;;
        -f|--json-file)
            JSON_FILE="$2"
            shift 2
            ;;
        --font-path)
            FONT_PATH="$2"
            shift 2
            ;;
        --root)
            ROOT_PATH="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            INPUT_FILE="$1"
            shift
            ;;
    esac
done

# 检查输入文件
if [ -z "$INPUT_FILE" ]; then
    echo -e "${RED}✗ 请指定输入文件${NC}"
    show_help
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}✗ 输入文件不存在: $INPUT_FILE${NC}"
    exit 1
fi

# 确定输出文件
if [ -z "$OUTPUT_FILE" ]; then
    OUTPUT_FILE="${INPUT_FILE%.typ}.pdf"
fi

# 检查 Typst
check_typst

# 构建命令
CMD="typst compile"

# 添加根目录
if [ -n "$ROOT_PATH" ]; then
    CMD="$CMD --root $ROOT_PATH"
fi

# 添加字体路径
if [ -n "$FONT_PATH" ]; then
    CMD="$CMD --font-path $FONT_PATH"
fi

# 添加 JSON 数据
if [ -n "$JSON_FILE" ]; then
    if [ ! -f "$JSON_FILE" ]; then
        echo -e "${RED}✗ JSON 文件不存在: $JSON_FILE${NC}"
        exit 1
    fi
    JSON_DATA=$(cat "$JSON_FILE")
fi

if [ -n "$JSON_DATA" ]; then
    CMD="$CMD --input payload='$JSON_DATA'"
fi

# 添加输入输出文件
CMD="$CMD $INPUT_FILE $OUTPUT_FILE"

# 执行编译
echo ""
echo -e "${YELLOW}编译中: $INPUT_FILE -> $OUTPUT_FILE${NC}"
echo "命令: typst compile ..."

if eval $CMD; then
    echo -e "${GREEN}✓ 编译成功: $OUTPUT_FILE${NC}"
    
    # 显示文件大小
    if [ -f "$OUTPUT_FILE" ]; then
        SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
        echo "  文件大小: $SIZE"
    fi
else
    echo -e "${RED}✗ 编译失败${NC}"
    exit 1
fi
