@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo    COMPILANDO QA DASHBOARD
echo ========================================
echo.

:: Define caminhos
set "ROOT_DIR=%~dp0"
set "BUILD_DIR=%ROOT_DIR%Gerador_EXE\build"
set "REQ_BUILD=%BUILD_DIR%\requirements_build.txt"

:: ============================================================
:: PASSO 1: INSTALAR / ATUALIZAR DEPENDENCIAS DE BUILD
:: ============================================================
echo [1/2] Verificando dependencias de build...
echo       (requirements_build.txt)
echo.
python -m pip install -r "%REQ_BUILD%" --quiet

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao instalar dependencias!
    echo Verifique sua conexao com a internet e tente novamente.
    echo.
    pause
    exit /b 1
)

echo [OK] Dependencias verificadas.
echo.

:: ============================================================
:: PASSO 2: COMPILAR
:: ============================================================
echo [2/2] Compilando QA Dashboard...
echo.
cd /d "%ROOT_DIR%Gerador_EXE"
python build\builder_pro.py --qa-dev "%ROOT_DIR%Testes_PDV"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Build falhou! Verifique os logs acima.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] EXE gerado em: Gerador_EXE\output\dist\
pause
