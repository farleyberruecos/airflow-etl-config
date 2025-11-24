"""
Custom exceptions for airflow-config library
"""

class AirflowConfigError(Exception):
    """Base exception class for all airflow-config related errors."""
    pass

class ConfigFileError(AirflowConfigError):
    """Raised when there are issues with configuration file operations."""
    pass

class VariableValidationError(AirflowConfigError):
    """Raised when variable names or values fail validation checks."""
    pass

class ConfigurationError(AirflowConfigError):
    """Raised when there are errors in the configuration setup process."""
    pass

class TemplateGenerationError(AirflowConfigError):
    """Raised when template generation operations fail."""
    pass

class VariableNotFoundError(AirflowConfigError):
    """Raised when a requested configuration variable cannot be found."""
    pass

class TemplateNotFoundError(AirflowConfigError):
    """Raised when a requested template type is not available."""
    pass

class VariableTypeError(AirflowConfigError):
    """Raised when variable type conversion or validation fails."""
    pass

class FileWriteError(AirflowConfigError):
    """Raised when file write operations fail during configuration generation."""
    pass

class SecurityError(AirflowConfigError):
    """Raised when security-related issues are detected with sensitive data."""
    pass

class DependencyError(AirflowConfigError):
    """Raised when required dependencies are missing or unavailable."""
    pass

class InvalidTemplateError(AirflowConfigError):
    """Raised when template structure or definition is invalid."""
    pass