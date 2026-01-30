"""
Tests unitaires pour JSONParser.
"""
import pytest
import json

from project_parser.parsers.json_parser import JSONParser
from project_parser.utils.exceptions import InvalidFormatError


class TestJSONParser:
    """Tests pour le parser JSON."""
    
    @pytest.fixture
    def parser(self):
        """Fixture pour créer un parser JSON."""
        return JSONParser()
    
    @pytest.fixture
    def sample_json_path(self):
        """Fixture pour le chemin du JSON de test."""
        return 'tests/fixtures/sample.json'
    
    def test_parse_basic_json(self, parser, sample_json_path):
        """Test parsing d'un JSON basique (tableau)."""
        data = parser.parse(sample_json_path)
        
        assert len(data) == 10
        assert len(data.headers) == 5
        assert 'name' in data.headers
        assert 'age' in data.headers
        assert 'city' in data.headers
    
    def test_parse_returns_correct_data(self, parser, sample_json_path):
        """Test que les données parsées sont correctes."""
        data = parser.parse(sample_json_path)
        
        first_row = data[0]
        assert first_row['name'] == 'Alice Martin'
        assert first_row['age'] == 30  # JSON conserve les types
        assert first_row['city'] == 'Paris'
    
    def test_parse_array_format(self, parser, tmp_path):
        """Test parsing format tableau."""
        json_file = tmp_path / 'test_array.json'
        json_data = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25}
        ]
        json_file.write_text(json.dumps(json_data), encoding='utf-8')
        
        data = parser.parse(str(json_file))
        
        assert len(data) == 2
        assert data[0]['name'] == 'Alice'
    
    def test_parse_object_with_data_key(self, parser, tmp_path):
        """Test parsing format objet avec clé 'data'."""
        json_file = tmp_path / 'test_object.json'
        json_data = {
            'data': [
                {'name': 'Alice', 'age': 30},
                {'name': 'Bob', 'age': 25}
            ]
        }
        json_file.write_text(json.dumps(json_data), encoding='utf-8')
        
        data = parser.parse(str(json_file))
        
        assert len(data) == 2
        assert data[0]['name'] == 'Alice'
    
    def test_parse_single_object(self, parser, tmp_path):
        """Test parsing d'un objet unique."""
        json_file = tmp_path / 'test_single.json'
        json_data = {'name': 'Alice', 'age': 30}
        json_file.write_text(json.dumps(json_data), encoding='utf-8')
        
        data = parser.parse(str(json_file))
        
        assert len(data) == 1
        assert data[0]['name'] == 'Alice'
    
    def test_parse_empty_array(self, parser, tmp_path):
        """Test parsing d'un tableau vide."""
        json_file = tmp_path / 'empty.json'
        json_file.write_text('[]', encoding='utf-8')
        
        data = parser.parse(str(json_file))
        
        assert len(data) == 0
        assert len(data.headers) == 0
    
    def test_parse_invalid_json(self, parser, tmp_path):
        """Test parsing d'un JSON invalide."""
        json_file = tmp_path / 'invalid.json'
        json_file.write_text('{invalid json', encoding='utf-8')
        
        with pytest.raises(InvalidFormatError):
            parser.parse(str(json_file))
    
    def test_parse_nonexistent_file(self, parser):
        """Test parsing d'un fichier inexistant."""
        with pytest.raises(FileNotFoundError):
            parser.parse('nonexistent.json')
    
    def test_validate_valid_json(self, parser, sample_json_path):
        """Test validation d'un JSON valide."""
        assert parser.validate(sample_json_path) is True
    
    def test_validate_nonexistent_file(self, parser):
        """Test validation d'un fichier inexistant."""
        assert parser.validate('nonexistent.json') is False
    
    def test_validate_wrong_extension(self, parser, tmp_path):
        """Test validation avec mauvaise extension."""
        txt_file = tmp_path / 'test.txt'
        txt_file.write_text('test', encoding='utf-8')
        
        assert parser.validate(str(txt_file)) is False
    
    def test_metadata_included(self, parser, sample_json_path):
        """Test que les métadonnées sont incluses."""
        data = parser.parse(sample_json_path)
        
        assert 'source' in data.metadata
        assert 'format' in data.metadata
        assert data.metadata['format'] == 'json'
        assert 'rows_count' in data.metadata
    
    def test_types_preserved(self, parser, tmp_path):
        """Test que les types JSON sont préservés."""
        json_file = tmp_path / 'types.json'
        json_data = [
            {
                'string': 'text',
                'number': 42,
                'float': 3.14,
                'boolean': True,
                'null': None
            }
        ]
        json_file.write_text(json.dumps(json_data), encoding='utf-8')
        
        data = parser.parse(str(json_file))
        
        row = data[0]
        assert isinstance(row['string'], str)
        assert isinstance(row['number'], int)
        assert isinstance(row['float'], float)
        assert isinstance(row['boolean'], bool)
        assert row['null'] is None
