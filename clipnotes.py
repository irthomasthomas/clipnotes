import tempfile
import os
from threading import Thread
import time
from typing import Optional
from datetime import datetime

try:
    import pyperclip
except ImportError:
    print("pyperclip module is not installed. Please install it using 'pip install pyperclip'.")
    exit(1)

class ClipboardMonitor:
    def __init__(self, sleep_time: float = 1.0, add_timestamps: bool = True):
        self.monitoring: bool = False
        self.output_file: str = ""
        self.last_clipboard_content: str = ""
        self.sleep_time: float = sleep_time
        self.add_timestamps: bool = add_timestamps

    def start_monitoring(self, paper_title: str) -> None:
        if not paper_title:
            raise ValueError("Paper title cannot be empty.")
        
        self.output_file = tempfile.mktemp(suffix=".txt")
        print(f"Monitoring clipboard for paper: {paper_title}")
        print(f"Copied items will be saved to: {self.output_file}")
        
        try:
            with open(self.output_file, 'w') as f:
                f.write(f"Notes for {paper_title}\n")
        except IOError as e:
            print(f"Error writing to file: {e}")
            return

        self.monitoring = True
        self._start_clipboard_monitoring()

    def stop_monitoring(self) -> None:
        print("Stopping clipboard monitoring")
        print(f"File path copied to clipboard: {self.output_file}")
        try:
            pyperclip.copy(self.output_file)
        except pyperclip.PyperclipException as e:
            print(f"Error copying to clipboard: {e}")
        self.monitoring = False

    def _clipboard_monitoring_task(self) -> None:
        while self.monitoring:
            try:
                current_clip = pyperclip.paste()
                if current_clip != self.last_clipboard_content:
                    self._write_to_file(current_clip)
                    self.last_clipboard_content = current_clip
            except pyperclip.PyperclipException as e:
                print(f"Error accessing clipboard: {e}")
            time.sleep(self.sleep_time)

    def _write_to_file(self, content: str) -> None:
        try:
            with open(self.output_file, 'a') as f:
                f.write("\n............\n")
                if self.add_timestamps:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}]\n")
                f.write(content + "\n")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def _start_clipboard_monitoring(self) -> None:
        thread = Thread(target=self._clipboard_monitoring_task)
        thread.daemon = True
        thread.start()

def main() -> None:
    clipboard_monitor = ClipboardMonitor()
    paper_title = input("Enter the title of the paper you're reading: ")
    
    if paper_title:
        clipboard_monitor.start_monitoring(paper_title)
        try:
            while clipboard_monitor.monitoring:
                input("Press Enter to stop monitoring, or Ctrl+C to exit: ")
                clipboard_monitor.stop_monitoring()
        except KeyboardInterrupt:
            print("\nExiting.")
            clipboard_monitor.monitoring = False
    else:
        print("No paper title provided. Exiting.")

if __name__ == "__main__":
    main()