import subprocess
import pyperclip

def get_primary_selection():
    try:
        return subprocess.check_output(['xclip', '-o', '-selection', 'primary'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Unable to get primary selection. Make sure xclip is installed.")
        return ""

def generate_abstract(text, max_words=30):
    words = text.split()
    if len(words) > max_words:
        abstract = ' '.join(words[:max_words]) + '...'
    else:
        abstract = text
    return f"Abstract: {abstract}"

def main():
    # Get text from primary selection
    primary_text = get_primary_selection()
    
    if not primary_text:
        print("No text in primary selection. Exiting.")
        return
    
    # Generate abstract
    abstract = generate_abstract(primary_text)
    
    # Copy abstract to clipboard
    try:
        pyperclip.copy(abstract)
        print("Abstract generated and copied to clipboard:")
        print(abstract)
    except pyperclip.PyperclipException:
        print("Error: Unable to copy to clipboard. Is a clipboard manager running?")
        print("Generated abstract:")
        print(abstract)

if __name__ == "__main__":
    main()