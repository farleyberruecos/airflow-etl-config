"""
Configuration and fixtures for pytest
"""
import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Mock airflow before any imports
sys.modules['airflow'] = MagicMock()
sys.modules['airflow.models'] = MagicMock()
Variable = MagicMock()
Variable.get = MagicMock(side_effect=lambda k, default_var=None: default_var)
sys.modules['airflow.models'].Variable = Variable

from airflow_config import create_etl_pipeline, create_project_structure

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def generated_config_file(temp_dir):
    """Create a configuration file using the ETL pipeline factory"""
    config_path = os.path.join(temp_dir, "config.py")
    create_etl_pipeline(
        source="postgresql",
        destination="bigquery",
        config_file=config_path
    )
    return config_path

@pytest.fixture
def scaffold_project(temp_dir):
    """Create a scaffolded project"""
    project_name = os.path.join(temp_dir, "test_project")
    create_project_structure(project_name)
    return project_name