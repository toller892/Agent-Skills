# Token 配置指南 🔑

## 📍 Token在哪里？

**Token不在任何文件中！** 它通过环境变量传递，这样更安全。

## 🔐 为什么不写在文件里？

❌ **不安全的做法：**
```python
# 不要这样做！
NANO_BANANA_TOKEN = "nb_xxxxx"  # 会被提交到Git，泄露Token
```

✅ **安全的做法：**
```bash
# 使用环境变量
export NANO_BANANA_TOKEN="nb_xxxxx"
```

## 🚀 三种配置方法

### 方法1: 临时配置（最简单）

每次使用前在终端运行：

```bash
export NANO_BANANA_TOKEN="nb_xxxxx"
python3 paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf
```

**优点**: 简单快速  
**缺点**: 关闭终端后失效

---

### 方法2: 永久配置（推荐）⭐

#### 在 WSL/Linux 中：

1. 编辑配置文件：
```bash
nano ~/.bashrc
```

2. 在文件末尾添加：
```bash
# Nano Banana API Token
export NANO_BANANA_TOKEN="nb_xxxxx"
```

3. 保存并重新加载：
```bash
source ~/.bashrc
```

4. 验证配置：
```bash
echo $NANO_BANANA_TOKEN
```

**优点**: 一次配置，永久有效  
**缺点**: 需要编辑配置文件

---

### 方法3: 使用 .env 文件（可选）

#### 步骤1: 创建 .env 文件

```bash
cd /home/tony0523/.claude/skills/paper-interpreter
nano .env
```

#### 步骤2: 添加Token

```bash
NANO_BANANA_TOKEN=nb_xxxxx
```

#### 步骤3: 安装 python-dotenv

```bash
pip3 install python-dotenv
```

#### 步骤4: 使用

程序会自动读取 `.env` 文件中的Token。

**优点**: 便于管理多个环境变量  
**缺点**: 需要额外安装库

---

## ✅ 验证配置

### 检查环境变量

```bash
echo $NANO_BANANA_TOKEN
```

应该显示你的Token（以 `nb_` 开头）。

### 测试API连接

```bash
curl -X POST https://api.nanobanana.ai/v1/images/generations \
  -H "Authorization: Bearer $NANO_BANANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.0-flash-exp",
    "prompt": "A simple test image",
    "n": 1,
    "size": "1024x1024",
    "response_format": "b64_json"
  }'
```

如果返回JSON数据，说明Token有效！

---

## 🔍 程序如何读取Token

在 `paper_interpreter.py` 中：

```python
def __init__(self, output_dir="paper_output"):
    # 从环境变量读取Token
    self.nano_banana_token = os.getenv("NANO_BANANA_TOKEN", "")
```

程序会自动从环境变量中读取 `NANO_BANANA_TOKEN`。

---

## 📝 完整使用流程

### 使用方法1（临时）

```bash
# 1. 设置Token
export NANO_BANANA_TOKEN="nb_xxxxx"

# 2. 运行程序
python3 paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf
```

### 使用方法2（永久）

```bash
# 1. 一次性配置（编辑 ~/.bashrc）
echo 'export NANO_BANANA_TOKEN="nb_xxxxx"' >> ~/.bashrc
source ~/.bashrc

# 2. 以后直接运行
python3 paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf
```

### 使用方法3（.env文件）

```bash
# 1. 创建 .env 文件
echo 'NANO_BANANA_TOKEN=nb_xxxxx' > .env

# 2. 安装依赖
pip3 install python-dotenv

# 3. 运行程序（自动读取.env）
python3 paper_interpreter.py https://arxiv.org/pdf/2301.12345.pdf
```

---

## 🐛 常见问题

### Q: 提示"未设置 NANO_BANANA_TOKEN"

**A:** Token没有正确设置，运行：
```bash
export NANO_BANANA_TOKEN="your_token_here"
```

### Q: 每次都要重新设置Token？

**A:** 使用方法2（永久配置），编辑 `~/.bashrc`

### Q: .env 文件不生效？

**A:** 确保安装了 python-dotenv：
```bash
pip3 install python-dotenv
```

### Q: 如何更换Token？

**A:** 重新设置环境变量：
```bash
export NANO_BANANA_TOKEN="new_token_here"
```

或修改 `~/.bashrc` 中的值。

---

## 🔒 安全提示

1. ✅ **不要**把Token写在代码里
2. ✅ **不要**把Token提交到Git
3. ✅ **不要**在公开场合分享Token
4. ✅ **使用**环境变量或 .env 文件
5. ✅ **添加** `.env` 到 `.gitignore`

---

## 📋 快速参考

| 方法 | 命令 | 持久性 | 难度 |
|------|------|--------|------|
| 临时 | `export NANO_BANANA_TOKEN="xxx"` | 当前会话 | ⭐ |
| 永久 | 编辑 `~/.bashrc` | 永久 | ⭐⭐ |
| .env | 创建 `.env` 文件 | 项目级 | ⭐⭐⭐ |

---

## 🎯 推荐配置

**对于个人使用**: 方法2（永久配置）  
**对于团队协作**: 方法3（.env文件）  
**对于快速测试**: 方法1（临时配置）

---

现在你知道如何配置Token了！选择一种方法，开始使用吧！🚀
