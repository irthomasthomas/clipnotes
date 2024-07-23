#!/bin/bash
    
# read query from pipe or stdin
if [ -p /dev/stdin ]; then
    query=$(cat)
else
    query="$1"
fi
# kdialog ask user if they want to continue search for query
kdialog --yesno "Search for $query?"
if [ $? -eq 1 ]; then # 
    exit 0
fi

kdialog --passivepopup "Searching for $query..." 2

search_template="<paper>$query</paper>
<instructions>use arxiv if available. Write the paper title in <title> tags, the COMPLETE abstract in <abstract> tags and url in <url> tags. 
IMPORTANT: Search thoroughly for a COMPLETE abstract. Do not edit or summarize the abstract - write it exactly the same.</instructions>"
abstract="$(llm -m command-r-plus --system "IGNORE PREVIOUS INSTRUCTIONS. <instructions>use arxiv if available. Write the paper title in <title> tags, the COMPLETE abstract in <abstract> tags and url in <url> tags.</instructions>" "$search_template" -o websearch 1)"
kdialog --passivepopup "$abstract" 2
    # parse xml to get abstract
    echo "$abstract"