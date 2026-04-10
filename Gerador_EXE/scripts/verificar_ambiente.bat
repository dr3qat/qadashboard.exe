@echo off
chcp 65001 >nul 2>&1
title Verificar Ambiente - Automacao PDV
setlocal EnableDelayedExpansion

echo ============================================================
echo       VERIFICACAO DE AMBIENTE - AUTOMACAO PDV MOBILE
echo ============================================================
echo.
echo Data/Hora: %DATE% %TIME%
echo Usuario: %USERNAME%
echo Computador: %COMPUTERNAME%
echo.
echo ============================================================
echo.

set ERROS=0
set AVISOS=0

:: ============================================================
:: [0/7] Verificar winget (Pré-requisito)
:: ============================================================
echo [0/7] Verificando winget (gerenciador de pacotes)...
echo ------------------------------------------------------------
winget --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('winget --version') do (
        echo    [OK] winget encontrado: %%v
    )
) else (
    echo    [AVISO] winget NAO encontrado
    echo           Necessario para instalacao automatica
    echo           Instale via Microsoft Store: "App Installer"
    set /a AVISOS+=1
)
echo.

:: ============================================================
:: [1/7] Verificar Java JDK
:: ============================================================
echo [1/7] Verificando Java JDK...
echo ------------------------------------------------------------
java -version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=3" %%g in ('java -version 2^>^&1 ^| findstr /i "version"') do (
        set "JAVA_VER=%%g"
    )
    echo    [OK] Java encontrado: !JAVA_VER!

    :: Verificar JAVA_HOME
    if defined JAVA_HOME (
        echo    [OK] JAVA_HOME: %JAVA_HOME%
    ) else (
        echo    [AVISO] JAVA_HOME nao definido (opcional)
        set /a AVISOS+=1
    )

    :: Verificar versão mínima (17+)
    echo !JAVA_VER! | findstr /r "\"1[789]\|\"2[0-9]" >nul
    if !ERRORLEVEL! NEQ 0 (
        echo    [AVISO] Recomendado Java 17 ou superior
        set /a AVISOS+=1
    )
) else (
    :: Tentar encontrar em caminhos conhecidos
    set "JAVA_FOUND=0"
    for %%P in (
        "%ProgramFiles%\Microsoft\jdk-17*\bin\java.exe"
        "%ProgramFiles%\Java\jdk-17*\bin\java.exe"
        "%ProgramFiles%\Eclipse Adoptium\jdk-17*\bin\java.exe"
    ) do (
        if exist "%%~P" (
            echo    [AVISO] Java encontrado mas NAO no PATH:
            echo           %%~P
            echo           Adicione ao PATH ou reinicie o computador
            set "JAVA_FOUND=1"
            set /a AVISOS+=1
        )
    )
    if "!JAVA_FOUND!"=="0" (
        echo    [ERRO] Java NAO encontrado!
        echo           Necessario: Java JDK 17 ou superior
        echo           Execute: instalar_dependencias.bat
        set /a ERROS+=1
    )
)
echo.

:: ============================================================
:: [2/7] Verificar Node.js
:: ============================================================
echo [2/7] Verificando Node.js...
echo ------------------------------------------------------------
node --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('node --version') do (
        echo    [OK] Node.js encontrado: %%v
    )

    :: Verificar versão mínima (18+)
    for /f "tokens=1 delims=v." %%m in ('node --version') do (
        set "NODE_MAJOR=%%m"
    )
    for /f "tokens=2 delims=v." %%m in ('node --version') do (
        set "NODE_MAJOR=%%m"
    )
) else (
    :: Tentar encontrar em caminhos conhecidos
    set "NODE_FOUND=0"
    for %%P in (
        "%ProgramFiles%\nodejs\node.exe"
        "%LOCALAPPDATA%\Programs\nodejs\node.exe"
    ) do (
        if exist "%%~P" (
            echo    [AVISO] Node.js encontrado mas NAO no PATH:
            echo           %%~P
            echo           Reinicie o computador para atualizar PATH
            set "NODE_FOUND=1"
            set /a AVISOS+=1
        )
    )
    if "!NODE_FOUND!"=="0" (
        echo    [ERRO] Node.js NAO encontrado!
        echo           Necessario: Node.js LTS (v18+)
        echo           Execute: instalar_dependencias.bat
        set /a ERROS+=1
    )
)
echo.

