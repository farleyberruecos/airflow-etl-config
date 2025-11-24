"""
Test script to verify the package installation and basic functionality
"""

try:
    # Test basic import
    import airflow_config
    from airflow_config import AirflowConfig
    from airflow_config import create_config_template
    
    print("✅ airflow_config imported successfully")
    
    # Test creating a config instance
    config = AirflowConfig("test_config.py")
    print("✅ AirflowConfig instance created")
    
    # Test setting some configuration
    config.set_database_config(host="test_host", port=5432)
    config.set_scheduling_config(default_retries=3)
    config.set_custom_variable("TEST_VAR", "test_value", "Test variable")
    print("✅ Configuration settings applied")
    
    # Test saving configuration
    config.save()
    print("✅ Configuration saved successfully")
    
    # Test template creation
    create_config_template("test_template.py")
    print("✅ Template created successfully")
    
    # Test query methods
    default_args = config.get_dag_default_args()
    print(f"✅ DAG default args: {default_args}")
    
    print("\n🎉 All tests passed! Package is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()