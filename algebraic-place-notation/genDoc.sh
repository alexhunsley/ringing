#!/bin/bash

export FILE=$(basename `find . -depth 1 -name '*.md'` .md)

echo "Operating on file $FILE"
echo


/usr/local/bin/pandoc -V geometry:margin=0.5in --pdf-engine=/Library/TeX/texbin/pdflatex -o "$FILE.pdf" "$FILE.md"

open "$FILE.pdf"

