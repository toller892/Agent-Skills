"""
Main processor that orchestrates transcription, analysis, and notification
"""
from .transcriber import Transcriber
from .analyzer import MeetingAnalyzer
from .notifier import SlackNotifier


class MeetingProcessor:
    def __init__(self, config: dict):
        """
        Initialize meeting processor

        Args:
            config: Configuration dictionary
        """
        self.config = config

        # Initialize components
        cache_dir = config.get('processing', {}).get('cache_dir')
        if cache_dir:
            import os
            cache_dir = os.path.expanduser(cache_dir)

        self.transcriber = Transcriber(
            api_key=config['openai']['api_key'],
            cache_dir=cache_dir
        )

        self.analyzer = MeetingAnalyzer(
            api_key=config['anthropic']['api_key']
        )

        self.notifier = SlackNotifier(
            webhook_url=config['slack']['webhook_url']
        )

    def process(self, audio_file_path: str) -> dict:
        """
        Process a meeting audio file

        Args:
            audio_file_path: Path to audio file

        Returns:
            dict with processing results
        """
        print(f"\n{'='*60}")
        print(f"Processing: {audio_file_path}")
        print(f"{'='*60}\n")

        # Step 1: Transcribe
        transcript_result = self.transcriber.transcribe(audio_file_path)
        transcript_text = transcript_result['text']
        metadata = transcript_result['metadata']

        print(f"✓ Transcription complete ({len(transcript_text)} characters)")

        # Step 2: Analyze
        analysis = self.analyzer.analyze(transcript_text, metadata)

        print(f"✓ Analysis complete")
        print(f"  - Summary: {len(analysis['summary'])} characters")
        print(f"  - Decisions: {len(analysis['decisions'])} items")
        print(f"  - Action items: {len(analysis['action_items'])} items")

        # Step 3: Notify
        success = self.notifier.send_summary(analysis, metadata['file'])

        if success:
            print(f"✓ Notification sent to Slack")
        else:
            print(f"✗ Failed to send notification")

        result = {
            "file": audio_file_path,
            "transcript": transcript_result,
            "analysis": analysis,
            "notification_sent": success
        }

        print(f"\n{'='*60}")
        print(f"Processing complete!")
        print(f"{'='*60}\n")

        return result
