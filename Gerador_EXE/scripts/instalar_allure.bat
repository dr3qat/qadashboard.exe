@echo off
echo ==========================================
echo      INSTALANDO ALLURE + COMBINE (ARQUIVO UNICO)
echo ==========================================
echo.

:: 1. INSTALAR BIBLIOTECA PYTHON (Gera o arquivo unico portavel)
echo [1/2] Instalando allure-combine via PIP...
python -m pip install allure-combine --upgrade
if %errorlevel%==0 (
    echo [OK] Biblioteca allure-combine instalada.
) else (
    echo [ERRO] Falha ao instalar allure-combine. Verifique seu Python.
)
echo.

:: 2. INSTALAR ALLURE CLI (Java - Gerador base)
echo [2/2] Verificando Allure Commandline...
call allure --version >nul 2>nul
if %errorlevel%==0 (
    echo [INFO] Allure CLI ja esta instalado.
    goto :FIM
)

:: Tenta via NPM (Geralmente o mais confiavel se tiver Node)
call npm --version >nul 2>nul
if %errorlevel%==0 (
    echo [INFO] Node.js detectado. Instalando via NPM...
    call npm install -g allure-commandline
    goto :FIM
)

:: Tenta via Winget
echo [AVISO] NPM nao encontrado. Tentando Winget...
winget install -e --id Qameta.Allure --accept-source-agreements --accept-package-agreements

:FIM
echo.
echo ==========================================
echo   CONCLUIDO! FECHANDO EM 5 SEGUNDOS...
echo ==========================================
timeout /t 5
exit