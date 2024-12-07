LARK_GRAMMAR = """
    // Basic structure
    chunk: block

    // Done
    block: stat* retstat?

    // Done
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
    // Done
    else_block: "else" block

    for_range: "for" NAME "=" exp "," exp ("," exp)? "do" block "end"
    for_in: "for" namelist "in" explist "do" block "end"
    function_def: "function" funcname funcbody
    // Done
    local_function: "local" "function" NAME funcbody
    local_assign: "local" attnamelist ("=" explist)?

    attnamelist: NAME attrib ("," NAME attrib)*
    attrib: ("<" NAME ">")?

    // Done
    retstat: "return" explist? ";"?

    // Unsupported
    label: "::" NAME "::"

    funcname: NAME ("." NAME)* (":" NAME)?

    // Done
    varlist: var ("," var)*
    // Done
    var: NAME | prefixexp "[" exp "]" | prefixexp "." NAME

    namelist: NAME ("," NAME)*
    // Done
    explist: exp ("," exp)*

    // Done
    exp: "nil" | "false" | "true" | NUMBER | STRING | "..." | functiondef
       | prefixexp | tableconstructor | exp binop exp | unop exp

    // Done
    prefixexp: var | functioncall | "(" exp ")"
    // Done
    functioncall: prefixexp args | prefixexp ":" NAME args
    // Done
    args: "(" explist? ")" | tableconstructor | STRING

    functiondef: "function" funcbody
    // Done
    funcbody: "(" parlist? ")" block "end"
    parlist: namelist ("," "...")? | "..."

    // Unsupported
    tableconstructor: "{" fieldlist? "}"

    fieldlist: field (fieldsep field)* fieldsep?
    field: "[" exp "]" "=" exp | NAME "=" exp | exp
    fieldsep: "," | ";"

    // Done
    !binop: "+" | "-" | "*" | "/" | "//" | "^" | "%"
         | "&" | "~" | "|" | ">>" | "<<" | ".."
         | "<" | "<=" | ">" | ">=" | "==" | "~="
         | "and" | "or"

    // Done
    !unop: "-" | "not" | "#" | "~"

    // Terminals
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.ESCAPED_STRING -> STRING

    // Whitespace
    %import common.WS
    %ignore WS
"""
