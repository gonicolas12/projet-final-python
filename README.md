# 🔍 Project Parser - Outil de Parsing Multi-Format

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Description

**Project Parser** est un outil Python professionnel capable de parser et transformer des fichiers dans plusieurs formats (CSV, JSON, XML) vers une structure de données standardisée. Conçu avec une architecture modulaire, il intègre un système de logs complet et une gestion d'erreurs robuste.

## ✨ Fonctionnalités

- ✅ **Parsing multi-format** : Support natif de CSV, JSON et XML
- ✅ **Structure standardisée** : Conversion automatique vers un modèle de données unifié
- ✅ **Système de logs** : Traçabilité complète avec différents niveaux (DEBUG, INFO, WARNING, ERROR)
- ✅ **Gestion des erreurs** : Exceptions personnalisées et validation des fichiers
- ✅ **Extensible** : Architecture modulaire facilitant l'ajout de nouveaux formats
- ✅ **Conversion entre formats** : Possibilité de convertir d'un format à un autre
- ✅ **CLI intuitif** : Interface en ligne de commande simple

## 🏗️ Architecture

```
project_parser/
├── parsers/          # Parsers pour chaque format (CSV, JSON, XML)
├── models/           # Modèles de données standardisés
├── utils/            # Utilitaires (logger, validation, exceptions)
├── converters/       # Conversion entre formats
├── config/           # Configuration de l'application
└── main.py           # Point d'entrée
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation depuis le dépôt

```bash
# Cloner le dépôt
git clone https://github.com/gonicolas12/projet-final-python.git
cd projet-final-python

# Installer les dépendances
pip install -r requirements.txt

# Installation en mode développement
pip install -e .
```

## 📖 Utilisation

### Utilisation de base

```python
from project_parser.parsers.parser_factory import ParserFactory

# Parser un fichier CSV
parser = ParserFactory.get_parser('data.csv')
data = parser.parse('data.csv')

print(data.to_dict())
```

### Via la ligne de commande

```bash
# Parser un fichier
python -m project_parser.main parse data.csv

# Parser et convertir
python -m project_parser.main convert data.csv --output data.json

# Afficher l'aide
python -m project_parser.main --help
```

### Exemples avancés

Consultez le dossier `examples/` pour des cas d'usage détaillés :

- `example_csv.py` : Parsing de fichiers CSV
- `example_json.py` : Parsing de fichiers JSON
- `example_xml.py` : Parsing de fichiers XML

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/

# Tests avec couverture
pytest --cov=project_parser tests/

# Tests d'un module spécifique
pytest tests/test_csv_parser.py
```

## 📝 Logs

Les logs sont automatiquement générés dans le dossier `logs/` :

- **Console** : WARNING et supérieur
- **Fichier** : INFO et supérieur (`logs/app.log`)

Format : `[2026-01-30 10:30:45] [INFO] [module] - Message`

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

### Processus de contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'feat: add amazing feature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Documentation

- [Architecture](docs/architecture.md) : Documentation technique détaillée
- [Guide d'utilisation](docs/usage.md) : Exemples et cas d'usage
- [Référence API](docs/api_reference.md) : Documentation complète de l'API

## 🐛 Signaler un bug

Ouvrez une issue sur GitHub en incluant :

- Description du problème
- Étapes pour reproduire
- Comportement attendu vs observé
- Version de Python et de l'OS

## 📜 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **Équipe Projet Final Python** - [YNOV](https://www.ynov.com/)

## 🙏 Remerciements

- Enseignants du cours Python Avancé
- Communauté Python pour les outils et bibliothèques
- Contributors du projet

## 📞 Contact

Pour toute question : [Créer une issue](https://github.com/gonicolas12/projet-final-python/issues)

---

⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !
