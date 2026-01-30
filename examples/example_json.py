"""
Exemple d'utilisation : Parsing JSON et conversion.

Ce script montre comment parser un JSON et le convertir en CSV.
"""
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from project_parser.converters.format_converter import FormatConverter
from project_parser.parsers.parser_factory import ParserFactory
from project_parser.utils.logger import CustomLogger

logger = CustomLogger.setup_logger(__name__, logging.INFO)


def main():
	"""Exemple de parsing JSON avec conversion."""

	logger.info("=== Exemple : Parsing JSON + Conversion ===")

	json_file = 'tests/fixtures/sample.json'
	outputs_dir = Path('outputs')
	outputs_dir.mkdir(parents=True, exist_ok=True)

	try:
		parser = ParserFactory.get_parser(json_file)
		data = parser.parse(json_file)

		print("\n📊 JSON parsé :")
		print(f"   Nombre d'éléments : {len(data)}")
		print(f"   Champs : {', '.join(data.headers)}")

		converter = FormatConverter(data)
		output_file = str(outputs_dir / 'output_from_json.csv')
		converter.to_csv(output_file)

		print(f"\n✅ Converti en CSV : {output_file}")

		logger.info("Parsing et conversion réussis")

	except Exception as e:
		logger.error(f"Erreur : {e}")
		raise


if __name__ == '__main__':
	main()
