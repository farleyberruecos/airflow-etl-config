#!/bin/bash
# Script interactivo para configurar credenciales de PyPI

set -e

echo "🔐 Configuración de Credenciales PyPI"
echo "======================================"
echo ""
echo "Este script te ayudará a configurar tus credenciales de PyPI de forma segura."
echo ""

# Verificar si ya existe .pypirc
if [ -f ~/.pypirc ]; then
    echo "⚠️  Ya existe un archivo ~/.pypirc"
    read -p "¿Deseas sobrescribirlo? (s/n): " overwrite
    if [ "$overwrite" != "s" ]; then
        echo "Operación cancelada."
        exit 0
    fi
    echo "Creando backup en ~/.pypirc.backup"
    cp ~/.pypirc ~/.pypirc.backup
fi

echo ""
echo "📝 Necesitas obtener tus tokens de API:"
echo "   - PyPI: https://pypi.org/manage/account/token/"
echo "   - TestPyPI: https://test.pypi.org/manage/account/token/"
echo ""
echo "IMPORTANTE: Los tokens comienzan con 'pypi-' y son muy largos"
echo ""

# Solicitar token de TestPyPI
read -sp "Ingresa tu token de TestPyPI: " testpypi_token
echo ""

# Solicitar token de PyPI
read -sp "Ingresa tu token de PyPI: " pypi_token
echo ""
echo ""

# Validar que los tokens no estén vacíos
if [ -z "$testpypi_token" ] || [ -z "$pypi_token" ]; then
    echo "❌ Error: Los tokens no pueden estar vacíos"
    exit 1
fi

# Validar formato básico (deben empezar con pypi-)
if [[ ! "$testpypi_token" =~ ^pypi- ]] || [[ ! "$pypi_token" =~ ^pypi- ]]; then
    echo "⚠️  Advertencia: Los tokens deberían comenzar con 'pypi-'"
    read -p "¿Continuar de todas formas? (s/n): " continue
    if [ "$continue" != "s" ]; then
        echo "Operación cancelada."
        exit 0
    fi
fi

# Crear archivo .pypirc
echo "📄 Creando archivo ~/.pypirc..."

cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = $pypi_token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = $testpypi_token
EOF

# Establecer permisos seguros
chmod 600 ~/.pypirc

echo ""
echo "✅ Archivo ~/.pypirc creado exitosamente"
echo ""
echo "🔒 Permisos configurados: 600 (solo tú puedes leer/escribir)"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Verifica: cat ~/.pypirc"
echo "   2. Prueba subir a TestPyPI: make publish-test"
echo "   3. Si funciona, sube a PyPI: make publish"
echo ""
