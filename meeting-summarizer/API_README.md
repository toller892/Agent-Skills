# Paraformer API Server

阿里 Paraformer 语音识别 API 服务，支持 HTTP 接口调用。

## 功能特性

- ✅ RESTful API 接口
- ✅ 支持文件上传转录
- ✅ 支持 URL 音频转录
- ✅ 自动说话人识别
- ✅ 高准确率（94%+）
- ✅ 支持多种音频格式（mp3, wav, m4a, mp4, flac, ogg）

## 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements_api.txt

# 启动服务
python api_server.py
```

服务将在 `http://localhost:8000` 启动。

### Docker 运行

```bash
# 构建镜像
docker build -t paraformer-api .

# 运行容器
docker run -p 8000:8000 paraformer-api
```

## API 文档

### 1. 健康检查

```bash
GET /
GET /health
```

返回示例：
```json
{
  "status": "ok",
  "service": "Paraformer ASR API",
  "version": "1.0.0",
  "model": "paraformer-zh"
}
```

### 2. 转录音频文件

```bash
POST /transcribe
Content-Type: multipart/form-data

参数:
- file: 音频文件
- language: 语言代码（可选，默认 zh）
```

示例：
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@meeting.mp3" \
  -F "language=zh"
```

返回示例：
```json
{
  "success": true,
  "data": {
    "utterances": [
      {
        "speaker": "1",
        "text": "大家好，今天我们讨论项目进展。",
        "start": 0
      },
      {
        "speaker": "2",
        "text": "好的，我先汇报一下技术部分。",
        "start": 3500
      }
    ],
    "confidence": 0.94,
    "model": "Paraformer",
    "audio_duration": 0
  }
}
```

### 3. 从 URL 转录音频

```bash
POST /transcribe/url
Content-Type: application/json

{
  "audio_url": "https://example.com/audio.mp3",
  "language": "zh"
}
```

示例：
```bash
curl -X POST "http://localhost:8000/transcribe/url" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/meeting.mp3",
    "language": "zh"
  }'
```

## 环境变量

- `PORT`: 服务端口（默认 8000）

## 部署到 Zeabur

1. 在 Zeabur 创建新项目
2. 连接 Git 仓库或上传代码
3. Zeabur 会自动检测 Dockerfile 并构建
4. 服务启动后即可通过分配的域名访问

## 性能说明

- **首次启动**: 需要下载模型文件（约 1-2 分钟）
- **转录速度**: 约 3 分钟音频需要 3 分钟处理时间
- **内存需求**: 建议 4GB+ RAM
- **准确率**: 94%+

## 支持的音频格式

- MP3
- WAV
- M4A
- MP4
- FLAC
- OGG

## 许可证

MIT License
