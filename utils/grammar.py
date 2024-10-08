from utils.token import TokenType


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
    "slash": {"DONE": TokenType.OP},
    "backslash": {"DONE": TokenType.OP},
    "equal": {"DONE": TokenType.OP},
    "colon": {"DONE": TokenType.COLON},
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
    "return_r": {"e": "return_re", "LETTER": id, "DONE": TokenType.ID},
    "return_re": {"t": "return_ret", "LETTER": id, "DONE": TokenType.ID},
    "return_ret": {"u": "return_retu", "LETTER": id, "DONE": TokenType.ID},
    "return_retu": {"r": "return_retur", "LETTER": id, "DONE": TokenType.ID},
    "return_retur": {"n": "return", "LETTER": id, "DONE": TokenType.ID},
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
    "func_fun": {"c": "func", "LETTER": "id", "DONE": TokenType.ID},
    "func": {"DONE": TokenType.KEYWORD, "LETTER": "id"},
    "while_w": {"h": "while_wh", "LETTER": "id", "DONE": TokenType.ID},
    "while_wh": {"i": "while_whi", "LETTER": "id", "DONE": TokenType.ID},
    "while_whi": {"l": "while_whil", "LETTER": "id", "DONE": TokenType.ID},
    "while_whil": {"e": "while", "LETTER": "id", "DONE": TokenType.ID},
    "while": {"DONE": TokenType.KEYWORD, "LETTER": "id"},

    "id": {"LETTER": "id", "DIGIT": "id", "_": "id", "DONE": TokenType.ID},
    "num": {"DIGIT": "num", "DONE": TokenType.INTEGER},
    "string": {"ANYTHING_BUT_QUOTE": "string", "\"": "string_done", "\\":
               "string_escape"},
    "string_escape": {"ANYTHING": "string"},
    "string_done": {"DONE": TokenType.STRING},
}
