"""
Validation et vérification des fichiers.
"""
from pathlib import Path
from typing import Optional


class FileValidator:
    """
    Utilitaires pour valider les fichiers avant parsing.
    """
    
    @staticmethod
    def exists(file_path: str) -> bool:
        """
        Vérifie si un fichier existe.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            bool: True si le fichier existe
        """
        return Path(file_path).exists()
    
    @staticmethod
    def is_readable(file_path: str) -> bool:
        """
        Vérifie si un fichier est lisible.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            bool: True si le fichier existe et est lisible
        """
        path = Path(file_path)
        return path.exists() and path.is_file()
    
    @staticmethod
    def get_size(file_path: str) -> int:
        """
        Retourne la taille du fichier en octets.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            int: Taille en octets
        """
        return Path(file_path).stat().st_size
    
    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """
        Détecte l'encodage d'un fichier.
        
        Teste UTF-8, puis Latin-1, puis CP1252.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            str: Encodage détecté ('utf-8', 'latin-1', 'cp1252')
        """
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        # Fallback
        return 'utf-8'
