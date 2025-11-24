"""
Tests for template generation utilities
"""
import pytest
from airflow_config.utils import (
    TemplateGenerator,
    DatabaseTemplateStrategy,
    TemplateStrategy
)
from airflow_config.exceptions import (
    TemplateNotFoundError,
    ConfigurationError,
    FileWriteError
)
import os
import tempfile


class TestDatabaseTemplateStrategy:
    """Test DatabaseTemplateStrategy"""
    
    def test_get_available_templates(self):
        """Test getting available templates"""
        strategy = DatabaseTemplateStrategy()
        templates = strategy.get_available_templates()
        
        assert isinstance(templates, list)
        assert "postgresql" in templates
        assert "bigquery" in templates
        assert "redis" in templates
        assert "kafka" in templates
        assert len(templates) >= 9
    
    def test_generate_section_postgresql(self):
        """Test generating PostgreSQL section"""
        strategy = DatabaseTemplateStrategy()
        section = strategy.generate_section("source", "postgresql")
        
        assert "SOURCE_POSTGRES_HOST" in section
        assert "SOURCE_POSTGRES_PORT" in section
        assert "SOURCE_POSTGRES_DB" in section
        assert "Variable.get" in section
    
    def test_generate_section_bigquery(self):
        """Test generating BigQuery section"""
        strategy = DatabaseTemplateStrategy()
        section = strategy.generate_section("dest", "bigquery")
        
        assert "DEST_BQ_PROJECT" in section
        assert "DEST_BQ_DATASET" in section
        assert "DEST_BQ_PRIVATE_KEY" in section
    
    def test_generate_section_invalid_template(self):
        """Test generating section with invalid template"""
        strategy = DatabaseTemplateStrategy()
        
        with pytest.raises(TemplateNotFoundError):
            strategy.generate_section("test", "invalid_template")
    
    def test_generate_variable_types(self):
        """Test variable generation with different types"""
        strategy = DatabaseTemplateStrategy()
        
        # Test int type
        var_int = strategy._generate_variable("TEST_PORT", ("test_port", "5432", "int"))
        assert "int(" in var_int
        
        # Test bool type
        var_bool = strategy._generate_variable("TEST_FLAG", ("test_flag", "True", "bool"))
        assert '.lower() == "true"' in var_bool
        
        # Test string type (default)
        var_str = strategy._generate_variable("TEST_HOST", ("test_host", "localhost"))
        assert "Variable.get" in var_str


class TestTemplateGenerator:
    """Test TemplateGenerator"""
    
    def test_initialization_default_strategy(self):
        """Test initialization with default strategy"""
        generator = TemplateGenerator()
        assert generator._strategy is not None
        assert isinstance(generator._strategy, DatabaseTemplateStrategy)
    
    def test_initialization_custom_strategy(self):
        """Test initialization with custom strategy"""
        custom_strategy = DatabaseTemplateStrategy()
        generator = TemplateGenerator(strategy=custom_strategy)
        assert generator._strategy is custom_strategy
    
    def test_set_strategy(self):
        """Test changing strategy"""
        generator = TemplateGenerator()
        new_strategy = DatabaseTemplateStrategy()
        generator.set_strategy(new_strategy)
        assert generator._strategy is new_strategy
    
    def test_get_available_templates(self):
        """Test getting available templates"""
        generator = TemplateGenerator()
        templates = generator.get_available_templates()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
    
    def test_create_config_basic(self, tmp_path):
        """Test creating basic configuration"""
        generator = TemplateGenerator()
        config_file = tmp_path / "test_config.py"
        
        sections = {
            "source": "postgresql",
            "destination": "bigquery"
        }
        
        generator.create_config(sections, str(config_file))
        
        assert config_file.exists()
        content = config_file.read_text()
        assert "SOURCE_POSTGRES_HOST" in content
        assert "DESTINATION_BQ_PROJECT" in content
        assert "from airflow.models import Variable" in content
    
    def test_create_config_empty_sections(self, tmp_path):
        """Test creating config with empty sections"""
        generator = TemplateGenerator()
        config_file = tmp_path / "test_config.py"
        
        with pytest.raises(ConfigurationError):
            generator.create_config({}, str(config_file))
    
    def test_create_config_invalid_template(self, tmp_path):
        """Test creating config with invalid template"""
        generator = TemplateGenerator()
        config_file = tmp_path / "test_config.py"
        
        sections = {"test": "invalid_template"}
        
        with pytest.raises(TemplateNotFoundError):
            generator.create_config(sections, str(config_file))
    
    def test_create_config_multiple_sections(self, tmp_path):
        """Test creating config with multiple sections"""
        generator = TemplateGenerator()
        config_file = tmp_path / "test_config.py"
        
        sections = {
            "db": "postgresql",
            "cache": "redis",
            "events": "kafka"
        }
        
        generator.create_config(sections, str(config_file))
        
        content = config_file.read_text()
        assert "DB_POSTGRES_HOST" in content
        assert "CACHE_REDIS_HOST" in content
        assert "EVENTS_KAFKA_BOOTSTRAP_SERVERS" in content
    
    def test_generate_header(self):
        """Test header generation"""
        generator = TemplateGenerator()
        header = generator._generate_header()
        
        assert "Airflow Configuration" in header
        assert "import os" in header
        assert "import logging" in header
        assert "from airflow.models import Variable" in header
