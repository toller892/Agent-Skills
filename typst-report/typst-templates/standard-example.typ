// standard-example.typ - 完全符合标准格式的示例

#import "templates/academic.typ": *

#show: academic-conf.with(
  title: "Typst 修复版示例文档",
  author: "AI 助手",
  show-header: false,
)

= 简介 (Introduction)

Typst 是一个基于 *标记* 的现代排版系统。它的特点是 *编译速度极快*，且拥有强大的脚本能力。

== 文本格式

我们不需要像 LaTeX 那样写复杂的命令：

- *加粗* 只需要用星号。
- _斜体_ 只需要用下划线。
- `代码片段` 用反引号。

= 数学公式 (Mathematics)

Typst 的数学公式语法非常直观，去掉了 LaTeX 中繁琐的反斜杠。

行内公式：爱因斯坦的方程是 $E = m c^2$。

块级公式（带自动编号）：

$ F(x) = integral_0^x frac(sin(t), t) dif t $

我们甚至可以写矩阵和多行对齐公式：

$ mat(1, 2; 3, 4) dot vec(x, y) = vec(5, 6) $

= 脚本能力 (Scripting)

这是 Typst 最酷的地方：*文档即代码*。

#let name = "Typst"
#let colors = (red, blue, green)

我现在可以使用变量：你好，#name！

下面展示一个简单的循环生成：

#for c in colors [
  - 这是一个 #text(fill: c)[彩色] 的列表项
]

= 结论

Typst 结合了 Markdown 的简洁和 LaTeX 的专业，是编写技术文档的极佳选择。
