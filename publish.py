import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Ejecuta un comando y muestra el resultado"""
    print(f"Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode == 0:
        print("✅ Comando ejecutado exitosamente")
    else:
        print(f"❌ Error en comando: {cmd}")
    return result

def main():
    """Función principal del proceso de publicación"""
    print("🚀 Iniciando proceso de publicación...")
    
    # Verificar que estamos en el directorio correcto
    if not Path("setup.py").exists():
        print("❌ Error: No se encuentra setup.py")
        sys.exit(1)
    
    # Limpiar builds anteriores
    print("\n🗑️ Limpiando builds anteriores...")
    run_command("make clean")
    
    # Instalar dependencias de build
    print("\n📦 Instalando dependencias de build...")
    run_command("pip install build twine wheel")
    
    # Ejecutar tests
    print("\n🧪 Ejecutando tests...")
    run_command("make test")
    
    # Construir paquete
    print("\n🏗️ Construyendo paquete...")
    run_command("python -m build")
    
    # Verificar paquete
    print("\n🔍 Verificando paquete...")
    run_command("twine check dist/*")
    
    # Publicar en PyPI
    print("\n📤 Publicando en PyPI...")
    run_command("twine upload dist/*")
    
    print("\n🎉 ¡Proceso de publicación completado!")

if __name__ == "__main__":
    main()