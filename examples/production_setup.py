"""
Production setup example for airflow-config
"""

from airflow_config import AirflowConfig, create_config_template

def setup_production_environment():
    """Setup a complete production environment configuration"""
    
    print("🚀 Setting up production Airflow configuration...")
    
    # First, create a comprehensive template
    create_config_template("production_template.py")
    print("📝 Production template created")
    
    # Create production configuration
    config = AirflowConfig("production.py")
    
    print("\n🔧 Configuring production settings...")
    
    # High-availability database configuration
    config.set_database_config(
        conn_id="airflow_production_ha",
        host="airflow-postgresql-ha.production.svc.cluster.local",
        port=5432,
        schema="airflow_prod",
        login="airflow_prod_user",
        password="${AIRFLOW_DB_PASSWORD}"  # From Kubernetes secrets
    )
    
    # Production scheduling with high concurrency
    config.set_scheduling_config(
        default_timezone="UTC",
        default_retries=5,
        default_retry_delay_minutes=10,
        max_active_runs=20,
        catchup_by_default=False
    )
    
    # Enterprise email configuration
    config.set_email_config(
        smtp_host="smtp.office365.com",
        smtp_port=587,
        smtp_starttls=True,
        smtp_user="airflow-alerts@company.com",
        smtp_password="${OFFICE365_PASSWORD}",
        default_email="data-engineering@company.com"
    )
    
    # Comprehensive monitoring and observability
    config.set_monitoring_config(
        log_level="INFO",
        remote_logging=True,
        metrics_enabled=True,
        statsd_enabled=True
    )
    
    # Production DAG configuration
    config.set_dag_config(
        dag_owner="data_engineering",
        default_pool="default_pool",
        pool_slots=512,
        parallelism=128,
        dag_concurrency=64
    )
    
    print("✅ Core configuration set")
    
    # Production feature flags
    print("\n🚩 Setting up feature flags...")
    production_flags = {
        "FEATURE_DAG_VERSIONING": True,
        "FEATURE_ADVANCED_MONITORING": True,
        "FEATURE_AUTO_SCALING": True,
        "FEATURE_BACKUP_AUTOMATION": True,
        "FEATURE_DISASTER_RECOVERY": True,
        "FEATURE_ROLLING_DEPLOYMENTS": False,  # Not yet enabled
        "FEATURE_CANARY_DEPLOYMENTS": False,   # Not yet enabled
    }
    
    for flag, value in production_flags.items():
        config.set_custom_variable(flag, value, f"Production feature flag: {flag}")
    
    # Infrastructure configuration
    print("\n🏗️ Configuring infrastructure...")
    config.set_custom_variable("CLOUD_PROVIDER", "AWS", "Cloud infrastructure provider")
    config.set_custom_variable("AWS_REGION", "us-east-1", "Primary AWS region")
    config.set_custom_variable("AWS_BACKUP_REGION", "us-west-2", "Backup AWS region")
    config.set_custom_variable("K8S_NAMESPACE", "airflow-production", "Kubernetes namespace")
    config.set_custom_variable("K8S_CLUSTER", "prod-cluster-01", "Kubernetes cluster name")
    
    # Data infrastructure
    config.set_custom_variable("DATA_LAKE_BUCKET", "company-datalake-prod", "Production data lake S3 bucket")
    config.set_custom_variable("DATA_WAREHOUSE_SCHEMA", "analytics_prod", "Production data warehouse schema")
    config.set_custom_variable("REDSHIFT_CLUSTER", "analytics-prod", "Redshift cluster identifier")
    
    # Security and compliance
    config.set_custom_variable("COMPLIANCE_STANDARD", "SOC2", "Security compliance standard")
    config.set_custom_variable("DATA_ENCRYPTION", True, "Enable data encryption at rest")
    config.set_custom_variable("NETWORK_ISOLATION", True, "Network isolation enabled")
    config.set_custom_variable("AUDIT_LOGGING", True, "Comprehensive audit logging")
    
    # Performance tuning
    config.set_custom_variable("WORKER_COUNT", 8, "Number of Airflow workers")
    config.set_custom_variable("WORKER_MEMORY_LIMIT", "4Gi", "Worker memory limit")
    config.set_custom_variable("WORKER_CPU_LIMIT", "2", "Worker CPU limit")
    config.set_custom_variable("SCHEDULER_MEMORY_LIMIT", "8Gi", "Scheduler memory limit")
    
    # External services configuration
    print("\n🔗 Configuring external services...")
    config.set_custom_variable("SNOWFLAKE_ACCOUNT", "company_prod", "Snowflake account")
    config.set_custom_variable("SNOWFLAKE_WAREHOUSE", "transform_wh", "Snowflake warehouse")
    config.set_custom_variable("DATABRICKS_HOST", "dbc-company-prod.cloud.databricks.com", "Databricks workspace")
    config.set_custom_variable("FIVETRAN_API_KEY", "${FIVETRAN_API_KEY}", "Fivetran API key")
    config.set_custom_variable("DBT_CLOUD_API_KEY", "${DBT_CLOUD_API_KEY}", "dbt Cloud API key")
    
    # Alerting and notifications
    config.set_custom_variable("PAGERDUTY_SERVICE_KEY", "${PAGERDUTY_SERVICE_KEY}", "PagerDuty integration key")
    config.set_custom_variable("SLACK_WEBHOOK_URL", "${SLACK_WEBHOOK_URL}", "Slack incoming webhook")
    config.set_custom_variable("OPSGENIE_API_KEY", "${OPSGENIE_API_KEY}", "OpsGenie API key")
    
    # Data processing limits
    config.set_custom_variable("MAX_DAG_RUN_TIME_HOURS", 24, "Maximum DAG run time")
    config.set_custom_variable("MAX_TASK_RETRIES", 5, "Maximum task retry attempts")
    config.set_custom_variable("DATA_PROCESSING_TIMEOUT", 7200, "Data processing timeout in seconds")
    
    # Save the complete production configuration
    config.save()
    
    print("\n✅ Production configuration completed!")
    
    # Generate configuration report
    generate_production_report(config)

