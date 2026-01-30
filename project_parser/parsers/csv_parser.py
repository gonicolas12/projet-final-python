"""
Parser pour les fichiers CSV.
"""
import csv
from pathlib import Path
from typing import List, Dict, Any

from project_parser.parsers.base_parser import BaseParser
from project_parser.models.data_model import StandardData
from project_parser.utils.exceptions import InvalidFormatError
from project_parser.utils.logger import CustomLogger

logger = CustomLogger.setup_logger(__name__)


class CSVParser(BaseParser):
    """
    Parser pour les fichiers CSV.
    
    Supporte différents délimiteurs, encodages et options CSV standard.
    Utilise csv.DictReader pour lire les fichiers.
    
    Example:
        >>> parser = CSVParser()
        >>> data = parser.parse('data.csv')
        >>> print(f"{len(data)} lignes parsées")
        
        >>> # Avec options personnalisées
        >>> data = parser.parse('data.csv', delimiter=';', encoding='latin-1')
    """
    
    def parse(self, file_path: str, **kwargs) -> StandardData:
        """
        Parse un fichier CSV et retourne StandardData.
        
        Args:
            file_path (str): Chemin vers le fichier CSV
            delimiter (str, optional): Séparateur de colonnes. Défaut: ','
            encoding (str, optional): Encodage du fichier. Défaut: 'utf-8'
            quotechar (str, optional): Caractère de citation. Défaut: '"'
            skipinitialspace (bool, optional): Ignorer les espaces. Défaut: True
        
        Returns:
            StandardData: Données parsées
        
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            InvalidFormatError: Si le format CSV est invalide
        """
        delimiter = kwargs.get('delimiter', ',')
        encoding = kwargs.get('encoding', 'utf-8')
        quotechar = kwargs.get('quotechar', '"')
        skipinitialspace = kwargs.get('skipinitialspace', True)
        
        logger.info(f"Parsing CSV : {file_path} (delimiter='{delimiter}', encoding='{encoding}')")
        
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                reader = csv.DictReader(
                    f,
                    delimiter=delimiter,
                    quotechar=quotechar,
                    skipinitialspace=skipinitialspace
                )
                
                # Récupérer les headers
                headers = reader.fieldnames
                if not headers:
                    raise InvalidFormatError(f"Aucun header trouvé dans {file_path}")
                
                # Lire toutes les lignes
                rows = list(reader)
                
                logger.info(f"CSV parsé avec succès : {len(rows)} lignes, {len(headers)} colonnes")
                
                # Créer StandardData
                return StandardData(
                    headers=headers,
                    rows=rows,
                    metadata={
                        'source': file_path,
                        'format': 'csv',
                        'delimiter': delimiter,
                        'encoding': encoding,
                        'rows_count': len(rows),
                        'columns_count': len(headers)
                    }
                )
                
        except FileNotFoundError:
            logger.error(f"Fichier introuvable : {file_path}")
            raise
        except csv.Error as e:
            logger.error(f"Erreur de parsing CSV : {e}")
            raise InvalidFormatError(f"Format CSV invalide dans {file_path}: {e}")
        except UnicodeDecodeError as e:
            logger.error(f"Erreur d'encodage : {e}")
            raise InvalidFormatError(f"Erreur d'encodage dans {file_path}. Essayez un autre encodage.")
    
    def validate(self, file_path: str) -> bool:
        """
        Valide qu'un fichier CSV peut être parsé.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            bool: True si valide
        """
        if not Path(file_path).exists():
            return False
        
        if self._get_file_extension(file_path) != '.csv':
            return False
        
        try:
            # Essayer de lire les premières lignes
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                next(reader, None)  # Essayer de lire une ligne
            return True
        except Exception:
            return False
