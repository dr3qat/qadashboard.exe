@echo off
chcp 65001 >nul 2>&1
title Instalar Python e Dependencias - Automacao PDV
setlocal EnableDelayedExpansion

echo ============================================================
echo     INSTALADOR DE PYTHON E DEPENDENCIAS - AUTOMACAO PDV
echo ============================================================
echo.
echo Este script ira instalar automaticamente:
echo   - Python 3.11+ (via winget)
echo   - pip (gerenciador de pacotes)
echo   - Dependencias do requirements.txt (pytest, appium, etc)
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
:: ETAPA 1: Verificar/Instalar winget
:: ============================================================
echo [ETAPA 1/4] Verificando winget...
echo ------------------------------------------------------------

set "WINGET_OK=0"

winget --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('winget --version') do (
        echo    [OK] winget encontrado: %%v
    )
    set "WINGET_OK=1"
) else (
    echo    [!] winget nao encontrado.
    echo    Por favor, instale o App Installer pela Microsoft Store.
    echo.
    pause
    exit /b 1
)
echo.

:: ============================================================
:: ETAPA 2: Verificar/Instalar Python
:: ============================================================
echo [ETAPA 2/4] Verificando/Instalando Python...
echo ------------------------------------------------------------

:: Verificar se Python já está instalado
call :BuscarPython
if "!PYTHON_FOUND!"=="1" (
    echo    [OK] Python ja esta instalado: !PYTHON_PATH!
    for /f "tokens=*" %%v in ('"!PYTHON_PATH!" --version 2^>^&1') do (
        echo    [OK] Versao: %%v
    )
    goto :PythonOK
)

:: Tentar instalar via winget
echo    Python nao encontrado. Instalando Python 3.11 via winget...
echo    (Isso pode demorar alguns minutos)
echo.

call :InstalarComRetry "winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements -h" 3

:: Atualizar PATH da sessão atual
call :AtualizarPathPython

:: Verificar novamente
call :BuscarPython
if "!PYTHON_FOUND!"=="1" (
    echo    [OK] Python instalado com sucesso!
    goto :PythonOK
)

:: Fallback: tentar Python 3.12
echo    [!] Python 3.11 falhou. Tentando Python 3.12...
call :InstalarComRetry "winget install Python.Python.3.12 --accept-source-agreements --accept-package-agreements -h" 2

call :AtualizarPathPython
call :BuscarPython
if "!PYTHON_FOUND!"=="1" (
    echo    [OK] Python 3.12 instalado com sucesso!
    goto :PythonOK
)

:: Fallback final
echo.
echo    [ERRO] Instalacao automatica falhou.
echo.
echo    Por favor, instale manualmente:
echo    https://www.python.org/downloads/
echo.
echo    IMPORTANTE: Marque "Add Python to PATH" durante a instalacao!
echo.
pause
exit /b 1

:PythonOK
echo.

:: ============================================================
:: ETAPA 3: Verificar/Instalar pip
:: ============================================================
echo [ETAPA 3/4] Verificando pip...
echo ------------------------------------------------------------

:: Verificar pip
"!PYTHON_PATH!" -m pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('"!PYTHON_PATH!" -m pip --version') do (
        echo    [OK] %%v
    )
) else (
    echo    [!] pip nao encontrado. Instalando...
    "!PYTHON_PATH!" -m ensurepip --upgrade
    if !ERRORLEVEL! NEQ 0 (
        echo    [AVISO] ensurepip falhou. Tentando get-pip.py...
        curl -sSL https://bootstrap.pypa.io/get-pip.py -o "%TEMP%\get-pip.py"
        "!PYTHON_PATH!" "%TEMP%\get-pip.py"
        del "%TEMP%\get-pip.py" 2>nul
    )
)

:: Atualizar pip
echo    Atualizando pip para ultima versao...
"!PYTHON_PATH!" -m pip install --upgrade pip >nul 2>&1
echo.

:: ============================================================
:: ETAPA 4: Instalar dependencias do requirements.txt
:: ============================================================
echo [ETAPA 4/4] Instalando dependencias Python...
echo ------------------------------------------------------------

:: Encontrar requirements.txt
set "REQUIREMENTS_FILE="

:: Primeiro, verificar na pasta do script
set "SCRIPT_DIR=%~dp0"
if exist "%SCRIPT_DIR%..\requirements.txt" (
    set "REQUIREMENTS_FILE=%SCRIPT_DIR%..\requirements.txt"
) else if exist "%SCRIPT_DIR%requirements.txt" (
    set "REQUIREMENTS_FILE=%SCRIPT_DIR%requirements.txt"
) else if exist "%~dp0..\..\..\requirements.txt" (
    set "REQUIREMENTS_FILE=%~dp0..\..\..\requirements.txt"
)

:: Se não encontrar, procurar em locais comuns
if "!REQUIREMENTS_FILE!"=="" (
    for %%P in (
        "%USERPROFILE%\Documents\PDV_AUTOMACAO\requirements.txt"
        "%ProgramFiles%\QA Dashboard\requirements.txt"
        "E:\PDV_AUTOMACAO\requirements.txt"
        "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\requirements.txt"
    ) do (
        if exist "%%~P" (
            set "REQUIREMENTS_FILE=%%~P"
        )
    )
)

