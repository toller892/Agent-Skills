# Paper Interpreter Skill

论文→黄叔风格解读+纽约客插画+2026设计网页。

## 快速开始

查看 `references/QUICKSTART.md` 获取快速上手指南。

## 项目结构

```
paper-interpreter/
├── SKILL.md              # Skill 定义文件（必需）
├── scripts/              # 可执行代码
│   ├── paper_interpreter.py
│   ├── diagnose.py
│   ├── example_usage.py
│   ├── quick_test.py
│   ├── requirements.txt
│   └── .env.example
├── references/           # 文档资料
│   ├── README.md
│   ├── WORKFLOW.md
│   ├── QUICKSTART.md
│   ├── TOKEN_SETUP.md
│   └── NANO_BANANA_SETUP.md
└── assets/               # 图片等资源
```

## 使用方法

直接对 AI Agent 说：

"解析这篇论文：https://arxiv.org/pdf/2301.12345.pdf"

或者

"黄叔风格解读这篇"

## 环境配置

需要设置 `NANO_BANANA_TOKEN` 环境变量。

详见 `references/TOKEN_SETUP.md`
