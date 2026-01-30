"""
Classe abstraite de base pour tous les parsers.
"""
from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path


class BaseParser(ABC):
    """
    Classe abstraite définissant l'interface commune pour tous les parsers.
    
    Tous les parsers concrets (CSV, JSON, XML) doivent hériter de cette classe
    et implémenter les méthodes abstraites parse() et validate().
    
    Example:
        >>> class MyParser(BaseParser):
        ...     def parse(self, file_path: str, **kwargs):
        ...         # Implementation
        ...         pass
        ...     def validate(self, file_path: str) -> bool:
        ...         # Implementation
        ...         return True
    """
    
    @abstractmethod
    def parse(self, file_path: str, **kwargs) -> 'StandardData':
        """
        Parse un fichier et retourne un objet StandardData.
        
        Args:
            file_path (str): Chemin vers le fichier à parser
            **kwargs: Arguments optionnels spécifiques au parser
        
        Returns:
            StandardData: Objet contenant les données parsées
        
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            InvalidFormatError: Si le format est invalide
            EncodingError: Si l'encodage pose problème
        """
        pass
    
    @abstractmethod
    def validate(self, file_path: str) -> bool:
        """
        Valide qu'un fichier peut être parsé.
        
        Args:
            file_path (str): Chemin vers le fichier
        
        Returns:
            bool: True si le fichier est valide, False sinon
        """
        pass
    
    def _read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """
        Lit le contenu d'un fichier (méthode commune protégée).
        
        Cette méthode peut être utilisée par les classes dérivées
        pour lire le contenu d'un fichier.
        
        Args:
            file_path (str): Chemin du fichier
            encoding (str, optional): Encodage du fichier. Défaut: 'utf-8'
        
        Returns:
            str: Contenu du fichier
        
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            UnicodeDecodeError: Si l'encodage est incorrect
        """
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
        
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    
    def _get_file_extension(self, file_path: str) -> str:
        """
        Retourne l'extension du fichier.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            str: Extension avec le point (ex: '.csv')
        """
        return Path(file_path).suffix.lower()
