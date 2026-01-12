# Nano Banana API 配置指南

## 🍌 什么是 Nano Banana？

Nano Banana 是一个 Gemini 图片生成 API 的中转站服务。

基于 Gemini 2.5 Flash Image 和 Gemini 3 Pro Image。

**完整 API 文档**: 查看 [NANO_BANANA_API.md](./NANO_BANANA_API.md)

## 🔑 获取 Token

1. 访问中转站服务提供商
2. 注册/登录账号
3. 获取你的 API Key

**API 端点**: `https://cdn.12ai.org/v1beta/models/{model}:generateContent`

## ⚙️ 配置方法

### 在 WSL/Linux 中配置

#### 临时配置（当前会话有效）

```bash
export NANO_BANANA_TOKEN="your_token_here"
```

#### 永久配置（推荐）

编辑 `~/.bashrc` 或 `~/.zshrc`：

```bash
nano ~/.bashrc
```

在文件末尾添加：

```bash
# Nano Banana API Token
export NANO_BANANA_TOKEN="your_token_here"
```

保存后重新加载：

```bash
source ~/.bashrc
```

### 在 Windows 中配置

#### PowerShell（临时）

```powershell
$env:NANO_BANANA_TOKEN="your_token_here"
```

#### 系统环境变量（永久）

1. 右键"此电脑" → 属性
2. 高级系统设置 → 环境变量
3. 新建用户变量：
   - 变量名: `NANO_BANANA_TOKEN`
   - 变量值: `your_token_here`

## ✅ 验证配置

### 检查环境变量

```bash
echo $NANO_BANANA_TOKEN
```

应该显示你的 API Key。

### 测试 API 调用

```bash
curl -s -X POST \
  "https://cdn.12ai.org/v1beta/models/gemini-2.5-flash-image:generateContent?key=$NANO_BANANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "A minimalist illustration of a cat"
      }]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "1:1"
      }
    }
  }'
```

如果返回 JSON 数据（包含 base64 图片），说明配置成功！

## 🎨 API 参数说明

### 支持的模型

- `gemini-2.5-flash-image` - Nano Banana（快速高效）
- `gemini-3-pro-image-preview` - Nano Banana Pro（专业素材，支持 4K）

### 宽高比选项

- `1:1` - 正方形（1024x1024）
- `16:9` - 横版（1344x768）
- `9:16` - 竖版（768x1344）
- `4:3`, `3:4`, `3:2`, `2:3` 等

### 图片尺寸（仅 Pro）

- `1K` - 标准分辨率
- `2K` - 高分辨率
- `4K` - 超高分辨率

### 响应格式

- `["IMAGE"]` - 仅返回图片
- `["TEXT", "IMAGE"]` - 返回文本和图片（默认）

**详细参数说明**: 查看 [NANO_BANANA_API.md](./NANO_BANANA_API.md)

## 💰 费用说明

- 请查看中转站服务提供商的定价信息
- 建议设置使用限额
- 每次生成约消耗 1290 tokens（标准分辨率）

**详细令牌消耗**: 查看 [NANO_BANANA_API.md](./NANO_BANANA_API.md#分辨率和令牌数)

## 🔧 在本项目中使用

### 基本使用

```bash
# 1. 设置 Token
export NANO_BANANA_TOKEN="your_token_here"

# 2. 运行脚本
python3 paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf
```

### 在 Python 代码中使用

```python
import os
from paper_interpreter import PaperInterpreter

# 确保设置了环境变量
os.environ['NANO_BANANA_TOKEN'] = 'your_token_here'

# 创建解析器
interpreter = PaperInterpreter()

# 处理论文
interpreter.process_paper("https://arxiv.org/pdf/2301.12345.pdf")
```

## 🐛 故障排除

### 问题1: "未设置 NANO_BANANA_TOKEN"

**解决方案:**
```bash
# 检查是否设置
echo $NANO_BANANA_TOKEN

# 如果为空，重新设置
export NANO_BANANA_TOKEN="your_token_here"
```

### 问题2: "API请求失败: 401 Unauthorized"

**原因:** Token 无效或过期

**解决方案:**
1. 检查 Token 是否正确
2. 登录 Nano Banana 官网检查 Token 状态
3. 如需要，重新生成 Token

### 问题3: "API请求失败: 429 Too Many Requests"

**原因:** 超过速率限制

**解决方案:**
1. 等待一段时间后重试
2. 检查账户配额
3. 考虑升级套餐

### 问题4: "API响应格式异常"

**原因:** API 返回格式不符合预期

**解决方案:**
1. 检查网络连接
2. 查看完整错误信息
3. 确认 API endpoint 是否正确

## 📝 API 调用示例

### 纽约客风格插画

```python
prompt = """Create a minimalist New Yorker magazine style illustration

Style requirements:
- Use only 3-4 muted colors: #FDFBF7, #7D9B76, #C4785A, #E8E4DD
- Mid-century modern aesthetic with clean geometric shapes
- Simple, conceptual, and metaphorical representation
- Lots of negative space and clean lines
- NO text, labels, or annotations
- Flat design with subtle shadows
- Abstract and minimalist composition"""

# API 会根据这个 prompt 生成纽约客风格的插画
```

## 🔗 相关链接

- API 端点: `https://cdn.12ai.org/v1beta/models/{model}:generateContent`
- 完整 API 文档: [NANO_BANANA_API.md](./NANO_BANANA_API.md)
- 官方文档: [Gemini Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)

## 💡 提示

1. **保护你的 Token**: 不要在代码中硬编码，不要提交到 Git
2. **监控使用量**: 定期检查 API 使用情况
3. **测试先行**: 先用简单 prompt 测试，确认可用后再批量使用
4. **备份 Token**: 将 Token 安全保存在密码管理器中

## 🎯 最佳实践

### 1. 使用 .env 文件（推荐）

创建 `.env` 文件：
```bash
NANO_BANANA_TOKEN=your_token_here
```

在代码中加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

### 2. 错误处理

```python
if not os.getenv("NANO_BANANA_TOKEN"):
    print("⚠️  请设置 NANO_BANANA_TOKEN")
    sys.exit(1)
```

### 3. 重试机制

```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        result = call_api()
        break
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # 指数退避
        else:
            raise
```

---

配置完成后，你就可以使用 Nano Banana 生成精美的纽约客风格插画了！🎨
