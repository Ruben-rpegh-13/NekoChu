@echo off
title NekoChu
cd /d "%~dp0"

echo ========================================
echo  NekoChu - Pikachu Desktop Pet
echo ========================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python no instalado.
    echo Descarga Python en: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Instalando dependencias...
pip install pygame --quiet

echo.
echo Iniciando NekoChu...
echo Presiona ESC para cerrar
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo Error al ejecutar. Presiona una tecla para salir.
    pause >nul
)
