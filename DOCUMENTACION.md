# Documentación de `airflow-config`

`airflow-config` es una librería de Python diseñada para gestionar variables de configuración de Apache Airflow mediante archivos `.py` centralizados. Permite generar archivos de configuración basados en plantillas y acceder a estas variables de forma tipada y segura.

## Instalación

```bash
pip install airflow-etl-config
```

O para instalar en modo editable desde el código fuente:

```bash
pip install -e .
```

## Uso Básico

La librería gira en torno a la clase `AirflowConfig` y el uso de generadores de plantillas.

### 1. Crear una Configuración Nueva

Puedes generar un archivo de configuración utilizando las funciones de fábrica o directamente la instancia de `AirflowConfig`.

#### Crear un Pipeline ETL Simple

La función `create_etl_pipeline` genera un archivo de configuración con secciones para una fuente y un destino.

```python
from airflow_config import create_etl_pipeline

# Esto creará un archivo 'config.py' (por defecto) con las plantillas especificadas
config = create_etl_pipeline(
    source="postgresql",
    destination="bigquery",
    config_file="mi_configuracion.py"
)
```

#### Crear un Pipeline de Datos Personalizado

Para configuraciones más complejas, usa `create_data_pipeline` pasando un diccionario de secciones y sus tipos de plantilla.

```python
from airflow_config import AirflowConfig

config = AirflowConfig("produccion_config.py")

secciones = {
    "main_db": "postgresql",
    "analytics": "bigquery",
    "cache": "redis",
    "events": "kafka"
}

config.create_data_pipeline(secciones)
```

### 3. Generar Estructura de Proyecto

Puedes inicializar rápidamente la estructura de carpetas y archivos para un nuevo proyecto ETL estándar.

```python
from airflow_config import create_project_structure

# Crea la estructura completa en la carpeta 'mi_nuevo_proyecto'
create_project_structure("mi_nuevo_proyecto")
```

Esto generará una estructura organizada con carpetas para `src` (sql, extract, transform, load, etc.), `config`, `connections`, y archivos base como `requirements.txt` y `README.md`.

### 4. Cargar y Leer Configuraciones

Una vez que tienes un archivo de configuración (que es un script de Python válido), puedes cargarlo y acceder a sus variables.

```python
from airflow_config import AirflowConfig

# Cargar configuración existente
config = AirflowConfig("mi_configuracion.py")

# Listar todas las variables cargadas
print(config.list_variables())

# Obtener una variable específica
valor = config.get_variable("MAIN_DB_POSTGRES_HOST", default="localhost")

# Verificar si existe una variable
if config.variable_exists("EVENTS_KAFKA_TOPIC"):
    print("Kafka topic configurado")
```

### 3. Obtener Parámetros de Conexión

Una característica útil es extraer todos los parámetros relacionados con una sección específica (por ejemplo, para configurar un `Hook` o `Operator` de Airflow).

```python
# Obtiene un diccionario con las variables de la sección 'main_db', 
# eliminando el prefijo y en minúsculas.
# Ej: MAIN_DB_POSTGRES_HOST -> postgres_host
db_params = config.get_connection_params("main_db")

print(db_params)
# Salida: {'postgres_host': '...', 'postgres_port': 5432, ...}
```

### 4. Validación

Puedes validar si una sección tiene variables configuradas.

```python
if config.validate_section("main_db"):
    print("La sección main_db es válida")
```

## Plantillas Disponibles

El sistema utiliza `TemplateStrategy` para generar configuraciones. Las plantillas soportadas actualmente son:

| Plantilla | Variables Generadas (Prefijos) |
|-----------|--------------------------------|
| `trino` | TRINO_HOST, TRINO_PORT, TRINO_USER, etc. |
| `postgresql` | POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, etc. |
| `sqlserver` | SQL_SERVER_HOST, SQL_SERVER_PORT, SQL_SERVER_DB, etc. |
| `mongodb` | MONGO_HOST, MONGO_PORT, MONGO_DB, etc. |
| `redis` | REDIS_HOST, REDIS_PORT, REDIS_DB, etc. |
| `bigquery` | BQ_PROJECT, BQ_DATASET, BQ_PRIVATE_KEY, etc. |
| `kafka` | KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, etc. |
| `api_keys` | API_BASE_URL, API_KEY, API_TIMEOUT, etc. |
| `dag_config` | DAG_OWNER, DAG_RETRIES, DAG_CATCHUP, etc. |

Puedes consultar las plantillas disponibles programáticamente:

```python
print(config.get_available_templates())
```

## Referencia de API

### Clase `AirflowConfig`

Ubicación: `src/airflow_config/core.py`

*   `__init__(config_file: str, template_generator: Optional[TemplateGenerator])`: Inicializa el gestor.
*   `create_etl_pipeline(source: str, destination: str)`: Crea configuración para ETL.
*   `create_data_pipeline(sections: Dict[str, str])`: Crea configuración con múltiples secciones.
*   `get_connection_params(section: str) -> Dict[str, Any]`: Obtiene parámetros limpios para una sección.
*   `validate_section(section: str) -> bool`: Valida si una sección tiene variables.
*   `get_variable(key: str, default: Any) -> Any`: Obtiene el valor de una variable.
*   `list_variables() -> List[str]`: Lista nombres de variables.
*   `variable_exists(key: str) -> bool`: Verifica existencia.
*   `get_available_templates() -> List[str]`: Lista plantillas soportadas.

### Funciones Auxiliares (`airflow_config`)

*   `create_etl_pipeline(source, destination, config_file)`: Helper para crear pipelines rápidamente.
*   `get_available_templates()`: Helper para listar plantillas.

---

> [!WARNING]
> **Nota sobre los Ejemplos**: El archivo `examples/basic_usage.py` está actualizado con la API actual. Sin embargo, `examples/advanced_usage.py` podría contener referencias a métodos antiguos.

## Pruebas

Para verificar el correcto funcionamiento de la librería, se incluye una suite de pruebas completa.

Debido a que el entorno puede no tener `pytest` instalado, se proporciona un script de ejecución personalizado.

### Ejecutar Pruebas

Para correr todas las pruebas, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python3 run_tests.py
```

Esto ejecutará:
1.  **Pruebas del Core**: Verificación de carga de configuración, acceso a variables y generación de plantillas.
2.  **Pruebas de Scaffolding**: Verificación de la creación de la estructura del proyecto.

Si todas las pruebas pasan, verás un mensaje final: `🎉 ALL TESTS PASSED`.
