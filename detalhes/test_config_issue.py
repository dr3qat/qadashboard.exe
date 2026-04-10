"""
Script de teste para reproduzir o problema de configuração
"""
import json
import os

# Simula o comportamento do dashboard

# 1. Carrega o settings.json atual
settings_file = r"D:\PDV_AUTOMACAO\Gerador_EXE\runner\settings.json"

print("=" * 60)
print("TESTE: Problema de Configuração no Dashboard")
print("=" * 60)

# Lê o arquivo atual
with open(settings_file, 'r', encoding='utf-8') as f:
    data_atual = json.load(f)

print("\n1. CAMPOS NO SETTINGS.JSON ATUAL:")
print(f"   Total de campos: {len(data_atual)}")
for key in sorted(data_atual.keys()):
    print(f"   - {key}: {data_atual[key]}")

# 2. Campos esperados pelo código (conforme app_runner.py linha 376-406)
campos_esperados = {
    "server_ip": "",
    "server_port": "",
    "company": "",
    "user": "",
    "password": "",
    "customer_id": "",
    "customer_id_troca": "",
    "appium_port": "4723",
    "appium_path": "",
    "qa_dev_path": "",
    "timeout_default": "30",
    "product_code_sale": "",
    "product_code_future_sale": "",
    "product_size_future": "",
    "product_code_stock_1": "",
    "product_code_stock_2": "",
    "clean_logs": False,
    "auto_open": False,
    "use_allure": False,
    "generate_single_file": False,
    "open_allure_end": False,
    "print_cupom_venda": False,
    "print_nfce": False,
    "print_danfe": False,
    "print_cupom_troca": False,
    "print_dialog_timeout": "20"
}

print(f"\n2. CAMPOS ESPERADOS PELO CÓDIGO:")
print(f"   Total de campos: {len(campos_esperados)}")
for key in sorted(campos_esperados.keys()):
    print(f"   - {key}: {campos_esperados[key]}")

# 3. Identifica campos faltando
faltando = set(campos_esperados.keys()) - set(data_atual.keys())
extras = set(data_atual.keys()) - set(campos_esperados.keys())

print(f"\n3. ANÁLISE DE DIFERENÇAS:")
if faltando:
    print(f"   ❌ Campos FALTANDO no settings.json ({len(faltando)}):")
    for campo in sorted(faltando):
        print(f"      - {campo} (padrão: {campos_esperados[campo]})")
else:
    print("   ✅ Nenhum campo faltando")

if extras:
    print(f"\n   ⚠️  Campos EXTRAS no settings.json ({len(extras)}):")
    for campo in sorted(extras):
        print(f"      - {campo}")
else:
    print("   ✅ Nenhum campo extra")

# 4. Simula o que acontece ao salvar
print(f"\n4. SIMULAÇÃO: O que acontece ao salvar?")
print("   Código: data = {k: v.get() for k, v in self.config_vars.items()}")
print("   Resultado: DEVERIA incluir TODOS os 27 campos de config_vars")
print("   Mas se os campos não existirem no arquivo original,")
print("   eles podem não ser carregados corretamente na inicialização!")

# 5. Diagnóstico
print(f"\n5. DIAGNÓSTICO:")
if faltando:
    print("   🔴 PROBLEMA IDENTIFICADO:")
    print(f"      O settings.json está faltando {len(faltando)} campos!")
    print("      Quando o dashboard carrega, esses campos ficam com valores padrão.")
    print("      Se o usuário não preencher manualmente, eles podem ser salvos vazios.")
    print("\n   💡 SOLUÇÃO:")
    print("      1. Adicionar os campos faltando ao settings.json")
    print("      2. Garantir que carregar_inicializacao() use valores padrão se campo não existir")
    print("      3. Limpar cache antes de compilar")
else:
    print("   ✅ Todos os campos estão presentes!")
    print("   O problema pode ser outro (cache, lógica de carregar/salvar)")

print("\n" + "=" * 60)