def generate_production_report(config):
    """Generate a production configuration report"""
    print("\n" + "="*60)
    print("📊 PRODUCTION CONFIGURATION REPORT")
    print("="*60)
    
    # Basic statistics
    total_vars = len(config.list_variables())
    summary = config.get_config_summary()
    
    print(f"📈 Total Variables: {total_vars}")
    print(f"🔍 Configuration Summary:")
    for section, count in summary.items():
        print(f"   - {section.title()}: {count} variables")
    
    # Feature flags status
    feature_flags = config.get_feature_flags()
    enabled_flags = [flag for flag, enabled in feature_flags.items() if enabled]
    disabled_flags = [flag for flag, enabled in feature_flags.items() if not enabled]
    
    print(f"\n🚩 Feature Flags:")
    print(f"   ✅ Enabled: {len(enabled_flags)}")
    print(f"   ❌ Disabled: {len(disabled_flags)}")
    
    # Critical configuration checks
    critical_vars = [
        "AIRFLOW_DB_HOST",
        "DATA_LAKE_BUCKET", 
        "CLOUD_PROVIDER",
        "COMPLIANCE_STANDARD",
        "PAGERDUTY_SERVICE_KEY"
    ]
    
    missing_critical = config.validate_required_variables(critical_vars)
    
    if missing_critical:
        print(f"\n❌ MISSING CRITICAL VARIABLES: {missing_critical}")
        print("   Please configure these variables before deployment!")
    else:
        print(f"\n✅ All critical variables are configured")
    
    # Database configuration
    db_config = config.get_database_connection()
    print(f"\n🗄️  Database Configuration:")
    print(f"   - Host: {db_config['host']}")
    print(f"   - Port: {db_config['port']}")
    print(f"   - Schema: {db_config['schema']}")
    
    # DAG configuration
    dag_args = config.get_dag_default_args()
    print(f"\n📋 DAG Default Arguments:")
    print(f"   - Owner: {dag_args['owner']}")
    print(f"   - Retries: {dag_args['retries']}")
    print(f"   - Retry Delay: {dag_args['retry_delay']}")
    
    print(f"\n🎯 Configuration file: production.py")
    print("🚀 Ready for production deployment!")

if __name__ == "__main__":
    setup_production_environment()