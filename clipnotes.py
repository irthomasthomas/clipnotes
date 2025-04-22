import argparse
import configparser
import csv
import datetime
import json
import logging
import os
import platform
import signal
import sys
import time
import threading
import base64
import re
import traceback

import psutil
import pyperclip
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Set up logging
logging.basicConfig(filename='clipnotes.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Conditional imports for different operating systems
if platform.system() == "Windows":
    import win32gui
    import win32process
elif platform.system() == "Darwin":  # macOS
    try:
        from AppKit import NSWorkspace
    except ImportError:
        logging.warning("AppKit not found. Window info will be limited on macOS.")
elif platform.system() == "Linux":
    try:
        import Xlib.display
    except ImportError:
        logging.warning("Xlib not found. Window info will be limited on Linux.")

class ClipnotesError(Exception):
    """Base exception class for ClipNotes"""
    pass

class EncryptionError(ClipnotesError):
    """Raised when there's an error with encryption or decryption"""
    pass

class ClipboardAccessError(ClipnotesError):
    """Raised when there's an error accessing the clipboard"""
    pass

class FileOperationError(ClipnotesError):
    """Raised when there's an error with file operations"""
    pass

class Encryptor:
    def __init__(self, password):
        try:
            salt = b'clipnotes_salt'  # In a real-world scenario, use a random salt and store it securely
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            self.fernet = Fernet(key)
        except Exception as e:
            raise EncryptionError(f"Error initializing encryptor: {str(e)}")

    def encrypt(self, data):
        try:
            return self.fernet.encrypt(data.encode()).decode()
        except Exception as e:
            raise EncryptionError(f"Error encrypting data: {str(e)}")

    def decrypt(self, data):
        try:
            return self.fernet.decrypt(data.encode()).decode()
        except Exception as e:
            raise EncryptionError(f"Error decrypting data: {str(e)}")

class ClipboardEntry:
    def __init__(self, content, timestamp, window_info):
        self.content = content
        self.timestamp = timestamp
        self.window_info = window_info

    def to_dict(self):
        return {
            "content": self.content,
            "timestamp": self.timestamp,
            "window_info": self.window_info
        }

def get_active_window_info():
    try:
        if platform.system() == "Windows":
            return get_active_window_info_windows()
        elif platform.system() == "Darwin":
            return get_active_window_info_macos()
        elif platform.system() == "Linux":
            return get_active_window_info_linux()
        else:
            return "Unsupported OS"
    except Exception as e:
        logging.error(f"Error getting active window info: {e}")
        return "Unknown"

def get_active_window_info_windows():
    try:
        window = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(window)
        process = psutil.Process(pid)
        return f"{process.name()} - {win32gui.GetWindowText(window)}"
    except Exception as e:
        logging.error(f"Error getting Windows window info: {e}")
        return "Unknown Windows Window"

def get_active_window_info_macos():
    try:
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.activeApplication()
        app_name = active_app['NSApplicationName']
        window_title = active_app['NSApplicationPath'].split('/')[-1].split('.')[0]
        return f"{app_name} - {window_title}"
    except Exception as e:
        logging.error(f"Error getting macOS window info: {e}")
        return "Unknown macOS Window"

def get_active_window_info_linux():
    try:
        # First, try using Xlib
        display = Xlib.display.Display()
        window = display.get_input_focus().focus
        wmname = window.get_wm_name()
        wmclass = window.get_wm_class()
        if wmclass is None and wmname is None:
            return "Unknown Linux Window"
        if wmclass:
            return f"{wmclass[1]} - {wmname}"
        return wmname
    except Exception as x_error:
        logging.warning(f"Error getting Linux window info with Xlib: {x_error}")
        try:
            # Fallback to psutil
            process = psutil.Process()
            return f"{process.name()} - {process.cwd()}"
        except Exception as psutil_error:
            logging.error(f"Error getting Linux window info with psutil: {psutil_error}")
            return "Unknown Linux Window"

def write_to_file(file, entry, args, encryptor=None):
    try:
        if args.format == 'txt':
            with open(file, 'a', encoding='utf-8') as f:
                f.write(f"{args.separator}\n")
                if args.include_timestamp:
                    f.write(f"Timestamp: {entry.timestamp}\n")
                if args.include_source:
                    f.write(f"Source: {entry.window_info}\n")
                content = entry.content if encryptor is None else encryptor.encrypt(entry.content)
                f.write(f"{content}\n")
        elif args.format == 'json':
            entries = []
            if os.path.exists(file):
                with open(file, 'r', encoding='utf-8') as f:
                    try:
                        entries = json.load(f)
                    except json.JSONDecodeError:
                        entries = []

            entry_dict = {}
            content = entry.content if encryptor is None else encryptor.encrypt(entry.content)
            
            if args.json_structure == 'content_only':
                entry_dict = content
            elif args.json_structure == 'content_time':
                entry_dict = {
                    "content": content,
                    "timestamp": entry.timestamp
                }
            else:  # full
                entry_dict = {
                    "content": content,
                    "timestamp": entry.timestamp,
                    "window_info": entry.window_info
                }
            
            entries.append(entry_dict)
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2)
        elif args.format == 'csv':
            file_exists = os.path.isfile(file)
            with open(file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["timestamp", "window_info", "content"])
                if not file_exists:
                    writer.writeheader()
                row = entry.to_dict()
                if encryptor is not None:
                    row['content'] = encryptor.encrypt(row['content'])
                writer.writerow(row)
    except IOError as e:
        raise FileOperationError(f"Error writing to file: {str(e)}")

