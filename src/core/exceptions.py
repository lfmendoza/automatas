"""
Custom exceptions for the automata package.
"""


class RegexSyntaxError(ValueError):
    """Error de sintaxis en la expresión regular."""
    
    def __init__(self, message: str, position: int = None):
        super().__init__(message)
        self.position = position
        self.message = message
    
    def __str__(self):
        if self.position is not None:
            return f"Error en posición {self.position}: {self.message}"
        return self.message 