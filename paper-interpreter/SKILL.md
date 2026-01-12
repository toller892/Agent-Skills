---
name: paper-interpreter
description: 论文→推文串解读。把学术论文变成病毒式传播的 Twitter Thread。
keywords: [论文, 推文, Thread, arxiv, 推特, Twitter, 病毒传播, 科普]
---

# 论文解析器

把学术论文变成推文串。

病毒式传播格式。
让复杂研究人人能懂。

---

## 输出格式：推文串 (Twitter Thread)

最终输出是一个完整的推文串，包含 8-15 条推文。

### 推文串结构

**1/ 钩子推文 (Hook)**

开篇必须在 0.5 秒内抓住注意力。

模板选择：
- 逆向思维："大多数人对 [主题] 的理解都是错的。"
- 数字冲击："这篇论文让 [指标] 提升了 47%。"
- 悬念制造："[大公司] 刚刚开源了一个改变游戏规则的东西。"

示例：
```
OpenAI 刚发了一篇论文。

悄悄的。没有发布会。

但这可能是 2024 年最重要的 AI 突破。

我花了 6 小时读完。

这是你需要知道的一切 🧵👇
```

**2/ 背景推文 (Context)**

一句话说清楚这篇论文解决什么问题。

```
先说问题：

现在的大模型有个致命缺陷——

它们会"幻觉"。

就是一本正经地胡说八道。

这篇论文？直接把幻觉率砍了 73%。
```

**3/ 核心发现推文 (Key Findings)**

每条推文只讲一个点。
用类比让外行秒懂。

```
核心思路其实很简单：

想象你在考试。

以前的 AI：闭卷考，全靠记忆，记错了就瞎编。

新方法：开卷考，随时查资料，但要标注出处。

就这么简单。但效果炸裂。
```

**4/ 技术细节推文 (Technical)**

给懂行的人看。
但依然要易读。

```
技术细节（给硬核读者）：

他们用了一个 retrieval-augmented 架构

简单说就是：
• 生成前先检索
• 检索结果作为 context
• 强制模型引用来源

不是新概念，但他们的实现方式很巧妙 👇
```

**5/ 数据/图表推文 (Data)**

配图说明。
让数据可视化。

```
看这张图就懂了：

[配图：论文核心图表的简化版]

蓝线：传统方法
红线：新方法

差距一目了然。

尤其在长文本生成时，优势更明显。
```

**6/ 影响推文 (Implications)**

这对普通人意味着什么。

```
这对你意味着什么？

如果你用 ChatGPT 写研究报告——

以后可能不用再逐条核实了。

AI 会自己标注"这句话来自哪里"。

事实核查？内置了。
```

**7/ 局限性推文 (Limitations)**

保持客观。
建立信任。

```
但别高兴太早。

局限性：
• 只在英文上测试过
• 计算成本增加 40%
• 实时信息还是搞不定

不是银弹。但方向对了。
```

**8/ 总结推文 (TL;DR)**

给跳到最后的人。

```
TL;DR（太长不看版）：

1. 问题：AI 爱瞎编
2. 方案：生成时强制引用来源
3. 效果：幻觉率降 73%
4. 代价：慢 40%
5. 意义：AI 可信度大幅提升

论文链接：[链接]
```

**9/ CTA 推文 (Call to Action)**

引导互动。

```
如果这个 thread 帮到你了：

1. 转发第一条推文
2. 关注我 @xxx 获取更多 AI 论文解读

每周拆解一篇改变行业的论文。

用人话。不用黑话。
```

---

## 推文写作规范

### 字符控制
- 每条推文 ≤ 280 字符（中文约 140 字）
- 宁可拆成两条，不要挤成一坨

### 视觉节奏
- 每句话独立成行
- 段落之间空行
- 避免超过 3 行的段落

### 语气
- 全小写可选（制造轻松感）
- 省略句号（句号=冷漠）
- 用 ... 或 — 制造停顿

### Emoji 使用
- 🧵 表示 thread 开始
- 👇 引导继续阅读
- 💡 标记关键洞察
- ⚠️ 标记警告/局限
- 🔥 标记重要发现
- 每条推文最多 2 个 emoji

### 钩子技巧
- 数字具体化："47%" 比 "大幅提升" 强
- 制造悬念："但有个问题..."
- 逆向开场："大多数人不知道..."
- 权威背书："Google 刚刚..."

### 禁忌
- ❌ 学术黑话（除非立刻解释）
- ❌ 长段落
- ❌ 被动语态
- ❌ "本文将介绍..." 这种官腔
- ❌ 过度使用感叹号!!!

---

## 工作流

