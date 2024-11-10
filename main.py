#!/usr/bin/env python3
from utils import lexer, grammar, dfa, parser
from argparse import ArgumentParser, BooleanOptionalAction
import logging
import sys


def setup_logger(verbosity):
    # Create a logger
    logger = logging.getLogger()

    # Set the logging level based on verbosity
    if verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logger.setLevel(level)

    # Create a console handler and set its level
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(level)

    # Create a formatter
    formatter = logging.Formatter(
        '%(name)s@%(levelname)s: %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger


def arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("text", help="Input to the compiler.")
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Increase verbosity (can be used multiple times)")
    parser.add_argument("--whitespace", action=BooleanOptionalAction)
    return parser


def main() -> int:
    args = arg_parser().parse_args()
    setup_logger(args.verbose)
    g = grammar.STATE_TABLE
    lexed = lexer.Lexer(args.text, dfa.SimpleAutomata(g), args).lex()
    parsed = parser.Parser(lexed, parser.SYNTAX_MAP).parse()
    print(parsed)
    return 0


if __name__ == "__main__":
    exit(main())
