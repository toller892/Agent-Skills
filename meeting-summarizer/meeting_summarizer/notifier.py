"""
Slack notifier module
"""
import requests
import json
from datetime import datetime


class SlackNotifier:
    def __init__(self, webhook_url: str):
        """
        Initialize Slack notifier

        Args:
            webhook_url: Slack webhook URL
        """
        self.webhook_url = webhook_url

    def send_summary(self, analysis: dict, meeting_file: str) -> bool:
        """
        Send meeting summary to Slack

        Args:
            analysis: Analysis result from MeetingAnalyzer
            meeting_file: Name of the meeting file

        Returns:
            bool indicating success
        """
        message = self._format_message(analysis, meeting_file)

        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(message),
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            print(f"Successfully sent summary to Slack")
            return True
        except Exception as e:
            print(f"Failed to send to Slack: {e}")
            return False

    def _format_message(self, analysis: dict, meeting_file: str) -> dict:
        """Format analysis result as Slack message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Build action items text
        action_items_text = ""
        for item in analysis.get('action_items', []):
            action_items_text += f"• {item['description']}\n"
            action_items_text += f"  👤 {item['assignee']} | 📅 {item['deadline']}\n\n"

        # Build decisions text
        decisions_text = ""
        for decision in analysis.get('decisions', []):
            decisions_text += f"• {decision}\n"

        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📝 会议摘要: {meeting_file}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"⏰ 处理时间: {timestamp}"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*📋 会议摘要*\n{analysis.get('summary', '无')}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*✅ 关键决策点*\n{decisions_text if decisions_text else '无'}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🎯 行动项*\n{action_items_text if action_items_text else '无'}"
                    }
                }
            ]
        }
