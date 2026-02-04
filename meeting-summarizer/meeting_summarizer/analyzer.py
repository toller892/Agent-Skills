"""
Analyzer module using Claude API
"""
from anthropic import Anthropic


class MeetingAnalyzer:
    def __init__(self, api_key: str):
        """
        Initialize analyzer with Anthropic API key

        Args:
            api_key: Anthropic API key
        """
        self.client = Anthropic(api_key=api_key)

    def analyze(self, transcript: str, meeting_metadata: dict = None) -> dict:
        """
        Analyze meeting transcript using Claude

        Args:
            transcript: Meeting transcript text
            meeting_metadata: Optional metadata about the meeting

        Returns:
            dict with summary, decisions, and action_items
        """
        prompt = self._build_prompt(transcript, meeting_metadata)

        print("Analyzing transcript with Claude...")

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Parse Claude's response
        response_text = message.content[0].text
        return self._parse_response(response_text)

    def _build_prompt(self, transcript: str, metadata: dict = None) -> str:
        """Build analysis prompt for Claude"""
        metadata_str = ""
        if metadata:
            metadata_str = f"\n\n**会议元数据：**\n"
            for key, value in metadata.items():
                metadata_str += f"- {key}: {value}\n"

        return f"""请分析以下会议录音转录文本，并生成结构化摘要。

**转录文本：**
{transcript}
{metadata_str}

请按以下格式输出：

## 会议摘要
[用 2-3 段话概括会议的主要内容和讨论重点]

## 关键决策点
[列出会议中做出的重要决策，每个决策一行，使用 "- " 开头]

## 行动项
[列出需要执行的行动项，格式为：]
- [行动项描述] | 负责人: [姓名] | 截止日期: [日期]

请确保输出清晰、准确、可操作。如果某些信息在转录中不明确，请标注为 "待确认"。
"""

    def _parse_response(self, response: str) -> dict:
        """Parse Claude's structured response"""
        sections = {
            "summary": "",
            "decisions": [],
            "action_items": []
        }

        current_section = None
        lines = response.split('\n')

        for line in lines:
            line = line.strip()

            if line.startswith('## 会议摘要'):
                current_section = 'summary'
                continue
            elif line.startswith('## 关键决策点'):
                current_section = 'decisions'
                continue
            elif line.startswith('## 行动项'):
                current_section = 'action_items'
                continue

            if not line or line.startswith('#'):
                continue

            if current_section == 'summary':
                sections['summary'] += line + '\n'
            elif current_section == 'decisions' and line.startswith('-'):
                sections['decisions'].append(line[1:].strip())
            elif current_section == 'action_items' and line.startswith('-'):
                # Parse action item: "description | 负责人: name | 截止日期: date"
                parts = line[1:].split('|')
                action_item = {
                    "description": parts[0].strip() if len(parts) > 0 else "",
                    "assignee": parts[1].replace('负责人:', '').strip() if len(parts) > 1 else "待确认",
                    "deadline": parts[2].replace('截止日期:', '').strip() if len(parts) > 2 else "待确认"
                }
                sections['action_items'].append(action_item)

        sections['summary'] = sections['summary'].strip()
        return sections
