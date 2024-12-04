import lark
from .ast_base import ASTNode
from .symbols import Symbol, SymbolTable


INDENT = "  "


def indent(text: str, level: int) -> str:
    return INDENT * level + ("\n" + INDENT * level).join(text.split("\n"))


class AttribNode(ASTNode):
    pass


class ForInNode(ASTNode):
    pass


class VarNode(ASTNode):
    def gen(self):
        assert isinstance(self.children[0], lark.Token)
        return self.children[0].value


class ForRangeNode(ASTNode):
    pass


class NamelistNode(ASTNode):
    pass


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


class LabelNode(ASTNode):
    pass


class FuncbodyNode(ASTNode):
    def gen(self):
        return "\n".join(map(lambda n: n.gen(), self.children[1:]))


class VarlistStar4Node(ASTNode):
    pass


class ExpNode(ASTNode):
    def gen(self):
        if len(self.children) > 1:
            return " ".join([c.gen() for c in self.children])
        c = self.children[0]
        if isinstance(c, lark.Token):
            return c.value
        return c.gen()


class StatNode(ASTNode):
    def gen(self):
        return "\n".join(map(lambda n: n.gen(), self.children))


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
        if_body = indent(self.children[1].gen(), 1)
        if len(self.children) > 2:
            else_body = "else\n" + indent(self.children[2].gen(), 1)
        return f"if [[ {cond} ]]; then\n" + if_body + "\n" + else_body + "\nfi\n"


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
    pass


class FunctionDefNode(ASTNode):
    pass


class ArgsNode(ASTNode):
    def gen(self):
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
        pars = body.children[0].children[0].children
        declaration = ""
        for i in range(0, len(pars)):
            par = pars[i]
            assert isinstance(par, lark.Token)
            declaration += f"{par.value}=${i}\n"
        declaration = indent(declaration, 1)
        body_gen = indent(body.gen(), 1)
        return f"function {name.value}() {{\n{declaration}\n{body_gen}\n}}\n"


class FunctiondefNode(ASTNode):
    pass


class LocalAssignNode(ASTNode):
    pass


class UnopNode(ASTNode):
    pass


class FieldsepNode(ASTNode):
    pass


class ParlistNode(ASTNode):
    pass


class VarlistNode(ASTNode):
    pass


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
    def gen(self):
        return self.children[0].gen() + f"({self.children[1].gen()})"


class IfStmtStar1Node(ASTNode):
    pass


class FuncnameNode(ASTNode):
    pass


class BinopNode(ASTNode):
    def gen(self):
        assert isinstance(self.children[0], lark.Token)
        return self.children[0].value


def snake_to_camel(name):
    """Converts a snake_case string to CamelCase."""
    words = name.split('_')
    return ''.join(word.capitalize() for word in words)


def ast_from_lark(ast: lark.Tree) -> ASTNode:
    node_type = snake_to_camel(ast.data) + "Node"
    node = globals()[node_type]()
    assert isinstance(node, ASTNode)
    children = []
    for c in ast.children:
        if isinstance(c, lark.Token):
            children += [c]
        else:
            cnode = ast_from_lark(c)
            cnode.parent = node
            cnode.symbol_table.parent = node.symbol_table
            children += [cnode]
    node.children = children
    node.name = ast.data
    return node
