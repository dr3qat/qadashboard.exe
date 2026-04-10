@echo off
chcp 65001 >nul 2>&1
title Iniciando Automacao PDV...
setlocal EnableDelayedExpansion

:: Obter diretório do script
set "SCRIPT_DIR=%~dp0"
:: Obter diretório pai (onde está o EXE)
for %%i in ("%SCRIPT_DIR%..") do set "APP_DIR=%%~fi"

:: ============================================================
:: VERIFICAÇÃO RÁPIDA DO AMBIENTE
:: ============================================================

set ERROS=0
set AVISOS=0

:: Verificar Java
java -version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :BuscarJava
    if "!JAVA_FOUND!"=="0" set /a ERROS+=1
)

:: Verificar Node.js
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :BuscarNode
    if "!NODE_FOUND!"=="0" set /a ERROS+=1
)

:: Verificar Appium
appium --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :BuscarAppium
    if "!APPIUM_FOUND!"=="0" set /a ERROS+=1
)

:: Verificar adb
adb version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :BuscarAdb
    if "!ADB_FOUND!"=="0" set /a ERROS+=1
)

:: ============================================================
:: DECISÃO
:: ============================================================

if %ERROS% EQU 0 (
    :: Tudo OK - iniciar programa diretamente
    if exist "%APP_DIR%\PainelTestes.exe" (
        start "" "%APP_DIR%\PainelTestes.exe"
    ) else (
        echo [ERRO] Executavel nao encontrado: %APP_DIR%\PainelTestes.exe
        pause
    )
    exit /b 0
)

:: Existem erros - mostrar menu
cls
echo ============================================================
echo           AUTOMACAO PDV MOBILE - VERIFICACAO
echo ============================================================
echo.
echo [!] Algumas dependencias nao foram encontradas.
echo.
echo Dependencias necessarias:
echo.

:: Mostrar status de cada dependência com detalhes
java -version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=3" %%g in ('java -version 2^>^&1 ^| findstr /i "version"') do (
        echo    [OK] Java %%g
    )
) else (
    call :BuscarJava
    if "!JAVA_FOUND!"=="1" (
        echo    [OK] Java (encontrado em !JAVA_PATH!)
    ) else (
        echo    [X]  Java - NAO ENCONTRADO
    )
)

node --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('node --version') do (
        echo    [OK] Node.js %%v
    )
) else (
    call :BuscarNode
    if "!NODE_FOUND!"=="1" (
        echo    [OK] Node.js (encontrado em !NODE_PATH!)
    ) else (
        echo    [X]  Node.js - NAO ENCONTRADO
    )
)

appium --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('appium --version') do (
        echo    [OK] Appium v%%v
    )
) else (
    call :BuscarAppium
    if "!APPIUM_FOUND!"=="1" (
        echo    [OK] Appium (encontrado em !APPIUM_PATH!)
    ) else (
        echo    [X]  Appium - NAO ENCONTRADO
    )
)

adb version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] Android SDK (adb)
) else (
    call :BuscarAdb
    if "!ADB_FOUND!"=="1" (
        echo    [OK] Android SDK (encontrado em !ADB_PATH!)
    ) else (
        echo    [X]  Android SDK (adb) - NAO ENCONTRADO
    )
)

echo.
echo ============================================================
echo.
echo O que deseja fazer?
echo.
echo   [1] Instalar dependencias automaticamente
echo   [2] Abrir programa mesmo assim (pode falhar)
echo   [3] Apenas verificar ambiente (sem instalar)
echo   [4] Cancelar
echo.
echo ============================================================
echo.

choice /c 1234 /n /m "Escolha uma opcao (1/2/3/4): "

