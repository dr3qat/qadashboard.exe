# Sistema de Limpeza Automática de Cache

## Problema Resolvido

Quando uma nova versão do exe é instalada por cima de uma versão anterior, o cache do pytest (`.pytest_cache` e `__pycache__`) pode causar problemas, fazendo com que testes deletados ainda apareçam na listagem.

## Solução Implementada

### 1. Limpeza Automática Durante Instalação

**Arquivo:** `scripts/post_install.bat`

Este script é executado automaticamente pelo instalador Inno Setup após a instalação/atualização. Ele:
- Limpa `.pytest_cache`
- Limpa `__pycache__` de todas as pastas
- Remove arquivos `.pyc`
- Remove `.version_atual` para forçar detecção de nova versão

### 2. Limpeza Automática Durante Execução

**Modificações em 3 Camadas:**

#### a) `pytest.ini`
```ini
addopts =
    --cache-clear              # Limpa cache do pytest
    -p no:cacheprovider        # Desabilita cache provider
```

#### b) `conftest.py`
```python
def pytest_sessionstart(session):
    """Hook chamado no início da sessão - limpa cache automaticamente."""
    _limpar_cache_pytest()
```

#### c) `run_debug.bat` e `run_normal.bat`
```batch
REM Limpar cache antes de executar
if exist .pytest_cache rmdir /s /q .pytest_cache
# ... remove todos os __pycache__
```

### 3. Script Manual de Limpeza

**Arquivo:** `clean_cache.bat`

Para usuários que queiram limpar o cache manualmente:
```batch
clean_cache.bat
```

## Integração com Builder

**ATENÇÃO:** O arquivo `scripts/post_install.bat` deve ser incluído no instalador Inno Setup.

### Adição no builder_pro.py

O builder já copia a pasta `scripts/` inteira, então o `post_install.bat` será incluído automaticamente.

### Configuração no Inno Setup

No arquivo `.iss` gerado, adicionar:

```iss
[Run]
; Executar script de limpeza após instalação
Filename: "{app}\scripts\post_install.bat"; \
    Parameters: ""; \
    WorkingDir: "{app}"; \
    Flags: runhidden waituntilterminated; \
    StatusMsg: "Limpando cache..."
```

## Estrutura Final de Testes

### Testes de Pedido e Consulta (Separados por Tipo)

```
tests/e2e/
├── test_pedido_vendaConsumidor.py          # Pedido sem cliente
├── test_consulta_pedidoConsumidor.py       # Consulta pedido consumidor
├── test_pedido_vendaCliente.py             # Pedido com cliente
└── test_consulta_pedidoCliente.py          # Consulta pedido cliente
```

**Total: 4 testes**
1. `test_pedido_venda_consumidor_sucesso`
2. `test_consulta_pedido_consumidor_sucesso`
3. `test_pedido_venda_cliente_sucesso`
4. `test_consulta_pedido_cliente_sucesso`

## Validação

### Testes E2E
```bash
pytest tests/e2e/test_*pedido*.py --collect-only
# Deve coletar exatamente 4 testes
```

### Testes Unitários
```bash
pytest tests/unit/ -v
# Deve passar todos os 200 testes unitários
```

## Benefícios

✅ **Cache sempre limpo** - Não há risco de testes fantasmas
✅ **Instalação automática** - Script post_install.bat roda sozinho
✅ **Múltiplas camadas** - Limpeza em install, runtime e manual
✅ **Arquivos separados** - Cada tipo de teste tem seu próprio arquivo
✅ **Ordem garantida** - conftest.py mantém a ordem correta de execução

## Ordem de Execução (conftest.py)

```python
ORDEM_TESTES = [
    # ... outros testes ...
    "test_pedido_venda_consumidor_sucesso",     # 1. Criar pedido consumidor
    "test_consulta_pedido_consumidor_sucesso",  # 2. Finalizar pedido consumidor
    "test_pedido_venda_cliente_sucesso",        # 3. Criar pedido cliente
    "test_consulta_pedido_cliente_sucesso",     # 4. Finalizar pedido cliente
    # ... outros testes ...
]
```

Esta ordem garante que:
1. O pedido é criado antes de ser consultado
2. O teste de consulta sempre encontra um pedido pendente
3. Os fluxos de consumidor e cliente não interferem entre si
