"""
Modèle de données standardisé pour tous les formats.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class StandardData:
    """
    Structure de données standardisée pour représenter les données parsées.
    
    Attributes:
        headers (List[str]): Noms des colonnes/champs
        rows (List[Dict[str, Any]]): Données sous forme de liste de dictionnaires
        metadata (Dict[str, Any]): Métadonnées (source, format, date, etc.)
    
    Example:
        >>> data = StandardData(
        ...     headers=['name', 'age'],
        ...     rows=[{'name': 'Alice', 'age': 30}],
        ...     metadata={'source': 'data.csv', 'format': 'csv'}
        ... )
        >>> print(len(data))
        1
    """
    headers: List[str]
    rows: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialise automatiquement les métadonnées."""
        if 'parsed_at' not in self.metadata:
            self.metadata['parsed_at'] = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet en dictionnaire.
        
        Returns:
            dict: Représentation complète sous forme de dictionnaire
        """
        return {
            'headers': self.headers,
            'rows': self.rows,
            'metadata': self.metadata
        }
    
    def __len__(self) -> int:
        """Retourne le nombre de lignes."""
        return len(self.rows)
    
    def __getitem__(self, index: int) -> Dict[str, Any]:
        """Permet l'accès par index : data[0]"""
        return self.rows[index]
    
    def __iter__(self):
        """Permet l'itération : for row in data:"""
        return iter(self.rows)
