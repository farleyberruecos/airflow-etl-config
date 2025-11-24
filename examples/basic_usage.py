"""
Basic usage example for airflow-config (Strategy Pattern)
"""

from airflow_config import AirflowConfig, create_etl_pipeline, create_project_structure

def main():
    print("🚀 Iniciando ejemplo de airflow-config...")

    # 1. Crear estructura de proyecto (Scaffolding)
    print("\n1. Generando estructura de proyecto...")
    create_project_structure("mi_nuevo_proyecto_etl")

    # 2. Crear una configuración de pipeline ETL
    print("\n2. Creando configuración ETL...")
    # Esto generará 'config.py' con plantillas para Postgres y BigQuery
    config = create_etl_pipeline(
        source="postgresql",
        destination="bigquery",
        config_file="mi_nuevo_proyecto_etl/config/config.py"
    )

    # 3. Cargar y leer variables
    print("\n3. Leyendo configuración...")
    # Recargamos desde el archivo generado
    config = AirflowConfig("mi_nuevo_proyecto_etl/config/config.py")
    
    # Listar variables disponibles
    vars = config.list_variables()
    print(f"Variables encontradas: {len(vars)}")
    for var in vars[:5]: # Mostrar algunas
        print(f" - {var}")

    # 4. Obtener parámetros de conexión limpios
    print("\n4. Obteniendo parámetros de conexión...")
    pg_params = config.get_connection_params("source")
    print(f"Parámetros Postgres: {pg_params}")

    print("\n✅ Ejemplo completado exitosamente.")

if __name__ == "__main__":
    main()