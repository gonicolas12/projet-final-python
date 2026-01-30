"""
Point d'entrée CLI pour Project Parser.

Commandes disponibles :
	- parse : Parser un fichier et afficher les résultats
	- convert : Convertir un fichier vers un autre format
	- info : Afficher les informations d'un fichier
"""
import argparse
import logging
import sys
from pathlib import Path

from project_parser import __version__
from project_parser.converters.format_converter import FormatConverter
from project_parser.parsers.parser_factory import ParserFactory
from project_parser.utils.exceptions import ParserException
from project_parser.utils.logger import CustomLogger


def setup_argparse() -> argparse.ArgumentParser:
	"""Configure et retourne le parser d'arguments."""

	parser = argparse.ArgumentParser(
		prog='project-parser',
		description='Outil de parsing multi-format (CSV, JSON, XML)',
		formatter_class=argparse.RawDescriptionHelpFormatter
	)

	parser.add_argument(
		'--version',
		action='version',
		version=f'%(prog)s {__version__}'
	)

	parser.add_argument(
		'--verbose', '-v',
		action='store_true',
		help='Mode verbeux (logs DEBUG)'
	)

	parser.add_argument(
		'--quiet', '-q',
		action='store_true',
		help='Mode silencieux (logs ERROR uniquement)'
	)

	subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')

	parse_parser = subparsers.add_parser('parse', help='Parser un fichier')
	parse_parser.add_argument('file', help='Chemin du fichier à parser')
	parse_parser.add_argument(
		'--show-all',
		action='store_true',
		help='Afficher toutes les lignes (pas seulement les 5 premières)'
	)

	convert_parser = subparsers.add_parser('convert', help='Convertir un fichier')
	convert_parser.add_argument('file', help='Fichier source')
	convert_parser.add_argument(
		'--output', '-o',
		required=True,
		help='Fichier de sortie (.csv, .json ou .xml)'
	)

	info_parser = subparsers.add_parser('info', help='Infos sur un fichier')
	info_parser.add_argument('file', help='Fichier à analyser')

	return parser


def command_parse(args, logger):
	"""Commande parse : parser et afficher les résultats."""

	logger.info(f"Parsing de {args.file}")

	parser = ParserFactory.get_parser(args.file)
	data = parser.parse(args.file)

	print("\n✅ Parsing réussi !")
	print(f"   Fichier : {args.file}")
	print(f"   Format : {data.metadata.get('format', 'unknown')}")
	print(f"   Colonnes : {', '.join(data.headers)}")
	print(f"   Lignes : {len(data)}")

	limit = None if args.show_all else 5
	print(f"\n📝 Aperçu des données (premières {limit or 'toutes les'} lignes) :")

	for i, row in enumerate(data[:limit]):
		print(f"\n   Ligne {i + 1}:")
		for key, value in row.items():
			print(f"     {key}: {value}")

	if len(data) > 5 and not args.show_all:
		print(f"\n   ... et {len(data) - 5} autres lignes")
		print("   (utilisez --show-all pour tout afficher)")


def command_convert(args, logger):
	"""Commande convert : convertir vers un autre format."""

	logger.info(f"Conversion de {args.file} vers {args.output}")

	parser = ParserFactory.get_parser(args.file)
	data = parser.parse(args.file)

	converter = FormatConverter(data)
	output_ext = Path(args.output).suffix.lower()

	if output_ext == '.csv':
		converter.to_csv(args.output)
	elif output_ext == '.json':
		converter.to_json(args.output)
	elif output_ext == '.xml':
		converter.to_xml(args.output)
	else:
		raise ValueError(f"Format de sortie non supporté : {output_ext}")

	print("\n✅ Conversion réussie !")
	print(f"   Source : {args.file} ({len(data)} lignes)")
	print(f"   Destination : {args.output}")


def command_info(args, logger):
	"""Commande info : afficher les informations."""

	from project_parser.utils.file_validator import FileValidator

	logger.info(f"Informations sur {args.file}")

	if not FileValidator.exists(args.file):
		print(f"❌ Fichier introuvable : {args.file}")
		sys.exit(1)

	size = FileValidator.get_size(args.file)
	encoding = FileValidator.detect_encoding(args.file)
	ext = Path(args.file).suffix

	print("\n📋 Informations sur le fichier :")
	print(f"   Chemin : {args.file}")
	print(f"   Extension : {ext}")
	print(f"   Taille : {size / 1024:.2f} KB")
	print(f"   Encodage détecté : {encoding}")
	print(f"   Lisible : {'✅ Oui' if FileValidator.is_readable(args.file) else '❌ Non'}")

	try:
		parser = ParserFactory.get_parser(args.file)
		data = parser.parse(args.file)

		print("\n📊 Contenu :")
		print(f"   Colonnes : {len(data.headers)}")
		print(f"   Lignes : {len(data)}")
		print(f"   Champs : {', '.join(data.headers)}")
	except Exception as e:
		print(f"\n⚠️  Impossible de parser : {e}")


def main():
	"""Point d'entrée principal."""

	parser = setup_argparse()
	args = parser.parse_args()

	if args.verbose:
		log_level = logging.DEBUG
	elif args.quiet:
		log_level = logging.ERROR
	else:
		log_level = logging.INFO

	logger = CustomLogger.setup_logger('main', log_level)

	if not args.command:
		parser.print_help()
		sys.exit(0)

	try:
		if args.command == 'parse':
			command_parse(args, logger)
		elif args.command == 'convert':
			command_convert(args, logger)
		elif args.command == 'info':
			command_info(args, logger)

	except ParserException as e:
		logger.error(f"Erreur de parsing : {e}")
		print(f"\n❌ Erreur : {e}")
		sys.exit(1)
	except Exception as e:
		logger.critical(f"Erreur inattendue : {e}", exc_info=True)
		print(f"\n❌ Erreur inattendue : {e}")
		if args.verbose:
			raise
		sys.exit(99)


if __name__ == '__main__':
	main()
