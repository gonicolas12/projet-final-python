"""
Configuration et gestion des logs.
"""
import logging
from pathlib import Path


class CustomLogger:
    """
    Gestionnaire de logs centralisé.
    
    Configure automatiquement les handlers pour console et fichier.
    """
    
    @staticmethod
    def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """
        Configure et retourne un logger.
        
        Args:
            name (str): Nom du logger (généralement __name__)
            level (int, optional): Niveau de log. Défaut: INFO
        
        Returns:
            logging.Logger: Logger configuré
        
        Example:
            >>> logger = CustomLogger.setup_logger('my_module')
            >>> logger.info("Message d'information")
        """
        logger = logging.getLogger(name)
        
        # Éviter les doublons si déjà configuré
        if logger.handlers:
            return logger
            
        logger.setLevel(level)
        
        # S'assurer que le dossier logs existe
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Handler fichier : INFO et au-dessus
        file_handler = logging.FileHandler('logs/app.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Handler console : WARNING et au-dessus
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Format des logs
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Ajouter les handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
