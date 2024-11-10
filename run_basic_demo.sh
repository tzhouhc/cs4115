#!/usr/bin/env bash

INPUT_STRING="local function sum() a = 5 b = 3 return (a + b) end"

echo "Running lexer on '${INPUT_STRING}'"
python3 main.py -v "${INPUT_STRING}"

echo "Running unit tests (tests/lexer_test.py)"
python3 -m unittest tests/*.py
