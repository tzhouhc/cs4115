from abc import ABC
from typing import Any, List, Optional, Type, Callable, Union
from .symbols import Symbol, SymbolTable
from lark import Token


class ASTNode(ABC):
    def __init__(self) -> None:
        self.name = ""
        self.symbol_table: SymbolTable = SymbolTable()
        self.symbol_table.node = self
        self.parent: Optional[ASTNode] = None
        self.children: List[Any] = []
        self.i: int
        self.assign = False
        self.capture = False
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

    def has(self, t: Type) -> bool:
        """Return if any children is of a specific type."""
        if not self.children:
            return False
        return any([isinstance(c, t) for c in self.children])

    def get_only(self, t: Type) -> 'ASTNode':
        """Return the one expected child of a specific type."""
        assert self.children
        found = [c for c in self.children if isinstance(c, t)]
        assert len(found) == 1
        return found[0]

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.symbol_table.lookup(name)

    def map(self, f: Callable[['ASTNode'], Any]) -> List[Any]:
        """Return result of calling function on all children."""
        return list(map(f, self.children))

    def map_nodes(self, f: Callable[['ASTNode'], Any]) -> List[Any]:
        """Return result of calling function on all AST children."""
        return list(map(f, self.child_nodes()))

    def get_symbols(self) -> List['Symbol']:
        """Return the new symbols generated in this node."""
        return []

    def update_symbols(self):
        """Default update behavior: call update on all AST children."""
        for c in self.child_nodes():
            c.update_symbols()

    def is_a(self, t: Type) -> bool:
        return isinstance(self, t)

    def set_recursive(self, name: str, val: Any) -> None:
        print(f"recursively setting on {self.name}")
        self.__dict__[name] = val
        for c in self.child_nodes():
            c.set_recursive(name, val)
