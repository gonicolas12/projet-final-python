"""
Configuration globale de l'application.
"""
from pathlib import Path


class Settings:
    """
    Paramètres globaux de l'application.
    
    Contient les constantes et configurations utilisées partout dans le projet.
    """
    
    # Chemins
    BASE_DIR = Path(__file__).parent.parent
    LOGS_DIR = BASE_DIR.parent / 'logs'
    
    # Configuration des logs
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s'
    LOG_FILE = LOGS_DIR / 'app.log'
    
    # Configuration du parsing
    DEFAULT_ENCODING = 'utf-8'
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
    
    # Formats supportés
    SUPPORTED_FORMATS = ['.csv', '.json', '.xml']
    
    # Délimiteurs CSV par défaut
    DEFAULT_CSV_DELIMITER = ','
    DEFAULT_CSV_QUOTECHAR = '"'
