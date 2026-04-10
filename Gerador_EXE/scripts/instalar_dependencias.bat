@echo off
chcp 65001 >nul 2>&1
title Instalar Dependencias - Automacao PDV
setlocal EnableDelayedExpansion

echo ============================================================
echo     INSTALADOR DE DEPENDENCIAS - AUTOMACAO PDV MOBILE
echo ============================================================
echo.
echo Este script ira instalar automaticamente:
echo   - Python 3.11+ e dependencias (pytest, appium-python-client)
echo   - Java JDK 17 (Microsoft OpenJDK)
echo   - Node.js LTS
echo   - Appium
echo   - Driver UiAutomator2
echo.
echo IMPORTANTE: Execute este script como ADMINISTRADOR!
echo.
echo ============================================================
echo.

:: Verificar se está rodando como administrador
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Este script precisa ser executado como Administrador!
    echo.
    echo Clique com botao direito no arquivo e selecione:
    echo "Executar como administrador"
    echo.
    pause
    exit /b 1
)

echo Pressione qualquer tecla para iniciar a instalacao...
echo (ou feche esta janela para cancelar)
pause >nul
echo.

:: ============================================================
:: ETAPA 0: Instalar Python e dependencias
:: ============================================================
echo [ETAPA 0/7] Instalando Python e dependencias pytest...
echo ------------------------------------------------------------

:: Verificar se o script de Python existe
set "SCRIPT_DIR=%~dp0"
if exist "%SCRIPT_DIR%instalar_python.bat" (
    echo    Executando instalador de Python...
    call "%SCRIPT_DIR%instalar_python.bat"
    if !ERRORLEVEL! NEQ 0 (
        echo    [AVISO] Instalacao de Python teve problemas.
        echo            Continuando com as demais dependencias...
    )
) else (
    echo    [AVISO] Script instalar_python.bat nao encontrado.
    echo            Instalando Python diretamente...

    :: Verificar se Python já está instalado
    python --version >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        py --version >nul 2>&1
        if !ERRORLEVEL! NEQ 0 (
            echo    Instalando Python via winget...
            winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements -h
        )
    )
)
echo.

:: ============================================================
:: ETAPA 1: Verificar/Instalar winget
:: ============================================================
echo [ETAPA 1/7] Verificando winget...
echo ------------------------------------------------------------

set "WINGET_OK=0"

winget --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('winget --version') do (
        echo    [OK] winget encontrado: %%v
    )
    set "WINGET_OK=1"
) else (
    echo    [!] winget nao encontrado. Tentando instalar...
    echo.
    call :InstalarWinget
)

if "!WINGET_OK!"=="0" (
    echo.
    echo    [AVISO] winget nao disponivel. Usando instalacao alternativa.
    echo.
)
echo.

:: ============================================================
:: ETAPA 2: Instalar Java JDK 17
:: ============================================================
echo [ETAPA 2/7] Verificando/Instalando Java JDK 17...
echo ------------------------------------------------------------

:: Verificar em caminhos conhecidos primeiro
call :BuscarJava
if "!JAVA_FOUND!"=="1" (
    echo    [OK] Java ja esta instalado, pulando...
    goto :JavaOK
)

:: Tentar instalar via winget
if "!WINGET_OK!"=="1" (
    echo    Instalando Microsoft OpenJDK 17 via winget...
    echo    (Isso pode demorar alguns minutos)
    echo.

    call :InstalarComRetry "winget install Microsoft.OpenJDK.17 --accept-source-agreements --accept-package-agreements -h" 3

    :: Verificar novamente
    call :BuscarJava
    if "!JAVA_FOUND!"=="1" (
        echo    [OK] Java JDK 17 instalado com sucesso!
        goto :JavaOK
    )
)

:: Fallback: Download manual
echo.
echo    [!] Instalacao automatica falhou. URLs para download manual:
echo.
echo    Microsoft OpenJDK 17:
echo    https://learn.microsoft.com/pt-br/java/openjdk/download
echo.
echo    Oracle JDK:
echo    https://www.oracle.com/java/technologies/downloads/
echo.
echo    Pressione qualquer tecla para continuar...
pause >nul

