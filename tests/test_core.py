"""
Tests for core AirflowConfig functionality (Strategy Pattern)
"""
import pytest
import os
import sys
import importlib.util
from airflow_config import AirflowConfig

class TestAirflowConfig:
    
    def test_create_and_load_config(self, generated_config_file):
        """Test creating and loading a configuration file"""
        assert os.path.exists(generated_config_file)
        
        config = AirflowConfig(generated_config_file)
        
        # Check that variables were loaded
        assert len(config.variables) > 0
        assert "SOURCE_POSTGRES_HOST" in config.variables
        assert "DESTINATION_BQ_PROJECT" in config.variables
        
    def test_get_variable(self, generated_config_file):
        """Test getting variables"""
        config = AirflowConfig(generated_config_file)
        
        # Test existing variable
        host = config.get_variable("SOURCE_POSTGRES_HOST")
        assert host == "localhost"
        
        # Test default value
        missing = config.get_variable("NON_EXISTENT", "default")
        assert missing == "default"
        
    def test_get_connection_params(self, generated_config_file):
        """Test getting connection parameters"""
        config = AirflowConfig(generated_config_file)
        
        # Test source params (PostgreSQL)
        source_params = config.get_connection_params("source")
        assert source_params["postgres_host"] == "localhost"
        assert source_params["postgres_port"] == 5432
        assert source_params["postgres_user"] == "airflow"
        
        # Test destination params (BigQuery)
        dest_params = config.get_connection_params("destination")
        assert dest_params["bq_project"] == "datastudio-327414"
        
    def test_validate_section(self, generated_config_file):
        """Test section validation"""
"""
Tests for core AirflowConfig functionality (Strategy Pattern)
"""
import pytest
import os
import sys
import importlib.util
from airflow_config import AirflowConfig

class TestAirflowConfig:
    
    def test_create_and_load_config(self, generated_config_file):
        """Test creating and loading a configuration file"""
        assert os.path.exists(generated_config_file)
        
        config = AirflowConfig(generated_config_file)
        
        # Check that variables were loaded
        assert len(config.variables) > 0
        assert "SOURCE_POSTGRES_HOST" in config.variables
        assert "DESTINATION_BQ_PROJECT" in config.variables
        
    def test_get_variable(self, generated_config_file):
        """Test getting variables"""
        config = AirflowConfig(generated_config_file)
        
        # Test existing variable
        host = config.get_variable("SOURCE_POSTGRES_HOST")
        assert host == "localhost"
        
        # Test default value
        missing = config.get_variable("NON_EXISTENT", "default")
        assert missing == "default"
        
    def test_get_connection_params(self, generated_config_file):
        """Test getting connection parameters"""
        config = AirflowConfig(generated_config_file)
        
        # Test source params (PostgreSQL)
        source_params = config.get_connection_params("source")
        assert source_params["postgres_host"] == "localhost"
        assert source_params["postgres_port"] == 5432
        assert source_params["postgres_user"] == "airflow"
        
        # Test destination params (BigQuery)
        dest_params = config.get_connection_params("destination")
        assert dest_params["bq_project"] == "datastudio-327414"
        
    def test_validate_section(self, generated_config_file):
        """Test section validation"""
        config = AirflowConfig(generated_config_file)
        
        assert config.validate_section("source") == True
        assert config.validate_section("destination") == True
        assert config.validate_section("non_existent") == False

    def test_generated_functions(self, generated_config_file):
        """Test that generated functions work (by importing the file)"""
        # Load the generated module
        spec = importlib.util.spec_from_file_location("generated_config", generated_config_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules["generated_config"] = module
        spec.loader.exec_module(module)
        
        # Verify variables are present as globals
        assert hasattr(module, "SOURCE_POSTGRES_HOST")
        assert hasattr(module, "DESTINATION_BQ_PROJECT")