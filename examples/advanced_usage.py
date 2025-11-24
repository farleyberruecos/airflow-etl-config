# Archivo creado - pendiente de contenido
"""
Advanced usage example for airflow-config
"""

from airflow_config import AirflowConfig, create_config_template

def main():
    # First, create a template to see available options
    create_config_template("advanced_template.py")
    print("📝 Template created: advanced_template.py")
    
    # Create a production-ready configuration
    config = AirflowConfig("production_config.py")
    
    # Production database configuration
    config.set_database_config(
        conn_id="airflow_production",
        host="postgresql.production.svc.cluster.local",
        port=5432,
        schema="airflow_prod",
        login="airflow_prod_user",
        password="${DATABASE_PASSWORD}"  # Use environment variable
    )
    
    # Advanced scheduling configuration
    config.set_scheduling_config(
        default_timezone="America/New_York",
        default_retries=5,
        default_retry_delay_minutes=15,
        max_active_runs=10,
        catchup_by_default=False
    )
    
    # Production email configuration
    config.set_email_config(
        smtp_host="smtp.sendgrid.net",
        smtp_port=587,
        smtp_user="apikey",
        smtp_password="${SENDGRID_API_KEY}",
        default_email="alerts@company.com"
    )
    
    # Comprehensive monitoring
    config.set_monitoring_config(
        log_level="INFO",
        remote_logging=True,
        metrics_enabled=True,
        statsd_enabled=True
    )
    
    # DAG configuration for production
    config.set_dag_config(
        dag_owner="data_engineering",
        default_pool="default_pool",
        pool_slots=256,
        parallelism=64,
        dag_concurrency=32
    )
    
    # Feature flags for gradual rollout
    config.set_custom_variable("FEATURE_NEW_UI", True, "Enable new UI features")
    config.set_custom_variable("FEATURE_ANALYTICS", False, "Enable analytics dashboard")
    config.set_custom_variable("FEATURE_EXPERIMENTAL", True, "Experimental features")
    
    # Environment-specific variables
    config.set_custom_variable("ENVIRONMENT", "production", "Deployment environment")
    config.set_custom_variable("REGION", "us-east-1", "AWS region")
    
    # Data pipeline configuration
    config.set_custom_variable("DATA_LAKE_BUCKET", "company-datalake-prod", "Production data lake")
    config.set_custom_variable("WAREHOUSE_SCHEMA", "analytics_prod", "Data warehouse schema")
    config.set_custom_variable("BACKUP_ENABLED", True, "Enable automated backups")
    
    # API configurations
    config.set_custom_variable("API_TIMEOUT_SECONDS", 300, "API request timeout")
    config.set_custom_variable("API_MAX_RETRIES", 3, "API retry attempts")
    config.set_custom_variable("EXTERNAL_API_BASE_URL", "https://api.external-service.com", "External service API")
    
    # Batch processing settings
    config.set_custom_variable("BATCH_SIZE", 10000, "Default batch size for processing")
    config.set_custom_variable("MAX_CONCURRENT_TASKS", 8, "Maximum concurrent tasks")
    config.set_custom_variable("SUPPORTED_FORMATS", ["parquet", "csv", "json"], "Supported file formats")
    
    # Save the configuration
    config.save()
    
    print("✅ Production configuration created!")
    
    # Demonstrate advanced features
    print(f"📊 Configuration summary: {config.get_config_summary()}")
    
    # Get feature flags
    feature_flags = config.get_feature_flags()
    print(f"🚩 Feature flags: {feature_flags}")
    
    # Get all database-related variables
    db_vars = config.get_variables_by_prefix("AIRFLOW_DB")
    print(f"🗄️  Database variables: {list(db_vars.keys())}")
    
    # Validate critical production variables
    critical_vars = [
        "AIRFLOW_DB_HOST",
        "DATA_LAKE_BUCKET", 
        "ENVIRONMENT",
        "FEATURE_NEW_UI"
    ]
    missing = config.validate_required_variables(critical_vars)
    
    if missing:
        print(f"❌ Missing critical variables: {missing}")
    else:
        print("✅ All critical variables are configured")

if __name__ == "__main__":
    main()