:JavaOK
echo.

:: ============================================================
:: ETAPA 3: Instalar Node.js LTS
:: ============================================================
echo [ETAPA 3/7] Verificando/Instalando Node.js LTS...
echo ------------------------------------------------------------

:: Verificar em caminhos conhecidos primeiro
call :BuscarNode
if "!NODE_FOUND!"=="1" (
    echo    [OK] Node.js ja esta instalado, pulando...
    goto :NodeOK
)

:: Tentar instalar via winget
if "!WINGET_OK!"=="1" (
    echo    Instalando Node.js LTS via winget...
    echo    (Isso pode demorar alguns minutos)
    echo.

    call :InstalarComRetry "winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements -h" 3

    :: Verificar novamente
    call :BuscarNode
    if "!NODE_FOUND!"=="1" (
        echo    [OK] Node.js LTS instalado com sucesso!
        goto :NodeOK
    )
)

:: Fallback: Download manual
echo.
echo    [!] Instalacao automatica falhou. URL para download manual:
echo.
echo    Node.js LTS:
echo    https://nodejs.org/pt-br/download/
echo.
echo    Pressione qualquer tecla para continuar...
pause >nul

:NodeOK
echo.

:: ============================================================
:: ETAPA 4: Atualizar PATH (necessário após instalações)
:: ============================================================
echo [ETAPA 4/7] Atualizando variaveis de ambiente...
echo ------------------------------------------------------------

:: Caminhos conhecidos onde Node.js/npm podem estar
set "NODE_PATHS=%ProgramFiles%\nodejs;%ProgramFiles(x86)%\nodejs;%LOCALAPPDATA%\Programs\nodejs"
set "NPM_PATHS=%APPDATA%\npm;%LOCALAPPDATA%\npm"

:: Adicionar ao PATH da sessão atual
set "PATH=%PATH%;%NODE_PATHS%;%NPM_PATHS%"

:: Tentar refreshenv se disponível (Chocolatey)
where refreshenv >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    Executando refreshenv...
    call refreshenv >nul 2>&1
)

:: Buscar npm em caminhos conhecidos
call :BuscarNpm
if "!NPM_FOUND!"=="1" (
    echo    [OK] npm disponivel no PATH: !NPM_PATH!
) else (
    echo    [AVISO] npm nao encontrado no PATH atual.
    echo            Pode ser necessario reiniciar o computador.
    echo.
    echo    Deseja continuar mesmo assim? (S/N)
    choice /c SN /n
    if !ERRORLEVEL! EQU 2 (
        echo.
        echo    Reinicie o computador e execute novamente.
        pause
        exit /b 1
    )
)
echo.

:: ============================================================
:: ETAPA 5: Instalar Appium e UiAutomator2
:: ============================================================
echo [ETAPA 5/7] Verificando/Instalando Appium...
echo ------------------------------------------------------------

:: Verificar se Appium já está instalado
call :BuscarAppium
if "!APPIUM_FOUND!"=="1" (
    echo    [OK] Appium ja esta instalado: !APPIUM_PATH!
    goto :VerificarDriver
)

:: Verificar se npm está disponível
if "!NPM_FOUND!"=="0" (
    echo    [ERRO] npm nao disponivel. Nao e possivel instalar Appium.
    echo           Reinicie o computador e execute novamente.
    goto :AppiumFail
)

echo    Instalando Appium globalmente via npm...
echo    (Isso pode demorar alguns minutos)
echo.

call :InstalarComRetry "call "!NPM_PATH!" install -g appium" 3

:: Verificar se instalou
call :BuscarAppium
if "!APPIUM_FOUND!"=="1" (
    echo    [OK] Appium instalado com sucesso!
) else (
    echo    [ERRO] Falha ao instalar Appium.
    echo           Tente manualmente: npm install -g appium
)

:VerificarDriver
echo.
echo    Verificando driver UiAutomator2...

if "!APPIUM_FOUND!"=="0" goto :AppiumFail

