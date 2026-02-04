# AssemblyAI 注册和配置指南

## 📋 注册步骤

### 第 1 步：访问注册页面

打开浏览器访问：**https://www.assemblyai.com/dashboard/signup**

### 第 2 步：填写注册信息

需要提供：
- 邮箱地址
- 密码
- 公司名称（可选）

**注意**：无需信用卡即可开始使用

### 第 3 步：验证邮箱

1. 检查你的邮箱收件箱
2. 找到来自 AssemblyAI 的确认邮件
3. 点击验证链接

### 第 4 步：获取 API Key

1. 登录后进入 Dashboard
2. 在左侧菜单找到 "API Keys"
3. 点击 "+ Create New API Key"
4. 输入 API Key 名称（例如：meeting-summarizer）
5. 点击 "Create"
6. **复制并保存 API Key**（只显示一次！）

API Key 格式类似：`aai_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 💰 定价信息

### 免费额度
- **$50 免费额度**（新用户）
- 约 **200 小时**转录时间

### 按量付费
- **$0.25/小时**（标准转录）
- **$0.65/小时**（实时转录）

### 成本计算
- 1 小时会议 = $0.25
- 20 次会议/月 = $5/月
- 加上 Claude 分析 = $5.60/月

**对比**：
- Vosk（免费）：$0.60/月（仅 Claude）
- AssemblyAI：$5.60/月（更高准确率）
- OpenAI Whisper：$7.80/月

---

## 🔑 配置 API Key

### 方法 1：环境变量（推荐）

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export ASSEMBLYAI_API_KEY='aai_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# 重新加载配置
source ~/.bashrc
```

### 方法 2：直接在脚本中配置

编辑 `assemblyai_summarizer.py`：

```python
# 在文件开头修改
ASSEMBLYAI_API_KEY = "aai_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## ✅ 验证配置

```bash
# 运行验证脚本
python verify_assemblyai_setup.py
```

**预期输出**：
```
✓ AssemblyAI Python SDK 已安装
✓ API Key 已配置
✓ API Key 有效
✓ Claude API 配置正确

🎉 所有配置已就绪！
```

---

## 🚀 使用示例

### 单文件处理

```bash
python assemblyai_summarizer.py "/path/to/meeting.mp3"
```

### 自动监控

```bash
python assemblyai_auto_monitor.py
```

---

## 📊 功能对比

| 功能 | Vosk | AssemblyAI |
|------|------|------------|
| 成本 | 免费 | $0.25/小时 |
| 准确率 | 中等 | 高 |
| 中文支持 | ✓ | ✓ |
| 离线使用 | ✓ | ✗ |
| 说话人识别 | ✗ | ✓ |
| 标点符号 | 基础 | 智能 |
| 处理速度 | 慢 | 快 |

---

## 🔧 故障排查

### 问题 1：API Key 无效

**症状**：
```
❌ Error: 401 Unauthorized
```

**解决**：
1. 检查 API Key 是否正确复制（包含 `aai_` 前缀）
2. 确认 API Key 未过期
3. 在 Dashboard 重新生成新的 API Key

### 问题 2：超出免费额度

**症状**：
```
❌ Error: 402 Payment Required
```

**解决**：
1. 登录 Dashboard 查看使用量
2. 添加付款方式继续使用
3. 或切换到 Vosk 免费方案

### 问题 3：转录失败

**症状**：
```
❌ Error: Transcription failed
```

**解决**：
1. 检查音频文件格式（支持 mp3, wav, m4a, mp4）
2. 确认文件大小 < 5GB
3. 检查网络连接

---

## 📁 相关文件

- **转录脚本**：`assemblyai_summarizer.py`
- **验证脚本**：`verify_assemblyai_setup.py`
- **自动监控**：`assemblyai_auto_monitor.py`

---

## 🔗 有用链接

- [注册页面](https://www.assemblyai.com/dashboard/signup)
- [API 文档](https://www.assemblyai.com/docs)
- [定价信息](https://www.assemblyai.com/pricing)
- [获取 API Key](https://www.assemblyai.com/docs/faq/how-to-get-your-api-key)

---

## 📝 注册检查清单

- [ ] 访问注册页面
- [ ] 填写邮箱和密码
- [ ] 验证邮箱
- [ ] 登录 Dashboard
- [ ] 创建 API Key
- [ ] 保存 API Key
- [ ] 配置环境变量或脚本
- [ ] 运行验证脚本
- [ ] 测试转录功能

完成后即可开始使用！🎉
