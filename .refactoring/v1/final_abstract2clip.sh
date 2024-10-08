#!/usr/bin/env bash

set -euo pipefail

PRIMARY_SELECTION=$(xclip -o -selection primary)
ABSTRACT=$(echo "$PRIMARY_SELECTION" | /home/ShellLM/Projects/clipnotes/fetch-abstract.sh)
echo "$ABSTRACT" | xclip -selection clipboard