#!/usr/bin/env python3
from utils import ast, parser
from argparse import ArgumentParser, BooleanOptionalAction
import logging
import sys
import lark


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
    parser.add_argument("-t", "--tree", action=BooleanOptionalAction,
                        help="Print the parsed AST.")
    return parser


def main() -> int:
    args = arg_parser().parse_args()
    setup_logger(args.verbose)
    lark_ast = None
    lark_parser = parser.PARSER
    try:
        lark_ast = lark_parser.parse(args.text)
        if args.tree:
            print(lark_ast.pretty())
    except lark.exceptions.LarkError as e:
        print(f"Lexing/Parsing error: {e}")
        exit(1)
    assert lark_ast is not None
    # generator = code_gen.CodeGenerator(ast)
    my_ast = ast.ast_from_lark(lark_ast)
    my_ast.update_symbols()
    my_ast.gen()
    unused = my_ast.get_unused_symbols()
    my_ast.clean_up(unused)
    print(my_ast.gen())
    return 0


if __name__ == "__main__":
    exit(main())
