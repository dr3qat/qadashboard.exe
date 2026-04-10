@echo off
REM ============================================================
REM Script para limpar cache do pytest manualmente
REM Use este script antes de reinstalar o exe ou quando houver
REM problemas com testes antigos aparecendo
REM ============================================================

echo ============================================================
echo   Limpando Cache do Pytest - VERSAO MELHORADA
echo ============================================================
echo.

REM Verifica se o script Python existe na pasta anterior
if exist "..\limpar_cache_completo.py" (
    REM Se existir, verifica se o Python esta instalado
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [INFO] Usando limpeza completa via Python...
        python ..\limpar_cache_completo.py
        goto :fim
    )
)

REM Se o script não existir ou o Python não estiver instalado, vai para a limpeza nativa
echo [AVISO] Script Python nao encontrado. Usando limpeza basica do Windows...
goto :limpeza_basica

:limpeza_basica
echo.
echo [INFO] Removendo cache do pytest...
if exist .pytest_cache (
    rmdir /s /q .pytest_cache
    echo [OK] .pytest_cache removido
) else (
    echo [INFO] .pytest_cache nao existe
)

echo.
echo [INFO] Removendo arquivos __pycache__...
if exist __pycache__ rmdir /s /q __pycache__
if exist tests\__pycache__ rmdir /s /q tests\__pycache__
if exist tests\e2e\__pycache__ rmdir /s /q tests\e2e\__pycache__
if exist tests\unit\__pycache__ rmdir /s /q tests\unit\__pycache__
if exist tests\smoke\__pycache__ rmdir /s /q tests\smoke\__pycache__
if exist pages\__pycache__ rmdir /s /q pages\__pycache__
echo [OK] Arquivos __pycache__ removidos

echo.
echo [INFO] Removendo arquivos .pyc recursivamente...
for /r %%i in (*.pyc) do del "%%i" >nul 2>&1
echo [OK] Arquivos .pyc removidos

echo.
echo ============================================================
echo   Cache limpo com sucesso!
echo ============================================================
echo.
echo Agora todos os testes serao carregados dos arquivos atuais.
echo.

:fim
pause