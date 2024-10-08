import tkinter as tk
    from tkinter import simpledialog
    import pyperclip
    from xml.etree.ElementTree import Element, tostring

    def get_clipboard_content():
        return pyperclip.paste()

    def ask_question(root):
        return simpledialog.askstring("Question", "Ask a question or add note:", parent=root)

    def create_xml_element(tag, text):
        element = Element(tag)
        element.text = text
        return tostring(element, encoding='unicode', method='xml')

    def main():
        root = tk.Tk()
        root.withdraw()

        try:
            subject = create_xml_element("subject", get_clipboard_content())
            question = create_xml_element("reader_note", ask_question(root))
            
            result = f"{subject}\n{question}"
            pyperclip.copy(result)
            print("Result copied to clipboard:")
            print(result)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            root.destroy()

    if __name__ == "__main__":
        main()