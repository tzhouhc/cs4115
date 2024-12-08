import lark
from .ast_base import ASTNode
from .symbols import Symbol


INDENT = "  "


def indent(text: str, level: int) -> str:
    return INDENT * level + ("\n" + INDENT * level).join(text.split("\n"))


class AttribNode(ASTNode):
    pass


class ForInNode(ASTNode):
    pass


class VarNode(ASTNode):
    def gen(self):
        # NAME
        if isinstance(self.children[0], lark.Token):
            if self.assign:
                return self.children[0].value
            else:
                return "${" + self.children[0] + "}"
        # PREFIX[exp]
        if isinstance(self.children[1], ExpNode):
            return self.children[0].gen() + "[" + self.children[1].gen() + "]"
        # PREFIX.NAME
        else:
            return self.children[0].gen() + "." + self.children[1].value


class ForRangeNode(ASTNode):
    pass


class NamelistNode(ASTNode):
    def gen(self):
        return " ".join(map(lambda n: n.gen(), self.children))


class FieldlistNode(ASTNode):
    pass


class FuncnameStar3Node(ASTNode):
    pass


class BlockNode(ASTNode):
    def gen(self):
        return "\n".join(map(lambda n: n.gen(), self.children))


class ChunkNode(ASTNode):
    def gen(self):
        return "\n".join(map(lambda n: n.gen(), self.children))


# Labels and GOTOs are unsupported in zsh
class LabelNode(ASTNode):
    pass


class FuncbodyNode(ASTNode):
    def gen(self):
        return self.get_only(BlockNode).gen()

    def update_symbols(self):
        pass
        # params = self.get_only(ParlistNode).get_only(NamelistNode)
        # for c in params.children:
        #     self.symbol_table.insert(c, Symbol())


class VarlistStar4Node(ASTNode):
    pass


class ExpNode(ASTNode):
    def gen(self):
        if len(self.children) < 1:
            return ""
        first = self.children[0]
        if isinstance(first, lark.Token):
            if first.value == "nil":
                return "\"\""
            elif first.value == "false":
                return "false"
            elif first.value == "true":
                return "true"
            elif first.value == "...":
                return "..."  # not actually handling this case
            elif first.type == "NUMBER":
                return first.value
            else:
                return first.value
        else:
            return " ".join([c.gen() for c in self.children])


class StatNode(ASTNode):
    def gen(self) -> str:
        if len(self.children) < 1:
            return ""
        first = self.children[0]
        if isinstance(self.children[0], lark.Token):
            if first.value == ";":
                return ";"
            elif first.value == "break":
                return "break"
            elif first.value == "do":  # do block
                return "do\n" + indent(self.children[1].gen(), 1) + \
                    "\ndone"
            elif first.value == "while":  # while
                return "while ((" + self.children[1].get() + "))\ndo\n" + \
                    indent(self.children[3].gen(), 1) + "\ndone"
            elif first.value == "repeat":  # repeat until
                return "while ! ((" + self.children[1].get() + "))\ndo\n" + \
                    indent(self.children[3].gen(), 1) + "\ndone"
        elif isinstance(first, VarlistNode):
            vars = self.get(VarlistNode)
            exps = self.get(ExplistNode)
            ventry = vars[0].children[0]
            ventry.assign = True
            eentry = exps[0].children[0]
            return ventry.gen() + "=" + eentry.gen()
        elif isinstance(first, FunctioncallNode):
            first.set_recursive("assign", True)
            return first.gen()
        else:
            return first.gen()
        return ""

    def get_symbols(self):
        if self.has(LocalAssignNode):
            return self.get_only(LocalAssignNode).get_symbols()
        vars = self.get(VarlistNode)
        if not vars:
            return []
        ventry = vars[0].children[0]
        sym = Symbol(ventry.gen(), "unknown")
        return [sym]

    def update_symbols(self):
        self.symbol_table.sequential = True
        syms = self.get_symbols()
        self.symbol_table.insert(syms)


class PrefixexpNode(ASTNode):
    def gen(self) -> str:
        if len(self.children) > 1:  # parens
            return "(" + self.children[1].gen() + ")"
        else:
            return self.children[0].gen()


class AttnamelistStar2Node(ASTNode):
    pass


class IfStmtNode(ASTNode):
    def gen(self) -> str:
        cond = self.children[0].gen()
        else_body = ""
        if_body = indent(self.get_only(BlockNode).gen(), 1)
        elif_body = "\n"
        elifs = self.get(ElseifBlockNode)
        if elifs:
            for el_if in elifs:
                elif_exp = el_if.get_only(ExpNode)
                elif_body += "elif [[ " + elif_exp.gen() + " ]]; then\n"
                elif_body += indent(el_if.gen(), 1) + "\n"
        if len(self.children) > 2:
            else_body = "else\n" + \
                indent(self.get_only(ElseBlockNode).gen(), 1)
        return f"if [[ {cond} ]]; then\n{if_body}{elif_body}{else_body}\nfi\n"


class FieldlistStar7Node(ASTNode):
    pass


class FieldNode(ASTNode):
    pass


class RetstatNode(ASTNode):
    def gen(self):
        return "echo " + self.children[0].gen()


