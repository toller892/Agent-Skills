# Nano Banana API 文档

Gemini 图片生成中转站 API。

基于 Gemini 2.5 Flash Image 和 Gemini 3 Pro Image。

---

## 可用模型

**gemini-2.5-flash-image (Nano Banana)**
快速高效
适合大批量、低延迟任务

**gemini-3-pro-image-preview (Nano Banana Pro)**
专业素材制作
支持高达 4K 分辨率

官方文档：[Gemini Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)

---

## 文本生成图片

根据文本描述生成图片。

### 端点

```
POST /v1beta/models/{model}:generateContent
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| contents | array | 是 | 包含文本提示的内容数组 |
| generationConfig | object | 否 | 生成配置 |

### generationConfig.imageConfig

| 参数 | 类型 | 说明 |
|------|------|------|
| aspectRatio | string | 宽高比：1:1、16:9、9:16、4:3、3:4、3:2、2:3、5:4、4:5、21:9 |
| imageSize | string | 图片尺寸（仅 Pro）：1K、2K、4K |

### generationConfig.responseModalities

| 值 | 说明 |
|------|------|
| ["IMAGE"] | 仅返回图片 |
| ["TEXT", "IMAGE"] | 返回文本和图片（默认） |

### 请求示例

```bash
curl -s -X POST \
  "https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Create a picture of a cute cat playing in the sunshine"
      }]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9"
      }
    }
  }' \
  | grep -o '"data": "[^"]*"' \
  | cut -d'"' -f4 \
  | base64 --decode > output.png
```

### Python 示例

```python
import requests
import base64

API_KEY = "your_api_key"
url = f"https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Create a picture of a cute cat playing in the sunshine"
        }]
    }],
    "generationConfig": {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": "16:9"
        }
    }
}

response = requests.post(url, json=payload)
data = response.json()

# 提取 base64 图片数据
image_data = data["candidates"][0]["content"]["parts"][0]["inline_data"]["data"]

# 解码并保存
with open("output.png", "wb") as f:
    f.write(base64.b64decode(image_data))
```

### 响应示例

```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inline_data": {
          "mime_type": "image/png",
          "data": "<BASE64_IMAGE_DATA>"
        }
      }],
      "role": "model"
    },
    "finishReason": "STOP"
  }],
  "usageMetadata": {
    "promptTokenCount": 10,
    "candidatesTokenCount": 1290,
    "totalTokenCount": 1300
  }
}
```

---

## 图片编辑

提供图片和文本提示来修改图片。

### 限制

仅支持通过 `inline_data` 以 base64 方式上传图片。

### 请求示例

```bash
# 将图片转为 base64
IMG_BASE64=$(base64 -w0 input.jpg)

curl -X POST \
  "https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent?key=$API_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"contents\": [{
      \"parts\": [
        {\"text\": \"Add a wizard hat to the cat in this image\"},
        {\"inline_data\": {
          \"mime_type\": \"image/jpeg\",
          \"data\": \"$IMG_BASE64\"
        }}
      ]
    }]
  }" \
  | grep -o '"data": "[^"]*"' \
  | cut -d'"' -f4 \
  | base64 --decode > edited.png
```

### Python 示例

```python
import requests
import base64

API_KEY = "your_api_key"
url = f"https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

# 读取并编码图片
with open("input.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

payload = {
    "contents": [{
        "parts": [
            {"text": "Add a wizard hat to the cat in this image"},
            {"inline_data": {
                "mime_type": "image/jpeg",
                "data": img_base64
            }}
        ]
    }]
}

response = requests.post(url, json=payload)
data = response.json()

# 保存编辑后的图片
image_data = data["candidates"][0]["content"]["parts"][0]["inline_data"]["data"]
with open("edited.png", "wb") as f:
    f.write(base64.b64decode(image_data))
```

---

## 多轮图片对话

通过多轮对话迭代优化图片。

### 示例流程

```bash
# 第一轮：生成信息图
curl -s -X POST \
  "https://cdn.12ai.org/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "role": "user",
      "parts": [{
        "text": "Create an infographic about photosynthesis for a 4th grader"
      }]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }' > turn1.json

# 第二轮：将文字改为西班牙语
# 需要将第一轮的响应加入对话历史
```

---

## 高级功能

### 高分辨率输出 (Pro)

```bash
curl -s -X POST \
  "https://cdn.12ai.org/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "A detailed butterfly illustration"
      }]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "1:1",
        "imageSize": "4K"
      }
    }
  }'
