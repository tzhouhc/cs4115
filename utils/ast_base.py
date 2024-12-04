from abc import ABC
from typing import Any, List, Optional, Type, Callable
from .symbols_base import SymbolTable


class ASTNode(ABC):
    def __init__(self) -> None:
        self.name = ""
        self.symbol_table: SymbolTable = SymbolTable()
        self.parent: Optional[ASTNode] = None
        self.children: List[Any] = []

    def gen(self) -> str:
        return str(self.name)

    def child_nodes(self) -> List['ASTNode']:
        return [c for c in self.children if isinstance(c, ASTNode)]

    def get(self, t: Type) -> List['ASTNode']:
        if not self.children:
            return []
        return [c for c in self.children if isinstance(c, t)]

    def map(self, f: Callable[['ASTNode'], Any]) -> List[Any]:
        return list(map(f, self.children))
