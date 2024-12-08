import logging
from .lib import PATH_BINS
from typing import Any

logger = logging.getLogger()


class Symbol:
    def __init__(self, name: str, type: str):
        self.name: str = name
        self.type: str = type
        self.is_initialized = False
        self.used = False
        self.used_at: Any = None
        self.source: Any = None
        self.scope_level: int = 0  # Useful for optimization later
        self.first_reference = None  # Line number/position

    def init(self):
        self.is_initialized = True

    def use(self, at=None):
        if at != self.source:
            self.used = True
            self.used_at = at

    def __str__(self) -> str:
        return f"{self.name}: {self.type}"


PATH_BIN_SYMS: dict[str, 'Symbol'] = {}
for name in PATH_BINS:
    res = Symbol(name, "function")
    res.is_initialized = True
    PATH_BIN_SYMS[name] = res


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.node: Any
        self.parent = parent
        self.children = []  # Useful for analysis
        self.sequential: bool = False  # if this is a sequential symbol table,
        # i.e. can lookup in previous nodes

    def lookup(self, name):
        # Look in current scope
        if name in self.symbols:
            return self.symbols[name]
        # if sequential symbol table, check previous node for definition.
        if self.sequential and self.node.prev:
            if res := self.node.prev.lookup(name):
                return res
        # Look in parent scope if it exists
        if self.parent:
            if res := self.parent.lookup(name):
                return res
        # if nothing found, check if this is a binary on PATH
        return PATH_BIN_SYMS.get(name, None)

    def insert(self, symbols: list['Symbol']):
        for sym in symbols:
            logger.debug(f"Inserted symbol {str(sym)}")
            self.symbols[sym.name] = sym