if %ERRORLEVEL% EQU 1 (
    echo.

    :: Verificar se está rodando como administrador
    net session >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo ============================================================
        echo    [!] ATENCAO: Permissao de Administrador Necessaria
        echo ============================================================
        echo.
        echo    A instalacao de dependencias requer permissoes de
        echo    administrador para:
        echo      - Instalar Java, Node.js e Appium
        echo      - Configurar variaveis de ambiente
        echo.
        echo    O que deseja fazer?
        echo.
        echo    [1] Reiniciar como Administrador (recomendado)
        echo    [2] Tentar instalar mesmo assim (pode falhar)
        echo    [3] Cancelar
        echo.
        choice /c 123 /n /m "Escolha (1/2/3): "

        if !ERRORLEVEL! EQU 1 (
            echo.
            echo    Reiniciando com permissoes de administrador...
            echo.
            :: Reiniciar o script como admin
            powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
            exit /b 0
        )

        if !ERRORLEVEL! EQU 3 (
            echo.
            echo    Operacao cancelada.
            pause
            exit /b 0
        )
    )

    echo Iniciando instalacao de dependencias...
    echo.

    :: Executar instalador de dependências
    if exist "%SCRIPT_DIR%instalar_dependencias.bat" (
        call "%SCRIPT_DIR%instalar_dependencias.bat"
    ) else (
        echo [ERRO] Script de instalacao nao encontrado!
        echo        Procurado em: %SCRIPT_DIR%instalar_dependencias.bat
        pause
        exit /b 1
    )

    echo.
    echo Deseja instalar o Android SDK tambem? (S/N)
    choice /c SN /n
    if !ERRORLEVEL! EQU 1 (
        if exist "%SCRIPT_DIR%instalar_android_sdk.bat" (
            call "%SCRIPT_DIR%instalar_android_sdk.bat"
        )
    )

    echo.
    echo ============================================================
    echo    Instalacao concluida!
    echo ============================================================
    echo.
    echo    IMPORTANTE: Reinicie o computador para aplicar todas
    echo                as mudancas nas variaveis de ambiente.
    echo.
    echo    Apos reiniciar, execute este programa novamente.
    echo.
    pause
    exit /b 0
)

if %ERRORLEVEL% EQU 2 (
    echo.
    echo Iniciando programa...
    echo.
    echo [AVISO] Algumas funcionalidades podem nao funcionar!
    echo.

    if exist "%APP_DIR%\PainelTestes.exe" (
        start "" "%APP_DIR%\PainelTestes.exe"
    ) else (
        echo [ERRO] Executavel nao encontrado: %APP_DIR%\PainelTestes.exe
        pause
    )
    exit /b 0
)

if %ERRORLEVEL% EQU 3 (
    echo.
    echo Executando verificacao completa do ambiente...
    echo.
    if exist "%SCRIPT_DIR%verificar_ambiente.bat" (
        call "%SCRIPT_DIR%verificar_ambiente.bat"
    ) else (
        echo [ERRO] Script de verificacao nao encontrado!
    )
    pause
    exit /b 0
)

if %ERRORLEVEL% EQU 4 (
    echo.
    echo Operacao cancelada.
    exit /b 0
)

exit /b 0

:: ============================================================
:: FUNCOES AUXILIARES
:: ============================================================

:BuscarJava
set "JAVA_FOUND=0"
set "JAVA_PATH="
for %%P in (
    "%ProgramFiles%\Microsoft\jdk-17*\bin\java.exe"
    "%ProgramFiles%\Java\jdk-17*\bin\java.exe"
    "%ProgramFiles%\Eclipse Adoptium\jdk-17*\bin\java.exe"
) do (
    if exist "%%~P" (
        set "JAVA_FOUND=1"
        set "JAVA_PATH=%%~P"
        set "PATH=!PATH!;%%~dpP"
        goto :eof
    )
)
goto :eof

:BuscarNode
set "NODE_FOUND=0"
set "NODE_PATH="
for %%P in (
    "%ProgramFiles%\nodejs\node.exe"
    "%LOCALAPPDATA%\Programs\nodejs\node.exe"
) do (
    if exist "%%~P" (
        set "NODE_FOUND=1"
        set "NODE_PATH=%%~P"
        set "PATH=!PATH!;%%~dpP"
        goto :eof
    )
)
goto :eof

:BuscarAppium
set "APPIUM_FOUND=0"
set "APPIUM_PATH="
for %%P in (
    "%APPDATA%\npm\appium.cmd"
    "%LOCALAPPDATA%\npm\appium.cmd"
) do (
    if exist "%%~P" (
        set "APPIUM_FOUND=1"
        set "APPIUM_PATH=%%~P"
        goto :eof
    )
)
goto :eof

:BuscarAdb
set "ADB_FOUND=0"
set "ADB_PATH="
for %%P in (
    "%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
    "%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe"
) do (
    if exist "%%~P" (
        set "ADB_FOUND=1"
        set "ADB_PATH=%%~P"
        set "PATH=!PATH!;%%~dpP"
        goto :eof
    )
)
goto :eof
