#!/usr/bin/env python3
from utils import lexer
from argparse import ArgumentParser


def arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("text", help="Input to the compiler.")
    return parser


def main() -> int:
    args = arg_parser().parse_args()
    result = lexer.Lexer(args.text)
    print(result.lex())
    return 0


if __name__ == "__main__":
    exit(main())
