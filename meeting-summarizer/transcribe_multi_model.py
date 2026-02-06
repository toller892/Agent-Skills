#!/usr/bin/env python3
"""
Meeting Transcriber - Dual Model Support
支持 Gemini (云端) 和 Paraformer (本地) 两种 ASR 模型
自动选择：有 Gemini key 则用 Gemini，否则回退到 Paraformer
"""
import os
import sys
import time
import requests
from pathlib import Path
from datetime import datetime

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your_gemini_api_key_here')

# 模型配置
MODELS = {
    '1': {
        'name': 'Gemini',
        'description': 'Google AI，准确率 90%+，100+语言，快速',
        'cost': '免费配额有限',
        'requires': 'API Key'
    },
    '2': {
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
        choice = input("\n请输入选项 (1-2): ").strip()
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
        import re

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
                    # 清理 SenseVoice 的元数据标签
                    # 移除 <|zh|>, <|NEUTRAL|>, <|Speech|>, <|withitn|> 等标签
                    text = re.sub(r'<\|[^|]+\|>', '', text)
                    # 移除多余空格
                    text = re.sub(r'\s+', ' ', text).strip()

                    if text:  # 确保清理后还有内容
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

        # 解析结果 - 从 sentence_info 中提取说话人信息
        utterances = []
        if isinstance(result, list) and len(result) > 0:
            for item in result:
                # 检查是否有 sentence_info（包含说话人分段）
                if 'sentence_info' in item and isinstance(item['sentence_info'], list):
                    for sent_info in item['sentence_info']:
                        text = sent_info.get('text', '')
                        speaker = sent_info.get('spk', 'A')  # 说话人标签
                        start = sent_info.get('start', 0)  # 开始时间（毫秒）

                        if text:
                            utterances.append({
                                'speaker': speaker,
                                'text': text,
                                'start': start
                            })
                else:
                    # 如果没有 sentence_info，使用整体文本
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

def transcribe_with_gemini(audio_file):
    """使用 Gemini API 转录"""
    try:
        import requests
        import base64

        if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_gemini_api_key_here':
            print("❌ GEMINI_API_KEY not set")
            print("\n请设置 API Key：")
            print("  export GEMINI_API_KEY='your_api_key'")
            return None

        print(f"\n[1/2] 读取音频文件...")
        with open(audio_file, 'rb') as f:
            audio_data = f.read()

        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        print(f"  ✓ 文件已编码")

        print(f"\n[2/2] 发送转录请求...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        # 检测文件类型
        suffix = Path(audio_file).suffix.lower()
        mime_type_map = {
            '.mp3': 'audio/mp3',
            '.wav': 'audio/wav',
            '.m4a': 'audio/m4a',
            '.mp4': 'video/mp4'
        }
        mime_type = mime_type_map.get(suffix, 'audio/mp3')

        payload = {
            "contents": [{
                "parts": [
                    {
                        "text": """请将这段音频转录为文字。要求：
1. 保留所有对话内容
2. 识别不同说话人，用"说话人 X"标注（说话人 1, 说话人 2, 说话人 3...）
3. 保持原始语言（中文）
4. 输出格式为 Markdown，每个说话人的发言使用三级标题（### [时间] 说话人 X）
5. 每段发言后添加分隔线（---）
6. 不要添加任何总结或分析，只输出转录内容"""
                    },
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": audio_base64
                        }
                    }
                ]
            }]
        }

        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=300)

        if response.status_code == 200:
            result = response.json()

            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"  ✓ 转录完成")

                # 解析转录结果
                utterances = []
                lines = text.strip().split('\n')

                current_speaker = None
                current_text = []

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    # 检查是否是说话人标题行（### 开头）
                    if line.startswith('###'):
                        # 保存之前的说话人内容
                        if current_speaker and current_text:
                            utterances.append({
                                'speaker': current_speaker,
                                'text': ' '.join(current_text),
                                'start': 0
                            })
                            current_text = []

                        # 提取说话人信息
                        # 格式: ### [时间] 说话人 X 或 ### 说话人 X
                        if '说话人' in line:
                            parts = line.split('说话人')
                            if len(parts) > 1:
                                speaker_num = parts[1].strip().split()[0]
                                current_speaker = speaker_num
                    elif line != '---':  # 跳过分隔线
                        # 累积当前说话人的文本
                        if current_speaker:
                            current_text.append(line)

                # 保存最后一个说话人的内容
                if current_speaker and current_text:
                    utterances.append({
                        'speaker': current_speaker,
                        'text': ' '.join(current_text),
                        'start': 0
                    })

                print(f"  ✓ 发言段落: {len(utterances)} 段")

                return {
                    'utterances': utterances,
                    'confidence': 0.90,
                    'audio_duration': 0,
                    'model': 'Gemini'
                }
            else:
                print(f"  ✗ 响应格式错误")
                return None
        else:
            error_info = response.json() if response.text else {}
            print(f"  ✗ API 错误 ({response.status_code})")
            if 'error' in error_info:
                print(f"     {error_info['error'].get('message', '')}")
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
    print("Meeting Transcriber")
    print("="*60)

    if len(sys.argv) < 2:
        print("\n用法: python transcribe_multi_model.py <audio_file> [model]")
        print("\n支持格式: mp3, wav, m4a, mp4")
        print("\n模型选项:")
        print("  1 - Gemini (云端，推荐)")
        print("  2 - Paraformer (本地，离线)")
        print("\n示例:")
        print("  python transcribe_multi_model.py meeting.mp3")
        print("  python transcribe_multi_model.py meeting.mp3 1")
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