:: ============================================================
:: [3/7] Verificar npm
:: ============================================================
echo [3/7] Verificando npm...
echo ------------------------------------------------------------
npm --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('npm --version') do (
        echo    [OK] npm encontrado: v%%v
    )

    :: Mostrar local global de instalação
    for /f "tokens=*" %%p in ('npm config get prefix 2^>nul') do (
        echo    [INFO] npm global: %%p
    )
) else (
    echo    [ERRO] npm NAO encontrado!
    echo           (Instalado junto com Node.js)
    set /a ERROS+=1
)
echo.

:: ============================================================
:: [4/7] Verificar Appium
:: ============================================================
echo [4/7] Verificando Appium...
echo ------------------------------------------------------------
appium --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('appium --version') do (
        echo    [OK] Appium encontrado: v%%v
    )

    echo.
    echo    Verificando drivers instalados...
    appium driver list --installed 2>&1 | findstr /i "uiautomator2" >nul
    if !ERRORLEVEL! EQU 0 (
        echo    [OK] Driver UiAutomator2 instalado
        :: Mostrar versão do driver
        for /f "tokens=*" %%d in ('appium driver list --installed 2^>^&1 ^| findstr /i "uiautomator2"') do (
            echo    [INFO] %%d
        )
    ) else (
        echo    [AVISO] Driver UiAutomator2 NAO instalado
        echo            Execute: appium driver install uiautomator2
        set /a AVISOS+=1
    )
) else (
    :: Tentar encontrar em caminhos conhecidos
    set "APPIUM_FOUND=0"
    for %%P in (
        "%APPDATA%\npm\appium.cmd"
        "%LOCALAPPDATA%\npm\appium.cmd"
    ) do (
        if exist "%%~P" (
            echo    [AVISO] Appium encontrado mas NAO no PATH:
            echo           %%~P
            echo           Adicione %APPDATA%\npm ao PATH
            set "APPIUM_FOUND=1"
            set /a AVISOS+=1
        )
    )
    if "!APPIUM_FOUND!"=="0" (
        echo    [ERRO] Appium NAO encontrado!
        echo           Execute: npm install -g appium
        set /a ERROS+=1
    )
)
echo.

:: ============================================================
:: [5/7] Verificar Android SDK (adb)
:: ============================================================
echo [5/7] Verificando Android SDK (adb)...
echo ------------------------------------------------------------
adb version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('adb version 2^>^&1 ^| findstr /i "Android Debug Bridge"') do (
        echo    [OK] %%v
    )

    echo.
    echo    Verificando ANDROID_HOME...
    if defined ANDROID_HOME (
        echo    [OK] ANDROID_HOME: %ANDROID_HOME%

        :: Verificar se pasta existe
        if exist "%ANDROID_HOME%" (
            echo    [OK] Pasta ANDROID_HOME existe
        ) else (
            echo    [AVISO] Pasta ANDROID_HOME nao encontrada
            set /a AVISOS+=1
        )
    ) else (
        echo    [AVISO] ANDROID_HOME nao definido
        echo            Alguns recursos podem nao funcionar
        set /a AVISOS+=1
    )

    :: Verificar dispositivos conectados
    echo.
    echo    Verificando dispositivos conectados...
    for /f "tokens=*" %%d in ('adb devices 2^>^&1 ^| findstr /v "List"') do (
        set "DEVICE_LINE=%%d"
        if not "!DEVICE_LINE!"=="" (
            echo    [INFO] %%d
        )
    )
) else (
    :: Tentar encontrar em caminhos conhecidos
    set "ADB_FOUND=0"
    for %%P in (
        "%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
        "%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe"
        "C:\Android\sdk\platform-tools\adb.exe"
    ) do (
        if exist "%%~P" (
            echo    [AVISO] adb encontrado mas NAO no PATH:
            echo           %%~P
            echo           Adicione ao PATH ou reinicie o computador
            set "ADB_FOUND=1"
            set /a AVISOS+=1
        )
    )
    if "!ADB_FOUND!"=="0" (
        echo    [ERRO] adb (Android SDK) NAO encontrado!
        echo           Execute: instalar_android_sdk.bat
        set /a ERROS+=1
    )
)
echo.

:: ============================================================
:: [6/7] Verificar Python (OBRIGATORIO para pytest)
:: ============================================================
echo [6/7] Verificando Python (OBRIGATORIO)...
echo ------------------------------------------------------------

