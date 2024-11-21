LARK_GRAMMAR = """
    // Basic structure
    chunk: block

    block: stat* retstat?

    stat: ";"
        | varlist "=" explist
        | functioncall
        | label
        | "break"
        | "goto" NAME
        | "do" block "end"
        | "while" exp "do" block "end"
        | "repeat" block "until" exp
        | if_stmt
        | for_range
        | for_in
        | function_def
        | local_function
        | local_assign

    if_stmt: "if" exp "then" block elseif_block* else_block? "end"
    elseif_block: "elseif" exp "then" block
    else_block: "else" block

    for_range: "for" NAME "=" exp "," exp ("," exp)? "do" block "end"
    for_in: "for" namelist "in" explist "do" block "end"
    function_def: "function" funcname funcbody
    local_function: "local" "function" NAME funcbody
    local_assign: "local" attnamelist ("=" explist)?

    attnamelist: NAME attrib ("," NAME attrib)*
    attrib: ("<" NAME ">")?

    retstat: "return" explist? ";"?

    label: "::" NAME "::"

    funcname: NAME ("." NAME)* (":" NAME)?

    varlist: var ("," var)*
    var: NAME | prefixexp "[" exp "]" | prefixexp "." NAME

    namelist: NAME ("," NAME)*
    explist: exp ("," exp)*

    exp: "nil" | "false" | "true" | NUMBER | STRING | "..." | functiondef
       | prefixexp | tableconstructor | exp binop exp | unop exp

    prefixexp: var | functioncall | "(" exp ")"
    functioncall: prefixexp args | prefixexp ":" NAME args
    args: "(" explist? ")" | tableconstructor | STRING

    functiondef: "function" funcbody
    funcbody: "(" parlist? ")" block "end"
    parlist: namelist ("," "...")? | "..."

    tableconstructor: "{" fieldlist? "}"
    fieldlist: field (fieldsep field)* fieldsep?
    field: "[" exp "]" "=" exp | NAME "=" exp | exp
    fieldsep: "," | ";"

    binop: "+" | "-" | "*" | "/" | "//" | "^" | "%"
         | "&" | "~" | "|" | ">>" | "<<" | ".."
         | "<" | "<=" | ">" | ">=" | "==" | "~="
         | "and" | "or"

    unop: "-" | "not" | "#" | "~"

    // Terminals
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.ESCAPED_STRING -> STRING

    // Whitespace
    %import common.WS
    %ignore WS
"""
