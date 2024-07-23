!#/bin/bash

# question = kdialog to ask user for a question
# xclip selection buffer to get subject of question
subject="<subject>$(xclip -o)</subject>"
question="<reader_note>$(kdialog --inputbox "Ask a question or add note" "Question: ")</reader_note>"
echo "$subject
$question" | xclip -selection clipboard
