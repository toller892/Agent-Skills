"""
File monitor using watchdog
"""
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MeetingFileHandler(FileSystemEventHandler):
    def __init__(self, processor_callback):
        """
        Initialize file handler

        Args:
            processor_callback: Function to call when new file is detected
        """
        self.processor_callback = processor_callback
        self.processed_files = set()

    def on_created(self, event):
        """Handle file creation event"""
        if event.is_directory:
            return

        file_path = event.src_path

        # Only process mp3 files
        if not file_path.lower().endswith('.mp3'):
            return

        # Avoid duplicate processing
        if file_path in self.processed_files:
            return

        print(f"New meeting file detected: {file_path}")

        # Wait a bit to ensure file is fully written
        time.sleep(2)

        # Process the file
        try:
            self.processor_callback(file_path)
            self.processed_files.add(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")


class MeetingMonitor:
    def __init__(self, watch_dir: str, processor_callback):
        """
        Initialize meeting monitor

        Args:
            watch_dir: Directory to monitor
            processor_callback: Function to call when new file is detected
        """
        self.watch_dir = Path(watch_dir).expanduser()
        self.watch_dir.mkdir(parents=True, exist_ok=True)

        self.event_handler = MeetingFileHandler(processor_callback)
        self.observer = Observer()

    def start(self):
        """Start monitoring directory"""
        print(f"Starting monitor on: {self.watch_dir}")

        self.observer.schedule(
            self.event_handler,
            str(self.watch_dir),
            recursive=False
        )
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop monitoring"""
        print("Stopping monitor...")
        self.observer.stop()
        self.observer.join()

    def process_existing_files(self):
        """Process any existing mp3 files in the directory"""
        print(f"Checking for existing files in {self.watch_dir}...")

        for file_path in self.watch_dir.glob("*.mp3"):
            if str(file_path) not in self.event_handler.processed_files:
                print(f"Processing existing file: {file_path}")
                try:
                    self.event_handler.processor_callback(str(file_path))
                    self.event_handler.processed_files.add(str(file_path))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
