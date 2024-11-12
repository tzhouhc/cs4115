# cs4115

Submissions for homework in CU CS4115

## Grammar

The token types are defined in `utils/token.py`.

The preliminary compiler defines the following _set_ of the lua grammar:

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

The syntax follows the
[official lua manual](https://www.lua.org/manual/5.4/manual.html), and is
manually adjusted from its eBNF form to better fit the style seen and used in
class, and cleared of left recursions.

## Implementation

The state machine definition is in `utils/dfa.py`, whereas the lexer is in
`utils/lexer.py`. The actual state table is in `utils/grammar.py`.

The program handles errors by recognizing them and storing an ERROR token
in the result token stream.

The parser feeds directly from the lexer's output of a TokenStream.

The parser uses Recursive Descent, and expects the grammar to be free of
left recursions. On failed parsing attempts, it records the expansion with
the greatest progress (number of tokens matched), and reports how the
expectation of the rule differs from the token found.

## How to Run

Either run the program directly if python is available:

```sh
./main.py "some input text"
```

or run the demo script:

```sh
./run_basic_demo.sh
```

Or run the provided shell script to install and run docker:

```sh
./run_assignment.sh
```

For state transition logging, run `main.py` with flags `-v`; use `-vv` for
more verbose logging.

## Tests

You can find the tests in `tests/`. You can run them with:

```sh
python3 -m unittest tests/*.py
```

Or use the provided commands in the justfile.

## Video

[Video link to Google Drive](https://drive.google.com/file/d/1yd55ag1o2JgzVgUijb3Dep029bz0l2re/view?usp=sharing)

Since everything is done on the commandline, here's a [Link to
asciinema](https://asciinema.org/a/688604).

Content:

- A brief look into the input file, the python `main`, and the script
- A run of the script, which runs the unit tests, and 5 sample programs.
- Manually invoked a bad input to demonstrate the error handling.

## Team

Team is myself, Ting Zhou (tz2635).

## References

Made use of LLM to generate helper functions like pretty-printing in order to
assist with the debugging and demonstration process.
