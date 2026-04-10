@echo off
chcp 65001 >nul 2>&1
title QA Dashboard - Modo Desenvolvimento
setlocal EnableDelayedExpansion

echo ============================================================
echo       QA DASHBOARD - Modo Desenvolvimento (Teste)
echo ============================================================
echo.
echo [INFO] Sincronizando arquivos atualizados...
echo.

:: Define diretórios
set "ROOT_DIR=%~dp0"
set "RUNNER_DIR=%ROOT_DIR%Gerador_EXE\runner"
set "STAGING_DIR=%ROOT_DIR%Gerador_EXE\output\staging"
set "SOURCE_DIR=%ROOT_DIR%Testes_PDV"

:: ============================================================
:: SINCRONIZAÇÃO DE ARQUIVOS
:: Copia arquivos atualizados para staging (simula ambiente do EXE)
:: ============================================================

:: Cria diretórios se não existirem
if not exist "%STAGING_DIR%" mkdir "%STAGING_DIR%"
if not exist "%STAGING_DIR%\pages" mkdir "%STAGING_DIR%\pages"
if not exist "%STAGING_DIR%\tests" mkdir "%STAGING_DIR%\tests"
if not exist "%STAGING_DIR%\tests\e2e" mkdir "%STAGING_DIR%\tests\e2e"
if not exist "%STAGING_DIR%\tests\smoke" mkdir "%STAGING_DIR%\tests\smoke"
if not exist "%STAGING_DIR%\tests\unit" mkdir "%STAGING_DIR%\tests\unit"

:: Copia TODOS os arquivos .py da raiz (config, test_data, framework, conftest, test_encoding, etc)
echo [1/6] Copiando arquivos principais da raiz...
for %%f in ("%SOURCE_DIR%\*.py") do (
    copy /Y "%%f" "%STAGING_DIR%\" >nul 2>&1
)
echo    [OK] Arquivos principais copiados.

:: Copia Page Objects
echo [2/6] Copiando Page Objects...
xcopy /Y /Q "%SOURCE_DIR%\pages\*.py" "%STAGING_DIR%\pages\" >nul 2>&1
echo    [OK] Page Objects copiados.

:: Copia Testes E2E
echo [3/6] Copiando Testes E2E...
xcopy /Y /Q "%SOURCE_DIR%\tests\e2e\*.py" "%STAGING_DIR%\tests\e2e\" >nul 2>&1
echo    [OK] Testes E2E copiados.

:: Copia Testes Smoke
echo [4/6] Copiando Testes Smoke...
xcopy /Y /Q "%SOURCE_DIR%\tests\smoke\*.py" "%STAGING_DIR%\tests\smoke\" >nul 2>&1
echo    [OK] Testes Smoke copiados.

:: Copia Testes Unitários
echo [5/6] Copiando Testes Unitarios...
xcopy /Y /Q "%SOURCE_DIR%\tests\unit\*.py" "%STAGING_DIR%\tests\unit\" >nul 2>&1
echo    [OK] Testes Unitarios copiados.

:: Copia __init__.py
echo [6/6] Copiando arquivos de inicializacao...
copy /Y "%SOURCE_DIR%\pages\__init__.py" "%STAGING_DIR%\pages\__init__.py" >nul 2>&1
copy /Y "%SOURCE_DIR%\tests\__init__.py" "%STAGING_DIR%\tests\__init__.py" >nul 2>&1
copy /Y "%SOURCE_DIR%\tests\e2e\__init__.py" "%STAGING_DIR%\tests\e2e\__init__.py" >nul 2>&1
copy /Y "%SOURCE_DIR%\tests\smoke\__init__.py" "%STAGING_DIR%\tests\smoke\__init__.py" >nul 2>&1
copy /Y "%SOURCE_DIR%\tests\unit\__init__.py" "%STAGING_DIR%\tests\unit\__init__.py" >nul 2>&1
echo    [OK] Arquivos de inicializacao copiados.

echo.
:: ============================================================
:: IMPORTAÇÃO DO settings.json (se existir)
:: Busca em locais conhecidos e copia para staging
:: ============================================================
echo [EXTRA] Procurando settings.json existente...

set "SETTINGS_FOUND=0"
set "SETTINGS_SOURCE="

:: PRIORIDADE 1: QA Dashboard instalado (D:\)
if exist "D:\QA Dashboard\settings.json" (
    set "SETTINGS_SOURCE=D:\QA Dashboard\settings.json"
    set "SETTINGS_FOUND=1"
    echo    [OK] Encontrado em D:\QA Dashboard\
)

:: PRIORIDADE 2: Program Files (instalação padrão)
if "!SETTINGS_FOUND!"=="0" (
    if exist "C:\Program Files\QA Dashboard\settings.json" (
        set "SETTINGS_SOURCE=C:\Program Files\QA Dashboard\settings.json"
        set "SETTINGS_FOUND=1"
        echo    [OK] Encontrado em C:\Program Files\QA Dashboard\
    )
)

:: PRIORIDADE 3: Pasta do usuário
if "!SETTINGS_FOUND!"=="0" (
    if exist "%USERPROFILE%\QA Dashboard\settings.json" (
        set "SETTINGS_SOURCE=%USERPROFILE%\QA Dashboard\settings.json"
        set "SETTINGS_FOUND=1"
        echo    [OK] Encontrado em %USERPROFILE%\QA Dashboard\
    )
)

:: PRIORIDADE 4: Staging anterior (backup)
if "!SETTINGS_FOUND!"=="0" (
    if exist "%STAGING_DIR%\settings.json" (
        echo    [OK] Usando settings.json do staging anterior.
        set "SETTINGS_FOUND=1"
        goto :skip_copy_settings
    )
)

:: Se encontrou, copia
if "!SETTINGS_FOUND!"=="1" (
    copy /Y "!SETTINGS_SOURCE!" "%STAGING_DIR%\settings.json" >nul 2>&1
    echo    [OK] Settings importado! Campos preenchidos automaticamente.
) else (
    echo    [INFO] Nenhum settings.json encontrado.
    echo    [INFO] Use 'Importar Settings' no Dashboard para carregar depois.
)

:skip_copy_settings

echo.
echo ============================================================
echo [SUCESSO] Todos os arquivos sincronizados!
echo ============================================================
echo.
echo [INFO] Iniciando QA Dashboard em modo desenvolvimento...
echo [INFO] Projeto: %STAGING_DIR%
echo.

:: ============================================================
:: EXECUÇÃO DO DASHBOARD
:: Usa o staging (simula ambiente do EXE compilado)
:: ============================================================

cd /d "%RUNNER_DIR%"
python app_runner.py

:: Volta ao diretório original
cd /d "%ROOT_DIR%"

echo.
echo [INFO] Dashboard encerrado.
pause
