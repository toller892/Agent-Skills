#!/usr/bin/env python3
"""
Meeting Transcriber - Transcription Only
仅转录，不调用外部 AI API
支持 Gemini (云端) 和 Paraformer (本地)
自动选择：有 Gemini key 则用 Gemini，否则回退到 Paraformer
AI 总结由 Claude Code skill 环境直接生成
"""
import sys
from pathlib import Path
from datetime import datetime

# 导入转录函数
from transcribe_multi_model import (
    transcribe_with_gemini,
    transcribe_with_paraformer,
    MODELS,
    GEMINI_API_KEY
)

def generate_markdown(transcription_data, filename):
    """生成 Markdown 转录文档（不含 AI 总结）"""
    utterances = transcription_data['utterances']
    confidence = transcription_data['confidence']
    duration = transcription_data.get('audio_duration', 0)
    model = transcription_data.get('model', 'Unknown')

    # 文档头部
    md_content = f"""# 会议转录

**文件名**: {filename}
**转录时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
**使用模型**: {model}
**音频时长**: {duration/1000:.1f} 秒
**准确率**: {confidence*100:.1f}%
**发言段落**: {len(utterances)} 段

---

## 转录内容

"""

    # 添加转录内容
    for i, utterance in enumerate(utterances, 1):
        speaker = utterance.get('speaker', 'Unknown')
        text = utterance.get('text', '')
        start = utterance.get('start', 0)

        if isinstance(start, (int, float)):
            start_ms = int(start)
        else:
            start_ms = 0

        minutes = int(start_ms // 60000)
        seconds = int((start_ms % 60000) // 1000)
        timestamp = f"{minutes:02d}:{seconds:02d}"

        md_content += f"### [{timestamp}] 说话人 {speaker}\n\n"
        md_content += f"{text}\n\n"
        md_content += "---\n\n"

    return md_content

def main():
    print("="*60)
    print("Meeting Transcriber")
    print("="*60)

    if len(sys.argv) < 2:
        print("\n用法: python transcribe_only.py <audio_file> [model]")
        print("\n支持格式: mp3, wav, m4a, mp4")
        print("\n模型选项:")
        print("  1 - Gemini (云端，推荐)")
        print("  2 - Paraformer (本地，离线)")
        print("\n示例:")
        print("  python transcribe_only.py meeting.mp3")
        print("  python transcribe_only.py meeting.mp3 1")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not Path(audio_file).exists():
        print(f"\n❌ 文件不存在: {audio_file}")
        sys.exit(1)

    print(f"\n📁 音频文件: {audio_file}")

    # 自动选择模型：优先 Gemini，无 key 则用 Paraformer
    if len(sys.argv) >= 3:
        model_choice = sys.argv[2]
        if model_choice not in MODELS:
            print(f"❌ 无效的模型选项: {model_choice}")
            sys.exit(1)
    else:
        # 检查是否有 Gemini API key
        if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here':
            model_choice = '1'  # 使用 Gemini
            print("\n✓ 检测到 GEMINI_API_KEY，使用 Gemini 模型")
        else:
            model_choice = '2'  # 回退到 Paraformer
            print("\n⚠️  未检测到 GEMINI_API_KEY，使用 Paraformer 本地模型")
            print("   提示：设置 export GEMINI_API_KEY='your_key' 可使用更快的 Gemini 模型")

    model_name = MODELS[model_choice]['name']
    print(f"✓ 已选择模型: {model_name}")

    filename = Path(audio_file).name
    base_name = Path(audio_file).stem

    try:
        # 根据选择调用不同的转录函数
        if model_choice == '1':
            transcription_data = transcribe_with_gemini(audio_file)
        elif model_choice == '2':
            transcription_data = transcribe_with_paraformer(audio_file)

        if not transcription_data:
            print("\n✗ 转录失败")
            sys.exit(1)

        # 生成 Markdown
        print(f"\n[生成文档] 正在生成 Markdown 文档...")
        markdown_content = generate_markdown(
            transcription_data,
            filename
        )

        # 保存文件
        model_suffix = model_name.lower().replace(' ', '_')
        output_file = f"{base_name}_transcript_{model_suffix}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"  ✓ 已保存: {output_file}")

        print("\n" + "="*60)
        print("✓ 转录完成！")
        print("="*60)
        print(f"\n📝 输出文件: {output_file}")
        print(f"🤖 使用模型: {model_name}")
        print(f"📊 发言段落: {len(transcription_data['utterances'])} 段")
        print(f"✅ 准确率: {transcription_data['confidence']*100:.1f}%")
        print(f"\n💡 提示: 使用 Claude Code 可以为此转录生成 AI 总结")

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
