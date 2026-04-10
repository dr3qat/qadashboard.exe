"""
Script Python para limpeza COMPLETA de cache
Mais robusto que o .bat - remove TODOS os arquivos de cache recursivamente
"""
import os
import shutil
import sys
from pathlib import Path


def limpar_cache_completo():
    """Limpa TODO o cache Python e Pytest do projeto."""
    print("=" * 60)
    print("  LIMPEZA COMPLETA DE CACHE - Testes PDV")
    print("=" * 60)
    print()

    # Diretório raiz do projeto
    raiz = Path(__file__).parent
    os.chdir(raiz)

    total_removido = 0
    pastas_removidas = []
    arquivos_removidos = []

    # 1. Remover .pytest_cache
    print("[1/4] Removendo .pytest_cache...")
    pytest_cache = raiz / ".pytest_cache"
    if pytest_cache.exists():
        shutil.rmtree(pytest_cache, ignore_errors=True)
        pastas_removidas.append(".pytest_cache")
        print("  [OK] .pytest_cache removido")
    else:
        print("  [OK] .pytest_cache não existia")

    # 2. Remover TODOS os __pycache__ recursivamente
    print("\n[2/4] Removendo TODOS os __pycache__ recursivamente...")
    for pycache_dir in raiz.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir, ignore_errors=True)
            pastas_removidas.append(str(pycache_dir.relative_to(raiz)))
            total_removido += 1
        except Exception as e:
            print(f"  [AVISO] Erro ao remover {pycache_dir}: {e}")

    if total_removido > 0:
        print(f"  [OK] {total_removido} pastas __pycache__ removidas")
    else:
        print("  [OK] Nenhuma pasta __pycache__ encontrada")

    # 3. Remover TODOS os arquivos .pyc recursivamente
    print("\n[3/4] Removendo TODOS os arquivos .pyc recursivamente...")
    total_pyc = 0
    for pyc_file in raiz.rglob("*.pyc"):
        try:
            pyc_file.unlink()
            arquivos_removidos.append(str(pyc_file.relative_to(raiz)))
            total_pyc += 1
        except Exception as e:
            print(f"  [AVISO] Erro ao remover {pyc_file}: {e}")

    if total_pyc > 0:
        print(f"  [OK] {total_pyc} arquivos .pyc removidos")
    else:
        print("  [OK] Nenhum arquivo .pyc encontrado")

    # 4. Remover allure-results (opcional)
    print("\n[4/4] Limpando allure-results...")
    allure_dir = raiz / "allure-results"
    if allure_dir.exists():
        shutil.rmtree(allure_dir, ignore_errors=True)
        allure_dir.mkdir(exist_ok=True)
        print("  [OK] allure-results limpo e recriado")
    else:
        print("  [OK] allure-results não existia")

    # 5. Remover .version_atual (força redetecção de versão)
    version_file = raiz / ".version_atual"
    if version_file.exists():
        version_file.unlink()
        print("  [OK] .version_atual removido (forçará redetecção)")

    # Relatório final
    print()
    print("=" * 60)
    print("  LIMPEZA CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print(f"\nTotal de pastas __pycache__ removidas: {total_removido}")
    print(f"Total de arquivos .pyc removidos: {total_pyc}")

    if pastas_removidas:
        print(f"\nPastas removidas ({len(pastas_removidas)}):")
        for pasta in pastas_removidas[:10]:  # Mostra apenas as 10 primeiras
            print(f"  - {pasta}")
        if len(pastas_removidas) > 10:
            print(f"  ... e mais {len(pastas_removidas) - 10} pastas")

    print("\n[INFO] Todos os testes serão carregados dos arquivos atuais.")
    print("[INFO] Execute novamente seus testes para garantir cache limpo.")
    print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(limpar_cache_completo())
    except KeyboardInterrupt:
        print("\n\n[CANCELADO] Limpeza cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO] Erro durante limpeza: {e}")
        sys.exit(1)
