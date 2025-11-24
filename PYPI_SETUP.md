# Configuración de Credenciales PyPI

## 🔐 Paso 1: Obtener Tokens de API

### Para PyPI (Producción)
1. Ve a https://pypi.org/manage/account/token/
2. Crea un nuevo token con scope "Entire account" (o específico para el proyecto después de la primera subida)
3. **Copia el token inmediatamente** (solo se muestra una vez)

### Para TestPyPI (Pruebas)
1. Ve a https://test.pypi.org/manage/account/token/
2. Crea un nuevo token con scope "Entire account"
3. **Copia el token inmediatamente**

## 📝 Paso 2: Crear archivo .pypirc

Tienes dos opciones para configurar tus credenciales.

### Opción A: Usando el Script Automático (Recomendado)

El proyecto incluye un script que facilita esta configuración y maneja los permisos de seguridad automáticamente.

1. Abre el archivo `create_pypirc_temp.sh` y edita las variables `PYPI_TOKEN` y `TESTPYPI_TOKEN` con tus tokens reales.
2. Ejecuta los siguientes comandos:

```bash
# Dar permisos de ejecución
chmod +x create_pypirc_temp.sh

# Ejecutar el script (se auto-eliminará al finalizar)
./create_pypirc_temp.sh
```

### Opción B: Configuración Manual

Si prefieres hacerlo manualmente, ejecuta estos comandos:

```bash
# Crear el archivo .pypirc en tu home
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
EOF

# Asegurar permisos correctos (solo tú puedes leer/escribir)
chmod 600 ~/.pypirc
```

**IMPORTANTE**: Si usas la opción manual, reemplaza `pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` con tus tokens reales.

## ✅ Paso 3: Verificar Configuración

```bash
# Ver el archivo (asegúrate de que los tokens estén correctos)
cat ~/.pypirc

# Verificar permisos
ls -la ~/.pypirc
# Debe mostrar: -rw------- (600)
```

## 🚀 Paso 4: Subir a TestPyPI (Prueba)

```bash
cd /home/farley/Documents/airflow-config/airflow-config

# Activar entorno virtual
source venv/bin/activate

# Subir a TestPyPI
make publish-test
# O manualmente:
# twine upload --repository testpypi dist/*
```

## 🧪 Paso 5: Probar Instalación desde TestPyPI

```bash
# En un nuevo terminal o entorno virtual limpio
pip install --index-url https://test.pypi.org/simple/ --no-deps airflow-etl-config

# Probar que funciona
python -c "from airflow_config import create_etl_pipeline; print('✅ Instalación exitosa!')"
```

## 📦 Paso 6: Subir a PyPI (Producción)

**Solo después de verificar que TestPyPI funciona correctamente:**

```bash
cd /home/farley/Documents/airflow-config/airflow-config
source venv/bin/activate

# Subir a PyPI producción
make publish
# O manualmente:
# twine upload dist/*
```

## 🔍 Verificar en PyPI

Después de subir, verifica en:
- TestPyPI: https://test.pypi.org/project/airflow-etl-config/
- PyPI: https://pypi.org/project/airflow-etl-config/

## ⚠️ Notas de Seguridad

1. **Nunca** compartas tus tokens de API
2. **Nunca** subas el archivo `.pypirc` a git
3. Si un token se compromete, revócalo inmediatamente en PyPI
4. Considera usar tokens con scope específico de proyecto después de la primera subida

## 🔄 Actualizar Versión

Para futuras actualizaciones:

1. Actualiza la versión en `setup.py` (ej: `1.0.0` → `1.0.1`)
2. Reconstruye: `make build`
3. Sube: `make publish-test` o `make publish`
