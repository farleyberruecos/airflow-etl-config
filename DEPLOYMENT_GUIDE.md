# Guía Completa de Despliegue a PyPI

Esta guía documenta el proceso completo y exitoso de despliegue del paquete `airflow-etl-config` a PyPI, incluyendo todos los archivos requeridos, configuraciones y pasos de verificación.

## 📋 Tabla de Contenidos

1. [Archivos Requeridos](#archivos-requeridos)
2. [Configuración de Credenciales](#configuración-de-credenciales)
3. [Proceso de Build](#proceso-de-build)
4. [Despliegue a TestPyPI](#despliegue-a-testpypi)
5. [Despliegue a PyPI Producción](#despliegue-a-pypi-producción)
6. [Verificación](#verificación)
7. [Solución de Problemas](#solución-de-problemas)

---

## 📁 Archivos Requeridos

### 1. Configuración del Paquete

#### `setup.py`
Archivo principal de configuración del paquete:

```python
from setuptools import setup, find_packages

setup(
    name="airflow-etl-config",  # Nombre en PyPI (con guiones)
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu.email@example.com",
    description="Python library for managing Apache Airflow configuration variables",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/airflow-config",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[],  # Dependencias de runtime (si las hay)
)
```

#### `pyproject.toml`
Configuración moderna de build system:

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm>=6.2"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --cov=airflow_config --cov-report=html --cov-report=term-missing --cov-fail-under=70"
testpaths = ["tests"]

[tool.coverage.run]
source = ["src/airflow_config"]
omit = ["*/tests/*", "*/test_*.py", "*/generator.py", "*/query.py"]
```

#### `MANIFEST.in`
Define qué archivos incluir en la distribución:

```
include README.md
include LICENSE
include DOCUMENTACION.md
include requirements.txt
recursive-include src *.py
recursive-exclude tests *
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

#### `requirements.txt`
Dependencias de desarrollo:

```
pytest>=7.0
pytest-cov>=4.0
black>=22.0
isort>=5.0
twine>=4.0
build>=0.10
```

### 2. Estructura del Proyecto

```
airflow-etl-config/
├── src/
│   └── airflow_config/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       ├── scaffold.py
│       └── exceptions.py
├── tests/
│   ├── conftest.py
│   ├── test_core.py
│   ├── test_utils.py
│   └── test_scaffold.py
├── setup.py
├── pyproject.toml
├── MANIFEST.in
├── requirements.txt
├── README.md
├── LICENSE
├── DOCUMENTACION.md
└── Makefile
```

**Nota Importante**: El nombre del directorio puede ser `airflow-etl-config`, pero el import en Python es `airflow_config` (con guión bajo).

---

## 🔐 Configuración de Credenciales

### 1. Crear Cuentas

- **TestPyPI**: https://test.pypi.org/account/register/
- **PyPI**: https://pypi.org/account/register/

### 2. Generar Tokens de API

#### Para TestPyPI:
1. Ve a: https://test.pypi.org/manage/account/token/
2. Click en "Add API token"
3. Token name: `airflow-etl-config`
4. Scope: "Entire account"
5. **Copia el token completo** (empieza con `pypi-` y tiene 100+ caracteres)

#### Para PyPI:
1. Ve a: https://pypi.org/manage/account/token/
2. Repite los mismos pasos

### 3. Configurar `~/.pypirc`

Crea el archivo `~/.pypirc` en tu directorio home:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-TU_TOKEN_COMPLETO_DE_PYPI_AQUI

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-TU_TOKEN_COMPLETO_DE_TESTPYPI_AQUI
```

**Establecer permisos seguros:**
```bash
chmod 600 ~/.pypirc
```

**⚠️ Importante:**
- El username **siempre** es `__token__` (literal)
- Los tokens son diferentes para PyPI y TestPyPI
- Los tokens son muy largos (100-200+ caracteres)
- Nunca compartas tus tokens

---

## 🏗️ Proceso de Build

### 1. Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar Dependencias de Build

```bash
pip install --upgrade pip
pip install build twine
```

### 3. Construir Paquetes de Distribución

```bash
python3 -m build
```

Esto genera:
- `dist/airflow_etl_config-1.0.0.tar.gz` (source distribution)
- `dist/airflow_etl_config-1.0.0-py3-none-any.whl` (wheel)

**Salida esperada:**
```
Successfully built airflow_etl_config-1.0.0.tar.gz and airflow_etl_config-1.0.0-py3-none-any.whl
```

---

## 🧪 Despliegue a TestPyPI

### 1. Subir a TestPyPI

```bash
twine upload --repository testpypi dist/*
```

**Salida esperada:**
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading airflow_etl_config-1.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.5/20.5 kB
Uploading airflow_etl_config-1.0.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 28.5/28.5 kB

View at:
https://test.pypi.org/project/airflow-etl-config/1.0.0/
```

### 2. Verificar en TestPyPI

Visita: https://test.pypi.org/project/airflow-etl-config/

### 3. Probar Instalación desde TestPyPI

```bash
# En un nuevo entorno virtual o terminal
pip install --index-url https://test.pypi.org/simple/ --no-deps airflow-etl-config

# Verificar que funciona
python3 -c "from airflow_config import create_etl_pipeline; print('✅ Instalación exitosa!')"
```

---

## 🚀 Despliegue a PyPI Producción

### 1. Subir a PyPI

**Solo después de verificar que TestPyPI funciona correctamente:**

```bash
twine upload dist/*
```

**Salida esperada:**
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading airflow_etl_config-1.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.5/20.5 kB
Uploading airflow_etl_config-1.0.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 28.5/28.5 kB

View at:
https://pypi.org/project/airflow-etl-config/1.0.0/
```

### 2. Verificar en PyPI

Visita: https://pypi.org/project/airflow-etl-config/

**Nota**: La interfaz web puede tardar 2-3 minutos en actualizar después de la subida.

---

## ✅ Verificación

### 1. Verificar con la API de PyPI

```bash
curl -s https://pypi.org/pypi/airflow-etl-config/json | grep '"name"'
```

**Salida esperada:**
```json
"name": "airflow-etl-config"
```

### 2. Instalar desde PyPI

```bash
pip install airflow-etl-config
```

### 3. Probar Funcionalidad

```python
from airflow_config import create_etl_pipeline, create_project_structure

# Crear configuración
create_etl_pipeline(
    source="postgresql",
    destination="bigquery",
    config_file="test_config.py"
)

# Crear estructura de proyecto
create_project_structure("mi_proyecto")

print("✅ Paquete funcionando correctamente!")
```

### 4. Verificar Metadatos

```bash
pip show airflow-etl-config
```

**Salida esperada:**
```
Name: airflow-etl-config
Version: 1.0.0
Summary: Python library for managing Apache Airflow configuration variables
Home-page: https://github.com/tuusuario/airflow-config
Author: Tu Nombre
License: UNKNOWN
Location: ...
Requires:
Required-by:
```

---

## 🛠️ Solución de Problemas

### Error: "Invalid or non-existent authentication information"

**Causa**: Token de API inválido o incompleto.

**Solución**:
1. Verifica que el token comience con `pypi-`
2. Asegúrate de copiar el token **completo** (100+ caracteres)
3. Verifica que el username sea `__token__` (literal)
4. Confirma que estás usando el token correcto (PyPI vs TestPyPI)

### Error: "File already exists"

**Causa**: Ya subiste esa versión anteriormente.

**Solución**:
1. Incrementa el número de versión en `setup.py`
2. Reconstruye: `python3 -m build`
3. Sube nuevamente: `twine upload dist/*`

### Error: "No module named 'build'"

**Causa**: Módulo `build` no instalado.

**Solución**:
```bash
pip install build twine
```

### La página web no aparece

**Causa**: Caché de PyPI tardando en actualizar.

**Solución**:
1. Espera 2-3 minutos
2. Verifica con la API: `curl https://pypi.org/pypi/airflow-etl-config/json`
3. Intenta instalar: `pip install airflow-etl-config`

---

## 📊 Checklist de Despliegue

- [ ] Archivos requeridos creados (`setup.py`, `pyproject.toml`, `MANIFEST.in`)
- [ ] Tests pasando con cobertura adecuada
- [ ] Tokens de API generados (TestPyPI y PyPI)
- [ ] Archivo `~/.pypirc` configurado con permisos 600
- [ ] Entorno virtual creado y activado
- [ ] Dependencias de build instaladas (`build`, `twine`)
- [ ] Paquetes construidos (`python3 -m build`)
- [ ] Subido a TestPyPI y verificado
- [ ] Instalación desde TestPyPI probada
- [ ] Subido a PyPI producción
- [ ] Instalación desde PyPI verificada
- [ ] Funcionalidad del paquete probada

---

## 🎯 Resultado Final

**Paquete publicado exitosamente:**
- **TestPyPI**: https://test.pypi.org/project/airflow-etl-config/1.0.0/
- **PyPI**: https://pypi.org/project/airflow-etl-config/1.0.0/

**Instalación:**
```bash
pip install airflow-etl-config
```

**Import:**
```python
from airflow_config import create_etl_pipeline, create_project_structure
```

---

## 📚 Referencias

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.pypa.io/)
