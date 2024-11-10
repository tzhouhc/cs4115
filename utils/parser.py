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
                 type: RuleElement, token: Optional[Token],
                 nodes: list['ASTNode']) -> None:
        self.type = type
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


class ASTMatchSet:
    def __init__(self, matches: list[ASTMatchResult]) -> None:
        self.matches = matches

    def __iter__(self):
        return iter(self.matches)


# Recursive Descent
class Parser:
    def __init__(self, tokens: TokenStream,
                 syntax: dict[str, list[list[Union[str, Token]]]]) -> None:
        self.tokens = tokens
        self.length = len(tokens)
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
        if cur >= self.length:
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

    # A *specific* rule matching attempt.
    # TODO:
    # Currently doesn't do any backtracking, so prone to getting stuck on a
    # successful but _incomplete_ parse if some other rule takes the cake.
    # Maybe lua doesn't need this? But still, could be considered.
    @cache
    def match_rule_starting_at(self,
                               cur: int, rule: ASTRule) -> ASTMatchResult:
        # every item of the rule must match tokens starting from index.
        forward = 0
        # forward records the total progress made. If the rule is all
        # terminals, then this should equal the length of the rule. If not,
        # we cannot say for sure.
        entries: list[Union[str, Token]] = rule.entries
        # entries are the individual things that need to match starting from
        # positino `cur`.
        result_node = ASTNode(rule.name, None, [])
        # Depending on the number of stuff matched in each entry, we should
        # gather the results AND update `forward` so that subsequent matches
        # can start correctly.

        # special case epsilon -- one entry in the rule only and it is epsilon
        if rule[0] == "EPSILON" and len(rule) == 1:
            return ASTMatchResult(True, 0, ASTNode("EPSILON", None, []))

        for i in range(0, len(entries)):
            entry: Union[str, Token] = entries[i]
            got_match = False
            if isinstance(entry, Token):
                match = self.match_terminal(cur + forward, entry)
                if match:
                    forward += match.forward
                    node = match.node
                    assert node is not None
                    result_node.nodes += [node]
                    got_match = True
            else:
                match: ASTMatchResult = ASTMatchResult(False, 0, None)
                # non-terminal, can have multiple rules, match any of them.
                for rule in self.syntax[entry]:
                    try_match = self.match_rule_starting_at(cur + forward,
                                                            rule)
                    if try_match:
                        match = try_match
                        assert match.node is not None
                        break
                if match:
                    forward += match.forward
                    node = match.node
                    assert node is not None
                    result_node.nodes += [node]
                    got_match = True
            if not got_match:
                return ASTMatchResult(False, 0, None)

        return ASTMatchResult(
            True, forward, result_node
        )

    def parse(self, init_name: str = "BLOCK") -> ASTMatchResult:
        init = self.syntax[init_name][0]  # BLOCK has only one production rule.
        current = 0
        match = self.match_rule_starting_at(current, init)
        if match.forward != len(self.tokens):
            match.match = False
        return match
