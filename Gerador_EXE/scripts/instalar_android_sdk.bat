@echo off
chcp 65001 >nul 2>&1
title Instalar Android SDK - Automacao PDV
setlocal EnableDelayedExpansion

echo ============================================================
echo      INSTALADOR DO ANDROID SDK - AUTOMACAO PDV MOBILE
echo ============================================================
echo.
echo Este script ira:
echo   1. Baixar Android Command-Line Tools (~150MB)
echo   2. Extrair para %LOCALAPPDATA%\Android\Sdk
echo   3. Instalar platform-tools (adb, fastboot)
echo   4. Configurar ANDROID_HOME e PATH
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

:: Definir caminhos
set "SDK_ROOT=%LOCALAPPDATA%\Android\Sdk"
set "CMDLINE_TOOLS_URL=https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
set "DOWNLOAD_FILE=%TEMP%\android-cmdline-tools.zip"
set "MAX_TENTATIVAS=3"

:: ============================================================
:: ETAPA 1: Verificar se adb já existe
:: ============================================================
echo [ETAPA 1/6] Verificando instalacao existente...
echo ------------------------------------------------------------

:: Verificar em caminhos conhecidos
call :BuscarAdb
if "!ADB_FOUND!"=="1" (
    echo    [OK] adb ja esta instalado e funcionando!
    echo.
    echo    Localizacao: !ADB_PATH!
    echo.
    "!ADB_PATH!" version 2>&1 | findstr /i "Android Debug Bridge"
    echo.
    echo    Deseja reinstalar mesmo assim? (S/N)
    choice /c SN /n
    if !ERRORLEVEL! EQU 2 (
        echo    Instalacao cancelada.
        pause
        exit /b 0
    )
)
echo.

:: ============================================================
:: ETAPA 2: Verificar Java (necessário para sdkmanager)
:: ============================================================
echo [ETAPA 2/6] Verificando Java (necessario para sdkmanager)...
echo ------------------------------------------------------------

call :BuscarJava
if "!JAVA_FOUND!"=="0" (
    echo    [ERRO] Java nao encontrado!
    echo.
    echo    O Java e necessario para o sdkmanager.
    echo    Execute primeiro: instalar_dependencias.bat
    echo.
    pause
    exit /b 1
)
echo    [OK] Java encontrado: !JAVA_PATH!
echo.

:: ============================================================
:: ETAPA 3: Criar pasta do SDK
:: ============================================================
echo [ETAPA 3/6] Criando estrutura de pastas...
echo ------------------------------------------------------------

if not exist "%SDK_ROOT%" (
    mkdir "%SDK_ROOT%"
    if !ERRORLEVEL! NEQ 0 (
        echo    [ERRO] Nao foi possivel criar pasta: %SDK_ROOT%
        pause
        exit /b 1
    )
    echo    [OK] Pasta criada: %SDK_ROOT%
) else (
    echo    [OK] Pasta ja existe: %SDK_ROOT%
)

if not exist "%SDK_ROOT%\cmdline-tools" (
    mkdir "%SDK_ROOT%\cmdline-tools"
)
echo.

:: ============================================================
:: ETAPA 4: Baixar Command-Line Tools (com retry)
:: ============================================================
echo [ETAPA 4/6] Baixando Android Command-Line Tools...
echo ------------------------------------------------------------
echo    URL: %CMDLINE_TOOLS_URL%
echo    Destino: %DOWNLOAD_FILE%
echo.
echo    Isso pode demorar alguns minutos dependendo da conexao...
echo.

set "DOWNLOAD_OK=0"
set "TENTATIVA=1"

:DownloadLoop
echo    Tentativa !TENTATIVA! de %MAX_TENTATIVAS%...

