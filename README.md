# airflow-etl-config

Python library for managing Apache Airflow configuration variables through centralized `.py` files. Generate configuration files using templates and access variables in a type-safe manner.

## Installation

```bash
pip install airflow-etl-config
```

## Quick Start

### 1. Create an ETL Pipeline Configuration

Generate a configuration file with source and destination sections:

```python
from airflow_config import create_etl_pipeline

# Creates a 'config.py' file with the specified templates
create_etl_pipeline(
    source="postgresql",
    destination="bigquery",
    config_file="my_config.py"
)
```

**Generated `my_config.py`:**
```python
from airflow.models import Variable

# Source PostgreSQL Configuration
SOURCE_POSTGRES_HOST = Variable.get("source_postgres_host", default_var="localhost")
SOURCE_POSTGRES_PORT = int(Variable.get("source_postgres_port", default_var="5432"))
SOURCE_POSTGRES_DB = Variable.get("source_postgres_db", default_var="mydb")
SOURCE_POSTGRES_USER = Variable.get("source_postgres_user", default_var="user")
SOURCE_POSTGRES_PASSWORD = Variable.get("source_postgres_password", default_var="password")

# Destination BigQuery Configuration
DESTINATION_BQ_PROJECT = Variable.get("destination_bq_project", default_var="my-project")
DESTINATION_BQ_DATASET = Variable.get("destination_bq_dataset", default_var="my_dataset")
# ... more variables
```

### 2. Create Multi-Source Data Pipeline

For complex configurations with multiple data sources:

```python
from airflow_config import AirflowConfig

config = AirflowConfig("production_config.py")

sections = {
    "main_db": "postgresql",
    "analytics": "bigquery",
    "cache": "redis",
    "events": "kafka"
}

config.create_data_pipeline(sections)
```

### 3. Generate Project Structure

Quickly scaffold a standard ETL project:

```python
from airflow_config import create_project_structure

# Creates complete folder structure
create_project_structure("my_new_project")
```

**Generated structure:**
```
my_new_project/
├── src/
│   ├── sql/          # SQL queries and DDL
│   ├── extract/      # Data extraction logic
│   ├── transform/    # Data transformation
│   ├── load/         # Data loading
│   ├── main/         # Orchestration
│   ├── factory/      # Factory patterns
│   └── dag/          # Airflow DAG definitions
├── config/           # Configuration files
├── connections/      # Connection definitions
├── requirements.txt
└── README.md
```

### 4. Load and Read Configurations

Once you have a configuration file, load and access its variables:

```python
from airflow_config import AirflowConfig

# Load existing configuration
config = AirflowConfig("my_config.py")

# List all loaded variables
print(config.list_variables())

# Get a specific variable
host = config.get_variable("MAIN_DB_POSTGRES_HOST", default="localhost")

# Check if variable exists
if config.variable_exists("EVENTS_KAFKA_TOPIC"):
    print("Kafka topic configured")
```

### 5. Get Connection Parameters

Extract all parameters for a specific section (useful for Airflow Hooks/Operators):

```python
# Get dictionary with section variables (prefix removed, lowercase)
# Example: MAIN_DB_POSTGRES_HOST -> postgres_host
db_params = config.get_connection_params("main_db")

print(db_params)
# Output: {'postgres_host': '...', 'postgres_port': 5432, ...}
```

### 6. Validate Configuration

Validate if a section has configured variables:

```python
if config.validate_section("main_db"):
    print("Section main_db is valid")
```

## Available Templates

The library uses `TemplateStrategy` to generate configurations. Currently supported templates:

| Template | Generated Variables (Prefixes) |
|----------|--------------------------------|
| `trino` | TRINO_HOST, TRINO_PORT, TRINO_USER, etc. |
| `postgresql` | POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, etc. |
| `sqlserver` | SQL_SERVER_HOST, SQL_SERVER_PORT, SQL_SERVER_DB, etc. |
| `mongodb` | MONGO_HOST, MONGO_PORT, MONGO_DB, etc. |
| `redis` | REDIS_HOST, REDIS_PORT, REDIS_DB, etc. |
| `bigquery` | BQ_PROJECT, BQ_DATASET, BQ_PRIVATE_KEY, etc. |
| `kafka` | KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, etc. |
| `api_keys` | API_BASE_URL, API_KEY, API_TIMEOUT, etc. |
| `dag_config` | DAG_OWNER, DAG_RETRIES, DAG_CATCHUP, etc. |

Query available templates programmatically:

```python
from airflow_config import get_available_templates

print(get_available_templates())
```

## API Reference

### Class `AirflowConfig`

**Methods:**

- `__init__(config_file: str, template_generator: Optional[TemplateGenerator])` - Initialize configuration manager
- `create_etl_pipeline(source: str, destination: str)` - Create ETL configuration
- `create_data_pipeline(sections: Dict[str, str])` - Create multi-section configuration
- `get_connection_params(section: str) -> Dict[str, Any]` - Get clean parameters for a section
- `validate_section(section: str) -> bool` - Validate if section has variables
- `get_variable(key: str, default: Any) -> Any` - Get variable value
- `list_variables() -> List[str]` - List variable names
- `variable_exists(key: str) -> bool` - Check variable existence
- `get_available_templates() -> List[str]` - List supported templates

### Helper Functions

- `create_etl_pipeline(source, destination, config_file)` - Quick pipeline creation
- `create_project_structure(project_name)` - Generate project scaffolding
- `get_available_templates()` - List available templates

## Testing

The library includes a complete test suite with 91% code coverage.

### Run Tests

```bash
# Using pytest (if installed)
pytest --cov=airflow_config --cov-report=html

# Using custom test runner
python3 run_tests.py
```

## Development

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Run linters
black --check src/ tests/
isort --check-only src/ tests/
```

## Requirements

- Python >= 3.7
- Apache Airflow (for production use)

## Features

- ✅ **Template-Based Generation**: Pre-built templates for popular data sources
- ✅ **Type Safety**: Full type hints and validation
- ✅ **Project Scaffolding**: Quick project structure generation
- ✅ **Centralized Management**: All variables in organized `.py` files
- ✅ **Multi-Environment**: Support for dev, staging, and production
- ✅ **Extensible**: Easy to add custom templates

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- **PyPI**: https://pypi.org/project/airflow-etl-config/
- **Documentation**: Full documentation available in Spanish (`DOCUMENTACION.md`)
- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md` for PyPI deployment instructions

## Support

For issues, questions, or contributions, please visit the project repository.
