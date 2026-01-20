# Markdown 到 Typst 格式自动转换

## 问题

Typst 和 Markdown 的粗体语法不同：
- **Markdown**: `**粗体文本**`
- **Typst**: `*粗体文本*`

如果在 Typst 文件中使用 `**text**`，会出现警告：
```
No text within stars (warning, line X)
```

## 解决方案

Skill 现在会自动转换格式：

### 在 JSON 数据中

你可以使用 Markdown 格式：

```json
{
  "summary": "这是一个 **重要** 的项目",
  "sections": [
    {
      "type": "text",
      "content": "**核心功能**: 支持自动转换"
    },
    {
      "type": "list",
      "items": [
        "**特性1**: 描述",
        "**特性2**: 描述"
      ]
    }
  ]
}
```

### 生成的 .typ 文件

Skill 会自动转换为 Typst 格式：

```typst
这是一个 *重要* 的项目

*核心功能*: 支持自动转换

- *特性1*: 描述
- *特性2*: 描述
```

## 影响的脚本

以下脚本已更新，包含自动转换功能：

1. `generate_standalone.py` - 独立版本生成器
2. `generate.py` - 标准生成器
3. `generate_report.py` - 完整工作流（通过调用上述脚本）

## 转换规则

使用正则表达式：`\*\*([^*]+)\*\*` → `*\1*`

- 匹配：`**文本**`
- 替换为：`*文本*`
- 不影响：已经是单星号的文本

## 测试

生成报告后，在 Typst 在线编辑器中不应再出现 "No text within stars" 警告。
