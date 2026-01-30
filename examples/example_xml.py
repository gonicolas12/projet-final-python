"""
Exemple d'utilisation : Parsing XML avec filtrage.

Ce script montre comment parser un XML, filtrer les données et convertir.
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
	"""Exemple de parsing XML avec filtrage."""

	logger.info("=== Exemple : Parsing XML + Filtrage ===")

	xml_file = 'tests/fixtures/sample.xml'
	outputs_dir = Path('outputs')
	outputs_dir.mkdir(parents=True, exist_ok=True)

	try:
		parser = ParserFactory.get_parser(xml_file)
		data = parser.parse(xml_file)

		print(f"\n📊 XML parsé : {len(data)} éléments")

		filtered_rows = [
			row for row in data.rows
			if int(row.get('age', 0)) > 30
		]

		print(f"\n🔍 Filtrage : {len(filtered_rows)} personnes de plus de 30 ans")
		for row in filtered_rows:
			print(f"   - {row['name']}, {row['age']} ans, {row['city']}")

		from project_parser.models.data_model import StandardData
		filtered_data = StandardData(
			headers=data.headers,
			rows=filtered_rows,
			metadata={'source': 'filtered', 'filter': 'age > 30'}
		)

		converter = FormatConverter(filtered_data)
		output_file = str(outputs_dir / 'output_filtered.json')
		converter.to_json(output_file)

		print(f"\n✅ Données filtrées exportées : {output_file}")

		logger.info("Parsing, filtrage et conversion réussis")

	except Exception as e:
		logger.error(f"Erreur : {e}")
		raise


if __name__ == '__main__':
	main()
