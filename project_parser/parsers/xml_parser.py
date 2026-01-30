"""
Parser pour les fichiers XML.
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any

from project_parser.parsers.base_parser import BaseParser
from project_parser.models.data_model import StandardData
from project_parser.utils.exceptions import InvalidFormatError
from project_parser.utils.logger import CustomLogger

logger = CustomLogger.setup_logger(__name__)


class XMLParser(BaseParser):
    """
    Parser pour les fichiers XML.
    
    Utilise xml.etree.ElementTree pour parser les fichiers XML.
    Convertit la structure XML en liste de dictionnaires.
    
    Format attendu:
        <root>
            <item>
                <field1>value1</field1>
                <field2>value2</field2>
            </item>
            <item>...</item>
        </root>
    
    Example:
        >>> parser = XMLParser()
        >>> data = parser.parse('data.xml')
        >>> print(f"{len(data)} éléments parsés")
    """
    
    def parse(self, file_path: str, **kwargs) -> StandardData:
        """
        Parse un fichier XML et retourne StandardData.
        
        Args:
            file_path (str): Chemin vers le fichier XML
            encoding (str, optional): Encodage du fichier. Défaut: 'utf-8'
            root_tag (str, optional): Tag racine à parser. Défaut: auto-détection
            item_tag (str, optional): Tag des items. Défaut: auto-détection
        
        Returns:
            StandardData: Données parsées
        
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            InvalidFormatError: Si le format XML est invalide
        """
        encoding = kwargs.get('encoding', 'utf-8')
        root_tag = kwargs.get('root_tag', None)
        item_tag = kwargs.get('item_tag', None)
        
        logger.info(f"Parsing XML : {file_path} (encoding='{encoding}')")
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Déterminer les items à parser
            if item_tag:
                items = root.findall(f'.//{item_tag}')
            else:
                # Auto-détection : prendre les enfants directs du root
                items = list(root)
            
            if not items:
                logger.warning(f"Aucun élément trouvé dans {file_path}")
                return StandardData(
                    headers=[],
                    rows=[],
                    metadata={
                        'source': file_path,
                        'format': 'xml',
                        'encoding': encoding,
                        'rows_count': 0,
                        'columns_count': 0
                    }
                )
            
            # Convertir les items XML en dictionnaires
            rows = []
            headers_set = set()
            
            for item in items:
                row = {}
                for child in item:
                    tag = child.tag
                    text = child.text or ''
                    row[tag] = text.strip()
                    headers_set.add(tag)
                rows.append(row)
            
            headers = sorted(list(headers_set))
            
            # S'assurer que toutes les lignes ont toutes les clés
            for row in rows:
                for header in headers:
                    if header not in row:
                        row[header] = ''
            
            logger.info(f"XML parsé avec succès : {len(rows)} éléments, {len(headers)} champs")
            
            return StandardData(
                headers=headers,
                rows=rows,
                metadata={
                    'source': file_path,
                    'format': 'xml',
                    'encoding': encoding,
                    'root_tag': root.tag,
                    'rows_count': len(rows),
                    'columns_count': len(headers)
                }
            )
            
        except FileNotFoundError:
            logger.error(f"Fichier introuvable : {file_path}")
            raise
        except ET.ParseError as e:
            logger.error(f"Erreur de parsing XML : {e}")
            raise InvalidFormatError(f"Format XML invalide dans {file_path}: {e}")
        except Exception as e:
            logger.error(f"Erreur inattendue : {e}")
            raise InvalidFormatError(f"Impossible de parser {file_path}: {e}")
    
    def validate(self, file_path: str) -> bool:
        """
        Valide qu'un fichier XML peut être parsé.
        
        Args:
            file_path (str): Chemin du fichier
        
        Returns:
            bool: True si valide
        """
        if not Path(file_path).exists():
            return False
        
        if self._get_file_extension(file_path) != '.xml':
            return False
        
        try:
            ET.parse(file_path)
            return True
        except Exception:
            return False
