# ClipNotes

ClipNotes is a Python utility that simplifies the process of taking notes while reading papers or conducting research. It automatically captures clipboard entries while it runs and saves them to a file for further processing when you finish.

## Features

- Collects clipboard entries while you read or research
- Saves notes to a single file for easy access

## Installation
```bash
pip install clipnotes
```

## Usage
    
```bash
python -m clipnotes
```
Enter the title of the paper you're reading:

1. Run the command to start capturing clipboard entries.
2. Read papers or browse the web, copying important snippets to the clipboard.
3. Press return to stop capturing notes.
4. A filepath to the generated notes file will be displayed and should be copied to your clipboard.
5. Use the generated notes file for further processing or export to Markdown.

## Roadmap
Possible features to be added in the future:
- Include context information for each clipboard entry (e.g., Window title, URL, etc.)
- Enable editing of individual note blocks before saving.
- Summarize as you go: automatically generate summaries of the notes taken. Or scrape abstracts from the web for copied papers.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss the proposed changes.

## License

[MIT](https://choosealicense.com/licenses/mit/)
