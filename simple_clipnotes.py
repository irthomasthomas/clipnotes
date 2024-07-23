import sys
import time
import pyperclip

def monitor_clipboard():
    last_content = pyperclip.paste()
    entry_counter = 1
    print("Monitoring clipboard. Copy text to see output.", file=sys.stderr)
    while True:
        try:
            current_content = pyperclip.paste()
            if current_content != last_content:
                print(f"\n--- Entry {entry_counter} ---")
                print(current_content)
                print("------------------------")
                sys.stdout.flush()
                last_content = current_content
                entry_counter += 1
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nExiting.", file=sys.stderr)
            break

if __name__ == "__main__":
    monitor_clipboard()