:: Usar PowerShell para download com progress
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri '%CMDLINE_TOOLS_URL%' -OutFile '%DOWNLOAD_FILE%' -UseBasicParsing; exit 0 } catch { Write-Host \"Erro: $_\"; exit 1 }}"

if !ERRORLEVEL! EQU 0 (
    if exist "%DOWNLOAD_FILE%" (
        :: Verificar se o arquivo tem tamanho razoável (> 100MB)
        for %%F in ("%DOWNLOAD_FILE%") do (
            set "FILE_SIZE=%%~zF"
        )
        if !FILE_SIZE! GTR 100000000 (
            echo    [OK] Download concluido! Tamanho: !FILE_SIZE! bytes
            set "DOWNLOAD_OK=1"
            goto :DownloadDone
        ) else (
            echo    [!] Arquivo muito pequeno (!FILE_SIZE! bytes). Download incompleto.
            del "%DOWNLOAD_FILE%" 2>nul
        )
    )
)

set /a TENTATIVA+=1
if !TENTATIVA! LEQ %MAX_TENTATIVAS% (
    echo    [!] Download falhou. Aguardando 5 segundos antes de tentar novamente...
    timeout /t 5 /nobreak >nul
    goto :DownloadLoop
)

:DownloadDone
if "!DOWNLOAD_OK!"=="0" (
    echo.
    echo    [ERRO] Falha no download apos %MAX_TENTATIVAS% tentativas!
    echo.
    echo    Verifique sua conexao com a internet e tente novamente.
    echo.
    echo    Ou baixe manualmente de:
    echo    https://developer.android.com/studio#command-tools
    echo.
    echo    E extraia para: %SDK_ROOT%\cmdline-tools\latest
    echo.
    pause
    exit /b 1
)
echo.

:: ============================================================
:: ETAPA 5: Extrair e instalar platform-tools
:: ============================================================
echo [ETAPA 5/6] Extraindo e configurando SDK...
echo ------------------------------------------------------------

:: Extrair ZIP
echo    Extraindo arquivos...
powershell -Command "& {try { Expand-Archive -Path '%DOWNLOAD_FILE%' -DestinationPath '%SDK_ROOT%\cmdline-tools' -Force; exit 0 } catch { Write-Host \"Erro: $_\"; exit 1 }}"

if !ERRORLEVEL! NEQ 0 (
    echo    [ERRO] Falha ao extrair arquivo ZIP!
    echo.
    echo    O arquivo pode estar corrompido. Tente novamente.
    del "%DOWNLOAD_FILE%" 2>nul
    pause
    exit /b 1
)

:: Verificar se extraiu corretamente
if not exist "%SDK_ROOT%\cmdline-tools\cmdline-tools" (
    echo    [ERRO] Estrutura de pastas incorreta apos extracao.
    pause
    exit /b 1
)

:: Renomear pasta para estrutura correta
if exist "%SDK_ROOT%\cmdline-tools\latest" (
    rmdir /s /q "%SDK_ROOT%\cmdline-tools\latest" 2>nul
)
rename "%SDK_ROOT%\cmdline-tools\cmdline-tools" "latest"

if not exist "%SDK_ROOT%\cmdline-tools\latest\bin\sdkmanager.bat" (
    echo    [ERRO] sdkmanager nao encontrado apos extracao!
    pause
    exit /b 1
)

echo    [OK] Arquivos extraidos corretamente
echo.

:: Instalar platform-tools usando sdkmanager
echo    Instalando platform-tools via sdkmanager...
echo    (Isso instalara adb, fastboot, etc.)
echo.

set "SDKMANAGER=%SDK_ROOT%\cmdline-tools\latest\bin\sdkmanager.bat"

:: Aceitar licenças automaticamente
echo y | call "%SDKMANAGER%" --licenses >nul 2>&1

:: Instalar platform-tools
echo y | call "%SDKMANAGER%" "platform-tools"
if !ERRORLEVEL! NEQ 0 (
    echo    [AVISO] Possivel erro na instalacao do platform-tools.
    echo            Tentando novamente...
    echo y | call "%SDKMANAGER%" "platform-tools"
)

:: Verificar se platform-tools foi instalado
if not exist "%SDK_ROOT%\platform-tools\adb.exe" (
    echo    [ERRO] adb.exe nao encontrado apos instalacao!
    echo.
    echo    Tente instalar manualmente:
    echo    %SDKMANAGER% "platform-tools"
    pause
    exit /b 1
)

echo    [OK] platform-tools instalado!
echo.

:: Limpar arquivo temporário
del "%DOWNLOAD_FILE%" 2>nul

:: ============================================================
:: ETAPA 6: Configurar variáveis de ambiente
:: ============================================================
echo [ETAPA 6/6] Configurando variaveis de ambiente...
echo ------------------------------------------------------------

:: Configurar ANDROID_HOME para o usuário
setx ANDROID_HOME "%SDK_ROOT%" >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    echo    [OK] ANDROID_HOME = %SDK_ROOT%
) else (
    echo    [AVISO] Nao foi possivel definir ANDROID_HOME automaticamente.
    echo            Defina manualmente: ANDROID_HOME = %SDK_ROOT%
)

