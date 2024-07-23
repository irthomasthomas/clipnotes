import tempfile
import os
from threading import Thread
import time
import argparse
import sys

try:
    import pyperclip
except ImportError:
    print("pyperclip module is not installed. Please install it using 'pip install pyperclip'.")
    exit(1)

class ClipboardMonitor:
    def __init__(self, pipe_to_stdout=False, paper_title=None):
        self.monitoring = False
        self.output_file = ""
        self.last_clipboard_content = ""
        self.pipe_to_stdout = pipe_to_stdout
        self.paper_title = paper_title

    def toggle_monitoring(self):
        if self.monitoring:
            print("Stopping clipboard monitoring", file=sys.stderr)
            if not self.pipe_to_stdout:
                print(f"File path copied to clipboard: {self.output_file}", file=sys.stderr)
                pyperclip.copy(self.output_file)
            self.monitoring = False
        else:
            if not self.paper_title:
                if sys.stdin.isatty() and sys.stdout.isatty():
                    self.paper_title = os.popen("kdialog --inputbox 'Enter the title of the paper'").read().strip()
                else:
                    self.paper_title = "Untitled Paper"

            if self.paper_title:
                if not self.pipe_to_stdout:
                    self.output_file = tempfile.mktemp(suffix=".txt")
                    print(f"Monitoring clipboard for paper: {self.paper_title}", file=sys.stderr)
                    print(f"Copied items will be saved to: {self.output_file}", file=sys.stderr)
                    with open(self.output_file, 'w') as f:
                        f.write(f"Notes for {self.paper_title}\n")
                    os.system(f"xdg-open {self.output_file}")
                else:
                    print(f"Monitoring clipboard for paper: {self.paper_title}", file=sys.stderr)
                    print(f"Notes for {self.paper_title}")
                self.monitoring = True
                self._start_clipboard_monitoring()
            else:
                print("No paper title provided. Exiting.", file=sys.stderr)

    def _clipboard_monitoring_task(self):
        self.last_clipboard_content = pyperclip.paste()
        entry_counter = 1
        while self.monitoring:
            current_clip = pyperclip.paste()
            if current_clip != self.last_clipboard_content:
                if self.pipe_to_stdout:
                    print(f"\n--- Entry {entry_counter} ---")
                    print(current_clip)
                    print("------------------------")
                    sys.stdout.flush()
                    entry_counter += 1
                else:
                    with open(self.output_file, 'a') as f:
                        f.write(f"\n--- Entry {entry_counter} ---\n")
                        f.write(current_clip + "\n")
                        f.write("------------------------\n")
                        entry_counter += 1
                self.last_clipboard_content = current_clip
            time.sleep(0.5)

    def _start_clipboard_monitoring(self):
        thread = Thread(target=self._clipboard_monitoring_task)
        thread.daemon = True
        thread.start()

def main():
    parser = argparse.ArgumentParser(description="Monitor clipboard and save content to file or stdout.")
    parser.add_argument("--stdout", action="store_true", help="Pipe output to stdout instead of saving to a file")
    parser.add_argument("--title", type=str, help="Specify the paper title")
    args = parser.parse_args()

    clipboard_monitor = ClipboardMonitor(pipe_to_stdout=args.stdout, paper_title=args.title)
    clipboard_monitor.toggle_monitoring()

    try:
        while clipboard_monitor.monitoring:
            if sys.stdin.isatty():
                input("Press Enter to stop monitoring, or Ctrl+C to exit: ")
                clipboard_monitor.toggle_monitoring()
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting.", file=sys.stderr)
        clipboard_monitor.monitoring = False

if __name__ == "__main__":
    main()