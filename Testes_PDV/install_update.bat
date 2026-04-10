@echo off
REM ============================================================
REM Script de Instalacao/Atualizacao Automatica
REM Limpa cache automaticamente ao detectar nova versao
REM ============================================================

echo ============================================================
echo   Sistema de Instalacao/Atualizacao - Testes PDV
echo ============================================================
echo.

REM Verifica se existe arquivo de versao atual
set VERSAO_ATUAL_FILE=.version_atual
set VERSAO_NOVA_FILE=VERSION

REM Le versao nova do arquivo VERSION
if not exist "%VERSAO_NOVA_FILE%" (
    echo [ERRO] Arquivo VERSION nao encontrado!
    goto :fim
)

set /p VERSAO_NOVA=<"%VERSAO_NOVA_FILE%"
echo [INFO] Versao a ser instalada: %VERSAO_NOVA%

REM Le versao atual (se existir)
if exist "%VERSAO_ATUAL_FILE%" (
    set /p VERSAO_ATUAL=<"%VERSAO_ATUAL_FILE%"
    echo [INFO] Versao atual instalada: %VERSAO_ATUAL%

    REM Compara versoes
    if "%VERSAO_ATUAL%"=="%VERSAO_NOVA%" (
        echo [INFO] Mesma versao ja instalada. Limpando cache mesmo assim...
    ) else (
        echo [AVISO] Detectada atualizacao de versao!
        echo [INFO] %VERSAO_ATUAL% --^> %VERSAO_NOVA%
    )
) else (
    echo [INFO] Primeira instalacao detectada
)

echo.
echo ============================================================
echo   Limpando Cache e Arquivos Temporarios
echo ============================================================
echo.

REM Verifica se Python esta disponivel para usar script robusto
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    if exist ..\limpar_cache_completo.py (
        echo [INFO] Usando limpeza COMPLETA via Python...
        python ..\limpar_cache_completo.py >nul
        if %ERRORLEVEL% EQU 0 (
            echo [OK] Cache limpo via Python
            goto :logs_limpeza
        )
    )
    echo [AVISO] Script Python nao encontrado, usando limpeza basica...
)

REM Limpeza basica (fallback)
echo [1/7] Limpando .pytest_cache...
if exist .pytest_cache (
    rmdir /s /q .pytest_cache 2>nul
    echo [OK] .pytest_cache removido
) else (
    echo [OK] .pytest_cache nao existia
)

echo [2/7] Limpando __pycache__ raiz...
if exist __pycache__ (
    rmdir /s /q __pycache__ 2>nul
    echo [OK] __pycache__ raiz removido
) else (
    echo [OK] __pycache__ raiz nao existia
)

echo [3/7] Limpando __pycache__ de tests...
if exist tests\__pycache__ rmdir /s /q tests\__pycache__ 2>nul
if exist tests\e2e\__pycache__ rmdir /s /q tests\e2e\__pycache__ 2>nul
if exist tests\unit\__pycache__ rmdir /s /q tests\unit\__pycache__ 2>nul
if exist tests\smoke\__pycache__ rmdir /s /q tests\smoke\__pycache__ 2>nul
echo [OK] __pycache__ de tests removidos

echo [4/7] Limpando __pycache__ de pages...
if exist pages\__pycache__ rmdir /s /q pages\__pycache__ 2>nul
echo [OK] __pycache__ de pages removido

echo [5/7] Limpando arquivos .pyc recursivamente...
for /r %%i in (*.pyc) do del "%%i" >nul 2>&1
echo [OK] Arquivos .pyc removidos

:logs_limpeza
echo [6/7] Limpando logs antigos...
if exist logs\*.log (
    forfiles /P logs /M *.log /D -7 /C "cmd /c del @path" 2>nul
    echo [OK] Logs com mais de 7 dias removidos
) else (
    echo [OK] Sem logs para limpar
)

echo [7/7] Limpando allure-results...
if exist allure-results (
    rmdir /s /q allure-results 2>nul
    mkdir allure-results
    echo [OK] allure-results limpo
) else (
    echo [OK] allure-results nao existia
)

echo.
echo ============================================================
echo   Atualizando Versao Instalada
echo ============================================================
echo.

REM Salva versao nova como versao atual
echo %VERSAO_NOVA%>"%VERSAO_ATUAL_FILE%"
echo [OK] Versao %VERSAO_NOVA% registrada como instalada

echo.
echo ============================================================
echo   Instalacao/Atualizacao Concluida!
echo ============================================================
echo.
echo Versao instalada: %VERSAO_NOVA%
echo Cache limpo com sucesso!
echo Todos os testes serao carregados dos arquivos atualizados.
echo.

:fim
pause
