#!/usr/bin/env bash

# Define colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

while IFS= read -r line || [ -n "$line" ]; do
    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi

    echo -e "${BLUE}Running lexer on '${line}'${NC}"
    python3 main.py "${line}"

    # Check the exit status of main.py
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Warning: main.py returned non-zero exit status for line: $line${NC}"
    fi

    sleep 3
done < "./sample_inputs.txt"
