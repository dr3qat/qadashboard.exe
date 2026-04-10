@echo off
chcp 65001 >nul 2>&1
title QA Dashboard - Inicialização Validada
setlocal EnableDelayedExpansion

:: ============================================================
:: SCRIPT DE INICIALIZAÇÃO VALIDADA
:: Atualiza variáveis de ambiente e inicia o executável
:: ============================================================

echo ============================================================
echo         QA DASHBOARD - Inicializacao Validada
echo ============================================================
echo.

:: Determina o diretório do aplicativo (onde está este script)
set "APP_DIR=%~dp0.."
cd /d "%APP_DIR%"

echo [INFO] Atualizando variaveis de ambiente...
echo.

:: ============================================================
:: ATUALIZAÇÃO DO PATH
:: Força reload das variáveis de ambiente do registro
:: ============================================================

:: Lê PATH do sistema
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SystemPath=%%b"

:: Lê PATH do usuário
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "UserPath=%%b"

:: Combina os dois PATHs
set "PATH=%SystemPath%;%UserPath%"

echo [OK] PATH atualizado com sucesso.
echo.

:: ============================================================
:: VALIDAÇÃO RÁPIDA DAS DEPENDÊNCIAS CRÍTICAS
:: ============================================================

set "CRITICOS_OK=1"

:: Verifica Java
java -version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Java nao encontrado no PATH.
    echo         Alguns recursos podem nao funcionar.
    echo         Recomendado: Reiniciar o computador apos instalacao.
    echo.
    set "CRITICOS_OK=0"
)

:: Verifica Node.js
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Node.js nao encontrado no PATH.
    echo         Alguns recursos podem nao funcionar.
    echo         Recomendado: Reiniciar o computador apos instalacao.
    echo.
    set "CRITICOS_OK=0"
)

:: Verifica Appium
appium --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Appium nao encontrado no PATH.
    echo         O programa ira tentar localizar automaticamente.
    echo.
)

:: ============================================================
:: INICIAR APLICATIVO
:: ============================================================

if "%CRITICOS_OK%"=="0" (
    echo ============================================================
    echo [ATENCAO] Algumas dependencias nao estao disponiveis no PATH.
    echo.
    echo Opcoes:
    echo  1. Reinicie o computador para atualizar o PATH completamente
    echo  2. Continue mesmo assim (o programa tentara localizar automaticamente)
    echo.
    echo ============================================================
    echo.

    choice /C 12 /M "Escolha uma opcao (1=Reiniciar depois, 2=Continuar)"

    if errorlevel 2 (
        echo.
        echo [OK] Continuando com inicializacao...
        echo.
    ) else (
        echo.
        echo [INFO] Fechando. Reinicie o computador e execute novamente.
        timeout /t 3 >nul
        exit /b 0
    )
)

echo [INFO] Iniciando QA Dashboard...
echo.

:: Inicia o executável em segundo plano
start "" "%APP_DIR%\QA_Dashboard.exe"

:: Aguarda 2 segundos e fecha este prompt
timeout /t 2 >nul
exit
