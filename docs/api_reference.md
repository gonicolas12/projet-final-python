# 📚 Référence API - Project Parser

## 📋 Table des matières

1. [Module parsers](#module-parsers)
2. [Module models](#module-models)
3. [Module utils](#module-utils)
4. [Module converters](#module-converters)
5. [Module config](#module-config)
6. [Exemples d'utilisation](#exemples-dutilisation)

---

## 📦 Module `parsers`

### `BaseParser` (Abstract Base Class)

Classe abstraite définissant l'interface commune pour tous les parsers.

```python
from abc import ABC, abstractmethod
from typing import Any
from project_parser.models.data_model import StandardData

class BaseParser(ABC):
    """
    Classe abstraite pour tous les parsers.
    
    Tous les parsers concrets doivent hériter de cette classe
    et implémenter les méthodes abstraites.
    """
```

#### Méthodes abstraites

##### `parse(file_path: str, **kwargs) -> StandardData`

Parse un fichier et retourne un objet StandardData.

**Paramètres :**
- `file_path` (str) : Chemin vers le fichier à parser
- `**kwargs` : Arguments optionnels spécifiques au parser

**Retourne :**
- `StandardData` : Objet contenant les données parsées

**Lève :**
- `FileNotFoundError` : Si le fichier n'existe pas
- `InvalidFormatError` : Si le format est invalide
- `EncodingError` : Si l'encodage pose problème

**Exemple :**
```python
parser = CSVParser()
data = parser.parse('data.csv', encoding='utf-8', delimiter=',')
```

##### `validate(file_path: str) -> bool`

Valide qu'un fichier peut être parsé.

**Paramètres :**
- `file_path` (str) : Chemin vers le fichier

**Retourne :**
- `bool` : True si valide, False sinon

**Exemple :**
```python
if parser.validate('data.csv'):
    data = parser.parse('data.csv')
```

#### Méthodes communes

##### `_read_file(file_path: str, encoding: str = 'utf-8') -> str`

Lit le contenu d'un fichier (méthode protégée).

**Paramètres :**
- `file_path` (str) : Chemin du fichier
- `encoding` (str, optional) : Encodage. Défaut: 'utf-8'

**Retourne :**
- `str` : Contenu du fichier

---

### `CSVParser`

Parser pour les fichiers CSV.

```python
from project_parser.parsers.csv_parser import CSVParser

class CSVParser(BaseParser):
    """
    Parser pour les fichiers CSV.
    
    Supporte différents délimiteurs, encodages et options CSV.
    """
```

#### Méthodes

##### `parse(file_path: str, delimiter: str = ',', encoding: str = 'utf-8', **kwargs) -> StandardData`

**Paramètres supplémentaires :**
- `delimiter` (str, optional) : Séparateur de colonnes. Défaut: ','
- `quotechar` (str, optional) : Caractère de citation. Défaut: '"'
- `skipinitialspace` (bool, optional) : Ignorer les espaces. Défaut: True

**Exemple :**
```python
parser = CSVParser()

# CSV standard (virgule)
data = parser.parse('data.csv')

# CSV avec point-virgule
data = parser.parse('data.csv', delimiter=';')

# CSV avec encodage spécifique
data = parser.parse('data.csv', encoding='latin-1')
```

---

### `JSONParser`

Parser pour les fichiers JSON.

```python
from project_parser.parsers.json_parser import JSONParser

class JSONParser(BaseParser):
    """
    Parser pour les fichiers JSON.
    
    Supporte les tableaux et objets JSON.
    """
```

#### Méthodes

##### `parse(file_path: str, encoding: str = 'utf-8', **kwargs) -> StandardData`

**Exemple :**
```python
parser = JSONParser()

# JSON simple
data = parser.parse('data.json')

# JSON avec encodage
data = parser.parse('data.json', encoding='utf-8')
```

**Format JSON attendu :**
```json
[
    {"col1": "value1", "col2": "value2"},
    {"col1": "value3", "col2": "value4"}
]
```

ou

```json
{
    "data": [
        {"col1": "value1", "col2": "value2"},
        {"col1": "value3", "col2": "value4"}
    ]
}
```

---

### `XMLParser`

Parser pour les fichiers XML.

```python
from project_parser.parsers.xml_parser import XMLParser

class XMLParser(BaseParser):
    """
    Parser pour les fichiers XML.
    
    Utilise xml.etree.ElementTree pour le parsing.
    """
```

#### Méthodes

##### `parse(file_path: str, root_tag: str = None, encoding: str = 'utf-8', **kwargs) -> StandardData`

**Paramètres supplémentaires :**
- `root_tag` (str, optional) : Tag racine à parser. Défaut: auto-détection

**Exemple :**
```python
parser = XMLParser()

# XML standard
data = parser.parse('data.xml')

# XML avec tag racine spécifique
data = parser.parse('data.xml', root_tag='records')
```

**Format XML attendu :**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<data>
    <record>
        <col1>value1</col1>
        <col2>value2</col2>
    </record>
    <record>
        <col1>value3</col1>
        <col2>value4</col2>
    </record>
</data>
```

---

### `ParserFactory`

Factory pour instancier le parser approprié.

```python
from project_parser.parsers.parser_factory import ParserFactory

class ParserFactory:
    """
    Factory pattern pour créer des parsers.
    
    Détecte automatiquement le format et retourne le parser approprié.
    """
```

#### Méthodes de classe

##### `get_parser(file_path: str) -> BaseParser`

Retourne le parser approprié selon l'extension du fichier.

**Paramètres :**
- `file_path` (str) : Chemin du fichier

**Retourne :**
- `BaseParser` : Instance du parser approprié

**Lève :**
- `UnsupportedFormatError` : Si le format n'est pas supporté

**Exemple :**
```python
# Détection automatique
parser = ParserFactory.get_parser('data.csv')  # → CSVParser
parser = ParserFactory.get_parser('data.json')  # → JSONParser
parser = ParserFactory.get_parser('data.xml')  # → XMLParser

# Utilisation
data = parser.parse('data.csv')
```

##### `register_parser(extension: str, parser_class: Type[BaseParser]) -> None`

Enregistre un nouveau parser pour une extension.

**Paramètres :**
- `extension` (str) : Extension (avec le point, ex: '.yaml')
- `parser_class` (Type[BaseParser]) : Classe du parser

**Exemple :**
```python
from project_parser.parsers.yaml_parser import YAMLParser

# Ajouter le support YAML
ParserFactory.register_parser('.yaml', YAMLParser)
ParserFactory.register_parser('.yml', YAMLParser)

# Maintenant utilisable
parser = ParserFactory.get_parser('data.yaml')
```

---

## 📊 Module `models`

### `StandardData`

Modèle de données standardisé pour tous les formats.

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class StandardData:
    """
    Structure de données standardisée.
    
    Représente les données parsées de manière uniforme,
    quel que soit le format source.
    """
    headers: List[str]
    rows: List[Dict[str, Any]]
    metadata: Dict[str, Any]
```

#### Attributs

- `headers` (List[str]) : Noms des colonnes/champs
- `rows` (List[Dict[str, Any]]) : Données sous forme de liste de dictionnaires
- `metadata` (Dict[str, Any]) : Métadonnées (source, format, date, etc.)

#### Méthodes

##### `to_dict() -> Dict[str, Any]`

Convertit en dictionnaire.

**Retourne :**
- `dict` : Représentation complète sous forme de dictionnaire

**Exemple :**
```python
data_dict = data.to_dict()
print(data_dict)
# {
#     'headers': ['name', 'age'],
#     'rows': [{'name': 'Alice', 'age': 30}],
#     'metadata': {'source': 'data.csv', 'parsed_at': '...'}
# }
```

##### `__len__() -> int`

Retourne le nombre de lignes.

**Exemple :**
```python
print(f"Nombre de lignes : {len(data)}")  # 150
```

##### `__getitem__(index: int) -> Dict[str, Any]`

Accès par index.

**Exemple :**
```python
first_row = data[0]
print(first_row)  # {'name': 'Alice', 'age': 30}
```

##### `__iter__()`

Itération sur les lignes.

**Exemple :**
```python
for row in data:
    print(row['name'])
```

---

## 🛠️ Module `utils`

### `logger.py` - CustomLogger

Gestion centralisée des logs.

```python
from project_parser.utils.logger import CustomLogger
import logging

class CustomLogger:
    """
    Configuration et gestion des logs.
    """
```

#### Méthodes statiques

##### `setup_logger(name: str, level: int = logging.INFO) -> logging.Logger`

Configure et retourne un logger.

**Paramètres :**
- `name` (str) : Nom du logger
- `level` (int, optional) : Niveau de log. Défaut: INFO

**Retourne :**
- `logging.Logger` : Instance configurée

**Exemple :**
```python
logger = CustomLogger.setup_logger('my_module', logging.DEBUG)

logger.debug("Message de debug")
logger.info("Opération réussie")
logger.warning("Attention")
logger.error("Erreur rencontrée")
logger.critical("Erreur critique")
```

---

### `file_validator.py` - FileValidator

Validation des fichiers.

```python
from project_parser.utils.file_validator import FileValidator

class FileValidator:
    """
    Validation et vérification des fichiers.
    """
```

#### Méthodes statiques

##### `exists(file_path: str) -> bool`

Vérifie si un fichier existe.

**Exemple :**
```python
if FileValidator.exists('data.csv'):
    print("Fichier trouvé")
```

##### `is_readable(file_path: str) -> bool`

Vérifie les permissions de lecture.

**Exemple :**
```python
if not FileValidator.is_readable('data.csv'):
    raise PermissionError("Impossible de lire le fichier")
```

##### `get_size(file_path: str) -> int`

Retourne la taille en octets.

**Exemple :**
```python
size = FileValidator.get_size('data.csv')
print(f"Taille : {size / 1024:.2f} KB")
```

##### `detect_encoding(file_path: str) -> str`

Détecte l'encodage du fichier.

**Retourne :**
- `str` : Encodage détecté ('utf-8', 'latin-1', etc.)

**Exemple :**
```python
encoding = FileValidator.detect_encoding('data.csv')
parser = CSVParser()
data = parser.parse('data.csv', encoding=encoding)
```

---

### `exceptions.py` - Exceptions personnalisées

```python
from project_parser.utils.exceptions import *
```

#### Hiérarchie

```
ParserException (base)
├── FileNotFoundError
├── InvalidFormatError
├── EncodingError
├── ValidationError
└── UnsupportedFormatError
```

#### Utilisation

```python
from project_parser.utils.exceptions import InvalidFormatError, FileNotFoundError

try:
    parser = ParserFactory.get_parser('data.csv')
    data = parser.parse('data.csv')
except FileNotFoundError as e:
    print(f"Fichier introuvable : {e}")
except InvalidFormatError as e:
    print(f"Format invalide : {e}")
except ParserException as e:
    print(f"Erreur de parsing : {e}")
```

---

## 🔄 Module `converters`

### `FormatConverter`

Conversion entre différents formats.

```python
from project_parser.converters.format_converter import FormatConverter
from project_parser.models.data_model import StandardData

class FormatConverter:
    """
    Conversion de StandardData vers différents formats.
    """
    
    def __init__(self, data: StandardData):
        """
        Initialise le convertisseur.
        
        Args:
            data: Objet StandardData à convertir
        """
        self.data = data
```

#### Méthodes

##### `to_csv(output_path: str, delimiter: str = ',', encoding: str = 'utf-8') -> None`

Exporte vers CSV.

**Exemple :**
```python
converter = FormatConverter(data)
converter.to_csv('output.csv', delimiter=';')
```

##### `to_json(output_path: str, indent: int = 2, encoding: str = 'utf-8') -> None`

Exporte vers JSON.

**Exemple :**
```python
converter = FormatConverter(data)
converter.to_json('output.json', indent=4)
```

##### `to_xml(output_path: str, root_tag: str = 'data', row_tag: str = 'record', encoding: str = 'utf-8') -> None`

Exporte vers XML.

**Exemple :**
```python
converter = FormatConverter(data)
converter.to_xml('output.xml', root_tag='users', row_tag='user')
```

---

## ⚙️ Module `config`

### `Settings`

Configuration de l'application.

```python
from project_parser.config.settings import Settings

class Settings:
    """
    Paramètres globaux de l'application.
    """
    
    # Chemins
    BASE_DIR: Path
    LOGS_DIR: Path
    
    # Logs
    LOG_LEVEL: str = 'INFO'
    LOG_FORMAT: str = '[%(asctime)s] [%(levelname)s] - %(message)s'
    LOG_FILE: Path
    
    # Parsing
    DEFAULT_ENCODING: str = 'utf-8'
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100 MB
    
    # Formats
    SUPPORTED_FORMATS: List[str] = ['.csv', '.json', '.xml']
```

**Utilisation :**
```python
from project_parser.config.settings import Settings

print(f"Formats supportés : {Settings.SUPPORTED_FORMATS}")
print(f"Taille max : {Settings.MAX_FILE_SIZE / 1024 / 1024} MB")
```

---

## 💡 Exemples d'utilisation

### Exemple complet

```python
import logging
from project_parser.parsers.parser_factory import ParserFactory
from project_parser.converters.format_converter import FormatConverter
from project_parser.utils.logger import CustomLogger
from project_parser.utils.file_validator import FileValidator
from project_parser.utils.exceptions import ParserException

# Configuration du logger
logger = CustomLogger.setup_logger('main', logging.INFO)

def process_file(input_file: str, output_format: str = 'json'):
    """
    Traite un fichier et le convertit.
    """
    try:
        # Validation
        logger.info(f"Traitement de {input_file}")
        
        if not FileValidator.exists(input_file):
            raise FileNotFoundError(f"Fichier {input_file} introuvable")
        
        # Détection encodage
        encoding = FileValidator.detect_encoding(input_file)
        logger.debug(f"Encodage détecté : {encoding}")
        
        # Parsing
        parser = ParserFactory.get_parser(input_file)
        data = parser.parse(input_file, encoding=encoding)
        logger.info(f"Parsing réussi : {len(data)} lignes")
        
        # Conversion
        converter = FormatConverter(data)
        output_file = f"output.{output_format}"
        
        if output_format == 'json':
            converter.to_json(output_file)
        elif output_format == 'xml':
            converter.to_xml(output_file)
        elif output_format == 'csv':
            converter.to_csv(output_file)
        
        logger.info(f"Export réussi : {output_file}")
        return data
        
    except ParserException as e:
        logger.error(f"Erreur de parsing : {e}")
        raise
    except Exception as e:
        logger.critical(f"Erreur inattendue : {e}", exc_info=True)
        raise

# Utilisation
if __name__ == '__main__':
    data = process_file('data.csv', output_format='json')
    print(f"Traité : {len(data)} lignes")
```

---

## 📝 Notes

- Tous les parsers sont **thread-safe**
- Les chemins de fichiers peuvent être absolus ou relatifs
- L'encodage par défaut est **UTF-8**
- Les logs sont écrits dans `logs/app.log`

---

**Documentation générée le 30 janvier 2026**
