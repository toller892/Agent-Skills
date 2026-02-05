#!/usr/bin/env python3
"""
Meeting Transcriber - Multi-Model Support
支持多种 ASR 模型：AssemblyAI, SenseVoice, Paraformer
"""
import os
import sys
import time
import requests
from pathlib import Path
from datetime import datetime

# Configuration
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY', 'your_assemblyai_api_key_here')

# 模型配置
MODELS = {
    '1': {
        'name': 'AssemblyAI',
        'description': '云端 API，准确率 87%+，支持说话人识别',
        'cost': '$0.25/小时',
        'requires': 'API Key'
    },
    '2': {
        'name': 'SenseVoice',
        'description': '阿里开源，准确率 95%+，50+语言，情感识别',
        'cost': '免费',
        'requires': '本地模型'
    },
    '3': {
        'name': 'Paraformer',
        'description': '阿里 FunASR，准确率 94%+，热词定制',
        'cost': '免费',
        'requires': '本地模型'
    }
}

def show_model_selection():
    """显示模型选择菜单"""
    print("\n" + "="*60)
    print("请选择语音识别模型")
    print("="*60)

    for key, model in MODELS.items():
        print(f"\n[{key}] {model['name']}")
        print(f"    描述: {model['description']}")
        print(f"    成本: {model['cost']}")
        print(f"    要求: {model['requires']}")

    print("\n" + "="*60)

    while True:
        choice = input("\n请输入选项 (1-3): ").strip()
        if choice in MODELS:
            return choice
        print("❌ 无效选项，请重新输入")

def transcribe_with_assemblyai(audio_file):
    """使用 AssemblyAI 转录"""
    if not ASSEMBLYAI_API_KEY or ASSEMBLYAI_API_KEY == 'your_assemblyai_api_key_here':
        print("❌ ASSEMBLYAI_API_KEY not set")
        print("\n请设置 API Key：")
        print("  export ASSEMBLYAI_API_KEY='your_api_key'")
        return None

    print(f"\n[1/2] 上传音频文件...")

    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }

    try:
        # Upload
        with open(audio_file, 'rb') as f:
            upload_response = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers={'authorization': ASSEMBLYAI_API_KEY},
                data=f,
                timeout=300
            )

        if upload_response.status_code != 200:
            print(f"  ✗ 上传失败: {upload_response.status_code}")
            return None

        audio_url = upload_response.json()['upload_url']
        print(f"  ✓ 上传完成")

        # Request transcription
        print(f"\n[2/2] 开始转录...")
        transcript_request = {
            "audio_url": audio_url,
            "speech_models": ["universal-2"],
            "language_code": "zh",
            "speaker_labels": True,
            "punctuate": True,
            "format_text": True
        }

        transcript_response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers=headers,
            json=transcript_request,
            timeout=30
        )

        if transcript_response.status_code != 200:
            print(f"  ✗ 转录请求失败: {transcript_response.status_code}")
            return None

        transcript_id = transcript_response.json()['id']
        print(f"  ✓ 转录任务已创建")

        # Poll for completion
        print(f"  ⏳ 处理中...")
        polling_url = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'

        while True:
            polling_response = requests.get(polling_url, headers=headers, timeout=30)
            if polling_response.status_code != 200:
                return None

            result = polling_response.json()
            status = result['status']

            if status == 'completed':
                print(f"  ✓ 转录完成")
                utterances = result.get('utterances', [])
                confidence = result.get('confidence', 0)
                print(f"  ✓ 准确率: {confidence*100:.1f}%")
                print(f"  ✓ 发言段落: {len(utterances)} 段")

                return {
                    'utterances': utterances,
                    'confidence': confidence,
                    'audio_duration': result.get('audio_duration', 0),
                    'model': 'AssemblyAI'
                }
            elif status == 'error':
                print(f"  ✗ 转录失败: {result.get('error', 'Unknown error')}")
                return None

            time.sleep(3)

    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return None

