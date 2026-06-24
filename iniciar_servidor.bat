@echo off
REM Script para iniciar o gerenciador de servidor SOS 102
REM Este script mantém o servidor rodando continuamente (24/7)

setlocal enabledelayedexpansion

title SOS 102 - Gerenciador de Servidor 24/7
color 0A

cd /d "%~dp0"

echo.
echo ========================================
echo    SOS 102 - SERVIDOR 24/7
echo ========================================
echo.
echo Iniciando gerenciador de servidor...
echo Servidor rodara continuamente com reinicio automatico!
echo.
echo Acesse em seu navegador:
echo   http://localhost:8000
echo.
echo Pressione Ctrl+C para ENCERRAR completamente
echo.

python gerenciador_servidor.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERRO ao iniciar o servidor!
    echo ========================================
    echo.
    echo Verifique:
    echo 1. Python esta instalado?
    echo 2. Arquivo gerenciador_servidor.py existe?
    echo 3. Voce tem permissao na pasta?
    echo.
    pause
)

