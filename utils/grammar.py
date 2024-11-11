from utils.token import Token, TokenType


KEYWORD_SET = {
    "and",
    "break",
    "do",
    "else",
    "elseif",
    "end",
    "false",
    "for",
    "function",
    "goto",
    "if",
    "in",
    "local",
    "nil",
    "not",
    "or",
    "repeat",
    "return",
    "then",
    "true",
    "until",
    "while",
}


STATE_TABLE = {
    "start": {" ": "white_space", "(": "lparen",
              ")": "rparen", "[": "lbrack", "]": "rbrack",
              "{": "lcurly", "}": "rcurly",
              "+": "plus", "-": "minus", "$": "dollar",
              "=": "equal", ":": "colon",
              "/": "slash", "\\": "backslash",
              "a": "and_a", "b": "break_b",
              "i": "if_i", "t": "then_t",
              "f": "for_func_f", "e": "end_else_e",
              "*": "asterisk", "%": "percent", "^": "caret", "#": "hash",
              "&": "ampersand", "~": "tilde", "|": "pipe", "<": "less",
              ">": "greater", ".": "dot", ",": "comma", ";": "semicolon",
              "d": "do_d", "g": "goto_g", "l": "local_l",
              "n": "nil_not_n", "o": "or_o", "p": "repeat_p",
              "u": "until_u",
              "r": "return_r",
              "w": "while_w",
              "\"": "string",
              "LETTER": "id",
              "DIGIT": "num",
              },
    "white_space": {" ": "white_space", "DONE": TokenType.WHITE_SPACE},
    "lparen": {"DONE": TokenType.LPAREN},
    "rparen": {"DONE": TokenType.RPAREN},
    "lbrack": {"DONE": TokenType.LBRACKET},
    "rbrack": {"DONE": TokenType.RBRACKET},
    "lcurly": {"DONE": TokenType.LCURLY},
    "rcurly": {"DONE": TokenType.RCURLY},
    "plus": {"DONE": TokenType.OP},
    "minus": {"DONE": TokenType.OP},
    "dollar": {"DONE": TokenType.OP},
    "backslash": {"DONE": TokenType.OP},
    "asterisk": {"DONE": TokenType.OP},
    "slash": {"/": "double_slash", "DONE": TokenType.OP},
    "double_slash": {"DONE": TokenType.OP},
    "percent": {"DONE": TokenType.OP},
    "caret": {"DONE": TokenType.OP},
    "hash": {"DONE": TokenType.OP},
    "ampersand": {"DONE": TokenType.OP},
    "tilde": {"=": "not_equal", "DONE": TokenType.OP},
    "not_equal": {"DONE": TokenType.OP},
    "pipe": {"DONE": TokenType.OP},
    "less": {"<": "left_shift", "=": "less_equal", "DONE": TokenType.OP},
    "left_shift": {"DONE": TokenType.OP},
    "less_equal": {"DONE": TokenType.OP},
    "greater": {">": "right_shift", "=": "greater_equal",
                "DONE": TokenType.OP},
    "right_shift": {"DONE": TokenType.OP},
    "greater_equal": {"DONE": TokenType.OP},
    "equal": {"=": "equal_equal", "DONE": TokenType.OP},
    "equal_equal": {"DONE": TokenType.OP},
    "dot": {".": "dot_dot", "DONE": TokenType.OP},
    "dot_dot": {".": "dot_dot_dot", "DONE": TokenType.OP},
    "dot_dot_dot": {"DONE": TokenType.OP},
    "comma": {"DONE": TokenType.OP},
    "semicolon": {"DONE": TokenType.SEMICOLON},
    "colon": {":": "double_colon", "DONE": TokenType.COLON},
    "double_colon": {"DONE": TokenType.OP},
    "and_a": {"n": "and_an", "LETTER": "id", "DONE": TokenType.ID},
    "and_an": {"d": "and", "LETTER": "id", "DONE": TokenType.ID},
    "and": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "break_b": {"r": "break_br", "LETTER": "id", "DONE": TokenType.ID},
    "break_br": {"e": "break_bre", "LETTER": "id", "DONE": TokenType.ID},
    "break_bre": {"a": "break_brea", "LETTER": "id", "DONE": TokenType.ID},
    "break_brea": {"k": "break", "LETTER": "id", "DONE": TokenType.ID},
    "break": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "if_i": {"f": "if", "LETTER": "id", "DONE": TokenType.ID},
    "if": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "then_t": {"h": "then_th", "LETTER": "id", "DONE": TokenType.ID},
    "then_th": {"e": "then_the", "LETTER": "id", "DONE": TokenType.ID},
    "then_the": {"n": "then", "LETTER": "id", "DONE": TokenType.ID},
    "then": {"DONE": "", "LETTER": "id"},
    "return_r": {"e": "return_re", "LETTER": "id", "DONE": TokenType.ID},
    "return_re": {"t": "return_ret", "LETTER": "id", "DONE": TokenType.ID},
    "return_ret": {"u": "return_retu", "LETTER": "id", "DONE": TokenType.ID},
    "return_retu": {"r": "return_retur", "LETTER": "id", "DONE": TokenType.ID},
    "return_retur": {"n": "return", "LETTER": "id", "DONE": TokenType.ID},
    "return": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "end_else_e": {"n": "end_en", "l": "else_el", "LETTER": "id",
                   "DONE": TokenType.ID},
    "end_en": {"d": "end", "LETTER": "id", "DONE": TokenType.ID},
    "end": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "else_el": {"s": "else_els", "LETTER": "id", "DONE": TokenType.ID},
    "else_els": {"e": "else", "LETTER": "id", "DONE": TokenType.ID},
    "else": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "for_func_f": {"o": "for_fo", "u": "func_fu", "LETTER": "id",
                   "DONE": TokenType.ID},
    "for_fo": {"r": "for", "LETTER": "id", "DONE": TokenType.ID},
    "for": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "func_fu": {"n": "func_fun", "LETTER": "id", "DONE": TokenType.ID},
    "func_fun": {"c": "func_func", "LETTER": "id", "DONE": TokenType.ID},
    "func_func": {"t": "func_funct", "LETTER": "id", "DONE": TokenType.ID},
    "func_funct": {"i": "func_functi", "LETTER": "id", "DONE": TokenType.ID},
    "func_functi": {"o": "func_functio", "LETTER": "id", "DONE": TokenType.ID},
    "func_functio": {"n": "func", "LETTER": "id", "DONE": TokenType.ID},
    "func": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "while_w": {"h": "while_wh", "LETTER": "id", "DONE": TokenType.ID},
    "while_wh": {"i": "while_whi", "LETTER": "id", "DONE": TokenType.ID},
    "while_whi": {"l": "while_whil", "LETTER": "id", "DONE": TokenType.ID},
    "while_whil": {"e": "while", "LETTER": "id", "DONE": TokenType.ID},
    "while": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "in_i": {"n": "in", "LETTER": "id", "DONE": TokenType.ID},
    "in": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "true_t": {"r": "true_tr", "LETTER": "id", "DONE": TokenType.ID},
    "true_tr": {"u": "true_tru", "LETTER": "id", "DONE": TokenType.ID},
    "true_tru": {"e": "true", "LETTER": "id", "DONE": TokenType.ID},
    "true": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "false_f": {"a": "false_fa", "LETTER": "id", "DONE": TokenType.ID},
    "false_fa": {"l": "false_fal", "LETTER": "id", "DONE": TokenType.ID},
    "false_fal": {"s": "false_fals", "LETTER": "id", "DONE": TokenType.ID},
    "false_fals": {"e": "false", "LETTER": "id", "DONE": TokenType.ID},
    "false": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "do_d": {"o": "do", "LETTER": "id", "DONE": TokenType.ID},
    "do": {"DONE": TokenType.KEYWORD, "LETTER": "id"},

    "goto_g": {"o": "goto_go", "LETTER": "id", "DONE": TokenType.ID},
    "goto_go": {"t": "goto_got", "LETTER": "id", "DONE": TokenType.ID},
    "goto_got": {"o": "goto", "LETTER": "id", "DONE": TokenType.ID},
    "goto": {"DONE": TokenType.KEYWORD, "LETTER": "id"},

    "local_l": {"o": "local_lo", "LETTER": "id", "DONE": TokenType.ID},
    "local_lo": {"c": "local_loc", "LETTER": "id", "DONE": TokenType.ID},
    "local_loc": {"a": "local_loca", "LETTER": "id", "DONE": TokenType.ID},
    "local_loca": {"l": "local", "LETTER": "id", "DONE": TokenType.ID},
    "local": {"DONE": TokenType.KEYWORD, "LETTER": "id"},

    "nil_not_n": {"i": "nil_ni", "o": "not_no", "LETTER": "id",
                  "DONE": TokenType.ID},
    "nil_ni": {"l": "nil", "LETTER": "id", "DONE": TokenType.ID},
    "nil": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "not_no": {"t": "not", "LETTER": "id", "DONE": TokenType.ID},
    "not": {"DONE": TokenType.KEYWORD, "LETTER": "id"},

    "or_o": {"r": "or", "LETTER": "id", "DONE": TokenType.ID},
    "or": {"DONE": TokenType.KEYWORD, "LETTER": "id"},

    "repeat_p": {"e": "repeat_re", "LETTER": "id", "DONE": TokenType.ID},
    "repeat_re": {"p": "repeat_rep", "LETTER": "id", "DONE": TokenType.ID},
    "repeat_rep": {"e": "repeat_repe", "LETTER": "id", "DONE": TokenType.ID},
    "repeat_repe": {"a": "repeat_repea", "LETTER": "id", "DONE": TokenType.ID},
    "repeat_repea": {"t": "repeat", "LETTER": "id", "DONE": TokenType.ID},
    "repeat": {"DONE": TokenType.KEYWORD, "LETTER": "id"},

    "until_u": {"n": "until_un", "LETTER": "id", "DONE": TokenType.ID},
    "until_un": {"t": "until_unt", "LETTER": "id", "DONE": TokenType.ID},
    "until_unt": {"i": "until_unti", "LETTER": "id", "DONE": TokenType.ID},
    "until_unti": {"l": "until", "LETTER": "id", "DONE": TokenType.ID},
    "until": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "id": {"LETTER": "id", "DIGIT": "id", "_": "id", "DONE": TokenType.ID},
    "num": {"DIGIT": "num", "DONE": TokenType.INTEGER},
    "string": {"ANYTHING_BUT_QUOTE": "string", "\"": "string_done", "\\":
               "string_escape"},
    "string_escape": {"ANYTHING": "string"},
    "string_done": {"DONE": TokenType.STRING},
}


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
