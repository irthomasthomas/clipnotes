#!/bin/bash
    
    # read query from pipe or stdin
    if [ -p /dev/stdin ]; then
        query=$(cat)
    else
        query="$1"
    fi
    
    search_template="<paper>$query</paper>

<instructions>use arxiv if available. Write the paper title in <title> tags, the COMPLETE abstract in <abstract> tags and url in <url> tags. 
IMPORTANT: Do not edit or summarize the abstract - write it exactly the same.</instructions>"
    kdialog --passivepopup "Searching for $query..." 2
    abstract="$(llm -m command-r --system "<instructions>
use arxiv if available. Write the paper title in <title> tags, the COMPLETE abstract in <abstract> tags and url in <url> tags.</instructions>" "$search_template")"
    # parse xml to get abstract
    echo "$abstract"