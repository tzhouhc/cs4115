from utils.ast_base import ASTNode


class GenerationError(Exception):
    pass


class UnknownVariableError(GenerationError):
    name: str
    source: ASTNode

    def __init__(self, name, source) -> None:
        self.name = name
        self.source = source
        self.msg = f"Unknown variable '{self.name}': {self.source.trace()}"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg
