# cs4115
Submissions for homework in CU CS4115

## Grammar

The token types are defined in `utils/token.py`.

The preliminary compiler defines the following *subset* of the lua grammar:

```
WHITE_SPACE = 0  # \s
LPAREN  # (
RPAREN  # )
LBRACKET  # [
RBRACKET  # ]
LCURLY  # {
RCURLY  # }
COLON  # :
KEYWORD
# The following are reserved as keywords:
# and       break     else      elseif    end
# for       function  if
# return
# then      while
ID
# IDs are at least one letter followed by alphanumerics.
OP
# +, -, $, =, /, \
COMMA  # ,
INTEGER  # at least one digit
ERROR
```

## Implementation

The state machine definition is in `utils/dfa.py`, whereas the lexer is in
`utils/lexer.py`. The actual state table is in `utils/grammar.py`.

The program handles errors by recognizing them and storing an ERROR token
in the result token stream.


## How to Run

Either run the program directly:

```sh
./main.py "some input text"
```

Or run the provided shell script

```sh
./run_assignment_1.sh
```

For state transition logging, run `main.py` with flags `-vv`.

## Tests

You can find the tests in `tests/lexer_test.py`. You can run it with:

```sh
python3 -m unittest tests/lexer_test.py
```

Or use the provided commands in the justfile.

## Team

Team is myself, Ting Zhou (tz2635).