set "PYTHON_CMD="
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=python"
) else (
    py --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set "PYTHON_CMD=py"
    )
)

if defined PYTHON_CMD (
    for /f "tokens=*" %%v in ('!PYTHON_CMD! --version') do (
        echo    [OK] %%v
    )

    :: Verificar pip
    !PYTHON_CMD! -m pip --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        for /f "tokens=1,2" %%a in ('!PYTHON_CMD! -m pip --version') do (
            echo    [OK] pip %%b
        )
    ) else (
        echo    [ERRO] pip nao encontrado
        echo           Execute: !PYTHON_CMD! -m ensurepip --upgrade
        set /a ERROS+=1
    )

    :: Verificar pytest
    echo.
    echo    Verificando pytest...
    !PYTHON_CMD! -m pytest --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        for /f "tokens=*" %%v in ('!PYTHON_CMD! -m pytest --version 2^>^&1') do (
            echo    [OK] %%v
        )
    ) else (
        echo    [ERRO] pytest NAO encontrado
        echo           Execute: pip install pytest pytest-html
        set /a ERROS+=1
    )

    :: Verificar Appium-Python-Client
    echo.
    echo    Verificando Appium-Python-Client...
    !PYTHON_CMD! -c "import appium; print('v' + appium.__version__)" >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        for /f "tokens=*" %%v in ('!PYTHON_CMD! -c "import appium; print(appium.__version__)"') do (
            echo    [OK] Appium-Python-Client v%%v
        )
    ) else (
        echo    [ERRO] Appium-Python-Client NAO encontrado
        echo           Execute: pip install Appium-Python-Client
        set /a ERROS+=1
    )

    :: Verificar allure-pytest (opcional mas recomendado)
    echo.
    echo    Verificando allure-pytest...
    !PYTHON_CMD! -c "import allure" >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo    [OK] allure-pytest instalado
    ) else (
        echo    [AVISO] allure-pytest NAO encontrado (opcional)
        echo            Execute: pip install allure-pytest
        set /a AVISOS+=1
    )
) else (
    :: Tentar encontrar em caminhos conhecidos
    set "PYTHON_FOUND=0"
    for %%P in (
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%ProgramFiles%\Python311\python.exe"
        "%ProgramFiles%\Python312\python.exe"
    ) do (
        if exist "%%~P" (
            echo    [AVISO] Python encontrado mas NAO no PATH:
            echo           %%~P
            echo           Reinicie o computador para atualizar PATH
            set "PYTHON_FOUND=1"
            set /a AVISOS+=1
        )
    )
    if "!PYTHON_FOUND!"=="0" (
        echo    [ERRO] Python NAO encontrado!
        echo           Necessario: Python 3.10 ou superior
        echo           Execute: instalar_dependencias.bat
        set /a ERROS+=1
    )
)
echo.

:: ============================================================
:: [7/7] Verificar conexao de rede
:: ============================================================
echo [7/7] Verificando conexao de rede...
echo ------------------------------------------------------------
ping -n 1 google.com >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] Conexao com internet funcionando
) else (
    echo    [AVISO] Sem conexao com internet
    echo            Algumas funcionalidades podem nao funcionar
    set /a AVISOS+=1
)
echo.

:: ============================================================
:: RESULTADO FINAL
:: ============================================================
echo ============================================================
echo                    RESULTADO DA VERIFICACAO
echo ============================================================
echo.

if %ERROS% EQU 0 (
    if %AVISOS% EQU 0 (
        echo    ============================================
        echo    [SUCESSO] Ambiente configurado corretamente!
        echo    ============================================
        echo.
        echo    Todos os componentes estao instalados.
        echo    Voce pode executar a Automacao PDV normalmente.
    ) else (
        echo    ============================================
        echo    [PARCIAL] Ambiente funcional com %AVISOS% aviso(s)
        echo    ============================================
        echo.
        echo    O programa pode funcionar, mas alguns
        echo    recursos podem estar limitados.
        echo.
        echo    Recomendado corrigir os avisos acima.
    )
) else (
    echo    ============================================
    echo    [FALHA] %ERROS% erro(s) e %AVISOS% aviso(s) encontrados
    echo    ============================================
    echo.
    echo    Componentes criticos estao faltando.
    echo.
    echo    Execute 'instalar_dependencias.bat' para corrigir.
    echo    Ou instale manualmente os componentes faltantes.
)

echo.
echo ============================================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul

exit /b %ERROS%
