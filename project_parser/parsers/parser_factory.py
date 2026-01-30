"""
Factory pour instancier le parser approprié selon le format.
"""
from pathlib import Path
from typing import Type, Dict

from project_parser.parsers.base_parser import BaseParser
from project_parser.parsers.csv_parser import CSVParser
from project_parser.parsers.json_parser import JSONParser
from project_parser.parsers.xml_parser import XMLParser
from project_parser.utils.exceptions import UnsupportedFormatError
from project_parser.utils.logger import CustomLogger

logger = CustomLogger.setup_logger(__name__)


class ParserFactory:
    """
    Factory pour créer des parsers selon l'extension du fichier.
    
    Utilise le pattern Factory pour instancier automatiquement
    le parser approprié (CSV, JSON ou XML) selon l'extension.
    
    Example:
        >>> parser = ParserFactory.get_parser('data.csv')
        >>> print(type(parser).__name__)  # CSVParser
        
        >>> data = parser.parse('data.csv')
    """
    
    # Mapping extension → classe de parser
    _parsers: Dict[str, Type[BaseParser]] = {
        '.csv': CSVParser,
        '.json': JSONParser,
        '.xml': XMLParser,
    }
    
    @classmethod
    def get_parser(cls, file_path: str) -> BaseParser:
        """
        Retourne le parser approprié selon l'extension du fichier.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            BaseParser: Instance du parser approprié (CSVParser, JSONParser, XMLParser)
        
        Raises:
            UnsupportedFormatError: Si le format n'est pas supporté
        
        Example:
            >>> parser = ParserFactory.get_parser('data.csv')
            >>> isinstance(parser, CSVParser)
            True
        """
        ext = Path(file_path).suffix.lower()
        
        logger.debug(f"Détection du parser pour extension : {ext}")
        
        parser_class = cls._parsers.get(ext)
        
        if not parser_class:
            supported = ', '.join(cls._parsers.keys())
            logger.error(f"Format non supporté : {ext}")
            raise UnsupportedFormatError(
                f"Format {ext} non supporté. Formats acceptés : {supported}"
            )
        
        logger.info(f"Parser sélectionné : {parser_class.__name__}")
        return parser_class()
    
    @classmethod
    def register_parser(cls, extension: str, parser_class: Type[BaseParser]) -> None:
        """
        Enregistre un nouveau parser pour une extension.
        
        Permet d'étendre les formats supportés dynamiquement.
        
        Args:
            extension (str): Extension avec le point (ex: '.yaml')
            parser_class (Type[BaseParser]): Classe du parser
        
        Example:
            >>> ParserFactory.register_parser('.yaml', YAMLParser)
        """
        if not extension.startswith('.'):
            extension = f'.{extension}'
        
        extension = extension.lower()
        cls._parsers[extension] = parser_class
        logger.info(f"Parser {parser_class.__name__} enregistré pour {extension}")
    
    @classmethod
    def get_supported_formats(cls) -> list:
        """
        Retourne la liste des formats supportés.
        
        Returns:
            list: Liste des extensions supportées
        
        Example:
            >>> formats = ParserFactory.get_supported_formats()
            >>> print(formats)  # ['.csv', '.json', '.xml']
        """
        return list(cls._parsers.keys())
