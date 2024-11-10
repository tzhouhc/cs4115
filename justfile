# Install python3 requirements
install-py-reqs:
  python3 -m pip install -r requirements.txt

run-lexer-tests:
  python3 -m unittest tests/lexer_test.py

run-parser-tests:
  python3 -m unittest tests/parser_test.py

run-tests:
  python3 -m unittest tests/*.py
