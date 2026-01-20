// 自动生成的报告 - 独立版本
// 生成时间: 2026-01-20 08:07:34
// 可直接在 Typst 在线编辑器中使用

#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  numbering: "1",
  header: context {
    align(right)[
      #text(size: 9pt, fill: gray)[🚀 AdCP：广告业的 AI 革命协议]
    ]
    line(length: 100%, stroke: 0.5pt + gray)
  },
  footer: context {
    line(length: 100%, stroke: 0.5pt + gray)
    v(0.25cm)
    align(center)[
      #text(size: 9pt, fill: gray)[第 #counter(page).display() 页]
    ]
  },
)

#set text(
  font: ("Noto Sans", "Noto Sans CJK SC"),
  size: 10.5pt,
  lang: "zh",
)

#set heading(numbering: "1.1")

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(1cm)
  text(size: 18pt, weight: "bold", fill: rgb("#0056b3"))[#it]
  v(0.5cm)
}

#show heading.where(level: 2): it => {
  v(0.5cm)
  text(size: 14pt, weight: "bold", fill: rgb("#343a40"))[#it]
  v(0.25cm)
}

#set par(justify: true, leading: 0.65em, first-line-indent: 2em)
#show heading: it => { it; par(first-line-indent: 0em)[] }

#set list(marker: [•], indent: 1em)
#set enum(numbering: "1.", indent: 1em)

#let styled-table(..args) = {
  table(
    stroke: (x, y) => {
      if y == 0 { (bottom: 2pt + rgb("#0056b3")) }
      else { (bottom: 0.5pt + gray) }
    },
    fill: (x, y) => {
      if y == 0 { rgb("#f8f9fa") }
      else if calc.rem(y, 2) == 0 { rgb("#f8f9fa").lighten(50%) }
    },
    inset: 0.5cm,
    ..args
  )
}

#let kpi-card(label, value, change) = {
  rect(
    width: 100%, fill: rgb("#f8f9fa"), stroke: 1pt + rgb("#dee2e6"),
    radius: 4pt, inset: 1cm,
  )[
    #text(size: 10pt, fill: rgb("#6c757d"), weight: "medium")[#label]
    #v(0.25cm)
    #text(size: 24pt, weight: "bold", fill: rgb("#0056b3"))[#value]
    #if change != none [
      #v(0.25cm)
      #let change-color = if change >= 0 { rgb("#28a745") } else { rgb("#dc3545") }
      #let change-icon = if change >= 0 { "↑" } else { "↓" }
      #let change-percent = calc.round(change * 100, digits: 0)
      #text(size: 12pt, fill: change-color, weight: "medium")[#change-icon #change-percent%]
    ]
  ]
}

#page(margin: 0cm, header: none, footer: none)[
  #place(top + center, dy: 30%)[
    #text(size: 28pt, weight: "bold", fill: rgb("#0056b3"))[🚀 AdCP：广告业的 AI 革命协议]

    #v(0.5cm)
    
    #text(
      size: 16pt,
      fill: rgb("#6c757d"),
    )[🎯 一句话总结]
    #v(2cm)
    #text(size: 14pt, fill: rgb("#495057"))[AI 生成]
    #v(0.25cm)
    #text(size: 12pt, fill: rgb("#6c757d"))[
      #datetime.today().display("[year]年[month]月[day]日")
    ]
  ]
]

#page[
  #outline(
    title: [
      #text(size: 18pt, weight: "bold", fill: rgb("#0056b3"))[目录]
      #v(1cm)
    ],
    indent: auto,
    depth: 3,
  )
]

= 概览

*本文由 AI 根据《Ad Context Protocol (AdCP) 与代理式 AI 广告架构》深度研究报告提炼生成*

== 关键指标

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 1cm,
  
  kpi-card("文档长度", "62 字符", 0),
  kpi-card("章节数量", "24 个", 0),
  kpi-card("表格数量", "2 个", 0),
)

= 🚀 AdCP：广告业的 AI 革命协议



== 🎯 一句话总结

AdCP（Ad Context Protocol）是首个专为 *AI 智能体*设计的广告通信标准，它标志着数字广告从"*机器跑腿*"（自动化执行）迈向"*AI谈判*"（智能化决策）的历史性转折点。简单来说：以前是人类填表格让机器买广告，未来是AI代表品牌直接和AI代表媒体谈判。

== 💎 核心要点



=== 1️⃣ 现有系统的三大致命缺陷

❌ *语义流失*：品牌想投"环保意识强的文章旁"，但被翻译成粗糙的关键词"环保"

❌ *人工瓶颈*：人类媒体策划被迫花大量时间在DSP里配置白名单、黑名单、各种定向条件

❌ *围墙花园垄断*：Google、Meta、Amazon拥有封闭生态，开放网络处于劣势

=== 2️⃣ AdCP 的革命性变化