def transcribe_with_sensevoice(audio_file):
    """使用 SenseVoice 转录"""
    try:
        from funasr import AutoModel

        print(f"\n[1/2] 加载 SenseVoice 模型...")

        # 初始化模型
        model = AutoModel(
            model="iic/SenseVoiceSmall",
            vad_model="fsmn-vad",
            vad_kwargs={"max_single_segment_time": 30000},
            device="cpu"
        )

        print(f"  ✓ 模型加载完成")

        print(f"\n[2/2] 开始转录...")

        # 转录
        result = model.generate(
            input=audio_file,
            cache={},
            language="zh",
            use_itn=True,
            batch_size_s=60
        )

        print(f"  ✓ 转录完成")

        # 解析结果
        utterances = []
        if isinstance(result, list) and len(result) > 0:
            for item in result:
                text = item.get('text', '')
                if text:
                    utterances.append({
                        'speaker': 'A',  # SenseVoice 不直接提供说话人标签
                        'text': text,
                        'start': 0
                    })

        print(f"  ✓ 发言段落: {len(utterances)} 段")

        return {
            'utterances': utterances,
            'confidence': 0.95,  # SenseVoice 平均准确率
            'audio_duration': 0,
            'model': 'SenseVoice'
        }

    except ImportError:
        print("❌ SenseVoice 未安装")
        print("\n安装方法：")
        print("  pip install funasr modelscope")
        return None
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def transcribe_with_paraformer(audio_file):
    """使用 Paraformer 转录"""
    try:
        from funasr import AutoModel

        print(f"\n[1/2] 加载 Paraformer 模型...")

        # 初始化模型
        model = AutoModel(
            model="paraformer-zh",
            vad_model="fsmn-vad",
            punc_model="ct-punc",
            spk_model="cam++",  # 说话人识别
            device="cpu"
        )

        print(f"  ✓ 模型加载完成")

        print(f"\n[2/2] 开始转录...")

        # 转录
        result = model.generate(
            input=audio_file,
            batch_size_s=60,
            hotword='',
            use_itn=True
        )

        print(f"  ✓ 转录完成")

        # 解析结果
        utterances = []
        if isinstance(result, list) and len(result) > 0:
            for item in result:
                text = item.get('text', '')
                speaker = item.get('speaker', 'A')
                start = item.get('timestamp', [[0]])[0][0] if 'timestamp' in item else 0

                if text:
                    utterances.append({
                        'speaker': speaker,
                        'text': text,
                        'start': start
                    })

        print(f"  ✓ 发言段落: {len(utterances)} 段")

        return {
            'utterances': utterances,
            'confidence': 0.94,  # Paraformer 平均准确率
            'audio_duration': 0,
            'model': 'Paraformer'
        }

    except ImportError:
        print("❌ Paraformer 未安装")
        print("\n安装方法：")
        print("  pip install funasr modelscope")
        return None
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_markdown(transcription_data, filename):
    """生成 Markdown 转录文档"""
    utterances = transcription_data['utterances']
    confidence = transcription_data['confidence']
    duration = transcription_data.get('audio_duration', 0)
    model = transcription_data.get('model', 'Unknown')

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
    print("Meeting Transcriber - 多模型支持")
    print("="*60)

    if len(sys.argv) < 2:
        print("\n用法: python transcribe_multi_model.py <audio_file> [model]")
        print("\n支持格式: mp3, wav, m4a, mp4")
        print("\n模型选项:")
        print("  1 - AssemblyAI (云端)")
        print("  2 - SenseVoice (本地)")
        print("  3 - Paraformer (本地)")
        print("\n示例:")
        print("  python transcribe_multi_model.py meeting.mp3")
        print("  python transcribe_multi_model.py meeting.mp3 2")
        sys.exit(1)

    audio_file = sys.argv[1]

    if not Path(audio_file).exists():
        print(f"\n❌ 文件不存在: {audio_file}")
        sys.exit(1)

    print(f"\n📁 音频文件: {audio_file}")

    # 选择模型
    if len(sys.argv) >= 3:
        model_choice = sys.argv[2]
        if model_choice not in MODELS:
            print(f"❌ 无效的模型选项: {model_choice}")
            sys.exit(1)
    else:
        model_choice = show_model_selection()

    model_name = MODELS[model_choice]['name']
    print(f"\n✓ 已选择模型: {model_name}")

    filename = Path(audio_file).name
    base_name = Path(audio_file).stem

    try:
        # 根据选择调用不同的转录函数
        if model_choice == '1':
            transcription_data = transcribe_with_assemblyai(audio_file)
        elif model_choice == '2':
            transcription_data = transcribe_with_sensevoice(audio_file)
        elif model_choice == '3':
            transcription_data = transcribe_with_paraformer(audio_file)

        if not transcription_data:
            print("\n✗ 转录失败")
            sys.exit(1)

        # 生成 Markdown
        print(f"\n[3/3] 生成 Markdown 文档...")
        markdown_content = generate_markdown(transcription_data, filename)

        # 保存
        md_file = f"{base_name}_transcript_{model_name.lower()}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"  ✓ 已保存: {md_file}")

        # 打印摘要
        print(f"\n{'='*60}")
        print("✓ 转录完成！")
        print(f"{'='*60}")
        print(f"\n📝 输出文件: {md_file}")
        print(f"🤖 使用模型: {model_name}")
        print(f"📊 发言段落: {len(transcription_data['utterances'])} 段")
        print(f"✅ 准确率: {transcription_data['confidence']*100:.1f}%")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
