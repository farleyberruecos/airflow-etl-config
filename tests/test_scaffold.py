"""
Tests for project scaffolding
"""
import os
import pytest
from airflow_config import create_project_structure

def test_create_project_structure(scaffold_project):
    """Test that project structure is created correctly"""
    project_path = scaffold_project
    
    assert os.path.exists(project_path)
    assert os.path.isdir(project_path)
    
    # Check key directories
    assert os.path.exists(os.path.join(project_path, "src"))
    assert os.path.exists(os.path.join(project_path, "config"))
    assert os.path.exists(os.path.join(project_path, "connections"))
    
    # Check key files
    assert os.path.exists(os.path.join(project_path, "requirements.txt"))
    assert os.path.exists(os.path.join(project_path, "README.md"))
    assert os.path.exists(os.path.join(project_path, "src", "extract", "extractor.py"))
