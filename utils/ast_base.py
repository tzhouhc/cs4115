from abc import ABC
from typing import Any, List, Optional, Type


class ASTNode(ABC):
    def __init__(self) -> None:
        self.name = ""
        self.symbol_table: Optional[dict] = None
        self.parent: Optional[ASTNode] = None
        self.children: List[Any] = []

    def gen(self) -> str:
        return str(self.name)

    def get(self, t: Type) -> List['ASTNode']:
        if not self.children:
            return []
        return [c for c in self.children if isinstance(c, t)]
