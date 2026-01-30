# 📋 Répartition du Travail - Projet Parser

## 👥 Équipe
- **Nicolas GOUY** : Parsers & Tests
- **Josué ADAMI** : Models, Utils & Config
- **Alexis REDAUD** : CLI, Converters & Examples

---

## 🔵 Partie 1 : Parsers & Factory (Branche: `feature/parsers-implementation`)

### Fichiers à implémenter (9 fichiers)

#### 1. `project_parser/parsers/base_parser.py`
**Description** : Classe abstraite de base pour tous les parsers
- Définir les méthodes abstraites `parse()` et `validate()`
- Implémenter `_read_file()` (méthode commune)
- Documenter avec docstrings

#### 2. `project_parser/parsers/csv_parser.py`
**Description** : Parser pour fichiers CSV
- Hériter de `BaseParser`
- Utiliser `csv.DictReader`
- Gérer les délimiteurs, encodages
- Retourner un objet `StandardData`

#### 3. `project_parser/parsers/json_parser.py`
**Description** : Parser pour fichiers JSON
- Hériter de `BaseParser`
- Utiliser `json.load()`
- Gérer les tableaux et objets JSON
- Retourner un objet `StandardData`

#### 4. `project_parser/parsers/xml_parser.py`
**Description** : Parser pour fichiers XML
- Hériter de `BaseParser`
- Utiliser `xml.etree.ElementTree`
- Parser la structure XML en dictionnaires
- Retourner un objet `StandardData`

#### 5. `project_parser/parsers/parser_factory.py`
**Description** : Factory pour instancier les parsers
- Méthode `get_parser(file_path)` qui détecte l'extension
- Dictionnaire `_parsers` avec mapping extension → classe
- Lever `UnsupportedFormatError` si format non supporté

#### 6. `project_parser/parsers/__init__.py`
**Description** : Exports du module parsers
- Exporter toutes les classes de parsers

#### 7-10. Tests
- `tests/test_csv_parser.py` : Tests unitaires CSV
- `tests/test_json_parser.py` : Tests unitaires JSON
- `tests/test_xml_parser.py` : Tests unitaires XML
- `tests/test_parser_factory.py` : Tests de la factory

**Tests à implémenter** :
- Test parsing réussi
- Test fichier introuvable
- Test format invalide
- Test encodage
- Utiliser les fixtures dans `tests/fixtures/`

### Dépendances
- Attendre `StandardData` de la Partie 2
- Attendre exceptions de la Partie 2

### Commit suggestions
```bash
feat(parsers): implement BaseParser abstract class
feat(parsers): add CSVParser implementation
feat(parsers): add JSONParser implementation
feat(parsers): add XMLParser implementation
feat(parsers): add ParserFactory with format detection
test(parsers): add unit tests for all parsers
```

---

## 🟢 Partie 2 : Models, Utils & Config (Branche: `feature/utils-models-config`)

### Fichiers à implémenter (8 fichiers)

#### 1. `project_parser/models/data_model.py`
**Description** : Modèle de données standardisé
- Classe `StandardData` avec dataclass
- Attributs : `headers`, `rows`, `metadata`
- Méthodes : `to_dict()`, `__len__()`, `__getitem__()`, `__iter__()`
- Auto-initialisation des métadonnées (`parsed_at`)

#### 2. `project_parser/models/__init__.py`
**Description** : Exports du module models
- Exporter `StandardData`

#### 3. `project_parser/utils/exceptions.py`
**Description** : Exceptions personnalisées
- `ParserException` (classe de base)
- `FileNotFoundError`
- `InvalidFormatError`
- `EncodingError`
- `ValidationError`
- `UnsupportedFormatError`

#### 4. `project_parser/utils/logger.py`
**Description** : Configuration des logs
- Classe `CustomLogger`
- Méthode statique `setup_logger(name, level)`
- Configuration FileHandler (logs/app.log)
- Configuration StreamHandler (console)
- Format : `[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s`

#### 5. `project_parser/utils/file_validator.py`
**Description** : Validation des fichiers
- Classe `FileValidator`
- Méthodes statiques :
  - `exists(file_path)` : vérifier existence
  - `is_readable(file_path)` : vérifier permissions
  - `get_size(file_path)` : taille en octets
  - `detect_encoding(file_path)` : détection encodage

#### 6. `project_parser/utils/__init__.py`
**Description** : Exports du module utils
- Exporter toutes les classes utilitaires

#### 7. `project_parser/config/settings.py`
**Description** : Configuration de l'application
- Classe `Settings` avec constantes
- Chemins (BASE_DIR, LOGS_DIR)
- Configuration logs (LOG_LEVEL, LOG_FORMAT)
- Configuration parsing (DEFAULT_ENCODING, MAX_FILE_SIZE)
- Formats supportés (SUPPORTED_FORMATS)

#### 8. `project_parser/config/__init__.py`
**Description** : Exports du module config
- Exporter `Settings`

#### 9. `setup.py`
**Description** : Configuration pour l'installation du package
- Utiliser `setuptools`
- Définir name, version, packages, install_requires
- Entry point pour la CLI

### Commit suggestions
```bash
feat(models): implement StandardData model
feat(utils): add custom exceptions hierarchy
feat(utils): implement logger configuration
feat(utils): add file validator utilities
feat(config): add application settings
chore: add setup.py for package installation
```

---

## 🟡 Partie 3 : CLI, Converters & Examples (Branche: `feature/cli-converters-examples`)

