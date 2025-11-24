"""
Query methods for Airflow configuration
"""

from datetime import timedelta
from typing import Dict, Any, List, Optional

class AirflowConfigQueryMixin:
    """Mixin with query methods for AirflowConfig"""
    
    def get_dag_default_args(self) -> Dict[str, Any]:
        """Get default arguments for DAGs"""
        return {
            'owner': self.variables.get('AIRFLOW__DEFAULT__DAG_OWNER', 'airflow'),
            'retries': self.variables.get('AIRFLOW__CORE__DEFAULT_RETRIES', 3),
            'retry_delay': timedelta(
                minutes=self.variables.get('AIRFLOW__CORE__DEFAULT_RETRY_DELAY_MINUTES', 5)
            ),
            'email_on_failure': True,
            'email_on_retry': False,
            'email': self.variables.get('AIRFLOW__EMAIL__DEFAULT_EMAIL', 'airflow@example.com')
        }
    
    def get_database_connection(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            'conn_id': self.variables.get('AIRFLOW_DB_CONN_ID', 'airflow_db'),
            'host': self.variables.get('AIRFLOW_DB_HOST', 'localhost'),
            'port': self.variables.get('AIRFLOW_DB_PORT', 5432),
            'schema': self.variables.get('AIRFLOW_DB_SCHEMA', 'airflow'),
            'login': self.variables.get('AIRFLOW_DB_LOGIN', 'airflow'),
            'password': self.variables.get('AIRFLOW_DB_PASSWORD', 'airflow')
        }
    
    def get_smtp_config(self) -> Dict[str, Any]:
        """Get SMTP configuration"""
        return {
            'smtp_host': self.variables.get('AIRFLOW__SMTP__SMTP_HOST', 'localhost'),
            'smtp_port': self.variables.get('AIRFLOW__SMTP__SMTP_PORT', 587),
            'smtp_starttls': self.variables.get('AIRFLOW__SMTP__SMTP_STARTTLS', True),
            'smtp_ssl': self.variables.get('AIRFLOW__SMTP__SMTP_SSL', False),
            'smtp_user': self.variables.get('AIRFLOW__SMTP__SMTP_USER', ''),
            'smtp_password': self.variables.get('AIRFLOW__SMTP__SMTP_PASSWORD', '')
        }
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return {
            'timeout': self.variables.get('API_TIMEOUT_SECONDS', 300),
            'max_retries': self.variables.get('API_MAX_RETRIES', 3)
        }
    
    def get_feature_flags(self) -> Dict[str, bool]:
        """Get feature flags (variables starting with FEATURE_)"""
        feature_flags = {}
        for key, value in self.variables.items():
            if key.startswith('FEATURE_') and isinstance(value, bool):
                feature_flags[key] = value
        return feature_flags
    
    def validate_required_variables(self, required_vars: List[str]) -> List[str]:
        """Validate that required variables exist"""
        missing = []
        for var_name in required_vars:
            if var_name not in self.variables:
                missing.append(var_name)
        return missing
    
    def get_variables_by_prefix(self, prefix: str) -> Dict[str, Any]:
        """Get all variables that start with the given prefix"""
        return {
            key: value for key, value in self.variables.items() 
            if key.startswith(prefix) and not key.startswith('__DOC_')
        }
    
    def get_config_summary(self) -> Dict[str, int]:
        """Get summary of configuration by section"""
        sections = {
            'database': 0,
            'email': 0,
            'scheduling': 0,
            'monitoring': 0,
            'dags': 0,
            'custom': 0
        }
        
        for key in self.variables.keys():
            if key.startswith('__DOC_'):
                continue
                
            if key.startswith('AIRFLOW_DB'):
                sections['database'] += 1
            elif key.startswith('AIRFLOW__SMTP') or key.startswith('AIRFLOW__EMAIL'):
                sections['email'] += 1
            elif key.startswith('AIRFLOW__CORE'):
                sections['scheduling'] += 1
            elif key.startswith('AIRFLOW__LOGGING') or key.startswith('AIRFLOW__METRICS'):
                sections['monitoring'] += 1
            elif key.startswith('AIRFLOW__DEFAULT'):
                sections['dags'] += 1
            else:
                sections['custom'] += 1
        
        return sections