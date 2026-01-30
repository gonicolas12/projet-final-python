"""
Parser pour les fichiers JSON.
"""
import json
from pathlib import Path
from typing import List, Dict, Any

from project_parser.parsers.base_parser import BaseParser
from project_parser.models.data_model import StandardData
from project_parser.utils.exceptions import InvalidFormatError
from project_parser.utils.logger import CustomLogger

logger = CustomLogger.setup_logger(__name__)


class JSONParser(BaseParser):
    """
    Parser pour les fichiers JSON.
    
    Supporte les tableaux JSON et les objets avec une clé 'data'.
    
    Formats acceptés:
        1. Tableau d'objets : [{"a": 1}, {"a": 2}]
        2. Objet avec clé 'data' : {"data": [{"a": 1}, {"a": 2}]}
    
    Example:
        >>> parser = JSONParser()
        >>> data = parser.parse('data.json')
        >>> print(f"{len(data)} éléments parsés")
    """
    
    def parse(self, file_path: str, **kwargs) -> StandardData:
        """
        Parse un fichier JSON et retourne StandardData.
        
        Args:
            file_path (str): Chemin vers le fichier JSON
            encoding (str, optional): Encodage du fichier. Défaut: 'utf-8'
            data_key (str, optional): Clé contenant les données. Défaut: 'data'
        
        Returns:
            StandardData: Données parsées
        
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            InvalidFormatError: Si le format JSON est invalide
        """
        encoding = kwargs.get('encoding', 'utf-8')
        data_key = kwargs.get('data_key', 'data')
        
        logger.info(f"Parsing JSON : {file_path} (encoding='{encoding}')")
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = json.load(f)
            
            # Déterminer le format
            if isinstance(content, list):
                # Format : [{...}, {...}]
                rows = content
            elif isinstance(content, dict) and data_key in content:
                # Format : {"data": [{...}, {...}]}
                rows = content[data_key]
            elif isinstance(content, dict):
                # Si c'est un objet unique, le mettre dans une liste
                rows = [content]
            else:
                raise InvalidFormatError("Format JSON non supporté")
            
            if not rows:
                logger.warning(f"Aucune donnée trouvée dans {file_path}")
                headers = []
            else:
                # Extraire les headers depuis la première ligne
                if isinstance(rows[0], dict):
                    headers = list(rows[0].keys())
                else:
                    raise InvalidFormatError("Les éléments JSON doivent être des objets")
            
            logger.info(f"JSON parsé avec succès : {len(rows)} éléments, {len(headers)} champs")
            
            return StandardData(
                headers=headers,
                rows=rows,
                metadata={
                    'source': file_path,
                    'format': 'json',
                    'encoding': encoding,
                    'rows_count': len(rows),
                    'columns_count': len(headers)
                }
            )
            
        except FileNotFoundError:
            logger.error(f"Fichier introuvable : {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de parsing JSON : {e}")
            raise InvalidFormatError(f"Format JSON invalide dans {file_path}: {e}")
        except UnicodeDecodeError as e:
            logger.error(f"Erreur d'encodage : {e}")
            raise InvalidFormatError(f"Erreur d'encodage dans {file_path}")
    
    def validate(self, file_path: str) -> bool:
        """
        Valide qu'un fichier JSON peut être parsé.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            bool: True si valide
        """
        if not Path(file_path).exists():
            return False
        
        if self._get_file_extension(file_path) != '.json':
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except Exception:
            return False
