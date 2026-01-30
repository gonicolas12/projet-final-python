"""
Tests unitaires pour ParserFactory.
"""
import pytest

from project_parser.parsers.parser_factory import ParserFactory
from project_parser.parsers.csv_parser import CSVParser
from project_parser.parsers.json_parser import JSONParser
from project_parser.parsers.xml_parser import XMLParser
from project_parser.parsers.base_parser import BaseParser
from project_parser.utils.exceptions import UnsupportedFormatError


class TestParserFactory:
    """Tests pour la factory de parsers."""
    
    def test_get_parser_for_csv(self):
        """Test création d'un CSVParser."""
        parser = ParserFactory.get_parser('test.csv')
        
        assert isinstance(parser, CSVParser)
        assert isinstance(parser, BaseParser)
    
    def test_get_parser_for_json(self):
        """Test création d'un JSONParser."""
        parser = ParserFactory.get_parser('test.json')
        
        assert isinstance(parser, JSONParser)
        assert isinstance(parser, BaseParser)
    
    def test_get_parser_for_xml(self):
        """Test création d'un XMLParser."""
        parser = ParserFactory.get_parser('test.xml')
        
        assert isinstance(parser, XMLParser)
        assert isinstance(parser, BaseParser)
    
    def test_get_parser_case_insensitive(self):
        """Test que l'extension est insensible à la casse."""
        parser_upper = ParserFactory.get_parser('test.CSV')
        parser_lower = ParserFactory.get_parser('test.csv')
        parser_mixed = ParserFactory.get_parser('test.CsV')
        
        assert isinstance(parser_upper, CSVParser)
        assert isinstance(parser_lower, CSVParser)
        assert isinstance(parser_mixed, CSVParser)
    
    def test_get_parser_with_path(self):
        """Test avec un chemin complet."""
        parser = ParserFactory.get_parser('path/to/file.json')
        
        assert isinstance(parser, JSONParser)
    
    def test_get_parser_unsupported_format(self):
        """Test format non supporté."""
        with pytest.raises(UnsupportedFormatError) as exc_info:
            ParserFactory.get_parser('test.txt')
        
        assert '.txt' in str(exc_info.value)
        assert 'non supporté' in str(exc_info.value).lower()
    
    def test_get_parser_no_extension(self):
        """Test fichier sans extension."""
        with pytest.raises(UnsupportedFormatError):
            ParserFactory.get_parser('test')
    
    def test_get_supported_formats(self):
        """Test récupération des formats supportés."""
        formats = ParserFactory.get_supported_formats()
        
        assert '.csv' in formats
        assert '.json' in formats
        assert '.xml' in formats
        assert len(formats) == 3
    
    def test_register_new_parser(self):
        """Test enregistrement d'un nouveau parser."""
        # Créer un faux parser pour le test
        class FakeParser(BaseParser):
            def parse(self, file_path, **kwargs):
                pass
            def validate(self, file_path):
                return True
        
        # Enregistrer
        ParserFactory.register_parser('.fake', FakeParser)
        
        # Vérifier
        assert '.fake' in ParserFactory.get_supported_formats()
        parser = ParserFactory.get_parser('test.fake')
        assert isinstance(parser, FakeParser)
        
        # Nettoyer (pour ne pas affecter les autres tests)
        ParserFactory._parsers.pop('.fake', None)
    
    def test_register_parser_without_dot(self):
        """Test enregistrement sans point dans l'extension."""
        class FakeParser(BaseParser):
            def parse(self, file_path, **kwargs):
                pass
            def validate(self, file_path):
                return True
        
        # Enregistrer sans point
        ParserFactory.register_parser('fake2', FakeParser)
        
        # Vérifier que le point est ajouté automatiquement
        assert '.fake2' in ParserFactory.get_supported_formats()
        
        # Nettoyer
        ParserFactory._parsers.pop('.fake2', None)
    
    def test_parser_instances_are_independent(self):
        """Test que chaque appel crée une nouvelle instance."""
        parser1 = ParserFactory.get_parser('test.csv')
        parser2 = ParserFactory.get_parser('test.csv')
        
        assert parser1 is not parser2
    
    def test_factory_with_fixtures(self):
        """Test factory avec les fichiers de fixtures réels."""
        csv_parser = ParserFactory.get_parser('tests/fixtures/sample.csv')
        json_parser = ParserFactory.get_parser('tests/fixtures/sample.json')
        xml_parser = ParserFactory.get_parser('tests/fixtures/sample.xml')
        
        assert isinstance(csv_parser, CSVParser)
        assert isinstance(json_parser, JSONParser)
        assert isinstance(xml_parser, XMLParser)
        
        # Test que les parsers fonctionnent
        csv_data = csv_parser.parse('tests/fixtures/sample.csv')
        json_data = json_parser.parse('tests/fixtures/sample.json')
        xml_data = xml_parser.parse('tests/fixtures/sample.xml')
        
        # Vérifier que tous parsent le même nombre de lignes
        assert len(csv_data) == 10
        assert len(json_data) == 10
        assert len(xml_data) == 10
