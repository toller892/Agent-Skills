---
name: meeting-transcriber
description: Use when you need to transcribe meeting recordings or audio files with speaker identification, outputting a Markdown transcript with timestamps and speaker labels
---

# Meeting Transcriber

实时转录音频文件，自动识别发言人，输出 Markdown 格式转录文档。

## 功能

- 实时转录音频（支持 mp3, wav, m4a, mp4）
- 自动识别发言人（说话人 A, B, C...）
- 按时间戳分段
- 输出 Markdown 文档
- **不做任何总结或分析**

## 使用方法

```bash
python transcribe_simple.py "/path/to/meeting.mp3"
```

## 输出

生成单个 Markdown 文件：`filename_transcript.md`

格式：
- 文件元信息（时长、准确率、发言段落数）
- 按发言人和时间戳分段的转录内容

## 配置

需要 AssemblyAI API Key：

```bash
export ASSEMBLYAI_API_KEY='your_api_key'
```

获取：https://www.assemblyai.com/dashboard/signup

## 成本

$0.25/小时（仅转录费用）
