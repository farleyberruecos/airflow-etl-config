"""
Main AirflowConfig class - Configuration Management
"""

import os
import importlib.util
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

from .exceptions import ConfigFileError, VariableNotFoundError
from .utils import TemplateGenerator


class AirflowConfig:
    """
    Main configuration manager for Airflow variables.
    Handles configuration lifecycle: creation, loading, validation, and access.
    """

    def __init__(self, config_file: str = "config.py", template_generator: Optional[TemplateGenerator] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Path to the Python configuration file.
            template_generator: Instance of TemplateGenerator. If not provided, a new one is created.
        """
        self.config_file = config_file
        self.variables: Dict[str, Any] = {}
        self._template_generator = template_generator or TemplateGenerator()
        self._load_existing_config()

    def _load_existing_config(self) -> None:
        """Load existing configuration from file if it exists."""
        if os.path.exists(self.config_file):
            self._parse_config_file()

    def _parse_config_file(self) -> None:
        """Parse configuration file safely."""
        try:
            # Load module safely using importlib
            spec = importlib.util.spec_from_file_location("airflow_config_module", self.config_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules["airflow_config_module"] = module
                spec.loader.exec_module(module)
                
                # Extract configuration variables
                for key, value in module.__dict__.items():
                    if key.isupper() and not key.startswith('_'):
                        self.variables[key] = value
            else:
                 raise ConfigFileError(f"Could not load config file '{self.config_file}'")

        except Exception as e:
            raise ConfigFileError(f"Error parsing config file '{self.config_file}': {e}")

    def create_etl_pipeline(self, source: str, destination: str) -> None:
        """
        Create ETL pipeline configuration.

        Args:
            source: Source database type.
            destination: Destination database type.
        """
        sections = {"source": source, "destination": destination}
        self._create_configuration(sections)

    def create_data_pipeline(self, sections: Dict[str, str]) -> None:
        """
        Create complex data pipeline configuration.

        Args:
            sections: Dictionary of section_name -> template_type.
        """
        self._create_configuration(sections)

    def _create_configuration(self, sections: Dict[str, str]) -> None:
        """Internal method to create configuration using template generator."""
        self._template_generator.create_config(sections, self.config_file)
        self._load_existing_config()  # Reload after creation

    def get_connection_params(self, section: str) -> Dict[str, Any]:
        """
        Get connection parameters for a specific section.

        Args:
            section: Section name.

        Returns:
            Dictionary of connection parameters (with section prefix removed and in lowercase).
        """
        section_vars = {}
        prefix = f"{section.upper()}_"

        for key, value in self.variables.items():
            if key.startswith(prefix):
                param_name = key.replace(prefix, "").lower()
                section_vars[param_name] = value

        return section_vars

    def validate_section(self, section: str) -> bool:
        """
        Validate if a section has all required variables.

        Args:
            section: Section name to validate.

        Returns:
            True if section has at least one variable, False otherwise.
        """
        section_vars = self.get_connection_params(section)
        return len(section_vars) > 0

    # Basic variable access methods
    def get_variable(self, key: str, default: Any = None) -> Any:
        """Get a variable value."""
        if key not in self.variables and default is None:
            raise VariableNotFoundError(f"Variable '{key}' not found")
        return self.variables.get(key, default)

    def list_variables(self) -> List[str]:
        """List all configuration variables."""
        return list(self.variables.keys())

    def variable_exists(self, key: str) -> bool:
        """Check if variable exists."""
        return key in self.variables

    def get_available_templates(self) -> List[str]:
        """Get available template types from the template generator."""
        return self._template_generator.get_available_templates()

    def __repr__(self) -> str:
        return f"AirflowConfig(file='{self.config_file}', variables={len(self.variables)})"