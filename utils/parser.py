import logging
from functools import cache
from utils.lexer import TokenStream
from utils.token import Token, TokenType, VARIABLE_TOKENS

from typing import Optional, Union

logger = logging.getLogger(__name__)

# The lua syntax essentials (abridged version for the sake of homework)
SYNTAX_MAP = {
    "CHUNK": [
        ["BLOCK"]
    ],

    "BLOCK": [
        ["LIST_STAT", "OPT_RETSTAT"]
    ],

    "LIST_STAT": [
        ["STAT", "LIST_STAT"],
        ["EPSILON"]
    ],

    "OPT_RETSTAT": [
        ["RETSTAT"],
        ["EPSILON"]
    ],

    "STAT": [
        [Token(TokenType.SEMICOLON, ";")],
        ["VARLIST", Token(TokenType.OP, "="), "EXPLIST"],
        ["FUNCTIONCALL"],
        ["LABEL"],
        [Token(TokenType.KEYWORD, "break")],
        [Token(TokenType.KEYWORD, "goto"), Token(TokenType.ID, "Name")],
        [Token(TokenType.KEYWORD, "do"), "BLOCK",
         Token(TokenType.KEYWORD, "end")],
        [Token(TokenType.KEYWORD, "while"), "EXP",
         Token(TokenType.KEYWORD, "do"), "BLOCK",
         Token(TokenType.KEYWORD, "end")],
        [Token(TokenType.KEYWORD, "repeat"), "BLOCK",
         Token(TokenType.KEYWORD, "until"), "EXP"],
        ["IF_STAT"],
        ["FOR_NUM_STAT"],
        ["FOR_IN_STAT"],
        ["FUNCTION_STAT"],
        ["LOCAL_FUNCTION_STAT"],
        ["LOCAL_STAT"]
    ],

    "IF_STAT": [
        [Token(TokenType.KEYWORD, "if"), "EXP",
         Token(TokenType.KEYWORD, "then"), "BLOCK",
         "LIST_ELSEIF", "OPT_ELSE",
         Token(TokenType.KEYWORD, "end")]
    ],

    "LIST_ELSEIF": [
        ["ELSEIF", "LIST_ELSEIF"],
        ["EPSILON"]
    ],

    "ELSEIF": [
        [Token(TokenType.KEYWORD, "elseif"), "EXP",
         Token(TokenType.KEYWORD, "then"), "BLOCK"]
    ],

    "OPT_ELSE": [
        [Token(TokenType.KEYWORD, "else"), "BLOCK"],
        ["EPSILON"]
    ],

    "FOR_NUM_STAT": [
        [Token(TokenType.KEYWORD, "for"),
         Token(TokenType.ID, "Name"),
         Token(TokenType.OP, "="),
         "EXP",
         Token(TokenType.COMMA, ","),
         "EXP", "OPT_STEP",
         Token(TokenType.KEYWORD, "do"),
         "BLOCK",
         Token(TokenType.KEYWORD, "end")]
    ],

    "OPT_STEP": [
        [Token(TokenType.COMMA, ","), "EXP"],
        ["EPSILON"]
    ],

    "FOR_IN_STAT": [
        [Token(TokenType.KEYWORD, "for"), "NAMELIST",
         Token(TokenType.KEYWORD, "in"), "EXPLIST",
         Token(TokenType.KEYWORD, "do"), "BLOCK",
         Token(TokenType.KEYWORD, "end")]
    ],

    "FUNCTION_STAT": [
        [Token(TokenType.KEYWORD, "function"), "FUNCNAME", "FUNCBODY"]
    ],

    "LOCAL_FUNCTION_STAT": [
        [Token(TokenType.KEYWORD, "local"),
         Token(TokenType.KEYWORD, "function"),
         Token(TokenType.ID, "Name"), "FUNCBODY"]
    ],

    "LOCAL_STAT": [
        [Token(TokenType.KEYWORD, "local"),
         "ATTNAMELIST", "OPT_ASSIGN_EXPLIST"]
    ],

    "OPT_ASSIGN_EXPLIST": [
        [Token(TokenType.OP, "="), "EXPLIST"],
        ["EPSILON"]
    ],

    "ATTNAMELIST": [
        ["NAME_ATTRIB", "LIST_NAME_ATTRIB"]
    ],

    "LIST_NAME_ATTRIB": [
        [Token(TokenType.COMMA, ","), "NAME_ATTRIB", "LIST_NAME_ATTRIB"],
        ["EPSILON"]
    ],

    "NAME_ATTRIB": [
        [Token(TokenType.ID, "Name"), "OPT_ATTRIB"]
    ],

    "OPT_ATTRIB": [
        [Token(TokenType.OP, "<"),
         Token(TokenType.ID, "Name"),
         Token(TokenType.OP, ">")],
        ["EPSILON"]
    ],

    "RETSTAT": [
        [Token(TokenType.KEYWORD, "return"), "OPT_EXPLIST", "OPT_SEMICOLON"]
    ],

    "OPT_EXPLIST": [
        ["EXPLIST"],
        ["EPSILON"]
    ],

    "OPT_SEMICOLON": [
        [Token(TokenType.SEMICOLON, ";")],
        ["EPSILON"]
    ],

    "LABEL": [
        [Token(TokenType.OP, "::"), Token(TokenType.ID, "Name"),
         Token(TokenType.OP, "::")]
    ],

    "FUNCNAME": [
        [Token(TokenType.ID, "Name"), "LIST_DOT_NAME", "OPT_METHOD_NAME"]
    ],

    "LIST_DOT_NAME": [
        [Token(TokenType.OP, "."), Token(
            TokenType.ID, "Name"), "LIST_DOT_NAME"],
        ["EPSILON"]
    ],

    "OPT_METHOD_NAME": [
        [Token(TokenType.COLON, ":"), Token(TokenType.ID, "Name")],
        ["EPSILON"]
    ],

    "VARLIST": [
        ["VAR", "LIST_VAR"]
    ],

    "LIST_VAR": [
        [Token(TokenType.COMMA, ","), "VAR", "LIST_VAR"],
        ["EPSILON"]
    ],

    "NAMELIST": [
        [Token(TokenType.ID, "Name"), "LIST_NAME"]
    ],

    "LIST_NAME": [
        [Token(TokenType.COMMA, ","), Token(
            TokenType.ID, "Name"), "LIST_NAME"],
        ["EPSILON"]
    ],

    "EXPLIST": [
        ["EXP", "LIST_EXP"]
    ],

    "LIST_EXP": [
        [Token(TokenType.COMMA, ","), "EXP", "LIST_EXP"],
        ["EPSILON"]
    ],

    "EXP": [
        ["SIMPLE_EXP", "LIST_BINOP_EXP"]
    ],

    "LIST_BINOP_EXP": [
        ["BINOP", "SIMPLE_EXP", "LIST_BINOP_EXP"],
        ["EPSILON"]
    ],

    "SIMPLE_EXP": [
        [Token(TokenType.KEYWORD, "nil")],
        [Token(TokenType.KEYWORD, "false")],
        [Token(TokenType.KEYWORD, "true")],
        [Token(TokenType.INTEGER, "")],
        [Token(TokenType.STRING, "LiteralString")],
        [Token(TokenType.OP, "...")],
        ["FUNCTIONDEF"],
        ["PREFIXEXP"],
        ["TABLECONSTRUCTOR"],
        ["UNOP", "SIMPLE_EXP"]  # Unary operators
    ],

    "VAR": [
        ["PRIMARYEXP", "LIST_VARSUFFIX"]  # Changed to use new structure
    ],

    "LIST_VARSUFFIX": [
        ["VARSUFFIX", "LIST_VARSUFFIX"],
        ["EPSILON"]
    ],

    "VARSUFFIX": [
        [Token(TokenType.LBRACKET, "["), "EXP",
         Token(TokenType.RBRACKET, "]")],
        [Token(TokenType.OP, "."),
         Token(TokenType.ID, "Name")]
    ],

    "PRIMARYEXP": [
        [Token(TokenType.ID, "Name")],
        [Token(TokenType.LPAREN, "("), "EXP", Token(TokenType.RPAREN, ")")]
    ],

    "PREFIXEXP": [
        ["PRIMARYEXP", "LIST_SUFFIX"]
    ],

    "LIST_SUFFIX": [
        ["SUFFIX", "LIST_SUFFIX"],
        ["EPSILON"]
    ],

    "SUFFIX": [
        ["VARSUFFIX"],  # Reuse VARSUFFIX for array indexing and field access
        ["CALLSUFFIX"]  # New rule for function calls
    ],

    "CALLSUFFIX": [
        ["ARGS"],
        [Token(TokenType.COLON, ":"), Token(TokenType.ID, "Name"), "ARGS"]
    ],

    "FUNCTIONCALL": [
        ["PRIMARYEXP", "LIST_SUFFIX", "CALLSUFFIX"]  # Must end with a call
    ],

    "ARGS": [
        [Token(TokenType.LPAREN, "("), "OPT_EXPLIST",
         Token(TokenType.RPAREN, ")")],
        ["TABLECONSTRUCTOR"],
        [Token(TokenType.STRING, "LiteralString")]
    ],

    "FUNCTIONDEF": [
        [Token(TokenType.KEYWORD, "function"), "FUNCBODY"]
    ],

    "FUNCBODY": [
        [Token(TokenType.LPAREN, "("), "OPT_PARLIST",
         Token(TokenType.RPAREN, ")"),
         "BLOCK", Token(TokenType.KEYWORD, "end")]
    ],

    "OPT_PARLIST": [
        ["PARLIST"],
        ["EPSILON"]
    ],

    "PARLIST": [
        ["NAMELIST", "OPT_COMMA_VARARG"],
        [Token(TokenType.OP, "...")]
    ],

    "OPT_COMMA_VARARG": [
        [Token(TokenType.COMMA, ","), Token(TokenType.OP, "...")],
        ["EPSILON"]
    ],

    "TABLECONSTRUCTOR": [
        [Token(TokenType.LCURLY, "{"), "OPT_FIELDLIST",
         Token(TokenType.RCURLY, "}")]
    ],

    "OPT_FIELDLIST": [
        ["FIELDLIST"],
        ["EPSILON"]
    ],

    "FIELDLIST": [
        ["FIELD", "LIST_FIELDSEP_FIELD", "OPT_FIELDSEP"]
    ],

    "LIST_FIELDSEP_FIELD": [
        ["FIELDSEP", "FIELD", "LIST_FIELDSEP_FIELD"],
        ["EPSILON"]
    ],

    "OPT_FIELDSEP": [
        ["FIELDSEP"],
        ["EPSILON"]
    ],

    "FIELD": [
        [Token(TokenType.LBRACKET, "["), "EXP", Token(TokenType.RBRACKET, "]"),
         Token(TokenType.OP, "="), "EXP"],
        [Token(TokenType.ID, "Name"), Token(TokenType.OP, "="), "EXP"],
        ["EXP"]
    ],

    "FIELDSEP": [
        [Token(TokenType.COMMA, ",")],
        [Token(TokenType.SEMICOLON, ";")]
    ],

    "BINOP": [
        [Token(TokenType.OP, "+")],
        [Token(TokenType.OP, "-")],
        [Token(TokenType.OP, "*")],
        [Token(TokenType.OP, "/")],
        [Token(TokenType.OP, "//")],
        [Token(TokenType.OP, "^")],
        [Token(TokenType.OP, "%")],
        [Token(TokenType.OP, "&")],
        [Token(TokenType.OP, "~")],
        [Token(TokenType.OP, "|")],
        [Token(TokenType.OP, ">>")],
        [Token(TokenType.OP, "<<")],
        [Token(TokenType.OP, "..")],
        [Token(TokenType.OP, "<")],
        [Token(TokenType.OP, "<=")],
        [Token(TokenType.OP, ">")],
        [Token(TokenType.OP, ">=")],
        [Token(TokenType.OP, "==")],
        [Token(TokenType.OP, "~=")],
        [Token(TokenType.KEYWORD, "and")],
        [Token(TokenType.KEYWORD, "or")]
    ],

    "UNOP": [
        [Token(TokenType.OP, "-")],
        [Token(TokenType.KEYWORD, "not")],
        [Token(TokenType.OP, "#")],
        [Token(TokenType.OP, "~")]
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


def pretty_print_ast(node: ASTNode, indent: int = 0,
                     indent_char: str = "  ") -> str:
    """
    Pretty prints an AST with cascading indentation levels.

    Args:
        node: The AST node to print
        indent: Current indentation level (default: 0)
        indent_char: Character(s) to use for indentation (default: two spaces)

    Returns:
        A formatted string representation of the AST
    """
    # Build the current line
    result = []
    indent_str = indent_char * indent

    # Add node type
    result.append(f"{indent_str}{node.type}")

    # Add token value if present
    if node.token:
        result.append(f"({node.token.string})")

    # If there are child nodes, add them with increased indentation
    if node.nodes:
        result.append(" {")

        # Process each child node
        for i, child in enumerate(node.nodes):
            child_str = pretty_print_ast(child, indent + 1, indent_char)
            result.append("\n" + child_str)

            # Add comma if not the last child
            if i < len(node.nodes) - 1:
                result[-1] += ","

        # Close the children block
        result.append("\n" + indent_str + "}")

    return "".join(result)


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
        if entry.type == TokenType.EOF and cur == len(self.tokens):
            return ASTMatchResult(True, 0,
                                  ASTNode(rule_element_name(entry), entry, []))
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
    def match_non_terminal(self, cur: int, name: str) -> ASTMatchResult:
        best = None

        for rule in self.syntax[name]:
            try_match = self.match_rule_starting_at(cur, rule)
            if not try_match:
                continue
            # Keep track of the longest successful match
            if best is None or try_match.forward > best.forward:
                best = try_match

        if best:
            return best
        return ASTMatchResult(False, 0, None)

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
                    logger.debug(f"matched T {entry}")
                    node = match.node
                    assert node is not None
                    got_match = True
                    if (node.type != "TokenType.EOF"):
                        forward += match.forward
                        saved_nodes.append(node)
            else:
                match = self.match_non_terminal(cur + forward, entry)
                if match:
                    logger.debug(f"matched NT {entry} with forward "
                                 "{match.forward}")
                    forward += match.forward
                    assert match.node is not None
                    got_match = True
                    if (match.node.type != "EPSILON"):
                        saved_nodes.append(match.node)

            if not got_match:
                # Nope, found nothing useful. Tell caller to try something
                # else.
                return ASTMatchResult(False, 0, None)

        logger.info(f"matched rule {rule} with forward {forward}")
        result_node.nodes = saved_nodes
        logger.debug(pretty_print_ast(result_node))
        return ASTMatchResult(True, forward, result_node)

    def parse(self, init_name: str = "CHUNK") -> ASTMatchResult:
        # hack to ensure that must match an EOF at the end to succeed
        eof = Token(TokenType.EOF, "")
        init: ASTRule = self.syntax[init_name][0]
        if init[-1] != eof:
            init.entries += [eof]
        if self.tokens[-1] != eof:
            self.tokens.append(eof)

        return self.match_non_terminal(0, init_name)
