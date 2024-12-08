# cs4115

Submissions for homework in CU CS4115

I might have biten more than I can chew when it came to the topic selection,
and a full compiler from zsh to lua is not easily done in 3 weeks while
competing for time with other courses, so this is a very lightweight
implementation with the bare minimum features -- a naive usage checker,
a basic typing and symbol system, and unknown var detection. Ultimately,
a shell scripting language is really different in many subtle ways from a
regular scripting language.

## Grammar

The token types are defined in `utils/grammar.py`. The lexing and parsing
are done via the python `lark` library.

## Implementation

The `ast_base.py` and `ast.py` classes contain the basic definition of the
ASTNode, and the expanded set of semantic nodes and method overrides.

The `symbols.py` contains rudimentary definitions for symbols and a symbol
table that allows scoping statically and upwards/backwards.

## How to Run

Either run the program directly if python is available:

```sh
./main.py "some input text"
```

or run the demo script:

```sh
./run_basic_demo.sh
```

Or run the provided shell script to install and run docker (though you
lose the interactivity):

```sh
./run_assignment.sh
```

For state transition logging, run `main.py` with flags `-v`; use `-vv` for
more verbose logging. Use the `-t` flag for printing the parse tree.

## Video

[Video link to Google Drive]()

- A brief look into the files.
- A run of the script, which runs the unit tests, and some sample programs.

## Team

Team is myself, Ting Zhou (tz2635).