class AttnamelistNode(ASTNode):
    pass


class ElseifBlockNode(ASTNode):
    def gen(self):
        return self.get_only(BlockNode).gen()


class FunctionDefNode(ASTNode):
    pass


class ArgsNode(ASTNode):
    def gen(self):
        clen = len(self.children)
        if clen == 0:
            return ""
        if clen > 1:
            return self.children[1].gen()
        else:
            if isinstance(self.children[0], TableconstructorNode):
                return ""  # table constructor not supported
            else:
                return self.children[0].gen()


class ExplistStar6Node(ASTNode):
    pass


class BlockStar0Node(ASTNode):
    pass


class LocalFunctionNode(ASTNode):
    def gen(self) -> str:
        assert len(self.children) == 2
        name, body = self.children
        assert isinstance(name, lark.Token)
        # the children goes funcbody -> parlist -> namelist
        declaration = ""
        parslist = body.get_only(ParlistNode)
        if parslist:
            pars = parslist.children[0].children
            declaration = ""
            for i in range(0, len(pars)):
                par = pars[i]
                assert isinstance(par, lark.Token)
                declaration += f"{par.value}=${i}\n"
        declaration = indent(declaration, 1)
        body_gen = indent(body.gen(), 1)
        return f"function {name.value}() {{\n{declaration}\n{body_gen}\n}}\n"


# Anonymous function
class FunctiondefNode(ASTNode):
    def gen(self):
        assert len(self.children) == 1
        body = self.children[0]
        # the children goes funcbody -> parlist -> namelist
        declaration = ""
        parslist = body.get_only(ParlistNode)
        if parslist:
            pars = parslist.children[0].children
            declaration = ""
            for i in range(0, len(pars)):
                par = pars[i]
                assert isinstance(par, lark.Token)
                declaration += f"{par.value}=${i}\n"
        declaration = indent(declaration, 1)
        body_gen = indent(body.gen(), 1)
        return f"function {{\n{declaration}\n{body_gen}\n}}\n"


class LocalAssignNode(ASTNode):
    def gen(self):
        attr = self.get_only(AttnamelistNode)
        exps = self.get_only(ExplistNode)
        return attr.children[0].value + "=" + exps.gen()

    def get_symbols(self):
        attr = self.get_only(AttnamelistNode)
        # exps = self.get_only(ExplistNode)
        res = Symbol(attr.children[0].value, "unknown")
        return [res]


class UnopNode(ASTNode):
    __mapping = {
        "!": "! "
    }

    def gen(self):
        c0 = self.children[0]
        assert isinstance(c0, lark.Token)
        return self.__mapping.get(c0.value, c0.value)


class FieldsepNode(ASTNode):
    pass


class ParlistNode(ASTNode):
    pass


class VarlistNode(ASTNode):
    def gen(self):
        return "\n".join(map(lambda n: n.gen(), self.children))


class ElseBlockNode(ASTNode):
    def gen(self):
        return self.children[0].gen()


class TableconstructorNode(ASTNode):
    pass


class NamelistStar5Node(ASTNode):
    pass


class ExplistNode(ASTNode):
    def gen(self):
        return "\n".join(map(lambda n: n.gen(), self.children))


class FunctioncallNode(ASTNode):
    def gen(self) -> str:
        if len(self.children) == 2:
            if self.capture:  # want the result wrapped
                return "$(" + self.children[0].gen() + \
                    " ".join(self.children[1].gen()) + ")"
            else:
                return self.children[0].gen() + " " + \
                    self.children[1].gen()
        else:
            return ""  # zsh does not support objects or methods


class IfStmtStar1Node(ASTNode):
    pass


class FuncnameNode(ASTNode):
    def gen(self):
        return "\n".join(map(lambda n: n.gen(), self.children))
        # zsh doesn't have classes and module-based func declarations


class BinopNode(ASTNode):
    __mapping = {
        "==": "-eq",
        "~=": "-ne",
        ">": "-gt",
        "<": "-lt",
        ">=": "-ge",
        "<=": "-le",
        "and": "&&",
        "or": "||",
    }

    def gen(self):
        c0 = self.children[0]
        assert isinstance(c0, lark.Token)
        return self.__mapping.get(c0.value, c0.value)


def snake_to_camel(name):
    """Converts a snake_case string to CamelCase."""
    words = name.split('_')
    return ''.join(word.capitalize() for word in words)


def ast_from_lark(ast: lark.Tree) -> ASTNode:
    node_type = snake_to_camel(ast.data) + "Node"
    node = globals()[node_type]()
    assert isinstance(node, ASTNode)
    children = []
    clen = len(ast.children)
    for i in range(clen):
        c = ast.children[i]
        if isinstance(c, lark.Token):
            children += [c]
        else:
            cnode = ast_from_lark(c)
            cnode.parent = node
            cnode.symbol_table.parent = node.symbol_table
            cnode.i = i
            children += [cnode]
    node.children = children
    node.name = ast.data
    cnodes = node.child_nodes()
    for i in range(0, len(cnodes) - 1):
        cnodes[i].next = cnodes[i + 1]
        cnodes[i + 1].prev = cnodes[i]

    return node
