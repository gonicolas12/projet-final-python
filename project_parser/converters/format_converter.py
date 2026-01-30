"""
Conversion de StandardData vers différents formats.
"""
import csv
import json
import xml.etree.ElementTree as ET

from project_parser.models.data_model import StandardData
from project_parser.utils.logger import CustomLogger

logger = CustomLogger.setup_logger(__name__)


class FormatConverter:
	"""
	Convertisseur pour exporter StandardData vers différents formats.

	Attributes:
		data (StandardData): Données à convertir

	Example:
		>>> data = StandardData(...)
		>>> converter = FormatConverter(data)
		>>> converter.to_json('output.json')
	"""

	def __init__(self, data: StandardData):
		"""
		Initialise le convertisseur.

		Args:
			data (StandardData): Données à convertir
		"""
		self.data = data
		logger.info(f"Convertisseur initialisé avec {len(data)} lignes")

	def to_csv(
		self,
		output_path: str,
		delimiter: str = ',',
		encoding: str = 'utf-8'
	) -> None:
		"""
		Exporte vers CSV.

		Args:
			output_path (str): Chemin du fichier de sortie
			delimiter (str, optional): Séparateur. Défaut: ','
			encoding (str, optional): Encodage. Défaut: 'utf-8'

		Example:
			>>> converter.to_csv('output.csv', delimiter=';')
		"""
		logger.info(f"Export CSV vers {output_path}")

		with open(output_path, 'w', newline='', encoding=encoding) as f:
			writer = csv.DictWriter(f, fieldnames=self.data.headers, delimiter=delimiter)
			writer.writeheader()
			writer.writerows(self.data.rows)

		logger.info(f"Export CSV réussi : {len(self.data)} lignes écrites")

	def to_json(
		self,
		output_path: str,
		indent: int = 2,
		encoding: str = 'utf-8'
	) -> None:
		"""
		Exporte vers JSON.

		Args:
			output_path (str): Chemin du fichier de sortie
			indent (int, optional): Indentation. Défaut: 2
			encoding (str, optional): Encodage. Défaut: 'utf-8'

		Example:
			>>> converter.to_json('output.json', indent=4)
		"""
		logger.info(f"Export JSON vers {output_path}")

		with open(output_path, 'w', encoding=encoding) as f:
			json.dump(self.data.rows, f, indent=indent, ensure_ascii=False)

		logger.info(f"Export JSON réussi : {len(self.data)} éléments écrits")

	def to_xml(
		self,
		output_path: str,
		root_tag: str = 'data',
		row_tag: str = 'record',
		encoding: str = 'utf-8'
	) -> None:
		"""
		Exporte vers XML.

		Args:
			output_path (str): Chemin du fichier de sortie
			root_tag (str, optional): Tag racine. Défaut: 'data'
			row_tag (str, optional): Tag pour chaque ligne. Défaut: 'record'
			encoding (str, optional): Encodage. Défaut: 'utf-8'

		Example:
			>>> converter.to_xml('output.xml', root_tag='employees', row_tag='employee')
		"""
		logger.info(f"Export XML vers {output_path}")

		root = ET.Element(root_tag)

		for row in self.data.rows:
			record = ET.SubElement(root, row_tag)
			for key, value in row.items():
				child = ET.SubElement(record, key)
				child.text = str(value)

		tree = ET.ElementTree(root)
		ET.indent(tree, space="    ")
		tree.write(output_path, encoding=encoding, xml_declaration=True)

		logger.info(f"Export XML réussi : {len(self.data)} éléments écrits")
