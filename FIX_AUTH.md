# ❌ Error de Autenticación PyPI

## Problema
Los tokens proporcionados están incompletos. Los tokens de PyPI son mucho más largos (100+ caracteres).

## Formato Correcto de Token
```
pypi-AgEIcHlwaS5vcmcCJGNiNzk4YjQzLWQ4YzItNGU4Ny04ZjZjLWE5ZjE3YjQ3ZTk4MgACKlszLCJiNDg3...
```
(continúa por muchos más caracteres)

## Solución

### 1. Obtener Tokens Completos

**TestPyPI:**
1. Ve a: https://test.pypi.org/manage/account/token/
2. Click en "Add API token"
3. Token name: `airflow-etl-config-upload`
4. Scope: "Entire account"
5. **COPIA EL TOKEN COMPLETO INMEDIATAMENTE** (solo se muestra una vez)

**PyPI:**
1. Ve a: https://pypi.org/manage/account/token/
2. Repite los mismos pasos

### 2. Actualizar ~/.pypirc

```bash
nano ~/.pypirc
```

Reemplaza las líneas de `password` con los tokens COMPLETOS:

```ini
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-TU_TOKEN_COMPLETO_DE_TESTPYPI_AQUI

[pypi]
username = __token__
password = pypi-TU_TOKEN_COMPLETO_DE_PYPI_AQUI
```

### 3. Verificar Permisos

```bash
chmod 600 ~/.pypirc
```

### 4. Reintentar Subida

```bash
cd /home/farley/Documents/airflow-config/airflow-etl-config
venv/bin/twine upload --repository testpypi dist/*
```

## Nota Importante
Los tokens deben comenzar con `pypi-` y ser muy largos (típicamente 200+ caracteres).