"!APPIUM_PATH!" driver list --installed 2>&1 | findstr /i "uiautomator2" >nul
if %ERRORLEVEL% EQU 0 (
    echo    [OK] Driver UiAutomator2 ja esta instalado
) else (
    echo    Instalando driver UiAutomator2...
    call "!APPIUM_PATH!" driver install uiautomator2
    if !ERRORLEVEL! EQU 0 (
        echo    [OK] Driver UiAutomator2 instalado com sucesso!
    ) else (
        echo    [AVISO] Falha ao instalar driver automaticamente.
        echo            Tente: appium driver install uiautomator2
    )
)

:AppiumFail
echo.

:: ============================================================
:: ETAPA 6: Validação Final
:: ============================================================
echo [ETAPA 6/7] Validando instalacoes...
echo ------------------------------------------------------------

set "TOTAL_ERROS=0"

:: Validar Python
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] Python: Instalado
) else (
    py --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo    [OK] Python: Instalado (via py launcher)
    ) else (
        echo    [X]  Python: NAO ENCONTRADO
        set /a TOTAL_ERROS+=1
    )
)

:: Validar pytest
python -m pytest --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] pytest: Instalado
) else (
    py -m pytest --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo    [OK] pytest: Instalado
    ) else (
        echo    [X]  pytest: NAO ENCONTRADO
        set /a TOTAL_ERROS+=1
    )
)

:: Validar Java
call :BuscarJava
if "!JAVA_FOUND!"=="1" (
    echo    [OK] Java: Instalado
) else (
    echo    [X]  Java: NAO ENCONTRADO
    set /a TOTAL_ERROS+=1
)

:: Validar Node
call :BuscarNode
if "!NODE_FOUND!"=="1" (
    echo    [OK] Node.js: Instalado
) else (
    echo    [X]  Node.js: NAO ENCONTRADO
    set /a TOTAL_ERROS+=1
)

:: Validar npm
call :BuscarNpm
if "!NPM_FOUND!"=="1" (
    echo    [OK] npm: Instalado
) else (
    echo    [X]  npm: NAO ENCONTRADO
    set /a TOTAL_ERROS+=1
)

:: Validar Appium
call :BuscarAppium
if "!APPIUM_FOUND!"=="1" (
    echo    [OK] Appium: Instalado
) else (
    echo    [X]  Appium: NAO ENCONTRADO
    set /a TOTAL_ERROS+=1
)

echo.

:: ============================================================
:: RESULTADO FINAL
:: ============================================================
echo ============================================================
echo                    INSTALACAO CONCLUIDA
echo ============================================================
echo.

if !TOTAL_ERROS! EQU 0 (
    echo    [SUCESSO] Todas as dependencias foram instaladas!
) else (
    echo    [PARCIAL] !TOTAL_ERROS! componente(s) nao foram instalados.
    echo              Verifique as mensagens acima.
)

echo.
echo IMPORTANTE:
echo   - REINICIE O COMPUTADOR para que todas as mudancas
echo     tenham efeito nas variaveis de ambiente.
echo.
echo   - O Android SDK (adb) precisa ser instalado separadamente.
echo     Execute: instalar_android_sdk.bat
echo.
echo Apos reiniciar, execute 'verificar_ambiente.bat' para
echo confirmar que tudo esta funcionando.
echo.
echo ============================================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
exit /b !TOTAL_ERROS!

:: ============================================================
:: FUNCOES AUXILIARES
:: ============================================================

:InstalarWinget
:: Tenta instalar winget via PowerShell
echo    Tentando instalar winget via PowerShell...
echo.

:: Método 1: Via Add-AppxPackage
powershell -Command "& {try { Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe -ErrorAction Stop; Write-Host 'Winget instalado via AppxPackage' } catch { Write-Host 'Metodo AppxPackage falhou' }}" 2>nul

:: Verificar se funcionou
winget --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] winget instalado com sucesso!
    set "WINGET_OK=1"
    goto :eof
)

:: Método 2: Download direto do GitHub
echo    Tentando download direto do GitHub...
set "WINGET_URL=https://github.com/microsoft/winget-cli/releases/latest/download/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle"
set "WINGET_FILE=%TEMP%\winget.msixbundle"

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri '%WINGET_URL%' -OutFile '%WINGET_FILE%' -UseBasicParsing } catch { Write-Host 'Download falhou' }}" 2>nul

