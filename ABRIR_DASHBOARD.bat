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
:: Robocopy /MIR: espelho completo e recursivo (só copia o que mudou)
:: /XF settings.json → preserva settings.json do staging
:: /XD __pycache__ .git → ignora caches e git
:: /NFL /NDL /NJH /NJS → log silencioso
:: ============================================================

echo [1/1] Sincronizando Testes_PDV para staging...
:: /E = recursivo sem deletar extras do staging (preserva settings.json, scripts, runner files)
:: /XD __pycache__ .git = ignora caches
:: /XF *.pyc settings.json = ignora bytecode e preserva settings
:: /MIR = espelho real (deleta do staging o que foi removido/movido no fonte)
:: /NFL /NDL /NJH /NJS = log silencioso (sem listagem de arquivos/dirs)
robocopy "%SOURCE_DIR%" "%STAGING_DIR%" /MIR /XD __pycache__ .git /XF *.pyc settings.json /NFL /NDL /NJH /NJS /NC /NS

:: Robocopy: 0-7 = sucesso (bit flags). 8+ = erro real.
if %ERRORLEVEL% GEQ 8 (
    echo.
    echo [ERRO] Falha na sincronizacao! Robocopy retornou: %ERRORLEVEL%
    pause
    exit /b 1
)
echo    [OK] Sincronizacao completa ^(pages, tests, subdirs, configs^).

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