:: Adicionar ao PATH do usuário
set "PLATFORM_TOOLS=%SDK_ROOT%\platform-tools"

:: Verificar se já está no PATH
echo %PATH% | findstr /i "%PLATFORM_TOOLS%" >nul
if %ERRORLEVEL% NEQ 0 (
    :: Obter PATH atual do usuário
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%b"

    if defined USER_PATH (
        :: Verificar se não está vazio e se o platform-tools não está lá
        echo !USER_PATH! | findstr /i "%PLATFORM_TOOLS%" >nul
        if !ERRORLEVEL! NEQ 0 (
            setx PATH "!USER_PATH!;%PLATFORM_TOOLS%" >nul 2>&1
        )
    ) else (
        setx PATH "%PLATFORM_TOOLS%" >nul 2>&1
    )
    echo    [OK] PATH atualizado com platform-tools
) else (
    echo    [OK] PATH ja contem platform-tools
)
echo.

:: Atualizar PATH da sessão atual
set "PATH=%PATH%;%PLATFORM_TOOLS%"
set "ANDROID_HOME=%SDK_ROOT%"

:: ============================================================
:: VERIFICAÇÃO FINAL
:: ============================================================
echo ============================================================
echo                    VERIFICACAO FINAL
echo ============================================================
echo.

:: Testar adb diretamente
set "ADB_EXE=%PLATFORM_TOOLS%\adb.exe"

if exist "!ADB_EXE!" (
    "!ADB_EXE!" version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo    [SUCESSO] Android SDK instalado corretamente!
        echo.
        "!ADB_EXE!" version 2>&1 | findstr /i "Android Debug Bridge"
        echo.
        echo    ANDROID_HOME: %SDK_ROOT%
        echo    adb: !ADB_EXE!
    ) else (
        echo    [AVISO] adb instalado mas nao respondeu.
        echo            Pode ser necessario reiniciar o computador.
    )
) else (
    echo    [ERRO] adb.exe nao encontrado em: !ADB_EXE!
    echo           A instalacao pode ter falhado.
)

echo.
echo ============================================================
echo.
echo IMPORTANTE:
echo   - Reinicie o terminal/computador para aplicar as variaveis
echo   - Para testar, abra um novo terminal e digite: adb version
echo.
echo   - Para conectar um dispositivo Android:
echo     1. Ative "Depuracao USB" nas opcoes de desenvolvedor
echo     2. Conecte o cabo USB
echo     3. Execute: adb devices
echo.
echo ============================================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
exit /b 0

:: ============================================================
:: FUNCOES AUXILIARES
:: ============================================================

:BuscarAdb
:: Busca adb em caminhos conhecidos
set "ADB_FOUND=0"
set "ADB_PATH="

:: Verificar no PATH
where adb >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%p in ('where adb') do (
        set "ADB_FOUND=1"
        set "ADB_PATH=%%p"
        goto :eof
    )
)

:: Verificar em caminhos conhecidos
for %%P in (
    "%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"
    "%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe"
    "%ProgramFiles%\Android\android-sdk\platform-tools\adb.exe"
    "%ProgramFiles(x86)%\Android\android-sdk\platform-tools\adb.exe"
    "C:\Android\sdk\platform-tools\adb.exe"
) do (
    if exist "%%~P" (
        set "ADB_FOUND=1"
        set "ADB_PATH=%%~P"
        goto :eof
    )
)
goto :eof

:BuscarJava
:: Busca Java em caminhos conhecidos
set "JAVA_FOUND=0"
set "JAVA_PATH="

:: Verificar no PATH
java -version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "JAVA_FOUND=1"
    set "JAVA_PATH=java (no PATH)"
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
        :: Adicionar ao PATH temporariamente
        set "PATH=!PATH!;%%~dpP"
        goto :eof
    )
)
goto :eof