```

### 使用 Google 搜索进行接地

根据实时信息生成图片：

```bash
curl -s -X POST \
  "https://cdn.12ai.org/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Visualize the current weather forecast for San Francisco"
      }]
    }],
    "tools": [{"google_search": {}}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9"
      }
    }
  }'
```

### 多张参考图片 (Pro)

最多可使用 14 张参考图片：
- 最多 6 张高保真对象图片
- 最多 5 张人像照片（保持角色一致性）

---

## 分辨率和令牌数

### gemini-2.5-flash-image

| 宽高比 | 分辨率 | 令牌数 |
|--------|--------|--------|
| 1:1 | 1024x1024 | 1290 |
| 16:9 | 1344x768 | 1290 |
| 9:16 | 768x1344 | 1290 |
| 4:3 | 1184x864 | 1290 |
| 3:4 | 864x1184 | 1290 |
| 3:2 | 1248x832 | 1290 |
| 2:3 | 832x1248 | 1290 |

### gemini-3-pro-image-preview

| 宽高比 | 1K 分辨率 | 2K 分辨率 | 4K 分辨率 |
|--------|-----------|-----------|-----------|
| 1:1 | 1024x1024 | 2048x2048 | 4096x4096 |
| 16:9 | 1376x768 | 2752x1536 | 5504x3072 |
| 9:16 | 768x1376 | 1536x2752 | 3072x5504 |
| 4:3 | 1200x896 | 2400x1792 | 4800x3584 |
| 3:4 | 896x1200 | 1792x2400 | 3584x4800 |

---

## 提示技巧

### 逼真场景

使用摄影术语：拍摄角度、镜头类型、光线和细节。

```
A photorealistic close-up portrait of an elderly Japanese ceramicist
with deep wrinkles and a warm smile. Soft, golden hour light streaming
through a window. Captured with an 85mm portrait lens with soft bokeh.
```

### 风格化插画

明确说明样式：

```
A kawaii-style sticker of a happy red panda wearing a bamboo hat.
Bold, clean outlines, simple cel-shading, vibrant colors. White background.
```

### 准确的文字渲染

清楚说明文字内容和字体样式：

```
Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'.
Clean, bold, sans-serif font. Black and white color scheme.
Put the logo in a circle. Use a coffee bean in a clever way.
```

---

## 限制

- 图片生成不支持音频或视频输入
- gemini-2.5-flash-image 最多接受 3 张输入图片
- gemini-3-pro-image-preview 最多接受 14 张输入图片
- 仅支持 base64 inline_data 方式上传图片

---

## 快速参考

### 基础生成

```python
import requests
import base64

def generate_image(prompt, aspect_ratio="16:9"):
    url = f"https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect_ratio}
        }
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    image_data = data["candidates"][0]["content"]["parts"][0]["inline_data"]["data"]
    return base64.b64decode(image_data)

# 使用
image_bytes = generate_image("A cute cat playing in sunshine")
with open("output.png", "wb") as f:
    f.write(image_bytes)
```

### 图片编辑

```python
def edit_image(image_path, edit_prompt):
    url = f"https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
    
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()
    
    payload = {
        "contents": [{
            "parts": [
                {"text": edit_prompt},
                {"inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_base64
                }}
            ]
        }]
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    image_data = data["candidates"][0]["content"]["parts"][0]["inline_data"]["data"]
    return base64.b64decode(image_data)

# 使用
edited = edit_image("input.jpg", "Add a wizard hat")
with open("edited.png", "wb") as f:
    f.write(edited)
```
