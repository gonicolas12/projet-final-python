# 🏗️ Architecture Technique - Project Parser

## 📋 Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Principes de conception](#principes-de-conception)
3. [Architecture des modules](#architecture-des-modules)
4. [Design Patterns utilisés](#design-patterns-utilisés)
5. [Flux de traitement](#flux-de-traitement)
6. [Gestion des erreurs](#gestion-des-erreurs)
7. [Système de logs](#système-de-logs)
8. [Extensibilité](#extensibilité)

---

## 🎯 Vue d'ensemble

**Project Parser** suit une architecture modulaire et orientée objet basée sur les principes SOLID. L'application est structurée en couches indépendantes qui communiquent via des interfaces bien définies.

### Diagramme de haut niveau

```
┌─────────────────────────────────────────────────────┐
│                    main.py (CLI)                    │
│                  Point d'entrée                     │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              ParserFactory                          │
│         Sélectionne le parser approprié             │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │CSVParser │  │JSONParser│  │XMLParser │
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │             │             │
       └─────────────┼─────────────┘
                     ▼
            ┌─────────────────┐
            │  StandardData   │
            │  (Data Model)   │
            └─────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Converters     │
            │  (Optionnel)    │
            └─────────────────┘
```

---

## 🎨 Principes de conception

### SOLID

#### **S** - Single Responsibility Principle
Chaque classe a une seule responsabilité :
- `CSVParser` : uniquement le parsing CSV
- `Logger` : uniquement la gestion des logs
- `FileValidator` : uniquement la validation des fichiers

#### **O** - Open/Closed Principle
Les parsers sont ouverts à l'extension (nouveaux formats) mais fermés à la modification (classe de base stable).

#### **L** - Liskov Substitution Principle
Tous les parsers héritent de `BaseParser` et sont interchangeables.

#### **I** - Interface Segregation Principle
Interfaces spécifiques plutôt qu'une interface monolithique.

#### **D** - Dependency Inversion Principle
Les modules de haut niveau dépendent d'abstractions (BaseParser), pas d'implémentations concrètes.

### DRY (Don't Repeat Yourself)
Logique commune factorisée dans `BaseParser` et `utils/`.

### Separation of Concerns
Séparation claire entre parsing, validation, logging et modèles de données.

---

## 🧩 Architecture des modules

### 1. Module `parsers/`

#### BaseParser (Classe abstraite)

```python
from abc import ABC, abstractmethod
from typing import Any

class BaseParser(ABC):
    """
    Classe abstraite définissant l'interface commune pour tous les parsers.
    """
    
    @abstractmethod
    def parse(self, file_path: str) -> 'StandardData':
        """Parse un fichier et retourne StandardData."""
        pass
    
    @abstractmethod
    def validate(self, file_path: str) -> bool:
        """Valide le format du fichier."""
        pass
    
    def _read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """Lit le contenu d'un fichier (méthode commune)."""
        pass
```

#### Parsers Concrets

- **CSVParser** : Utilise `csv.DictReader`
- **JSONParser** : Utilise `json.load()`
- **XMLParser** : Utilise `xml.etree.ElementTree`

Chaque parser implémente la logique spécifique à son format.

#### ParserFactory

```python
class ParserFactory:
    """
    Factory pattern pour instancier le parser approprié.
    """
    
    _parsers = {
        '.csv': CSVParser,
        '.json': JSONParser,
        '.xml': XMLParser,
    }
    
    @classmethod
    def get_parser(cls, file_path: str) -> BaseParser:
        """Retourne le parser approprié selon l'extension."""
        ext = Path(file_path).suffix.lower()
        parser_class = cls._parsers.get(ext)
        
        if not parser_class:
            raise UnsupportedFormatError(f"Format {ext} non supporté")
        
        return parser_class()
```

### 2. Module `models/`

#### StandardData

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class StandardData:
    """
    Structure de données standardisée pour tous les formats.
    """
    headers: List[str]
    rows: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        """Initialise les métadonnées automatiquement."""
        if 'parsed_at' not in self.metadata:
            self.metadata['parsed_at'] = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire."""
        return {
            'headers': self.headers,
            'rows': self.rows,
            'metadata': self.metadata
        }
    
    def __len__(self) -> int:
        """Retourne le nombre de lignes."""
        return len(self.rows)
```

### 3. Module `utils/`

#### Logger

```python
import logging
from pathlib import Path

class CustomLogger:
    """
    Configuration centralisée des logs.
    """
    
    @staticmethod
    def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Handler fichier
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setLevel(logging.INFO)
        
        # Handler console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Format
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
```

#### FileValidator

```python
from pathlib import Path
import magic  # optionnel

class FileValidator:
    """
    Validation des fichiers avant parsing.
    """
    
    @staticmethod
    def exists(file_path: str) -> bool:
        """Vérifie l'existence du fichier."""
        return Path(file_path).exists()
    
    @staticmethod
    def is_readable(file_path: str) -> bool:
        """Vérifie les permissions de lecture."""
        path = Path(file_path)
        return path.exists() and path.is_file()
    
    @staticmethod
    def get_size(file_path: str) -> int:
        """Retourne la taille en octets."""
        return Path(file_path).stat().st_size
    
    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """Détecte l'encodage du fichier."""
        # Tente UTF-8 puis Latin-1
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                continue
        return 'utf-8'  # fallback
```

#### Exceptions

```python
class ParserException(Exception):
    """Exception de base pour tous les parsers."""
    pass

class FileNotFoundError(ParserException):
    """Fichier introuvable."""
    pass

class InvalidFormatError(ParserException):
    """Format de fichier invalide."""
    pass

class EncodingError(ParserException):
    """Erreur d'encodage."""
    pass

class ValidationError(ParserException):
    """Erreur de validation."""
    pass

class UnsupportedFormatError(ParserException):
    """Format non supporté."""
    pass
```

### 4. Module `converters/`

```python
class FormatConverter:
    """
    Conversion entre différents formats.
    """
    
    def __init__(self, data: StandardData):
        self.data = data
    
    def to_csv(self, output_path: str) -> None:
        """Export vers CSV."""
        pass
    
    def to_json(self, output_path: str) -> None:
        """Export vers JSON."""
        pass
    
    def to_xml(self, output_path: str) -> None:
        """Export vers XML."""
        pass
```

### 5. Module `config/`

```python
from pathlib import Path

class Settings:
    """
    Configuration de l'application.
    """
    
    # Chemins
    BASE_DIR = Path(__file__).parent.parent
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Logs
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s'
    LOG_FILE = LOGS_DIR / 'app.log'
    
    # Parsing
    DEFAULT_ENCODING = 'utf-8'
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
    
    # Formats supportés
    SUPPORTED_FORMATS = ['.csv', '.json', '.xml']
```

---

## 🎭 Design Patterns utilisés

### 1. Factory Pattern (ParserFactory)
**Problème** : Instancier le bon parser selon le format  
**Solution** : Factory qui retourne le parser approprié

### 2. Strategy Pattern (BaseParser)
**Problème** : Algorithmes de parsing différents  
**Solution** : Interface commune, implémentations spécifiques

### 3. Singleton Pattern (Logger)
**Problème** : Une seule instance du logger  
**Solution** : Logger partagé via `logging.getLogger(name)`

### 4. Template Method Pattern (BaseParser)
**Problème** : Workflow commun avec étapes spécifiques  
**Solution** : Méthodes abstraites pour les étapes personnalisables

---

## 🔄 Flux de traitement

### Parsing standard

```
1. User → main.py (CLI)
   ↓
2. main.py → ParserFactory.get_parser(file_path)
   ↓
3. ParserFactory → Instancie le bon parser (CSV/JSON/XML)
   ↓
4. Parser → FileValidator.validate(file_path)
   ↓
5. FileValidator → Vérifie existence, permissions, encodage
   ↓
6. Parser → parse(file_path)
   ↓
7. Parser → Lit et transforme les données
   ↓
8. Parser → Retourne StandardData
   ↓
9. StandardData → Peut être converti (FormatConverter)
   ↓
10. Output → Affichage ou export
```

### Gestion des logs

```
Chaque étape génère des logs :

[INFO]    Début du parsing de data.csv
[DEBUG]   Encodage détecté : utf-8
[INFO]    156 lignes parsées avec succès
[WARNING] Colonne 'age' manquante à la ligne 42
[ERROR]   Échec du parsing : format invalide
```

---

## ⚠️ Gestion des erreurs

### Hiérarchie des exceptions

```
ParserException (base)
├── FileNotFoundError
├── InvalidFormatError
├── EncodingError
├── ValidationError
└── UnsupportedFormatError
```

### Stratégie de gestion

```python
try:
    parser = ParserFactory.get_parser(file_path)
    data = parser.parse(file_path)
except FileNotFoundError as e:
    logger.error(f"Fichier introuvable : {e}")
    sys.exit(1)
except InvalidFormatError as e:
    logger.error(f"Format invalide : {e}")
    sys.exit(2)
except Exception as e:
    logger.critical(f"Erreur inattendue : {e}", exc_info=True)
    sys.exit(99)
```

---

## 📊 Système de logs

### Niveaux utilisés

| Niveau | Usage | Exemple |
|--------|-------|----------|
| DEBUG | Détails techniques | `Lecture de 1024 octets` |
| INFO | Opérations normales | `Parsing réussi : 100 lignes` |
| WARNING | Situations anormales | `Encodage forcé en latin-1` |
| ERROR | Erreurs récupérables | `Ligne 42 ignorée : format invalide` |
| CRITICAL | Erreurs fatales | `Corruption du fichier` |

### Configuration

```
Console : WARNING et au-dessus
Fichier : INFO et au-dessus (logs/app.log)
Rotation : 10 MB, 5 fichiers max
```

---

## 🔧 Extensibilité

### Ajouter un nouveau format (exemple : YAML)

#### 1. Créer le parser

```python
# parsers/yaml_parser.py
import yaml
from .base_parser import BaseParser

class YAMLParser(BaseParser):
    def parse(self, file_path: str) -> StandardData:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        # Transformation en StandardData
        return StandardData(...)
```

#### 2. Enregistrer dans la Factory

```python
# parsers/parser_factory.py
from .yaml_parser import YAMLParser

class ParserFactory:
    _parsers = {
        '.csv': CSVParser,
        '.json': JSONParser,
        '.xml': XMLParser,
        '.yaml': YAMLParser,  # ← Ajout
        '.yml': YAMLParser,
    }
```

#### 3. Ajouter les tests

```python
# tests/test_yaml_parser.py
def test_yaml_parser():
    parser = YAMLParser()
    data = parser.parse('tests/fixtures/sample.yaml')
    assert len(data.rows) > 0
```

### Points d'extension

✅ Nouveaux formats (YAML, TOML, Excel)  
✅ Nouvelles validations (schéma JSON, DTD XML)  
✅ Nouveaux exports (Parquet, Avro)  
✅ Middlewares de transformation  
✅ Plugins de logging (Sentry, ELK)  

---

## 📈 Performance

### Optimisations prévues

- **Streaming** : Parser les gros fichiers par chunks
- **Parallélisation** : Traiter plusieurs fichiers en concurrent
- **Cache** : Mettre en cache les résultats de parsing
- **Lazy loading** : Charger les données à la demande

### Limites actuelles

- Fichiers chargés entièrement en mémoire
- Pas de traitement parallèle
- Pas de cache

---

## 🔒 Sécurité

### Considérations

- Validation stricte des chemins de fichiers (pas d'injection)
- Limitation de la taille des fichiers
- Sanitization des données XML (prévention XXE)
- Pas d'exécution de code arbitraire

---

## 📚 Références

- [PEP 8](https://peps.python.org/pep-0008/) : Style Guide
- [Design Patterns](https://refactoring.guru/design-patterns) : Gang of Four
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Python Logging](https://docs.python.org/3/library/logging.html)

---

**Cette architecture est conçue pour être :**
- ✅ Maintenable
- ✅ Testable
- ✅ Extensible
- ✅ Documentée
- ✅ Performante