#styled-table(
  columns: (1fr, 1fr),
  [*传统程序化 (OpenRTB)*], [*代理式广告 (AdCP)*],
  [⏱️ 毫秒级拍卖], [🤔 异步协商（可花时间思考）],
  [📋 僵化的规则匹配], [🧠 基于意图的推理],
  [🔢 冷漠的数字ID], [💬 自然语言沟通],
  [👤 人肉接口操作], [🤖 AI自主谈判],
)

=== 3️⃣ 建立在什么技术上？

*MCP (Model Context Protocol)* — 由 Anthropic 开源，被称为"AI的USB-C接口"

> 如果 MCP 是 USB-C 接口，AdCP 就是在这个接口上传输的"广告专用指令集"

== 🧠 核心概念



=== 什么是"代理式 AI" (Agentic AI)？

- 🔍 *感知环境*
- 🧠 *推理规划*
- 🔧 *使用工具*自主执行任务

=== 六大核心智能体

#styled-table(
  columns: (1fr, 1fr, 1fr),
  [*代理*], [*角色*], [*能力*],
  [🏪 *卖方代理*], [媒体的"数字店面"], [主动推销、拒绝低价、发起反报价],
  [💰 *买方代理*], [品牌的"全能执行者"], [翻译营销目标、跨平台寻找最优资源],
  [📊 *信号代理*], [隐私问题的解决者], ["可用不可见"地激活受众数据],
  [🎨 *创意代理*], [GenAI的连接器], [自动生成、调整、预检素材],
  [🎼 *编排代理*], [总指挥], [协调所有代理按序执行任务],
  [📈 *测量代理*], [反馈闭环], [回传数据让AI从错误中学习],
)

== 🚀 实战案例：AI 如何完成一笔广告交易



=== 背景

一个户外品牌想在英国投放广告，目标是"*道德攀岩者*"，要求供应链必须低碳。

=== 阶段1️⃣：意图定义

> *人类*："为我们新款夹克规划活动。目标英国关心可持续发展的攀岩者。预算5万。避免广告量过大的网站。"
>
> *买方代理*：识别出意图 → 攀岩 + 英国 + 可持续性约束 + \$50k预算

=== 阶段2️⃣：发现与信号侦讯

> *买方代理*广播："查询：受众 > 攀岩 + 可持续性。地区：英国。"
>
> *卖方代理A*："我有'体育'受众。相关性：低。" ❌
>
> *卖方代理B*："我有'攀岩爱好者'。数据新鲜度：24小时。碳排放：A级。" ✅

=== 阶段3️⃣：谈判与规划

> *买方代理*："50万曝光，视频格式，目标\$15 CPM"
>
> *卖方代理B*："Q4是旺季，反提案\$18 CPM，或改展示广告可\$15"
>
> *买方代理*："接受\$18 CPM，但要求可视度>70\%"
>
> *卖方代理B*："成交！✅"

=== 阶段4️⃣：激活与执行

- 卖方代理推送 Deal ID 到广告服务器
- 买方代理推送创意素材到 DSP
- *一笔直购交易在数秒内完成，无需人类发任何邮件！*

=== 阶段5️⃣：反馈与优化

> *卖方代理*："报告：第一天交付1万曝光，可视度75\%"
>
> *买方代理*："确认。继续交付"

== 📚 深度解读



=== AdCP 谁在推动？

- *Scope3*、*PubMatic*、*Yahoo*、*Swivel*、*Triton Digital* 等

=== 经济影响：谁赢谁输？

✅ *广告主赢*：从"购买受众ID"升级为"购买意图"，获得前所未有的可审计性

✅ *发布商赢*：夺回定价主权，可以销售内容的"语境价值"而非仅卖"眼球"

⚠️ *中间商面临转型*：仅靠信息传递赚价差的模式将消亡，必须转型为"代理托管商"

=== 三大实施挑战

🥚 *先有鸡还是先有蛋*：买卖双方都需要有代理才能起效

💸 *成本与延迟*：运行LLM进行推理需要时间和计算资源

🤖 *治理风险*：如何防止代理"幻觉"或"共谋"？需要"人机协作"机制

== 📌 总结

✅ AdCP 是*数字广告成熟的标志* — 环境复杂度已超过人类认知能力

✅ 它不是新的"广告工具"，而是*未来广告劳动力（AI代理）的操作系统*

✅ 创新方向清晰：*广告正在变得代理化*

=== 2030 愿景三阶段

| 2025-2026 | 混合期 | AdCP 与 OpenRTB 并行运行 |
| 2027-2028 | 代理翻转 | "经过推理"的曝光量超过"盲目"的曝光量 |
| 2029+ | 自主经济 | 机器对机器商务占主导，你的个人AI助理与媒体AI代理协商 |

== 🏷️ 标签

\#AdCP \#代理式AI \#程序化广告 \#MarTech \#AI革命 \#数字营销 \#广告科技 \#MCP \#Anthropic \#媒体购买

== 📊 文档统计

- 📝 原文长度：约20,000字
- 📑 章节数：7大部 + 附录
- 🎯 核心概念：15+个
- 📚 参考文献：20+篇

