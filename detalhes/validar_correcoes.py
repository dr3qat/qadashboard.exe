"""
Script de validacao das correcoes de configuracao
Executa verificacoes automaticas para confirmar que tudo esta correto
"""
import json
import os
import sys
from pathlib import Path

# Configura encoding UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def validar_correcoes():
    print("=" * 70)
    print("  VALIDACAO DAS CORRECOES - Dashboard QA")
    print("=" * 70)
    print()

    # Caminho do settings.json
    settings_file = Path(__file__).parent.parent / "Gerador_EXE" / "runner" / "settings.json"

    # Campos esperados (conforme app_runner.py)
    campos_obrigatorios = {
        "server_ip", "server_port", "company", "user", "password",
        "customer_id", "customer_id_troca", "appium_port", "appium_path",
        "qa_dev_path", "timeout_default", "product_code_sale",
        "product_code_future_sale", "product_size_future",
        "product_code_stock_1", "product_code_stock_2",
        "clean_logs", "auto_open", "use_allure",
        "generate_single_file", "open_allure_end",
        "print_cupom_venda", "print_nfce", "print_danfe",
        "print_cupom_troca", "print_dialog_timeout"
    }

    total_checks = 0
    checks_ok = 0

    # CHECK 1: Arquivo settings.json existe
    total_checks += 1
    print(f"[CHECK 1/7] Verificando existencia do settings.json...")
    if settings_file.exists():
        print("  [OK] Arquivo encontrado:", settings_file)
        checks_ok += 1
    else:
        print("  [ERRO] Arquivo nao encontrado!")
        print("     Esperado em:", settings_file)
        return False

    # CHECK 2: Arquivo e JSON valido
    total_checks += 1
    print(f"\n[CHECK 2/7] Validando formato JSON...")
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  [OK] JSON valido ({len(data)} campos)")
        checks_ok += 1
    except json.JSONDecodeError as e:
        print(f"  [ERRO] JSON invalido - {e}")
        return False

    # CHECK 3: Todos os campos obrigatorios existem
    total_checks += 1
    print(f"\n[CHECK 3/7] Verificando campos obrigatorios...")
    campos_atuais = set(data.keys())
    faltando = campos_obrigatorios - campos_atuais
    extras = campos_atuais - campos_obrigatorios

    if not faltando:
        print(f"  [OK] Todos os {len(campos_obrigatorios)} campos obrigatorios presentes")
        checks_ok += 1
    else:
        print(f"  [ERRO] Faltando {len(faltando)} campos:")
        for campo in sorted(faltando):
            print(f"     - {campo}")

    if extras:
        print(f"  [AVISO] Campos extras (nao obrigatorios): {len(extras)}")
        for campo in sorted(extras):
            print(f"     - {campo}")

    # CHECK 4: Campos de impressao estao presentes
    total_checks += 1
    print(f"\n[CHECK 4/7] Verificando campos de impressao...")
    campos_impressao = {
        "print_cupom_venda", "print_nfce", "print_danfe",
        "print_cupom_troca", "print_dialog_timeout"
    }
    impressao_ok = all(campo in data for campo in campos_impressao)

    if impressao_ok:
        print("  [OK] Todos os 5 campos de impressao presentes:")
        for campo in sorted(campos_impressao):
            valor = data[campo]
            print(f"     - {campo}: {valor}")
        checks_ok += 1
    else:
        print("  [ERRO] Campos de impressao faltando!")

    # CHECK 5: Tipos de dados corretos
    total_checks += 1
    print(f"\n[CHECK 5/7] Verificando tipos de dados...")
    tipos_incorretos = []

    # Strings
    campos_string = {
        "server_ip", "server_port", "company", "user", "password",
        "customer_id", "customer_id_troca", "appium_port", "appium_path",
        "qa_dev_path", "timeout_default", "product_code_sale",
        "product_code_future_sale", "product_size_future",
        "product_code_stock_1", "product_code_stock_2", "print_dialog_timeout"
    }

    for campo in campos_string:
        if campo in data and not isinstance(data[campo], str):
            tipos_incorretos.append(f"{campo} (esperado: str, atual: {type(data[campo]).__name__})")

    # Booleans
    campos_bool = {
        "clean_logs", "auto_open", "use_allure",
        "generate_single_file", "open_allure_end",
        "print_cupom_venda", "print_nfce", "print_danfe", "print_cupom_troca"
    }

    for campo in campos_bool:
        if campo in data and not isinstance(data[campo], bool):
            tipos_incorretos.append(f"{campo} (esperado: bool, atual: {type(data[campo]).__name__})")

    if not tipos_incorretos:
        print(f"  [OK] Todos os tipos de dados estao corretos")
        checks_ok += 1
    else:
        print(f"  [ERRO] {len(tipos_incorretos)} tipos incorretos:")
        for erro in tipos_incorretos:
            print(f"     - {erro}")

    # CHECK 6: Cache Python limpo
    total_checks += 1
    print(f"\n[CHECK 6/7] Verificando cache Python...")
    raiz = Path(__file__).parent.parent
    pycache_dirs = list(raiz.rglob("__pycache__"))
    pyc_files = list(raiz.rglob("*.pyc"))

    if not pycache_dirs and not pyc_files:
        print(f"  [OK] Cache limpo (0 __pycache__, 0 .pyc)")
        checks_ok += 1
    else:
        print(f"  [AVISO] Cache encontrado:")
        print(f"     - {len(pycache_dirs)} pastas __pycache__")
        print(f"     - {len(pyc_files)} arquivos .pyc")
        print(f"     Execute: python detalhes/limpar_cache_completo.py")

    # CHECK 7: Codigo do builder_pro.py tem limpeza de cache
    total_checks += 1
    print(f"\n[CHECK 7/7] Verificando builder_pro.py...")
    builder_file = raiz / "Gerador_EXE" / "build" / "builder_pro.py"

    if builder_file.exists():
        with open(builder_file, 'r', encoding='utf-8') as f:
            builder_code = f.read()

        if "clean_python_cache" in builder_code and "self.clean_python_cache()" in builder_code:
            print(f"  [OK] Limpeza de cache integrada ao builder")
            checks_ok += 1
        else:
            print(f"  [ERRO] Limpeza de cache NAO integrada!")
    else:
        print(f"  [ERRO] builder_pro.py nao encontrado!")

    # RESUMO FINAL
    print()
    print("=" * 70)
    print("  RESUMO DA VALIDACAO")
    print("=" * 70)
    print(f"  Total de checks: {total_checks}")
    print(f"  Checks OK:       {checks_ok}")
    print(f"  Checks falhos:   {total_checks - checks_ok}")
    print()

    if checks_ok == total_checks:
        print("  [SUCESSO] TODAS AS CORRECOES VALIDADAS COM SUCESSO!")
        print()
        print("  Proximos passos:")
        print("  1. Teste manual no dashboard (python app_runner.py)")
        print("  2. Recompile o EXE (COMPILAR.bat)")
        print("  3. Teste o EXE compilado")
        print()
        return True
    else:
        print("  [ATENCAO] ALGUMAS CORRECOES FALHARAM!")
        print()
        print("  Revise os erros acima e execute:")
        print("  - python detalhes/limpar_cache_completo.py")
        print("  - Verifique o settings.json manualmente")
        print()
        return False

if __name__ == "__main__":
    try:
        sucesso = validar_correcoes()
        exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\n[ERRO] ERRO DURANTE VALIDACAO: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