### 1/ 读取文件 �

用户提供本地文件路径，直接读取内容。

支持格式：
- `.md` - Markdown 文件
- `.pdf` - PDF 文档
- `.txt` - 纯文本文件
- `.doc` / `.docx` - Word 文档

读取方式：
```
readFile: 读取用户指定的本地文件路径
```

示例输入：
```
"把这个文件变成推文串：D:/papers/attention.pdf"
"解读这篇：./research/gpt4-report.md"
"推特风格解读：~/Documents/论文.docx"
```

### 2/ 提炼要点 📝

从论文中提取：
- 一句话问题描述
- 核心方法（用类比解释）
- 关键数据点
- 实际影响
- 局限性

### 3/ 生成推文串 🐦

按照上述结构生成 8-15 条推文。

每条推文：
- 独立可读
- 有钩子引向下一条
- 符合字符限制

### 4/ 配图生成 🎨

API: Nano Banana (Gemini 2.5 Flash)

为关键推文生成配图：
- 简化版论文图表
- 概念可视化
- 对比图

风格：
- 极简
- 高对比
- 适合手机屏幕

### 5/ 输出 📤

生成完整推文串文件：
- 每条推文带编号
- 标注配图位置
- 包含论文原链接

---

## 输出示例

```markdown
# [论文标题] 推文串

## 1/12 🧵

[钩子内容]

---

## 2/12

[背景内容]

---

## 3/12

[核心发现]

[配图: illustration_01.png]

---

...

## 12/12

[CTA]

---

论文链接: https://arxiv.org/abs/xxxx.xxxxx
```

---

## 怎么用

直接说：

"把这个文件变成推文串：D:/papers/attention.pdf"

或者

"推特风格解读这个：./research/report.md"

或者

"帮我写个 thread：~/Documents/论文.docx"

支持格式：md、pdf、txt、doc/docx

---

## 输出文件

```
输出目录/
├── {文件名}/
│   ├── thread.md          # 推文串正文
│   ├── thread.html        # 图文并茂版（截图用）
│   ├── thread_images/     # 配图
│   │   ├── 01_hook.png
│   │   ├── 03_diagram.png
│   │   └── ...
│   └── metadata.json      # 源文件元信息
```

---

## HTML 输出规范

`thread.html` 专为截图发推设计。

### 设计要求

**尺寸适配**
- 宽度固定 600px（推特图片最佳宽度）
- 每条推文独立卡片
- 卡片间距 20px

**视觉风格**
- 深色模式（#15202B 背景，推特同款）
- 白色文字 #E7E9EA
- 圆角卡片 16px
- 头像 + 用户名模拟真实推文

**字体**
- 系统字体栈：-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto
- 正文 15px
- 行高 1.5

**配图嵌入**
- 图片直接嵌入卡片内
- 圆角 12px
- 最大宽度 100%

### HTML 结构示例

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      background: #15202B;
      padding: 20px;
      max-width: 600px;
      margin: 0 auto;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .tweet {
      background: #192734;
      border-radius: 16px;
      padding: 16px;
      margin-bottom: 20px;
      color: #E7E9EA;
    }
    .tweet-header {
      display: flex;
      align-items: center;
      margin-bottom: 12px;
    }
    .avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: #1DA1F2;
      margin-right: 12px;
    }
    .username {
      font-weight: bold;
    }
    .handle {
      color: #8899A6;
    }
    .tweet-content {
      font-size: 15px;
      line-height: 1.5;
      white-space: pre-line;
    }
    .tweet-image {
      margin-top: 12px;
      border-radius: 12px;
      max-width: 100%;
    }
    .thread-line {
      width: 2px;
      height: 20px;
      background: #38444D;
      margin-left: 23px;
    }
  </style>
</head>
<body>
  <div class="tweet">
    <div class="tweet-header">
      <div class="avatar"></div>
      <div>
        <div class="username">Your Name</div>
        <div class="handle">@yourhandle · 1/12</div>
      </div>
    </div>
    <div class="tweet-content">推文内容在这里

支持换行显示</div>
    <img class="tweet-image" src="thread_images/01_hook.png">
  </div>
  <div class="thread-line"></div>
  <!-- 更多推文卡片 -->
</body>
</html>
```

### 截图指南

1. 浏览器打开 `thread.html`
2. 使用浏览器截图或截图工具
3. 每 2-3 条推文截一张图
4. 发推时作为图片附件上传

**推荐截图尺寸**：600 x 800px（单张含 2-3 条推文）

---

## 环境变量

`NANO_BANANA_TOKEN`

必需。用于生成配图。

---

## 依赖

```
pip install requests
```

完事。
