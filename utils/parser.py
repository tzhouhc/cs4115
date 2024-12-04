import lark
from . import grammar


PARSER = lark.Lark(grammar.LARK_GRAMMAR, start="chunk")
