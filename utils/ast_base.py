from abc import ABC
from typing import Any, List, Optional, Type, Callable, Union
from .symbols import SymbolTable
from lark import Token


class ASTNode(ABC):
    def __init__(self) -> None:
        self.name = ""
        self.symbol_table: SymbolTable = SymbolTable()
        self.parent: Optional[ASTNode] = None
        self.children: List[Any] = []
        self.i: int
        self.prev: Optional[Union[ASTNode, Token]] = None
        self.next: Optional[Union[ASTNode, Token]] = None

    def gen(self) -> str:
        """Default gen behavior: print rule name."""
        return str(self.name)

    def child_nodes(self) -> List['ASTNode']:
        """Return all children that are ASTNodes."""
        return [c for c in self.children if isinstance(c, ASTNode)]

    def get(self, t: Type) -> List['ASTNode']:
        """Return all children of a specific type."""
        if not self.children:
            return []
        return [c for c in self.children if isinstance(c, t)]

    def get_only(self, t: Type) -> 'ASTNode':
        """Return the one expected child of a specific type."""
        assert self.children
        found = [c for c in self.children if isinstance(c, t)]
        assert len(found) == 1
        return found[0]

    def map(self, f: Callable[['ASTNode'], Any]) -> List[Any]:
        """Return result of calling function on all children."""
        return list(map(f, self.children))

    def map_nodes(self, f: Callable[['ASTNode'], Any]) -> List[Any]:
        """Return result of calling function on all AST children."""
        return list(map(f, self.child_nodes()))

    def update_symbols(self):
        """Default update behavior: call update on all AST children."""
        for c in self.child_nodes():
            c.update_symbols()
