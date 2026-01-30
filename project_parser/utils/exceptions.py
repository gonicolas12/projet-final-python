"""
Exceptions personnalisées pour le projet Parser.
"""


class ParserException(Exception):
    """Exception de base pour tous les parsers."""
    pass


class FileNotFoundError(ParserException):
    """Levée quand un fichier n'est pas trouvé."""
    pass


class InvalidFormatError(ParserException):
    """Levée quand le format du fichier est invalide."""
    pass


class EncodingError(ParserException):
    """Levée quand il y a un problème d'encodage."""
    pass


class ValidationError(ParserException):
    """Levée quand la validation échoue."""
    pass


class UnsupportedFormatError(ParserException):
    """Levée quand le format n'est pas supporté."""
    pass