### Fichiers à implémenter (6 fichiers)

#### 1. `project_parser/main.py`
**Description** : Point d'entrée CLI
- Utiliser `argparse` pour les arguments
- Commandes : `parse`, `convert`, `info`, `stats`
- Options : `--verbose`, `--quiet`, `--output`
- Gestion des erreurs avec try/except
- Logs appropriés pour chaque opération
- Exemple de structure :
  ```python
  def main():
      parser = argparse.ArgumentParser()
      subparsers = parser.add_subparsers()
      
      # Commande parse
      parse_cmd = subparsers.add_parser('parse')
      parse_cmd.add_argument('file')
      
      # Commande convert
      convert_cmd = subparsers.add_parser('convert')
      convert_cmd.add_argument('file')
      convert_cmd.add_argument('--output')
  ```

#### 2. `project_parser/__init__.py`
**Description** : Initialisation du package principal
- Définir `__version__`
- Imports principaux

#### 3. `project_parser/converters/format_converter.py`
**Description** : Conversion entre formats
- Classe `FormatConverter`
- Constructeur prend un `StandardData`
- Méthodes :
  - `to_csv(output_path, delimiter, encoding)`
  - `to_json(output_path, indent, encoding)`
  - `to_xml(output_path, root_tag, row_tag, encoding)`
- Utiliser les modules standard (csv, json, xml)

#### 4. `project_parser/converters/__init__.py`
**Description** : Exports du module converters
- Exporter `FormatConverter`

#### 5. `examples/example_csv.py`
**Description** : Exemple d'utilisation pour CSV
- Parser un fichier CSV
- Afficher les résultats
- Montrer les options (delimiter, encoding)
- Commentaires explicatifs

#### 6. `examples/example_json.py`
**Description** : Exemple d'utilisation pour JSON
- Parser un fichier JSON
- Conversion vers CSV
- Commentaires explicatifs

#### 7. `examples/example_xml.py`
**Description** : Exemple d'utilisation pour XML
- Parser un fichier XML
- Filtrage des données
- Conversion vers JSON
- Commentaires explicatifs

### Dépendances
- Attendre tous les parsers de la Partie 1
- Attendre `StandardData` de la Partie 2
- Attendre exceptions et logger de la Partie 2

### Commit suggestions
```bash
feat(cli): implement main CLI with argparse
feat(converters): add FormatConverter for multi-format export
docs(examples): add CSV parsing example
docs(examples): add JSON parsing example
docs(examples): add XML parsing example
```

---

## 📊 Estimation de charge

| Partie | Fichiers | Complexité | Temps estimé |
|--------|----------|------------|--------------|
| Partie 1 (Parsers) | 9 | Moyenne-Haute | ~4-6h |
| Partie 2 (Utils) | 8 | Moyenne | ~4-5h |
| Partie 3 (CLI) | 6 | Moyenne | ~4-5h |

---

## 🔄 Workflow Git

### Créer et travailler sur sa branche

```bash
# Personne 1
git checkout -b feature/parsers-implementation
# ... coder ...
git add .
git commit -m "feat(parsers): implement BaseParser abstract class"
git push origin feature/parsers-implementation

# Personne 2
git checkout -b feature/utils-models-config
# ... coder ...
git add .
git commit -m "feat(models): implement StandardData model"
git push origin feature/utils-models-config

# Personne 3
git checkout -b feature/cli-converters-examples
# ... coder ...
git add .
git commit -m "feat(cli): implement main CLI with argparse"
git push origin feature/cli-converters-examples
```

### Ordre de merge recommandé

1. **D'abord Partie 2** (Models & Utils) → car dépendances pour les autres
2. **Ensuite Partie 1** (Parsers) → dépend de Partie 2
3. **Enfin Partie 3** (CLI) → dépend de Parties 1 & 2

---

## ✅ Checklist par partie

### Partie 1 - Parsers
- [ ] BaseParser implémenté avec ABC
- [ ] CSVParser fonctionnel avec tests
- [ ] JSONParser fonctionnel avec tests
- [ ] XMLParser fonctionnel avec tests
- [ ] ParserFactory avec détection automatique
- [ ] Tous les tests passent (pytest)
- [ ] Code respecte PEP8 (flake8)
- [ ] Docstrings présentes

### Partie 2 - Utils & Models
- [ ] StandardData avec toutes les méthodes
- [ ] Exceptions personnalisées définies
- [ ] Logger configuré et testé
- [ ] FileValidator fonctionnel
- [ ] Settings complètes
- [ ] setup.py fonctionnel
- [ ] Code respecte PEP8

### Partie 3 - CLI & Converters
- [ ] CLI fonctionnel avec toutes les commandes
- [ ] FormatConverter avec export CSV/JSON/XML
- [ ] Exemples fonctionnels et documentés
- [ ] Gestion d'erreurs dans le CLI
- [ ] Logs appropriés
- [ ] Code respecte PEP8

---

## 🤝 Communication

- **Bloquer ?** Créer une issue GitHub
- **Question ?** Discussions GitHub ou message direct
- **Conflit ?** Communiquer avant de merger

---

## 🎯 Objectif final

Une fois les 3 parties mergées dans `main`, le projet doit :
- ✅ Parser CSV, JSON, XML
- ✅ Convertir entre formats
- ✅ CLI fonctionnel
- ✅ Logs présents
- ✅ Tests passent
- ✅ Documentation complète

**Bon courage à toute l'équipe ! 🚀**
