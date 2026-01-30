"""
Project Parser - Outil de parsing multi-format (CSV, JSON, XML).

Un parser modulaire et extensible pour lire et convertir des fichiers
dans différents formats.
"""

__version__ = '0.1.0'
__author__ = 'Nicolas GOUY, Josué ADAMI, Alexis REDAUD'

# Imports principaux pour faciliter l'utilisation
from project_parser.parsers.parser_factory import ParserFactory
from project_parser.models.data_model import StandardData
from project_parser.converters.format_converter import FormatConverter

__all__ = [
	'ParserFactory',
	'StandardData',
	'FormatConverter',
]
