#!/bin/bash
xclip -o -selection primary | /home/ShellLM/Projects/clipnotes/fetch-abstract.sh | xclip -selection clipboard
