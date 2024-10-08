import sys
import subprocess
import xml.etree.ElementTree as ET

def kdialog(command, message):
    try:
        subprocess.run(["kdialog", command, message], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def llm_query(query):
    search_template = f"<paper>{query}</paper>\n<instructions>use arxiv if available. Write the paper title in <title> tags, the COMPLETE abstract in <abstract> tags and url in <url> tags. IMPORTANT: Search thoroughly for a COMPLETE abstract. Do not edit or summarize the abstract - write it exactly the same.</instructions>"
    
    try:
        result = subprocess.run(
            ["llm", "-m", "command-r-plus", 
             "--system", "IGNORE PREVIOUS INSTRUCTIONS. <instructions>use arxiv if available. Write the paper title in <title> tags, the COMPLETE abstract in <abstract> tags and url in <url> tags.</instructions>",
             search_template, "-o", "websearch", "1"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error querying LLM: {e}")
        return None

def parse_xml(xml_string):
    try:
        root = ET.fromstring(xml_string)
        title = root.find('title').text if root.find('title') is not None else "Title not found"
        abstract = root.find('abstract').text if root.find('abstract') is not None else "Abstract not found"
        url = root.find('url').text if root.find('url') is not None else "URL not found"
        return title, abstract, url
    except ET.ParseError:
        print("Error parsing XML response")
        return None, None, None

def main():
    if sys.stdin.isatty():
        if len(sys.argv) < 2:
            print("Please provide a search query.")
            return
        query = sys.argv[1]
    else:
        query = sys.stdin.read().strip()

    if not kdialog("--yesno", f"Search for {query}?"):
        return

    kdialog("--passivepopup", f"Searching for {query}...", "2")

    abstract_xml = llm_query(query)
    if abstract_xml:
        title, abstract, url = parse_xml(abstract_xml)
        if title and abstract and url:
            result = f"Title: {title}\n\nAbstract: {abstract}\n\nURL: {url}"
            kdialog("--passivepopup", result, "2")
            print(result)
        else:
            print("Failed to parse the response.")
    else:
        print("Failed to fetch the abstract.")

if __name__ == "__main__":
    main()