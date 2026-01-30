"""
Exemple d'utilisation : Parsing CSV.

Ce script montre comment parser un fichier CSV avec différentes options.
"""
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from project_parser.converters.format_converter import FormatConverter
from project_parser.parsers.parser_factory import ParserFactory
from project_parser.utils.logger import CustomLogger

# Configuration du logger
logger = CustomLogger.setup_logger(__name__, logging.INFO)


def main():
	"""Exemple de parsing CSV."""

	logger.info("=== Exemple : Parsing CSV ===")

	csv_file = 'tests/fixtures/sample.csv'
	outputs_dir = Path('outputs')
	outputs_dir.mkdir(parents=True, exist_ok=True)

	try:
		parser = ParserFactory.get_parser(csv_file)
		logger.info(f"Parser créé : {parser.__class__.__name__}")

		data = parser.parse(csv_file)

		print("\n📊 Résultats du parsing :")
		print(f"   Colonnes : {', '.join(data.headers)}")
		print(f"   Nombre de lignes : {len(data)}")
		print("\n📝 Premières lignes :")

		for i, row in enumerate(data[:3]):
			print(f"\n   Ligne {i + 1}:")
			for key, value in row.items():
				print(f"     - {key}: {value}")

		print("\n🔍 Métadonnées :")
		for key, value in data.metadata.items():
			print(f"   - {key}: {value}")

		converter = FormatConverter(data)
		output_file = str(outputs_dir / 'output_from_csv.xml')
		converter.to_xml(output_file)
		print(f"\n✅ Export XML : {output_file}")

		logger.info("Parsing CSV terminé avec succès")

	except Exception as e:
		logger.error(f"Erreur lors du parsing : {e}")
		raise


if __name__ == '__main__':
	main()
