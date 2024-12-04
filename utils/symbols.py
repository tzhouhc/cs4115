class Symbol:
    def __init__(self):
        self.name = None
        self.type = None
        self.is_initialized = False
        self.scope_level = 0  # Useful for optimization later
        self.first_reference = None  # Line number/position


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.children = []  # Useful for analysis

    def lookup(self, name):
        # Look in current scope
        if name in self.symbols:
            return self.symbols[name]
        # Look in parent scope if it exists
        elif self.parent:
            return self.parent.lookup(name)
        return None

    def insert(self, name, symbol):
        self.symbols[name] = symbol

