#!/usr/bin/env bash

# Define colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
DARKGRAY='\033[1;30m'
NC='\033[0m' # No Color

pause() {
    echo -en "${DARKGRAY}Press any key to continue...${NC}"
    read -n 1 -s -r dummy </dev/tty && echo
}

while IFS= read -r line || [ -n "$line" ]; do
    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi

    echo -e "${BLUE}Running lexer on '${line}'${NC}"
    out=$(python3 main.py "${line}")

    # Check the exit status of main.py
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Warning: main.py returned non-zero exit status for line: $line${NC}"
        echo "${out}"
    else
        echo "${out}"

        echo -e "${BLUE}Output:${NC}"
        echo $(eval "${out}")
    fi


    pause

done < "./sample_inputs.txt"