if exist "%WINGET_FILE%" (
    echo    Instalando winget...
    powershell -Command "Add-AppxPackage -Path '%WINGET_FILE%'" 2>nul
    del "%WINGET_FILE%" 2>nul

    winget --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo    [OK] winget instalado com sucesso!
        set "WINGET_OK=1"
        goto :eof
    )
)

echo    [AVISO] Nao foi possivel instalar winget automaticamente.
echo.
echo    Para instalar manualmente:
echo    1. Abra a Microsoft Store
echo    2. Busque por "App Installer"
echo    3. Instale ou atualize o aplicativo
echo.
echo    Ou baixe de: https://github.com/microsoft/winget-cli/releases
echo.
set "WINGET_OK=0"
goto :eof

:InstalarComRetry
:: Executa comando com retry
:: %~1 = comando
:: %~2 = numero de tentativas
set "CMD=%~1"
set "MAX_TENTATIVAS=%~2"
set "TENTATIVA=1"

:RetryLoop
echo    Tentativa !TENTATIVA! de !MAX_TENTATIVAS!...
%CMD%
if !ERRORLEVEL! EQU 0 goto :eof

set /a TENTATIVA+=1
if !TENTATIVA! LEQ !MAX_TENTATIVAS! (
    echo    [!] Falhou. Aguardando 5 segundos antes de tentar novamente...
    timeout /t 5 /nobreak >nul
    goto :RetryLoop
)
echo    [!] Todas as !MAX_TENTATIVAS! tentativas falharam.
goto :eof

:BuscarJava
:: Busca Java em caminhos conhecidos
set "JAVA_FOUND=0"
set "JAVA_PATH="

:: Verificar no PATH
java -version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "JAVA_FOUND=1"
    set "JAVA_PATH=java"
    goto :eof
)

:: Verificar em caminhos conhecidos
for %%P in (
    "%ProgramFiles%\Microsoft\jdk-17*\bin\java.exe"
    "%ProgramFiles%\Java\jdk-17*\bin\java.exe"
    "%ProgramFiles%\Eclipse Adoptium\jdk-17*\bin\java.exe"
    "%ProgramFiles%\Zulu\zulu-17*\bin\java.exe"
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
:: Busca Node.js em caminhos conhecidos
set "NODE_FOUND=0"
set "NODE_PATH="

:: Verificar no PATH
node --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "NODE_FOUND=1"
    set "NODE_PATH=node"
    goto :eof
)

:: Verificar em caminhos conhecidos
for %%P in (
    "%ProgramFiles%\nodejs\node.exe"
    "%ProgramFiles(x86)%\nodejs\node.exe"
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

:BuscarNpm
:: Busca npm em caminhos conhecidos
set "NPM_FOUND=0"
set "NPM_PATH="

:: Verificar no PATH
where npm >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%p in ('where npm') do (
        set "NPM_FOUND=1"
        set "NPM_PATH=%%p"
        goto :eof
    )
)

:: Verificar em caminhos conhecidos
for %%P in (
    "%ProgramFiles%\nodejs\npm.cmd"
    "%APPDATA%\npm\npm.cmd"
    "%LOCALAPPDATA%\npm\npm.cmd"
) do (
    if exist "%%~P" (
        set "NPM_FOUND=1"
        set "NPM_PATH=%%~P"
        goto :eof
    )
)
goto :eof

:BuscarAppium
:: Busca Appium em caminhos conhecidos
set "APPIUM_FOUND=0"
set "APPIUM_PATH="

:: Verificar no PATH
where appium >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%p in ('where appium') do (
        set "APPIUM_FOUND=1"
        set "APPIUM_PATH=%%p"
        goto :eof
    )
)

:: Verificar em caminhos conhecidos
for %%P in (
    "%APPDATA%\npm\appium.cmd"
    "%LOCALAPPDATA%\npm\appium.cmd"
    "%ProgramFiles%\nodejs\appium.cmd"
) do (
    if exist "%%~P" (
        set "APPIUM_FOUND=1"
        set "APPIUM_PATH=%%~P"
        goto :eof
    )
)
goto :eof
