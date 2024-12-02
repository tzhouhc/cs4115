import lark

INDENT = "  "


def indent(text: str, level: int) -> str:
    return INDENT * level + ("\n" + INDENT * level).join(text.split("\n"))


def gen_chunk(ast: lark.Tree) -> str:
    return "\n".join(map(gen, ast.children))


def gen_block(ast: lark.Tree) -> str:
    return "\n".join(map(gen, ast.children))


def gen_stat(ast: lark.Tree) -> str:
    return "\n".join(map(gen, ast.children))


def gen_local_function(ast: lark.Tree) -> str:
    assert len(ast.children) == 2
    name, body = ast.children
    assert isinstance(name, lark.Token)
    # the children goes funcbody -> parlist -> namelist
    pars = body.children[0].children[0].children
    declaration = ""
    for i in range(0, len(pars)):
        par = pars[i]
        assert isinstance(par, lark.Token)
        declaration += f"{par.value}=${i}\n"
    declaration = indent(declaration, 1)
    body_gen = indent(gen(body), 1)
    return f"function {name.value}() {{\n{declaration}\n{body_gen}\n}}\n"


def gen_funcbody(ast: lark.Tree) -> str:
    # skip parlist
    return "\n".join(map(gen, ast.children[1:]))


def gen_if_stmt(ast: lark.Tree) -> str:
    cond = gen(ast.children[0])
    else_body = ""
    if_body = indent(gen(ast.children[1]), 1)
    if len(ast.children) > 2:
        else_body = "else\n" + indent(gen(ast.children[2]), 1)
    return f"if [[ {cond} ]]; then\n" + if_body + "\n" + else_body + "\nfi\n"


def gen_else_block(ast: lark.Tree) -> str:
    return gen(ast.children[0])


def gen_retstat(ast: lark.Tree) -> str:
    return "echo " + gen(ast.children[0])


def gen_explist(ast: lark.Tree) -> str:
    return ", ".join([gen(c) for c in ast.children])


def gen_prefixexp(ast: lark.Tree) -> str:
    if len(ast.children) > 1:  # parens
        return "(" + gen(ast.children[1]) + ")"
    else:
        return gen(ast.children[0])


def gen_functioncall(ast: lark.Tree) -> str:
    return gen(ast.children[0]) + f"({gen(ast.children[1])})"


def gen_args(ast: lark.Tree) -> str:
    return gen(ast.children[0])


def gen_var(ast: lark.Tree) -> str:
    assert isinstance(ast.children[0], lark.Token)
    return ast.children[0].value


def gen_exp(ast: lark.Tree) -> str:
    if len(ast.children) > 1:
        return " ".join([gen(c) for c in ast.children])
    c = ast.children[0]
    if isinstance(c, lark.Token):
        return c.value
    return gen(c)


def gen_binop(ast: lark.Tree) -> str:
    assert isinstance(ast.children[0], lark.Token)
    return ast.children[0].value


CODE_GEN_FUNCS = {
    "chunk": gen_chunk,
    "block": gen_block,
    "stat": gen_stat,
    "local_function": gen_local_function,
    "funcbody": gen_funcbody,
    "functioncall": gen_functioncall,
    "if_stmt": gen_if_stmt,
    "else_block": gen_else_block,
    "retstat": gen_retstat,
    "explist": gen_explist,
    "exp": gen_exp,
    "var": gen_var,
    "args": gen_args,
    "prefixexp": gen_prefixexp,
    "binop": gen_binop,
}


def gen(ast: lark.Tree) -> str:
    if ast.data in CODE_GEN_FUNCS:
        return CODE_GEN_FUNCS[ast.data](ast)
    else:
        return ast.data


class CodeGenerator:

    def __init__(self, ast: lark.Tree) -> None:
        self.ast = ast

    def gen(self):
        return gen(self.ast)