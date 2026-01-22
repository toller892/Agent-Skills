"""通知推送模块"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional
from datetime import datetime


class Notifier:
    """通知推送器"""
    
    def __init__(self, method: str = "system"):
        """
        初始化通知器
        
        Args:
            method: 通知方式 - system, slack, email
        """
        self.method = method
    
    def notify(
        self,
        title: str,
        message: str,
        file_path: Optional[Path] = None,
    ) -> bool:
        """发送通知"""
        if self.method == "system":
            return self._system_notify(title, message, file_path)
        elif self.method == "slack":
            return self._slack_notify(title, message, file_path)
        elif self.method == "email":
            return self._email_notify(title, message)
        else:
            print(f"Unknown notification method: {self.method}")
            return False
    
    def _system_notify(
        self,
        title: str,
        message: str,
        file_path: Optional[Path] = None,
    ) -> bool:
        """系统通知（跨平台）"""
        try:
            if sys.platform == "darwin":
                # macOS
                script = f'''
                display notification "{message}" with title "{title}"
                '''
                subprocess.run(["osascript", "-e", script], check=True)
                
                # 如果有文件路径，打开 Obsidian
                if file_path:
                    obsidian_uri = f"obsidian://open?path={file_path}"
                    subprocess.run(["open", obsidian_uri])
                
            elif sys.platform == "win32":
                # Windows - 使用 PowerShell toast notification
                ps_script = f'''
                [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
                [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
                
                $template = @"
                <toast>
                    <visual>
                        <binding template="ToastText02">
                            <text id="1">{title}</text>
                            <text id="2">{message}</text>
                        </binding>
                    </visual>
                </toast>
"@
                
                $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
                $xml.LoadXml($template)
                $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
                [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Daily Digest").Show($toast)
                '''
                
                # 简化版：使用 msg 命令
                subprocess.run(
                    ["msg", "*", f"{title}\n{message}"],
                    shell=True,
                    capture_output=True,
                )
                
                # 打开 Obsidian
                if file_path:
                    obsidian_uri = f"obsidian://open?path={file_path}"
                    os.startfile(obsidian_uri)
                
            elif sys.platform.startswith("linux"):
                # Linux - 使用 notify-send
                subprocess.run(
                    ["notify-send", title, message],
                    check=True,
                )
                
                if file_path:
                    obsidian_uri = f"obsidian://open?path={file_path}"
                    subprocess.run(["xdg-open", obsidian_uri])
            
            return True
            
        except Exception as e:
            print(f"System notification failed: {e}")
            return False
    
    def _slack_notify(
        self,
        title: str,
        message: str,
        file_path: Optional[Path] = None,
    ) -> bool:
        """Slack 通知"""
        try:
            import requests
            
            webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
            if not webhook_url:
                print("SLACK_WEBHOOK_URL not set")
                return False
            
            payload = {
                "text": f"*{title}*\n{message}",
            }
            
            if file_path:
                obsidian_uri = f"obsidian://open?path={file_path}"
                payload["text"] += f"\n<{obsidian_uri}|📖 在 Obsidian 中打开>"
            
            resp = requests.post(webhook_url, json=payload, timeout=10)
            return resp.status_code == 200
            
        except Exception as e:
            print(f"Slack notification failed: {e}")
            return False
    
    def _email_notify(self, title: str, message: str) -> bool:
        """邮件通知"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.environ.get("SMTP_PORT", "587"))
            username = os.environ.get("SMTP_USERNAME")
            password = os.environ.get("SMTP_PASSWORD")
            to_email = os.environ.get("NOTIFY_EMAIL")
            
            if not all([username, password, to_email]):
                print("Email configuration incomplete")
                return False
            
            msg = MIMEText(message)
            msg["Subject"] = title
            msg["From"] = username
            msg["To"] = to_email
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Email notification failed: {e}")
            return False
    
    def open_in_obsidian(self, file_path: Path) -> bool:
        """在 Obsidian 中打开文件"""
        try:
            # 构建 Obsidian URI
            obsidian_uri = f"obsidian://open?path={file_path.absolute()}"
            
            if sys.platform == "darwin":
                subprocess.run(["open", obsidian_uri])
            elif sys.platform == "win32":
                os.startfile(obsidian_uri)
            else:
                subprocess.run(["xdg-open", obsidian_uri])
            
            return True
            
        except Exception as e:
            print(f"Failed to open Obsidian: {e}")
            return False


def send_daily_notification(file_path: Path, method: str = "system") -> bool:
    """发送每日摘要通知"""
    notifier = Notifier(method=method)
    
    today = datetime.now().strftime("%Y-%m-%d")
    title = f"📰 每日摘要已就绪"
    message = f"{today} 的信息摘要已生成，点击在 Obsidian 中查看"
    
    return notifier.notify(title, message, file_path)


if __name__ == "__main__":
    # 测试
    notifier = Notifier(method="system")
    notifier.notify(
        "测试通知",
        "这是一条测试消息",
    )