if "!REQUIREMENTS_FILE!"=="" (
    echo    [AVISO] requirements.txt nao encontrado.
    echo    Instalando pacotes essenciais manualmente...
    echo.

    echo    Instalando pytest...
    "!PYTHON_PATH!" -m pip install pytest pytest-html pytest-xdist --quiet

    echo    Instalando Appium-Python-Client...
    "!PYTHON_PATH!" -m pip install Appium-Python-Client --quiet

    echo    Instalando allure-pytest...
    "!PYTHON_PATH!" -m pip install allure-pytest --quiet

    echo    Instalando selenium...
    "!PYTHON_PATH!" -m pip install selenium --quiet

    echo    Instalando requests...
    "!PYTHON_PATH!" -m pip install requests --quiet

    echo    Instalando Faker...
    "!PYTHON_PATH!" -m pip install Faker --quiet

    echo.
    echo    [OK] Pacotes essenciais instalados!
) else (
    echo    Encontrado: !REQUIREMENTS_FILE!
    echo    Instalando todas as dependencias...
    echo    (Isso pode demorar alguns minutos)
    echo.

    "!PYTHON_PATH!" -m pip install -r "!REQUIREMENTS_FILE!" --quiet

    if !ERRORLEVEL! EQU 0 (
        echo    [OK] Todas as dependencias instaladas com sucesso!
    ) else (
        echo    [AVISO] Algumas dependencias podem ter falhado.
        echo    Tentando instalar pacotes essenciais...
        "!PYTHON_PATH!" -m pip install pytest Appium-Python-Client allure-pytest Faker requests --quiet
    )
)
echo.

:: ============================================================
:: VALIDACAO FINAL
:: ============================================================
echo ============================================================
echo                    VALIDACAO FINAL
echo ============================================================
echo.

set "TOTAL_ERROS=0"

:: Validar Python
call :BuscarPython
if "!PYTHON_FOUND!"=="1" (
    echo    [OK] Python: Instalado
) else (
    echo    [X]  Python: NAO ENCONTRADO
    set /a TOTAL_ERROS+=1
)

:: Validar pip
"!PYTHON_PATH!" -m pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] pip: Instalado
) else (
    echo    [X]  pip: NAO ENCONTRADO
    set /a TOTAL_ERROS+=1
)

:: Validar pytest
"!PYTHON_PATH!" -m pytest --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%v in ('"!PYTHON_PATH!" -m pytest --version 2^>^&1') do (
        echo    [OK] pytest: %%v
    )
) else (
    echo    [X]  pytest: NAO ENCONTRADO
    set /a TOTAL_ERROS+=1
)

:: Validar Appium-Python-Client
"!PYTHON_PATH!" -c "import appium; print('OK')" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] Appium-Python-Client: Instalado
) else (
    echo    [X]  Appium-Python-Client: NAO ENCONTRADO
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
    echo    [SUCESSO] Python e todas as dependencias instaladas!
    echo.
    echo    Voce pode executar testes com:
    echo      pytest tests/ --html=report.html
    echo.
) else (
    echo    [PARCIAL] !TOTAL_ERROS! componente(s) nao foram instalados.
    echo              Verifique as mensagens acima.
)

echo.
echo IMPORTANTE:
echo   - Pode ser necessario REINICIAR O COMPUTADOR para que
echo     as variaveis de ambiente sejam atualizadas.
echo.
echo ============================================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
exit /b !TOTAL_ERROS!

:: ============================================================
:: FUNCOES AUXILIARES
:: ============================================================

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

:BuscarPython
:: Busca Python em caminhos conhecidos
set "PYTHON_FOUND=0"
set "PYTHON_PATH="

:: Verificar py launcher primeiro (mais confiável no Windows)
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_FOUND=1"
    set "PYTHON_PATH=py"
    goto :eof
)

:: Verificar python no PATH
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_FOUND=1"
    set "PYTHON_PATH=python"
    goto :eof
)

:: Verificar python3 no PATH
python3 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_FOUND=1"
    set "PYTHON_PATH=python3"
    goto :eof
)

:: Verificar em caminhos conhecidos
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%ProgramFiles%\Python311\python.exe"
    "%ProgramFiles%\Python312\python.exe"
    "%ProgramFiles%\Python310\python.exe"
    "C:\Python311\python.exe"
    "C:\Python312\python.exe"
    "C:\Python310\python.exe"
) do (
    if exist "%%~P" (
        set "PYTHON_FOUND=1"
        set "PYTHON_PATH=%%~P"
        goto :eof
    )
)
goto :eof

:AtualizarPathPython
:: Adiciona caminhos conhecidos do Python ao PATH da sessão
set "PYTHON_PATHS=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"
set "PYTHON_PATHS=!PYTHON_PATHS!;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts"
set "PYTHON_PATHS=!PYTHON_PATHS!;%ProgramFiles%\Python311;%ProgramFiles%\Python311\Scripts"
set "PYTHON_PATHS=!PYTHON_PATHS!;%ProgramFiles%\Python312;%ProgramFiles%\Python312\Scripts"
set "PATH=%PATH%;!PYTHON_PATHS!"

:: Tentar refreshenv se disponível (Chocolatey)
where refreshenv >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    call refreshenv >nul 2>&1
)
goto :eof
