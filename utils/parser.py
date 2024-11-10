import logging
from functools import cache
from utils.lexer import TokenStream
from utils.token import Token, TokenType, VARIABLE_TOKENS

from typing import Optional, Union

logger = logging.getLogger(__name__)

# The lua syntax essentials (abridged version for the sake of homework)
SYNTAX_MAP = {
    "VAR": [
        ["NAME"],
        ["PREFIX_EXP", Token(TokenType.LBRACKET, "["), "EXP",
         Token(TokenType.RBRACKET, "]")],
    ],
    "PREFIX_EXP": [
        ["VAR"],
        ["FUNC_CALL"],
        [Token(TokenType.LPAREN, "("), "EXP", Token(TokenType.RPAREN, ")")]
    ],
    "BLOCK": [
        ["LIST_STAT", "OPT_RETSTAT"]
    ],
    "LIST_STAT": [
        ["STAT", "LIST_STAT"],
        ["EPSILON"],
    ],
    "OPT_RETSTAT": [
        ["RETSTAT"],
        ["EPSILON"]
    ],
    "RETSTAT": [
        [Token(TokenType.KEYWORD, "return"), "EXP_LIST"]
    ]
}

RuleElement = Union[str, Token]


def rule_element_name(e: RuleElement):
    if isinstance(e, str):
        return e
    else:
        return str(e.type)


class ASTRule:
    def __init__(self, name: str, entries: list[Union[str, Token]]):
        self.name = name
        self.entries = entries

    def __getitem__(self, i: int) -> RuleElement:
        return self.entries[i]

    def __len__(self) -> int:
        return len(self.entries)

    def __str__(self) -> str:
        return f"{self.name} -> " + " ".join([str(e) for e in self.entries])


class ASTNode:
    def __init__(self,
                 e: RuleElement, token: Optional[Token],
                 nodes: list['ASTNode']) -> None:
        self.type = rule_element_name(e)
        self.token = token
        self.nodes = nodes
        self.parent = None

    def __str__(self) -> str:
        result = f"{self.type}"
        if self.token:
            result += f"({self.token.string})"
        if self.nodes:
            children = ", ".join(str(node) for node in self.nodes)
            result += f"[{children}]"
        return result

    def __repr__(self) -> str:
        return (f"ASTNode(type={repr(self.type)}, "
                f"token={repr(self.token)}, "
                f"nodes={repr(self.nodes)})")


class ASTMatchResult:
    def __init__(self, match: bool, forward: int,
                 node: Optional[ASTNode]) -> None:
        self.match = match
        self.forward = forward
        self.node = node

    def __bool__(self):
        return self.match

    def __str__(self):
        return str(self.node)

    def __repr__(self):
        return f"ASTMatchResult(match={self.match}, " \
            f"forward={self.forward}, node={repr(self.node)})"


# Recursive Descent Parser
class Parser:
    def __init__(self, tokens: TokenStream,
                 syntax: dict[str, list[list[Union[str, Token]]]]) -> None:
        self.tokens = tokens
        self.syntax: dict[str, list[ASTRule]] = {
            key: [ASTRule(key, rule) for rule in item]
            for key, item in syntax.items()
        }

    def __str__(self) -> str:
        res = f"Tokens: {self.tokens}\n"
        for rules in self.syntax.values():
            for rule in rules:
                res += str(rule) + "\n"
        return res

    @cache
    def get_at(self, index: int) -> Token:
        return self.tokens[index]

    @cache
    def token_match_at(self, i: int, want: Token) -> bool:
        if not isinstance(self.get_at(i), Token):
            return False
        return self.get_at(i) == want

    # A terminal match is either a literal match -- type and content both equal
    # -- or a variable match, where type is equal, and content doesn't matter.
    @cache
    def match_terminal(self, cur: int, entry: Token) -> ASTMatchResult:
        # no more symbols to match, entry is known not to be epsilon,
        # fail gracefully
        if cur >= len(self.tokens):
            return ASTMatchResult(False, 0, None)
        cur_entity = self.get_at(cur)
        # some tokens must match explicitly, e.g. keywords, symbols; others
        # only need to match type.
        if cur_entity == entry or (cur_entity.type == entry.type
                                   and entry.type in VARIABLE_TOKENS):
            return ASTMatchResult(True,
                                  1, ASTNode(rule_element_name(entry),
                                             cur_entity, []))
        return ASTMatchResult(False, 0, None)

    # A bit of an awkward two-stage recursion: match_non_terminal is about
    # the node, where it needs to explore a number of different rules,
    # and then match_rule_starting_at is for a single rule.
    @cache
    def match_non_terminal(self, name: str, cur: int) -> ASTMatchResult:
        best = None

        for rule in self.syntax[name]:
            try_match = self.match_rule_starting_at(cur, rule)
            if not try_match:
                continue
            # Keep track of the longest successful match
            if best is None or try_match.forward > best.forward:
                best = try_match

        return best if best else ASTMatchResult(False, 0, None)

    @cache
    def match_rule_starting_at(self, cur: int,
                               rule: ASTRule) -> ASTMatchResult:
        # Special case for epsilon
        if rule[0] == "EPSILON" and len(rule) == 1:
            return ASTMatchResult(True, 0, ASTNode("EPSILON", None, []))

        forward = 0
        result_node = ASTNode(rule.name, None, [])
        saved_nodes = []

        for entry in rule.entries:
            got_match = False

            if isinstance(entry, Token):
                match = self.match_terminal(cur + forward, entry)
                if match:
                    node = match.node
                    assert node is not None
                    got_match = True
                    if (node.type != "TokenType.EOF"):
                        forward += match.forward
                        saved_nodes.append(node)
            else:
                match = self.match_non_terminal(entry, cur + forward)
                if match:
                    forward += match.forward
                    assert match.node is not None
                    saved_nodes.append(match.node)
                    got_match = True

            if not got_match:
                # Nope, found nothing useful. Tell caller to try something
                # else.
                return ASTMatchResult(False, 0, None)

        result_node.nodes = saved_nodes
        return ASTMatchResult(True, forward, result_node)

    def parse(self, init_name: str = "BLOCK") -> ASTMatchResult:
        # hack to ensure that must match an EOF at the end to succeed
        eof = Token(TokenType.EOF, "")
        init: ASTRule = self.syntax[init_name][0]
        if init[-1] != eof:
            init.entries += [eof]
        if self.tokens[-1] != eof:
            self.tokens.append(eof)

        return self.match_non_terminal(init_name, 0)
