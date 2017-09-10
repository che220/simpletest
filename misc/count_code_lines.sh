#!/bin/bash

if [ $# -ne 2 ]; then
    echo "usage: $0 <search dir> <file extension>"
    exit 1
fi

lines=$(find $1 -name "*.${2}" -exec wc -l {} \;)
tot=0
for line in $lines; do
    if [[ $line == *.R ]]; then
	continue
    fi
    if [[ $line == [a-cA-Z.]* ]]; then
	continue
    fi
    echo $line
    tot=$(expr $tot + $line)
done
echo "Total lines: $tot"

