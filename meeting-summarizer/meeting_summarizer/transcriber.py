"""
Transcription module using OpenAI Whisper API
"""
import os
import hashlib
import json
from pathlib import Path
from openai import OpenAI


class Transcriber:
    def __init__(self, api_key: str, cache_dir: str = None, base_url: str = None):
        """
        Initialize transcriber with OpenAI API key

        Args:
            api_key: OpenAI API key
            cache_dir: Directory to cache transcripts (optional)
            base_url: Custom API base URL (optional, for relay services)
        """
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
        self.cache_dir = Path(cache_dir) if cache_dir else None

        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of file for caching"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _get_cache_path(self, file_hash: str) -> Path:
        """Get cache file path for a given file hash"""
        return self.cache_dir / f"{file_hash}.json"

    def _load_from_cache(self, file_path: str) -> dict:
        """Load transcript from cache if available"""
        if not self.cache_dir:
            return None

        file_hash = self._get_file_hash(file_path)
        cache_path = self._get_cache_path(file_hash)

        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        return None

    def _save_to_cache(self, file_path: str, transcript: dict):
        """Save transcript to cache"""
        if not self.cache_dir:
            return

        file_hash = self._get_file_hash(file_path)
        cache_path = self._get_cache_path(file_hash)

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)

    def transcribe(self, audio_file_path: str) -> dict:
        """
        Transcribe audio file using Whisper API

        Args:
            audio_file_path: Path to audio file (mp3, mp4, wav, etc.)

        Returns:
            dict with 'text' and 'metadata'
        """
        # Check cache first
        cached = self._load_from_cache(audio_file_path)
        if cached:
            print(f"Using cached transcript for {audio_file_path}")
            return cached

        print(f"Transcribing {audio_file_path}...")

        # Transcribe using Whisper API
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )

        # Handle different response formats (official API vs relay)
        if isinstance(transcript, str):
            # Relay might return string directly
            result = {
                "text": transcript,
                "metadata": {
                    "language": "unknown",
                    "duration": 0,
                    "file": os.path.basename(audio_file_path)
                }
            }
        elif hasattr(transcript, 'text'):
            # Official API returns object with attributes
            result = {
                "text": transcript.text,
                "metadata": {
                    "language": getattr(transcript, 'language', 'unknown'),
                    "duration": getattr(transcript, 'duration', 0),
                    "file": os.path.basename(audio_file_path)
                }
            }
        else:
            # Fallback: try to parse as dict
            result = {
                "text": transcript.get('text', str(transcript)),
                "metadata": {
                    "language": transcript.get('language', 'unknown'),
                    "duration": transcript.get('duration', 0),
                    "file": os.path.basename(audio_file_path)
                }
            }

        # Save to cache
        self._save_to_cache(audio_file_path, result)

        return result
