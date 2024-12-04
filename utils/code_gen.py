import lark
from . import ast_base

INDENT = "  "


def gen(n: ast_base.ASTNode) -> str:
    return n.gen()


def indent(text: str, level: int) -> str:
    return INDENT * level + ("\n" + INDENT * level).join(text.split("\n"))


def gen_chunk(ast: ast_base.ASTNode) -> str:
    return "\n".join(map(gen, ast.children))


def gen_block(ast: ast_base.ASTNode) -> str:
    return "\n".join(map(gen, ast.children))


def gen_stat(ast: ast_base.ASTNode) -> str:
    return "\n".join(map(gen, ast.children))


def gen_local_function(ast: ast_base.ASTNode) -> str:
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


def gen_funcbody(ast: ast_base.ASTNode) -> str:
    # skip parlist
    return "\n".join(map(gen, ast.children[1:]))


def gen_if_stmt(ast: ast_base.ASTNode) -> str:
    cond = gen(ast.children[0])
    else_body = ""
    if_body = indent(gen(ast.children[1]), 1)
    if len(ast.children) > 2:
        else_body = "else\n" + indent(gen(ast.children[2]), 1)
    return f"if [[ {cond} ]]; then\n" + if_body + "\n" + else_body + "\nfi\n"


def gen_else_block(ast: ast_base.ASTNode) -> str:
    return gen(ast.children[0])


def gen_retstat(ast: ast_base.ASTNode) -> str:
    return "echo " + gen(ast.children[0])


def gen_explist(ast: ast_base.ASTNode) -> str:
    return ", ".join([gen(c) for c in ast.children])


def gen_prefixexp(ast: ast_base.ASTNode) -> str:
    if len(ast.children) > 1:  # parens
        return "(" + gen(ast.children[1]) + ")"
    else:
        return gen(ast.children[0])


def gen_functioncall(ast: ast_base.ASTNode) -> str:
    return gen(ast.children[0]) + f"({gen(ast.children[1])})"


def gen_args(ast: ast_base.ASTNode) -> str:
    return gen(ast.children[0])


def gen_var(ast: ast_base.ASTNode) -> str:
    assert isinstance(ast.children[0], lark.Token)
    return ast.children[0].value


def gen_exp(ast: ast_base.ASTNode) -> str:
    if len(ast.children) > 1:
        return " ".join([gen(c) for c in ast.children])
    c = ast.children[0]
    if isinstance(c, lark.Token):
        return c.value
    return gen(c)


def gen_binop(ast: ast_base.ASTNode) -> str:
    assert isinstance(ast.children[0], lark.Token)
    return ast.children[0].value
