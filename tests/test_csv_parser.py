"""
Tests unitaires pour CSVParser.
"""
import pytest
from pathlib import Path

from project_parser.parsers.csv_parser import CSVParser
from project_parser.utils.exceptions import InvalidFormatError


class TestCSVParser:
    """Tests pour le parser CSV."""
    
    @pytest.fixture
    def parser(self):
        """Fixture pour créer un parser CSV."""
        return CSVParser()
    
    @pytest.fixture
    def sample_csv_path(self):
        """Fixture pour le chemin du CSV de test."""
        return 'tests/fixtures/sample.csv'
    
    def test_parse_basic_csv(self, parser, sample_csv_path):
        """Test parsing d'un CSV basique."""
        data = parser.parse(sample_csv_path)
        
        assert len(data) == 10  # 10 lignes dans le fichier
        assert len(data.headers) == 5  # 5 colonnes
        assert 'name' in data.headers
        assert 'age' in data.headers
        assert 'city' in data.headers
        assert 'email' in data.headers
        assert 'department' in data.headers
    
    def test_parse_returns_correct_data(self, parser, sample_csv_path):
        """Test que les données parsées sont correctes."""
        data = parser.parse(sample_csv_path)
        
        # Vérifier la première ligne
        first_row = data[0]
        assert first_row['name'] == 'Alice Martin'
        assert first_row['age'] == '30'
        assert first_row['city'] == 'Paris'
        assert first_row['department'] == 'Engineering'
    
    def test_parse_with_different_delimiter(self, parser, tmp_path):
        """Test parsing avec un délimiteur différent."""
        # Créer un fichier CSV avec point-virgule
        csv_file = tmp_path / 'test_semicolon.csv'
        csv_file.write_text('name;age\nAlice;30\nBob;25', encoding='utf-8')
        
        data = parser.parse(str(csv_file), delimiter=';')
        
        assert len(data) == 2
        assert data[0]['name'] == 'Alice'
        assert data[0]['age'] == '30'
    
    def test_parse_with_different_encoding(self, parser, tmp_path):
        """Test parsing avec un encodage différent."""
        # Créer un fichier avec encodage latin-1
        csv_file = tmp_path / 'test_latin1.csv'
        csv_file.write_text('name,city\nJosé,París', encoding='latin-1')
        
        data = parser.parse(str(csv_file), encoding='latin-1')
        
        assert len(data) == 1
        assert data[0]['name'] == 'José'
        assert data[0]['city'] == 'París'
    
    def test_parse_empty_csv(self, parser, tmp_path):
        """Test parsing d'un CSV vide."""
        csv_file = tmp_path / 'empty.csv'
        csv_file.write_text('', encoding='utf-8')
        
        with pytest.raises(InvalidFormatError):
            parser.parse(str(csv_file))
    
    def test_parse_nonexistent_file(self, parser):
        """Test parsing d'un fichier inexistant."""
        with pytest.raises(FileNotFoundError):
            parser.parse('nonexistent.csv')
    
    def test_validate_valid_csv(self, parser, sample_csv_path):
        """Test validation d'un CSV valide."""
        assert parser.validate(sample_csv_path) is True
    
    def test_validate_nonexistent_file(self, parser):
        """Test validation d'un fichier inexistant."""
        assert parser.validate('nonexistent.csv') is False
    
    def test_validate_wrong_extension(self, parser, tmp_path):
        """Test validation avec mauvaise extension."""
        txt_file = tmp_path / 'test.txt'
        txt_file.write_text('test', encoding='utf-8')
        
        assert parser.validate(str(txt_file)) is False
    
    def test_metadata_included(self, parser, sample_csv_path):
        """Test que les métadonnées sont incluses."""
        data = parser.parse(sample_csv_path)
        
        assert 'source' in data.metadata
        assert 'format' in data.metadata
        assert data.metadata['format'] == 'csv'
        assert 'rows_count' in data.metadata
        assert data.metadata['rows_count'] == 10
    
    def test_iteration(self, parser, sample_csv_path):
        """Test qu'on peut itérer sur les données."""
        data = parser.parse(sample_csv_path)
        
        count = 0
        for row in data:
            count += 1
            assert isinstance(row, dict)
        
        assert count == 10
    
    def test_indexing(self, parser, sample_csv_path):
        """Test l'accès par index."""
        data = parser.parse(sample_csv_path)
        
        first = data[0]
        last = data[-1]
        
        assert first['name'] == 'Alice Martin'
        assert last['name'] == 'Julia Petit'
