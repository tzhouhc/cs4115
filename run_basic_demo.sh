#!/usr/bin/env bash

INPUT_STRING="hello (world) 123"

echo "Running lexer on ${INPUT_STRING}"
python3 main.py -v "${INPUT_STRING}"


echo "Running unit tests (tests/lexer_test.py)"
python3 -m unittest tests/lexer_test.py
