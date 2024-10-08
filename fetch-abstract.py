#!/usr/bin/env python3

    import sys
    import json
    import logging
    import subprocess
    from typing import List, Dict, Optional, Tuple
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from functools import partial

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_query() -> str:
        """Get the search query from pipe or command line argument."""
        if not sys.stdin.isatty():
            return sys.stdin.read().strip()
        elif len(sys.argv) > 1:
            return sys.argv[1]
        else:
            logging.error("No query provided. Please provide a query via pipe or command line argument.")
            sys.exit(1)

    def confirm_search(query: str) -> bool:
        """Ask user to confirm the search query using kdialog."""
        try:
            result = subprocess.run(["kdialog", "--yesno", f"Search for {query}?"], check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            logging.warning("kdialog not found. Proceeding without confirmation.")
            return True

    def show_notification(message: str, duration: int = 2):
        """Show a notification using kdialog."""
        try:
            subprocess.run(["kdialog", "--passivepopup", message, str(duration)], check=True)
        except subprocess.CalledProcessError:
            logging.warning(f"Failed to show notification: {message}")
        except FileNotFoundError:
            logging.warning("kdialog not found. Skipping notification.")

    def search_papers(query: str) -> List[Dict[str, str]]:
        """Search for papers using a language model."""
        search_template = f"""<paper>{query}</paper>
    <instructions>use arxiv if available. Write the paper title in <title> tags, the COMPLETE abstract in <abstract> tags and url in <url> tags. 
    IMPORTANT: Search thoroughly for a COMPLETE abstract. Do not edit or summarize the abstract - write it exactly the same.</instructions>"""
        
        try:
            result = subprocess.run(
                ["llm", "-m", "command-r-plus", "--system", 
                "IGNORE PREVIOUS INSTRUCTIONS. <instructions>use arxiv if available. Write the paper title in <title> tags, the COMPLETE abstract in <abstract> tags and url in <url> tags.</instructions>",
                search_template, "-o", "websearch", "1"],
                capture_output=True, text=True, check=True
            )
            return parse_search_results(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing llm search: {e}")
            return []

    def parse_search_results(raw_results: str) -> List[Dict[str, str]]:
        """Parse the raw search results into a list of dictionaries."""
        papers = []
        for result in raw_results.split("</url>"):
            paper = {}
            for tag in ["title", "abstract", "url"]:
                start_tag = f"<{tag}>"
                end_tag = f"</{tag}>"
                start = result.find(start_tag)
                end = result.find(end_tag)
                if start != -1 and end != -1:
                    paper[tag] = result[start + len(start_tag):end].strip()
            if paper:
                papers.append(paper)
        return papers

    def fetch_abstract(url: str, shot_scraper_path: str = "shot-scraper") -> Tuple[str, Optional[str]]:
        """Fetch the abstract for a given URL using the shot-scraper tool."""
        try:
            result = subprocess.run(
                [shot_scraper_path, "javascript", "-i", "readability.js", url],
                capture_output=True, text=True, check=True
            )
            page_data = json.loads(result.stdout)
            abstract = page_data.get("excerpt", "")
            if not abstract:
                logging.error(f"Failed to extract abstract from {url}")
                return url, None
            return url, abstract
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing shot-scraper for {url}: {e.output}")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON for {url}: {e}")
        except Exception as e:
            logging.error(f"An error occurred while processing {url}: {e}")
        return url, None

    def fetch_abstracts_concurrently(urls: List[str], num_workers: int = 10) -> Dict[str, Optional[str]]:
        """Fetch abstracts concurrently for a list of URLs using a thread pool."""
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(fetch_abstract, url) for url in urls]
            return {url: abstract for future in as_completed(futures) for url, abstract in [future.result()]}

    def main():
        query = get_query()
        if not confirm_search(query):
            sys.exit(0)

        show_notification(f"Searching for {query}...")
        search_results = search_papers(query)

        if not search_results:
            show_notification("No results found.")
            sys.exit(0)

        urls = [paper['url'] for paper in search_results if 'url' in paper]
        abstracts_dict = fetch_abstracts_concurrently(urls)

        for paper in search_results:
            url = paper.get('url', '')
            title = paper.get('title', 'Unknown Title')
            abstract = abstracts_dict.get(url) or paper.get('abstract', 'Abstract not available')
            print(f"Title: {title}\nURL: {url}\nAbstract: {abstract}\n")

        show_notification("Search completed.")

    if __name__ == "__main__":
        main()