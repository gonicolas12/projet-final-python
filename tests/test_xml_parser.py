"""
Tests unitaires pour XMLParser.
"""
import pytest

from project_parser.parsers.xml_parser import XMLParser
from project_parser.utils.exceptions import InvalidFormatError


class TestXMLParser:
    """Tests pour le parser XML."""
    
    @pytest.fixture
    def parser(self):
        """Fixture pour créer un parser XML."""
        return XMLParser()
    
    @pytest.fixture
    def sample_xml_path(self):
        """Fixture pour le chemin du XML de test."""
        return 'tests/fixtures/sample.xml'
    
    def test_parse_basic_xml(self, parser, sample_xml_path):
        """Test parsing d'un XML basique."""
        data = parser.parse(sample_xml_path)
        
        assert len(data) == 10
        assert len(data.headers) == 5
        assert 'name' in data.headers
        assert 'age' in data.headers
        assert 'city' in data.headers
    
    def test_parse_returns_correct_data(self, parser, sample_xml_path):
        """Test que les données parsées sont correctes."""
        data = parser.parse(sample_xml_path)
        
        first_row = data[0]
        assert first_row['name'] == 'Alice Martin'
        assert first_row['age'] == '30'
        assert first_row['city'] == 'Paris'
    
    def test_parse_simple_xml(self, parser, tmp_path):
        """Test parsing d'un XML simple."""
        xml_file = tmp_path / 'test.xml'
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item>
        <name>Alice</name>
        <age>30</age>
    </item>
    <item>
        <name>Bob</name>
        <age>25</age>
    </item>
</root>'''
        xml_file.write_text(xml_content, encoding='utf-8')
        
        data = parser.parse(str(xml_file))
        
        assert len(data) == 2
        assert data[0]['name'] == 'Alice'
        assert data[1]['name'] == 'Bob'
    
    def test_parse_empty_xml(self, parser, tmp_path):
        """Test parsing d'un XML vide."""
        xml_file = tmp_path / 'empty.xml'
        xml_content = '<?xml version="1.0"?><root></root>'
        xml_file.write_text(xml_content, encoding='utf-8')
        
        data = parser.parse(str(xml_file))
        
        assert len(data) == 0
        assert len(data.headers) == 0
    
    def test_parse_xml_with_missing_fields(self, parser, tmp_path):
        """Test parsing XML avec champs manquants."""
        xml_file = tmp_path / 'missing.xml'
        xml_content = '''<?xml version="1.0"?>
<root>
    <item>
        <name>Alice</name>
        <age>30</age>
    </item>
    <item>
        <name>Bob</name>
    </item>
</root>'''
        xml_file.write_text(xml_content, encoding='utf-8')
        
        data = parser.parse(str(xml_file))
        
        assert len(data) == 2
        assert data[0]['age'] == '30'
        assert data[1]['age'] == ''  # Champ manquant = chaîne vide
    
    def test_parse_xml_with_whitespace(self, parser, tmp_path):
        """Test parsing XML avec espaces."""
        xml_file = tmp_path / 'whitespace.xml'
        xml_content = '''<?xml version="1.0"?>
<root>
    <item>
        <name>  Alice  </name>
        <age> 30 </age>
    </item>
</root>'''
        xml_file.write_text(xml_content, encoding='utf-8')
        
        data = parser.parse(str(xml_file))
        
        # Les espaces doivent être trimés
        assert data[0]['name'] == 'Alice'
        assert data[0]['age'] == '30'
    
    def test_parse_invalid_xml(self, parser, tmp_path):
        """Test parsing d'un XML invalide."""
        xml_file = tmp_path / 'invalid.xml'
        xml_file.write_text('<root><item>invalid</root>', encoding='utf-8')
        
        with pytest.raises(InvalidFormatError):
            parser.parse(str(xml_file))
    
    def test_parse_nonexistent_file(self, parser):
        """Test parsing d'un fichier inexistant."""
        with pytest.raises(FileNotFoundError):
            parser.parse('nonexistent.xml')
    
    def test_validate_valid_xml(self, parser, sample_xml_path):
        """Test validation d'un XML valide."""
        assert parser.validate(sample_xml_path) is True
    
    def test_validate_nonexistent_file(self, parser):
        """Test validation d'un fichier inexistant."""
        assert parser.validate('nonexistent.xml') is False
    
    def test_validate_wrong_extension(self, parser, tmp_path):
        """Test validation avec mauvaise extension."""
        txt_file = tmp_path / 'test.txt'
        txt_file.write_text('test', encoding='utf-8')
        
        assert parser.validate(str(txt_file)) is False
    
    def test_metadata_included(self, parser, sample_xml_path):
        """Test que les métadonnées sont incluses."""
        data = parser.parse(sample_xml_path)
        
        assert 'source' in data.metadata
        assert 'format' in data.metadata
        assert data.metadata['format'] == 'xml'
        assert 'root_tag' in data.metadata
        assert 'rows_count' in data.metadata
    
    def test_headers_sorted(self, parser, tmp_path):
        """Test que les headers sont triés."""
        xml_file = tmp_path / 'sorted.xml'
        xml_content = '''<?xml version="1.0"?>
<root>
    <item>
        <zebra>z</zebra>
        <alpha>a</alpha>
        <beta>b</beta>
    </item>
</root>'''
        xml_file.write_text(xml_content, encoding='utf-8')
        
        data = parser.parse(str(xml_file))
        
        # Les headers doivent être triés alphabétiquement
        assert data.headers == ['alpha', 'beta', 'zebra']
