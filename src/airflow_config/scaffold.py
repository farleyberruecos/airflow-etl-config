import logging
import os
from typing import Dict, Union

logger = logging.getLogger(__name__)

def create_project_structure(project_name: str = "ignition_anomaly_historical_sync"):
    """
    Creates a standard ETL project structure.
    
    Args:
        project_name: Name of the project directory to create.
    """
    base_dir = project_name
    
    # Configure basic logging if not configured
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    # Estructura de directorios y archivos (sin contenido)
    structure = {
        "src": {
            "__init__.py": "",
            "sql": {
                "__init__.py": "",
                "queries.py": "",
                "ddl_manager.py": ""
            },
            "extract": {
                "__init__.py": "",
                "extractor.py": ""
            },
            "transform": {
                "__init__.py": "",
                "cleaner.py": ""
            },
            "load": {
                "__init__.py": "",
                "loader.py": ""
            },
            "main": {
                "__init__.py": "",
                "orchestrator.py": ""
            },
            "factory": {
                "__init__.py": "",
                "executor_factory.py": ""
            },
            "dag": {
                "__init__.py": "",
                "workflow.py": ""
            }
        },
        "config": {
            "__init__.py": "",
            "config.py": ""
        },
        "connections": {
            "__init__.py": "",
            "source_db.py": "",
            "dwh_db.py": ""
        },
        "requirements.txt": "",
        "main.py": "",
        "README.md": ""
    }

    def create_files(path: str, content: Union[Dict, str]):
        if isinstance(content, dict):
            for name, subcontent in content.items():
                new_path = os.path.join(path, name)
                if "." in name:  # Es un archivo
                    with open(new_path, "w", encoding="utf-8") as f:
                        f.write(subcontent)
                    logger.info(f"📄 Creado: {new_path}")
                else:  # Es una carpeta
                    os.makedirs(new_path, exist_ok=True)
                    create_files(new_path, subcontent)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"📄 Creado: {path}")

    # Crear directorio base
    if os.path.exists(base_dir):
        logger.warning(f"⚠️  El directorio '{base_dir}' ya existe.")
    else:
        os.makedirs(base_dir, exist_ok=True)
        logger.info(f"🚀 Creando proyecto en: {base_dir}")
    
    # Crear estructura completa
    create_files(base_dir, structure)
    
    logger.info(f"\n✅ Proyecto '{base_dir}' creado exitosamente!")
