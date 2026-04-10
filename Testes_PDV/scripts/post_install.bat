@echo off
REM ============================================================
REM Script Post-Install - Executado automaticamente apos instalacao
REM Limpa cache para garantir que arquivos atualizados sejam carregados
REM ============================================================

cd /d "%~dp0\.."

echo [POST-INSTALL] Limpando cache do pytest...

REM Tentar usar script Python da pasta raiz (mais robusto)
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    if exist ..\limpar_cache_completo.py (
        python ..\limpar_cache_completo.py >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            echo [POST-INSTALL] Cache limpo via Python (completo)
            exit /b 0
        )
    )
)

REM Fallback: Limpeza basica
REM Limpar .pytest_cache
if exist .pytest_cache (
    rmdir /s /q .pytest_cache >nul 2>&1
)

REM Limpar __pycache__ de todas as pastas (incluindo smoke)
if exist __pycache__ rmdir /s /q __pycache__ >nul 2>&1
if exist tests\__pycache__ rmdir /s /q tests\__pycache__ >nul 2>&1
if exist tests\e2e\__pycache__ rmdir /s /q tests\e2e\__pycache__ >nul 2>&1
if exist tests\unit\__pycache__ rmdir /s /q tests\unit\__pycache__ >nul 2>&1
if exist tests\smoke\__pycache__ rmdir /s /q tests\smoke\__pycache__ >nul 2>&1
if exist pages\__pycache__ rmdir /s /q pages\__pycache__ >nul 2>&1

REM Limpar arquivos .pyc recursivamente
for /r %%i in (*.pyc) do del "%%i" >nul 2>&1

REM Limpar .version_atual para forcar deteccao de nova versao
if exist .version_atual del .version_atual >nul 2>&1

REM Limpar allure-results
if exist allure-results rmdir /s /q allure-results >nul 2>&1

echo [POST-INSTALL] Cache limpo com sucesso!

exit /b 0
