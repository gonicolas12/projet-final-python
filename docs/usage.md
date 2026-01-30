# 📖 Guide d'Utilisation - Project Parser

## 📋 Table des matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Utilisation de base](#utilisation-de-base)
4. [Utilisation avancée](#utilisation-avancée)
5. [Interface CLI](#interface-cli)
6. [Exemples pratiques](#exemples-pratiques)
7. [Gestion des erreurs](#gestion-des-erreurs)
8. [FAQ](#faq)

---

## 🎯 Introduction

**Project Parser** permet de parser facilement des fichiers CSV, JSON et XML vers une structure de données Python standardisée. Ce guide vous montrera comment l'utiliser efficacement.

---

## 💾 Installation

### Installation standard

```bash
# Cloner le dépôt
git clone https://github.com/gonicolas12/projet-final-python.git
cd projet-final-python

# Installer les dépendances
pip install -r requirements.txt
```

### Installation en mode développement

```bash
# Installation éditable
pip install -e .

# Vérifier l'installation
python -m project_parser.main --version
```

---

## 🚀 Utilisation de base

### 1. Parser un fichier CSV

```python
from project_parser.parsers.parser_factory import ParserFactory

# Méthode automatique (détection du format)
parser = ParserFactory.get_parser('data.csv')
data = parser.parse('data.csv')

# Afficher les résultats
print(f"Colonnes : {data.headers}")
print(f"Nombre de lignes : {len(data)}")
print(f"Première ligne : {data.rows[0]}")
```

**Exemple de fichier CSV :**
```csv
name,age,city
Alice,30,Paris
Bob,25,Lyon
Charlie,35,Marseille
```

**Résultat :**
```python
{
    'headers': ['name', 'age', 'city'],
    'rows': [
        {'name': 'Alice', 'age': '30', 'city': 'Paris'},
        {'name': 'Bob', 'age': '25', 'city': 'Lyon'},
        {'name': 'Charlie', 'age': '35', 'city': 'Marseille'}
    ],
    'metadata': {
        'source': 'data.csv',
        'format': 'csv',
        'parsed_at': '2026-01-30T10:30:45'
    }
}
```

### 2. Parser un fichier JSON

```python
from project_parser.parsers.parser_factory import ParserFactory

parser = ParserFactory.get_parser('data.json')
data = parser.parse('data.json')

print(data.to_dict())
```

**Exemple de fichier JSON :**
```json
[
    {"name": "Alice", "age": 30, "city": "Paris"},
    {"name": "Bob", "age": 25, "city": "Lyon"}
]
```

### 3. Parser un fichier XML

```python
from project_parser.parsers.parser_factory import ParserFactory

parser = ParserFactory.get_parser('data.xml')
data = parser.parse('data.xml')

for row in data.rows:
    print(f"{row['name']} - {row['age']} ans")
```

**Exemple de fichier XML :**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<data>
    <person>
        <name>Alice</name>
        <age>30</age>
        <city>Paris</city>
    </person>
    <person>
        <name>Bob</name>
        <age>25</age>
        <city>Lyon</city>
    </person>
</data>
```

---

## 🎓 Utilisation avancée

### 1. Utilisation directe d'un parser spécifique

```python
from project_parser.parsers.csv_parser import CSVParser
from project_parser.parsers.json_parser import JSONParser
from project_parser.parsers.xml_parser import XMLParser

# Parser CSV avec options
csv_parser = CSVParser()
data = csv_parser.parse('data.csv', delimiter=';', encoding='latin-1')

# Parser JSON
json_parser = JSONParser()
data = json_parser.parse('data.json')

# Parser XML
xml_parser = XMLParser()
data = xml_parser.parse('data.xml')
```

### 2. Conversion entre formats

```python
from project_parser.parsers.parser_factory import ParserFactory
from project_parser.converters.format_converter import FormatConverter

# Parser un CSV
parser = ParserFactory.get_parser('data.csv')
data = parser.parse('data.csv')

# Convertir en JSON
converter = FormatConverter(data)
converter.to_json('output.json')

# Convertir en XML
converter.to_xml('output.xml')
```

### 3. Filtrage et transformation des données

```python
# Parser les données
parser = ParserFactory.get_parser('data.csv')
data = parser.parse('data.csv')

# Filtrer les données
filtered_rows = [
    row for row in data.rows 
    if int(row['age']) > 25
]

print(f"Personnes de plus de 25 ans : {len(filtered_rows)}")

# Transformer les données
for row in data.rows:
    row['age'] = int(row['age'])  # Convertir en entier
    row['name'] = row['name'].upper()  # Majuscules
```

### 4. Gestion de l'encodage

```python
from project_parser.utils.file_validator import FileValidator

# Détecter automatiquement l'encodage
encoding = FileValidator.detect_encoding('data.csv')
print(f"Encodage détecté : {encoding}")

# Parser avec l'encodage correct
parser = ParserFactory.get_parser('data.csv')
data = parser.parse('data.csv', encoding=encoding)
```

### 5. Validation avant parsing

```python
from project_parser.utils.file_validator import FileValidator
from project_parser.utils.exceptions import ValidationError

file_path = 'data.csv'

# Valider le fichier
if not FileValidator.exists(file_path):
    raise ValidationError(f"Fichier {file_path} introuvable")

if not FileValidator.is_readable(file_path):
    raise ValidationError(f"Impossible de lire {file_path}")

size = FileValidator.get_size(file_path)
if size > 100 * 1024 * 1024:  # 100 MB
    print(f"Attention : fichier volumineux ({size / 1024 / 1024:.2f} MB)")

# Parser
parser = ParserFactory.get_parser(file_path)
data = parser.parse(file_path)
```

---

## 💻 Interface CLI

### Commandes disponibles

#### 1. Parser un fichier

```bash
# Syntaxe de base
python -m project_parser.main parse <fichier>

# Exemples
python -m project_parser.main parse data.csv
python -m project_parser.main parse data.json
python -m project_parser.main parse data.xml
```

#### 2. Convertir un fichier

```bash
# CSV vers JSON
python -m project_parser.main convert data.csv --output data.json

# JSON vers XML
python -m project_parser.main convert data.json --output data.xml

# XML vers CSV
python -m project_parser.main convert data.xml --output data.csv
```

#### 3. Afficher les informations

```bash
# Afficher les métadonnées
python -m project_parser.main info data.csv

# Afficher les statistiques
python -m project_parser.main stats data.csv
```

#### 4. Options globales

```bash
# Aide
python -m project_parser.main --help

# Version
python -m project_parser.main --version

# Mode verbeux (logs DEBUG)
python -m project_parser.main parse data.csv --verbose

# Mode silencieux (logs ERROR uniquement)
python -m project_parser.main parse data.csv --quiet
```

---

## 🧪 Tests manuels rapides

```bash
# Tester le CLI
python -m project_parser.main parse tests/fixtures/sample.csv
python -m project_parser.main convert tests/fixtures/sample.csv --output outputs/output.json
python -m project_parser.main info tests/fixtures/sample.json

# Tester les exemples
python examples/example_csv.py
python examples/example_json.py
python examples/example_xml.py
```

---

## 💡 Exemples pratiques

### Exemple 1 : Fusion de plusieurs CSV

```python
from project_parser.parsers.csv_parser import CSVParser
from project_parser.models.data_model import StandardData

# Parser plusieurs fichiers
files = ['data1.csv', 'data2.csv', 'data3.csv']
parser = CSVParser()

all_rows = []
for file in files:
    data = parser.parse(file)
    all_rows.extend(data.rows)

# Créer un nouvel objet StandardData fusionné
merged_data = StandardData(
    headers=data.headers,
    rows=all_rows,
    metadata={'source': 'merged', 'files': files}
)

print(f"Total de lignes fusionnées : {len(merged_data)}")
```

### Exemple 2 : Export vers différents formats

```python
from project_parser.parsers.parser_factory import ParserFactory
from project_parser.converters.format_converter import FormatConverter

# Parser un fichier source
parser = ParserFactory.get_parser('source.csv')
data = parser.parse('source.csv')

# Export multiple
converter = FormatConverter(data)
converter.to_csv('output.csv')
converter.to_json('output.json')
converter.to_xml('output.xml')

print("Fichiers exportés avec succès !")
```

### Exemple 3 : Traitement par lots

```python
import os
from pathlib import Path
from project_parser.parsers.parser_factory import ParserFactory

# Traiter tous les CSV d'un dossier
data_dir = Path('data/')
csv_files = data_dir.glob('*.csv')

for csv_file in csv_files:
    try:
        parser = ParserFactory.get_parser(str(csv_file))
        data = parser.parse(str(csv_file))
        print(f"✓ {csv_file.name} : {len(data)} lignes")
    except Exception as e:
        print(f"✗ {csv_file.name} : {e}")
```

### Exemple 4 : Validation de schéma

```python
def validate_schema(data, required_columns):
    """
    Valide que les colonnes requises sont présentes.
    """
    missing = set(required_columns) - set(data.headers)
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")
    return True

# Utilisation
parser = ParserFactory.get_parser('data.csv')
data = parser.parse('data.csv')

required = ['name', 'age', 'email']
if validate_schema(data, required):
    print("✓ Schéma valide")
```

### Exemple 5 : Statistiques sur les données

```python
from collections import Counter

parser = ParserFactory.get_parser('data.csv')
data = parser.parse('data.csv')

# Statistiques
print(f"Nombre total de lignes : {len(data)}")
print(f"Colonnes : {', '.join(data.headers)}")

# Compter les valeurs d'une colonne
if 'city' in data.headers:
    cities = [row['city'] for row in data.rows]
    city_counts = Counter(cities)
    print("\nRépartition par ville :")
    for city, count in city_counts.most_common():
        print(f"  {city}: {count}")
```

---

## ⚠️ Gestion des erreurs

### Erreurs courantes

#### 1. Fichier introuvable

```python
try:
    parser = ParserFactory.get_parser('missing.csv')
    data = parser.parse('missing.csv')
except FileNotFoundError as e:
    print(f"Erreur : {e}")
    # Proposer une alternative ou créer le fichier
```

#### 2. Format non supporté

```python
try:
    parser = ParserFactory.get_parser('data.xlsx')  # Excel non supporté
except UnsupportedFormatError as e:
    print(f"Format non supporté : {e}")
    print("Formats acceptés : .csv, .json, .xml")
```

#### 3. Encodage incorrect

```python
from project_parser.utils.file_validator import FileValidator

try:
    parser = ParserFactory.get_parser('data.csv')
    data = parser.parse('data.csv', encoding='utf-8')
except UnicodeDecodeError:
    # Détecter et réessayer avec le bon encodage
    encoding = FileValidator.detect_encoding('data.csv')
    data = parser.parse('data.csv', encoding=encoding)
```

#### 4. Fichier corrompu

```python
try:
    parser = ParserFactory.get_parser('corrupt.json')
    data = parser.parse('corrupt.json')
except InvalidFormatError as e:
    print(f"Fichier corrompu : {e}")
    # Logger l'erreur, notifier l'utilisateur
```

---

## ❓ FAQ

### Q1 : Quels formats sont supportés ?
**R :** CSV, JSON et XML. D'autres formats peuvent être ajoutés facilement.

### Q2 : Quelle est la taille maximale de fichier ?
**R :** Par défaut, pas de limite stricte, mais recommandé < 100 MB pour éviter les problèmes de mémoire.

### Q3 : Comment gérer les gros fichiers ?
**R :** Utilisez le parsing par chunks (à implémenter) ou traitez les fichiers par sections.

### Q4 : Les données sont-elles modifiées lors du parsing ?
**R :** Non, les données sont lues telles quelles. Les types sont préservés (sauf CSV où tout est string).

### Q5 : Puis-je parser des fichiers distants (HTTP) ?
**R :** Pas directement. Téléchargez d'abord le fichier localement avec `requests`.

### Q6 : Comment contribuer ou signaler un bug ?
**R :** Consultez [CONTRIBUTING.md](../CONTRIBUTING.md) et ouvrez une issue sur GitHub.

### Q7 : Y a-t-il une API REST ?
**R :** Pas actuellement, mais elle peut être ajoutée avec Flask/FastAPI.

### Q8 : Les logs peuvent-ils être désactivés ?
**R :** Oui, configurez le niveau de log à `CRITICAL` ou désactivez les handlers.

---

## 📚 Ressources supplémentaires

- [Architecture technique](architecture.md)
- [Référence API](api_reference.md)
- [README principal](../README.md)
- [Guide de contribution](../CONTRIBUTING.md)

---

## 🆘 Support

Pour toute question ou problème :

- 📖 Consultez d'abord cette documentation
- 🐛 Signalez un bug : [Issues GitHub](https://github.com/gonicolas12/projet-final-python/issues)
- 💬 Posez une question : [Discussions GitHub](https://github.com/gonicolas12/projet-final-python/discussions)

---

**Bon parsing ! 🚀**
