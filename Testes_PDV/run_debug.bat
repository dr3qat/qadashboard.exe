@echo off
REM ============================================================
REM Script para rodar testes em MODO DEBUG (logs técnicos completos)
REM ============================================================

echo ============================================================
echo   MODO DEBUG - Logs técnicos completos
echo ============================================================
echo.

REM Limpar cache do pytest e arquivos .pyc antes de executar
echo [INFO] Limpando cache do pytest...
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist __pycache__ rmdir /s /q __pycache__
if exist tests\__pycache__ rmdir /s /q tests\__pycache__
if exist tests\e2e\__pycache__ rmdir /s /q tests\e2e\__pycache__
if exist tests\unit\__pycache__ rmdir /s /q tests\unit\__pycache__
if exist pages\__pycache__ rmdir /s /q pages\__pycache__
echo [OK] Cache limpo com sucesso!
echo.

set DEBUG_MODE=true
pytest tests/e2e/test_venda_futura.py -v -s

echo.
echo ============================================================
echo   Testes finalizados
echo ============================================================
pause
