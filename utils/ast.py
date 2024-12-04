import lark
import inspect
from . import code_gen, parser
from .ast_base import ASTNode


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


def define_ast_node_classes(parser: lark.Lark) -> None:
    rules = parser.rules
    rule_names = [snake_to_camel(rule.origin.name) for rule in rules]
    for name in rule_names:
        node_class = type(f"{name}Node", (ASTNode,), {})
        globals()[f"{name}Node"] = node_class


def attach_generators():
    for func_name, func in inspect.getmembers(code_gen, inspect.isfunction):
        if func_name.startswith('gen_'):
            class_name = snake_to_camel(func_name[4:]) + 'Node'
            if class_name in globals():
                class_type = globals()[class_name]
                setattr(class_type, 'gen', func)


define_ast_node_classes(parser.PARSER)
attach_generators()
