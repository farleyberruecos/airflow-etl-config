import os
import sys
import shutil
import tempfile
import importlib.util
import logging

# Mock Airflow environment
os.makedirs("airflow/models", exist_ok=True)
os.makedirs("airflow/operators", exist_ok=True)
with open("airflow/__init__.py", "w") as f: f.write("class DAG: pass\n")
with open("airflow/models/__init__.py", "w") as f: f.write("class Variable: get = lambda k, default_var=None: default_var\n")
with open("airflow/operators/__init__.py", "w") as f: f.write("")
with open("airflow/operators/python.py", "w") as f: f.write("class PythonOperator: pass\n")
with open("airflow/operators/bash.py", "w") as f: f.write("class BashOperator: pass\n")

sys.path.append(os.getcwd())

# Import library
from airflow_config import AirflowConfig, create_etl_pipeline, create_project_structure

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TEST_RUNNER")

def run_test_core():
    logger.info("Running TestAirflowConfig...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = os.path.join(temp_dir, "config.py")
        
        # Test create_etl_pipeline
        create_etl_pipeline(
            source="postgresql",
            destination="bigquery",
            config_file=config_path
        )
        if not os.path.exists(config_path):
            raise Exception("Config file not created")
            
        # Test AirflowConfig loading
        config = AirflowConfig(config_path)
        if "SOURCE_POSTGRES_HOST" not in config.variables:
            raise Exception("Variables not loaded")
            
        # Test get_variable
        if config.get_variable("SOURCE_POSTGRES_HOST") != "localhost":
            raise Exception("get_variable failed")
            
        # Test get_connection_params
        params = config.get_connection_params("source")
        if params.get("postgres_host") != "localhost":
            raise Exception("get_connection_params failed")
            
        # Test generated functions
        spec = importlib.util.spec_from_file_location("generated_config", config_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["generated_config"] = module
        spec.loader.exec_module(module)
        
        if not hasattr(module, "SOURCE_POSTGRES_HOST"):
            raise Exception("Generated module missing variables")
            
    logger.info("✅ TestAirflowConfig PASSED")

def run_test_scaffold():
    logger.info("Running TestScaffold...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        project_name = os.path.join(temp_dir, "test_project")
        create_project_structure(project_name)
        
        if not os.path.exists(os.path.join(project_name, "src", "extract", "extractor.py")):
            raise Exception("Scaffold failed: missing files")
            
    logger.info("✅ TestScaffold PASSED")

if __name__ == "__main__":
    try:
        run_test_core()
        run_test_scaffold()
        print("\n🎉 ALL TESTS PASSED")
    except Exception as e:
        print(f"\n❌ TESTS FAILED: {e}")
        sys.exit(1)
    finally:
        # Cleanup mock airflow
        if os.path.exists("airflow"):
            shutil.rmtree("airflow")