class ClipboardMonitor:
    def __init__(self, args):
        self.args = args
        self.running = False
        self.previous_entries = set()
        self.last_entry = None
        try:
            self.encryptor = Encryptor(args.password) if args.encrypt else None
        except EncryptionError as e:
            logging.error(f"Error initializing encryptor: {str(e)}")
            raise
        self.include_regex = re.compile(args.include) if args.include else None
        self.exclude_regex = re.compile(args.exclude) if args.exclude else None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.monitor_clipboard)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def should_process_content(self, content):
        if self.include_regex and not self.include_regex.search(content):
            return False
        if self.exclude_regex and self.exclude_regex.search(content):
            return False
        return True

    def monitor_clipboard(self):
        while self.running:
            try:
                current_content = pyperclip.paste()
            except pyperclip.PyperclipException as e:
                logging.error(f"Error accessing clipboard: {e}")
                raise ClipboardAccessError(f"Error accessing clipboard: {str(e)}")

            if current_content and current_content not in self.previous_entries:
                if self.should_process_content(current_content):
                    try:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        window_info = get_active_window_info()
                        entry = ClipboardEntry(current_content, timestamp, window_info)
                        write_to_file(self.args.output, entry, self.args, self.encryptor)
                        self.previous_entries.add(current_content)
                        if len(self.previous_entries) > self.args.dedup_limit:
                            self.previous_entries.pop()
                        self.last_entry = entry
                    except (EncryptionError, FileOperationError) as e:
                        logging.error(f"Error processing clipboard content: {str(e)}")
                        # Consider implementing a retry mechanism or notifying the user

            time.sleep(self.args.interval)

def signal_handler(sig, frame):
    print("\nReceived signal to terminate. Exiting gracefully...")
    sys.exit(0)

def load_config():
    try:
        config = configparser.ConfigParser()
        config.read('clipnotes.cfg')
        return config['DEFAULT']
    except Exception as e:
        logging.error(f"Error loading configuration: {str(e)}")
        return {}

def main():
    try:
        config = load_config()

        parser = argparse.ArgumentParser(description="Monitor clipboard and save contents to a file.")
        parser.add_argument('-o', '--output', default=config.get('output_file', 'clipboard_contents.txt'), help="Output file name")
        parser.add_argument('-i', '--interval', type=float, default=config.getfloat('interval', 0.5), help="Polling interval in seconds")
        parser.add_argument('-s', '--separator', default=config.get('separator', '---'), help="Separator between clipboard entries (only for txt format)")
        parser.add_argument('-f', '--format', choices=['txt', 'json', 'csv'], default=config.get('format', 'txt'), help="Output file format")
        parser.add_argument('-d', '--dedup-limit', type=int, default=config.getint('dedup_limit', 1000), help="Number of recent entries to keep for deduplication")
        parser.add_argument('--include-timestamp', action='store_true', help="Include timestamps in output")
        parser.add_argument('--include-source', action='store_true', help="Include source window information in output")
        parser.add_argument('--json-structure', choices=['content_only', 'content_time', 'full'], default='full', help="JSON output structure (only applies when format is json)")
        parser.add_argument('-e', '--encrypt', action='store_true', help="Encrypt clipboard contents")
        parser.add_argument('-p', '--password', help="Password for encryption (required if --encrypt is used)")
        parser.add_argument('--include', help="Regular expression pattern to include content")
        parser.add_argument('--exclude', help="Regular expression pattern to exclude content")
        args = parser.parse_args()

        if args.encrypt and not args.password:
            parser.error("--password is required when using --encrypt")

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        print(f"Monitoring clipboard on {platform.system()}. Press Ctrl+C to stop.")
        print(f"Saving clipboard contents to: {args.output}")
        print(f"Output format: {args.format}")
        if args.encrypt:
            print("Encryption enabled")
        if args.include:
            print(f"Including content matching: {args.include}")
        if args.exclude:
            print(f"Excluding content matching: {args.exclude}")
        
        monitor = ClipboardMonitor(args)
        monitor.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nClipboard monitoring stopped.")
            monitor.stop()
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
        print(f"An error occurred: {str(e)}")
        print("Check the log file for more details.")
        traceback.print_exc()

if __name__ == "__main__":
    main()