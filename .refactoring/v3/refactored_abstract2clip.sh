#!/usr/bin/env bash

set -euo pipefail

PRIMARY_SELECTION=$(xclip -o -selection primary)
ABSTRACT=$(/home/ShellLM/Projects/clipnotes/fetch-abstract.sh <<< "$PRIMARY_SELECTION")
echo -n "$ABSTRACT" | xclip -selection clipboard