import sys
from Xlib import X, display, Xatom

def get_primary_selection():
    """Get the primary selection text using Xlib."""
    d = display.Display()
    try:
        primary = d.get_selection_owner(d.get_atom("PRIMARY"))
        if primary:
            data = primary.convert_selection(d.get_atom("PRIMARY"), d.get_atom("STRING"), d.get_atom("TEXT"), X.CurrentTime)
            if data:
                return data.value.decode('utf-8').strip()
    except Exception as e:
        print(f"Error: Unable to get primary selection. {str(e)}")
    return ""

def generate_and_copy_abstract(text, max_words=30):
    """Generate an abstract from the given text and copy to clipboard."""
    words = text.split()
    if len(words) > max_words:
        abstract = ' '.join(words[:max_words]) + '...'
    else:
        abstract = text
    abstract = f"Abstract: {abstract}"

    d = display.Display()
    clipboard = d.get_selection_owner(d.get_atom("CLIPBOARD"))
    if clipboard:
        clipboard.change_property(d.get_atom("CLIPBOARD"), d.get_atom("STRING"), 8, abstract.encode('utf-8'))
        d.flush()
        print("Abstract generated and copied to clipboard:")
        print(abstract)
    else:
        print("Error: Unable to copy to clipboard. Is a clipboard manager running?")
        print("Generated abstract:")
        print(abstract)

def main():
    """Main function to generate an abstract from primary selection and copy to clipboard."""
    max_words = 30
    if len(sys.argv) > 1:
        try:
            max_words = int(sys.argv[1])
        except ValueError:
            print("Invalid argument. Using default max_words=30.")

    primary_text = get_primary_selection()
    if not primary_text:
        print("No text in primary selection. Exiting.")
        return

    generate_and_copy_abstract(primary_text, max_words)

if __name__ == "__main__":
    main()