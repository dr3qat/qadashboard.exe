@echo off
echo ========================================
echo    EXECUTANDO TESTES
echo ========================================
cd /d "%~dp0Testes_PDV"
pytest tests/e2e/ -v
pause
