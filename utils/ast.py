import lark
from .ast_base import ASTNode
from .errors import UnknownVariableError


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
            name = self.children[0].value
            sym = self.lookup(name)
            if not sym and not self.assign:
                raise UnknownVariableError
            elif (sym and sym.type == "function") or self.assign:
                return name
            else:
                return "${" + name + "}"

        # PREFIX[exp]; unsupported
        if isinstance(self.children[1], ExpNode):
            return self.children[0].gen() + "[" + self.children[1].gen() + "]"
        # PREFIX.NAME; unsupported
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

    def get_type(self):
        return self.get_only(RetstatNode).get_type()


class ChunkNode(ASTNode):
    def gen(self):
        return "\n".join(map(lambda n: n.gen(), self.children))


# Labels and GOTOs are unsupported in zsh
class LabelNode(ASTNode):
    pass


class FuncbodyNode(ASTNode):
    def gen(self):
        return self.get_only(BlockNode).gen()


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

    def get_type(self):
        first = self.children[0]
        if isinstance(first, lark.Token):
            if first.value == "nil":
                return "string"
            elif first.value == "false":
                return "bool"
            elif first.value == "true":
                return "bool"
            elif first.type == "NUMBER":
                return "number"
            elif first.type == "STRING":
                return "string"
        else:
            return first.get_type()
        return "unknown"


class StatNode(ASTNode):
    def gen(self) -> str:
        if len(self.children) < 1:
            return ""
        first = self.children[0]
        if isinstance(first, lark.Token):
            if first.value == ";":
                return ";"
        elif first.is_a(BreakNode):
            return "break"
        elif first.is_a(GotoNode):  # not supported
            return "goto"
        elif first.is_a(DoNode):
            return "do\n" + indent(self.children[1].gen(), 1) + \
                "\ndone"
        elif first.is_a(WhileNode):
            return "while [[ " + self.children[1].gen() + " ]]; do\n" + \
                indent(self.children[2].gen(), 1) + "\ndone"
        elif first.is_a(RepeatNode):
            return "while ! ((" + self.children[1].gen() + "))\ndo\n" + \
                indent(self.children[2].gen(), 1) + "\ndone"
        elif first.is_a(VarlistNode):
            var = self.get_only(VarlistNode)
            exp = self.get_only(ExplistNode)
            var.set_recursive('assign', True)
            # TODO: handle RHS cases between
            # - simple expression: $exp
            # - string of multiple components: ""
            # - function output: $()
            return var.gen() + "=\"" + exp.gen() + '"'  # safe
        elif first.is_a(FunctioncallNode):
            return first.gen()
        else:
            return first.gen()
        return ""

    def get_symbols(self):
        if self.has(LocalAssignNode):
            return self.get_only(LocalAssignNode).get_symbols()
        if self.has(LocalFunctionNode):
            return self.get_only(LocalFunctionNode).get_symbols()
        vars = self.get(VarlistNode)
        if not vars:
            return []
        ventry = vars[0].children[0].children[0]
        exp = self.get_only(ExplistNode)
        sym = self.make_symbol(ventry.value, exp.get_type())
        return [sym]

    def update_symbols(self):
        self.symbol_table.sequential = True
        syms = self.get_symbols()
        self.symbol_table.insert(syms)
        super().update_symbols()


class PrefixexpNode(ASTNode):
    def gen(self) -> str:
        if len(self.children) > 1:  # parens
            return "(" + self.children[1].gen() + ")"
        if self.children[0].is_a(FunctioncallNode):
            self.children[0].set_recursive('capture', True)
        return self.children[0].gen()

    def get_type(self):
        if (n := self.get(VarNode)):
            return n[0].get_type()
        return "unknown"


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

    def update_symbols(self):
        self.symbol_table.sequential = True
        super().update_symbols()


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


class WhileNode(ASTNode):
    pass


class DoNode(ASTNode):
    pass


class GotoNode(ASTNode):
    pass


class BreakNode(ASTNode):
    pass


class RepeatNode(ASTNode):
    pass


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
                declaration += f"{par.value}=${i + 1}\n"
        declaration = indent(declaration, 1)
        body_gen = indent(body.gen(), 1)
        return f"function {name.value}() {{\n{declaration}\n{body_gen}\n}}\n"

    def get_symbols(self):
        assert len(self.children) == 2
        name, _ = self.children
        return [self.make_symbol(name, "function")]

    def update_symbols(self):
        syms = self.get_symbols()
        _, body = self.children
        parslist = body.get_only(ParlistNode)
        if parslist:
            pars = parslist.children[0].children
            for i in range(0, len(pars)):
                par = pars[i]
                syms += [self.make_symbol(par.value, "unknown")]
        self.symbol_table.insert(syms)  # recursion possible
        super().update_symbols()


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
        res = self.make_symbol(attr.children[0].value, "unknown")
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
                return "$(" + self.children[0].gen() + " " + \
                    self.children[1].gen() + ")"
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
