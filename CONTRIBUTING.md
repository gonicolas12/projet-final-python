# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à **Project Parser** ! Ce document vous guidera à travers le processus de contribution.

## 📋 Table des matières

1. [Code de conduite](#code-de-conduite)
2. [Comment contribuer](#comment-contribuer)
3. [Convention de commits](#convention-de-commits)
4. [Standards de code](#standards-de-code)
5. [Processus de Pull Request](#processus-de-pull-request)
6. [Structure des branches](#structure-des-branches)

---

## 🛡️ Code de conduite

En participant à ce projet, vous vous engagez à :

- Être respectueux et inclusif
- Accepter les critiques constructives
- Collaborer de manière professionnelle
- Prioriser l'intérêt du projet

---

## 🚀 Comment contribuer

### 1. Fork et Clone

```bash
# Fork le projet sur GitHub, puis :
git clone https://github.com/VOTRE_USERNAME/projet-final-python.git
cd projet-final-python
```

### 2. Configurer l'environnement

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Créer une branche

```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

### 4. Développer

- Écrivez du code propre et documenté
- Ajoutez des tests pour vos fonctionnalités
- Suivez les standards PEP8
- Testez localement avant de commit

### 5. Commit

```bash
git add .
git commit -m "feat: ajouter le parser YAML"
```

### 6. Push et Pull Request

```bash
git push origin feature/ma-nouvelle-fonctionnalite
```

Puis créez une Pull Request sur GitHub.

---

## 📝 Convention de Commits

Nous suivons la spécification [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <description>

[corps optionnel]

[footer optionnel]
```

### Types de commits

| Type | Description | Exemple |
|------|-------------|----------|
| `feat` | Nouvelle fonctionnalité | `feat: ajouter parser YAML` |
| `fix` | Correction de bug | `fix: corriger encoding UTF-8` |
| `docs` | Documentation | `docs: mettre à jour le README` |
| `style` | Formatage, PEP8 | `style: formater avec black` |
| `refactor` | Refactoring | `refactor: optimiser CSVParser` |
| `test` | Ajout/modification tests | `test: ajouter tests XML parser` |
| `chore` | Maintenance | `chore: mettre à jour dépendances` |
| `perf` | Performance | `perf: optimiser parsing JSON` |
| `ci` | Intégration continue | `ci: ajouter GitHub Actions` |

### Exemples de bons commits

```bash
# Feature
git commit -m "feat(parsers): ajouter support du format YAML"

# Bug fix
git commit -m "fix(csv): corriger gestion des guillemets doubles"

# Documentation
git commit -m "docs: ajouter exemples d'utilisation avancée"

# Tests
git commit -m "test(json): ajouter tests pour objets imbriqués"

# Refactoring
git commit -m "refactor(logger): extraire configuration dans settings"
```

### ❌ Mauvais exemples

```bash
# Trop vague
git commit -m "fix bug"
git commit -m "update"

# Pas de type
git commit -m "ajouter une fonction"

# Trop long
git commit -m "feat: ajouter une nouvelle fonctionnalité super cool qui permet de faire plein de choses"
```

---

## 🎨 Standards de Code

### PEP8

Tout le code doit respecter [PEP8](https://peps.python.org/pep-0008/).

```bash
# Vérifier avec flake8
flake8 project_parser/

# Formatter avec black
black project_parser/
```

### Docstrings

Utilisez le format Google/NumPy :

```python
def parse_file(file_path: str, encoding: str = 'utf-8') -> dict:
    """
    Parse un fichier et retourne une structure de données.
    
    Args:
        file_path (str): Chemin vers le fichier à parser
        encoding (str, optional): Encodage du fichier. Défaut: 'utf-8'
    
    Returns:
        dict: Données parsées sous forme de dictionnaire
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        InvalidFormatError: Si le format est invalide
    
    Example:
        >>> data = parse_file('data.csv')
        >>> print(data['rows'][0])
        {'name': 'John', 'age': 30}
    """
    pass
```

### Type Hints

Utilisez les annotations de type :

```python
from typing import List, Dict, Optional

def process_data(rows: List[Dict[str, str]], limit: Optional[int] = None) -> List[Dict]:
    pass
```

### Gestion des erreurs

```python
# Utilisez les exceptions personnalisées
from project_parser.utils.exceptions import InvalidFormatError

if not is_valid_format(file):
    logger.error(f"Format invalide: {file}")
    raise InvalidFormatError(f"Le fichier {file} n'est pas au bon format")
```

---

## 🔀 Structure des Branches

### Branches principales

- `main` : Code en production, stable
- `develop` : Branche de développement (intégration)

### Branches de travail

| Préfixe | Usage | Exemple |
|---------|-------|----------|
| `feature/` | Nouvelle fonctionnalité | `feature/yaml-parser` |
| `fix/` | Correction de bug | `fix/csv-encoding` |
| `docs/` | Documentation | `docs/api-reference` |
| `refactor/` | Refactoring | `refactor/logger-module` |
| `test/` | Tests | `test/xml-parser` |
| `chore/` | Maintenance | `chore/update-deps` |

### Workflow

```bash
# Créer une feature depuis develop
git checkout develop
git pull origin develop
git checkout -b feature/ma-feature

# Développer et commit
git add .
git commit -m "feat: ma fonctionnalité"

# Push
git push origin feature/ma-feature

# Créer une Pull Request vers develop
```

---

## 🔍 Processus de Pull Request

### Checklist avant PR

- [ ] Le code respecte PEP8 (`flake8 project_parser/`)
- [ ] Le code est formaté avec black (`black project_parser/`)
- [ ] Les tests passent (`pytest tests/`)
- [ ] Les nouveaux tests sont ajoutés pour les nouvelles fonctionnalités
- [ ] La documentation est à jour
- [ ] Les docstrings sont présentes et complètes
- [ ] Les commits suivent la convention
- [ ] Pas de fichiers inutiles (cache, IDE, logs)

### Template de Pull Request

```markdown
## Description
Brève description des changements

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Tests
Description des tests ajoutés

## Checklist
- [ ] Code conforme PEP8
- [ ] Tests passent
- [ ] Documentation mise à jour
```

### Review

- Au moins **1 approbation** requise
- Les commentaires doivent être adressés
- Les conflicts doivent être résolus
- Les tests CI doivent passer

---

## 🧪 Tests

### Écrire des tests

```python
import pytest
from project_parser.parsers.csv_parser import CSVParser

def test_csv_parser_basic():
    """Test parsing d'un CSV simple."""
    parser = CSVParser()
    data = parser.parse('tests/fixtures/sample.csv')
    
    assert len(data.rows) > 0
    assert 'name' in data.headers

def test_csv_parser_invalid_file():
    """Test erreur si fichier invalide."""
    parser = CSVParser()
    
    with pytest.raises(FileNotFoundError):
        parser.parse('nonexistent.csv')
```

### Lancer les tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=project_parser

# Mode verbose
pytest -v

# Test spécifique
pytest tests/test_csv_parser.py::test_csv_parser_basic
```

---

## 📞 Questions ?

N'hésitez pas à :

- Ouvrir une [issue](https://github.com/gonicolas12/projet-final-python/issues) pour poser une question
- Consulter la [documentation](docs/)
- Contacter l'équipe via GitHub

---

**Merci de contribuer à Project Parser ! 🎉**
