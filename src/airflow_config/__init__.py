"""
airflow-config - Configuration management for Apache Airflow
"""

from .core import AirflowConfig
from .utils import TemplateGenerator
from .scaffold import create_project_structure
from .exceptions import (
    AirflowConfigError, ConfigFileError, VariableNotFoundError,
    TemplateGenerationError, TemplateNotFoundError,
    VariableTypeError, FileWriteError, ConfigurationError
)

__version__ = "1.0.0"
__author__ = "farley"
__email__ = "farleyberruecosg@gmail.com"

# Factory function para crear un pipeline ETL
def create_etl_pipeline(source: str, destination: str, config_file: str = "config.py"):
    """Factory function para crear pipeline ETL"""
    config = AirflowConfig(config_file)
    config.create_etl_pipeline(source, destination)
    return config

# Otra función de fachada para obtener plantillas disponibles
def get_available_templates():
    """Obtener la lista de plantillas disponibles"""
    return TemplateGenerator().get_available_templates()

# Definir __all__ para controlar las importaciones con *
__all__ = [
    'AirflowConfig',
    'TemplateGenerator',
    'create_etl_pipeline',
    'create_project_structure',
    'get_available_templates',
    'AirflowConfigError',
    'ConfigFileError',
    'VariableNotFoundError',
    'TemplateGenerationError',
    'TemplateNotFoundError',
    'VariableTypeError',
    'FileWriteError',
    'ConfigurationError'
]