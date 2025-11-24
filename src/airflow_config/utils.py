"""
Template generation utilities with Strategy Pattern
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from .exceptions import (
    TemplateGenerationError, TemplateNotFoundError,
    FileWriteError, ConfigurationError, VariableTypeError
)

logger = logging.getLogger(__name__)

class TemplateStrategy(ABC):
    """Strategy interface para generación de templates"""
    
    @abstractmethod
    def generate_section(self, section_name: str, template_type: str) -> str:
        pass
    
    @abstractmethod
    def get_available_templates(self) -> List[str]:
        pass


class DatabaseTemplateStrategy(TemplateStrategy):
    """Strategy para templates de bases de datos"""
    
    TEMPLATES = {
        "trino": {
            "TRINO_HOST": ("trino_host", "trino.empresa.com"),
            "TRINO_PORT": ("trino_port", "8080", "int"),
            "TRINO_USER": ("trino_user", "users"),
            "TRINO_PASSWORD": ("trino_password", "", "secret"),
            "TRINO_CATALOG": ("trino_catalog", "hive"),
            "TRINO_SCHEMA": ("trino_schema", "default"),
            "TRINO_SOURCE": ("trino_source", "etl_pipeline"),
        },
        "postgresql": {
            "POSTGRES_HOST": ("postgres_host", "localhost"),
            "POSTGRES_PORT": ("postgres_port", "5432", "int"),
            "POSTGRES_DB": ("postgres_db", "airflow"),
            "POSTGRES_USER": ("postgres_user", "airflow"),
            "POSTGRES_PASSWORD": ("postgres_password", "airflow", "secret"),
            "POSTGRES_SCHEMA": ("postgres_schema", "public"),
            "POSTGRES_CONN_ID": ("postgres_conn_id", "postgres_default"),
        },
        "sqlserver": {
            "SQL_SERVER_HOST": ("sql_server_host", "localhost"),
            "SQL_SERVER_PORT": ("sql_server_port", "1433", "int"),
            "SQL_SERVER_DB": ("sql_server_db", "master"),
            "SQL_SERVER_USER": ("sql_server_user", "sa"),
            "SQL_SERVER_PASSWORD": ("sql_server_password", "", "secret"),
            "SQL_SERVER_DRIVER": ("sql_server_driver", "ODBC Driver 17 for SQL Server"),
            "SQL_SERVER_CONN_ID": ("sql_server_conn_id", "mssql_default"),
        },
        "mongodb": {
            "MONGO_HOST": ("mongo_host", "localhost"),
            "MONGO_PORT": ("mongo_port", "27017", "int"),
            "MONGO_DB": ("mongo_db", "admin"),
            "MONGO_USER": ("mongo_user", "mongo"),
            "MONGO_PASSWORD": ("mongo_password", "", "secret"),
            "MONGO_AUTH_SOURCE": ("mongo_auth_source", "admin"),
            "MONGO_CONN_ID": ("mongo_conn_id", "mongo_default"),
        },
        "redis": {
            "REDIS_HOST": ("redis_host", "redis"),
            "REDIS_PORT": ("redis_port", "6379", "int"),
            "REDIS_DB": ("redis_db", "1", "int"),
            "REDIS_PASSWORD": ("redis_password", "", "secret"),
        },
        "bigquery": {
            "BQ_PROJECT": ("bq_project", "datastudio-327414"),
            "BQ_DATASET": ("bq_dataset", "Dashboard"),
            "BQ_DEFAULT_TABLE": ("bq_default_table", "daily"),
            "BQ_CREDENTIALS_TYPE": ("bq_credentials_type", "service_account"),
            "BQ_PRIVATE_KEY_ID": ("bq_private_key_id", "7e6b000000000000000000000"),
            "BQ_PRIVATE_KEY": ("bq_private_key", "", "secret"),
            "BQ_CLIENT_EMAIL": ("bq_client_email", "bigquerydata@datastudio-00000.iam.service.com"),
            "BQ_CLIENT_ID": ("bq_client_id", "1156176228000000000"),
            "BQ_AUTH_URI": ("bq_auth_uri", "https://accounts.google.com/o/oauth2/auth"),
            "BQ_TOKEN_URI": ("bq_token_uri", "https://oauth2.googleapis.com/token"),
            "BQ_AUTH_PROVIDER_CERT_URL": ("bq_auth_provider_cert_url", "https://www.googleapis.com/oauth2/v1/certs"),
            "BQ_CLIENT_CERT_URL": ("bq_client_cert_url", "https://www.googleapis.com/robot/v1/metadata/x509/bigqueryxxxxx@datastudio-000000.iam.gserviceaccount.com"),
        },
        "kafka": {
            "KAFKA_BOOTSTRAP_SERVERS": ("kafka_bootstrap_servers", "localhost:9092"),
            "KAFKA_GROUP_ID": ("kafka_group_id", "airflow_etl"),
            "KAFKA_TOPIC": ("kafka_topic", "etl_events"),
            "KAFKA_SECURITY_PROTOCOL": ("kafka_security_protocol", "PLAINTEXT"),
        },
        "api_keys": {
            "API_TIMEOUT": ("api_timeout", "30", "int"),
            "API_MAX_RETRIES": ("api_max_retries", "3", "int"),
            "API_BASE_URL": ("api_base_url", "https://api.example.com"),
            "API_KEY": ("api_key", "", "secret"),
        },
        "dag_config": {
            "DAG_OWNER": ("dag_owner", "airflow"),
            "DAG_RETRIES": ("dag_retries", "3", "int"),
            "DAG_RETRY_DELAY_MINUTES": ("dag_retry_delay_minutes", "5", "int"),
            "DAG_CATCHUP": ("dag_catchup", "False", "bool"),
        }
    }
    
    def get_available_templates(self) -> List[str]:
        return list(self.TEMPLATES.keys())
    
    def generate_section(self, section_name: str, template_type: str) -> str:
        if template_type not in self.TEMPLATES:
            raise TemplateNotFoundError(f"Template '{template_type}' not found")
        
        template = self.TEMPLATES[template_type]
        content = [f"\n# SECTION: {section_name.upper()} ({template_type.upper()})\n"]
        
        for var_name, var_config in template.items():
            section_var = f"{section_name.upper()}_{var_name}"
            content.append(self._generate_variable(section_var, var_config))
        
        return "\n".join(content)
    
    def _generate_variable(self, var_name: str, var_config: tuple) -> str:
        var_key, default_val = var_config[0], var_config[1]
        var_type = var_config[2] if len(var_config) > 2 else "str"
        
        converters = {"str": "", "int": "int", "bool": "bool", "secret": "", "float": "float", "json": "json.loads"}
        converter = converters.get(var_type)
        
        if not converter:
            return f'{var_name} = Variable.get("{var_key}", default_var="{default_val}")'
        
        if var_type == "bool":
            return f'{var_name} = Variable.get("{var_key}", default_var="{default_val}").lower() == "true"'
        
        return f'{var_name} = {converter}(Variable.get("{var_key}", default_var="{default_val}"))'


class TemplateGenerator:
    """
    Template generator usando Strategy Pattern
    """
    
    def __init__(self, strategy: TemplateStrategy = None):
        self._strategy = strategy or DatabaseTemplateStrategy()
    
    def set_strategy(self, strategy: TemplateStrategy) -> None:
        """Cambiar estrategia de generación"""
        self._strategy = strategy
    
    def get_available_templates(self) -> List[str]:
        """Obtener templates disponibles"""
        return self._strategy.get_available_templates()
    
    def create_config(self, sections: Dict[str, str], output_file: str) -> None:
        """Crear archivo de configuración"""
        self._validate_sections(sections)
        content = self._generate_file_content(sections)
        self._write_config_file(content, output_file)
    
    def _validate_sections(self, sections: Dict[str, str]) -> None:
        """Validar secciones"""
        if not sections:
            raise ConfigurationError("Sections cannot be empty")
        
        available = self.get_available_templates()
        invalid = [t for t in sections.values() if t not in available]
        if invalid:
            raise TemplateNotFoundError(f"Invalid templates: {invalid}")
    
    def _generate_file_content(self, sections: Dict[str, str]) -> str:
        """Generar contenido del archivo"""
        content = self._generate_header()
        
        for section_name, template_type in sections.items():
            content += self._strategy.generate_section(section_name, template_type) + "\n"
        
        return content
    
    def _generate_header(self) -> str:
        """Generar cabecera del archivo"""
        return '''"""
Airflow Configuration
Auto-generated configuration file
"""

import os
import logging
import json
from airflow.models import Variable

logger = logging.getLogger("airflow.task")

'''
    
    def _write_config_file(self, content: str, output_file: str) -> None:
        """Escribir archivo de configuración"""
        try:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ Configuration file created: {output_file}")
        except Exception as e:
            raise FileWriteError(f"Error writing '{output_file}': {e}")