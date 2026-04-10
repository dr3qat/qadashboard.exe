# 📋 Testes - Visão Geral

Estratégia completa de testes do PDV Mobile com 4 camadas de validação.

---

## 🎯 Pirâmide de Testes

```
           /\
          /  \          E2E Tests
         / 48 \         (Testes completos de ponta a ponta)
        /______\        Tempo: 30-45 min
       /        \
      /   Smoke  \      Smoke Tests
     /    18     \     (Testes críticos de sanidade)
    /____________\     Tempo: 8-10 min
   /              \
  /   Unit Tests   \   Unit Tests
 /       236       \  (Testes isolados dos Page Objects)
/__________________\ Tempo: ~25 segundos

         + 5 Negativos (validação de rejeição de entradas inválidas)

TOTAL: 323 TESTES
```

---

## 📊 Resumo Executivo

| Camada | Quantidade | Tempo | Quando Executar | Requer Dispositivo |
|---|---|---|---|---|
| **Unitários** | 236 | ~25s | Sempre (desenvolvimento) | ❌ Não |
| **Smoke** | 18 | 8-10 min | Antes de E2E | ✅ Sim |
| **E2E** | 48 | 30-45 min | Release/CI/CD | ✅ Sim |
| **Negativos** | 5 | ~5 min | Regressão | ✅ Sim |
| **TOTAL** | **323** | | | |

---

## 🧪 Camada 1: Testes Unitários

### Objetivo
Validar Page Objects de forma isolada, sem Appium.

### Características
- ✅ **Rápidos** (~25 segundos total)
- ✅ **Sem dependências** externas (mocks via MagicMock)
- ✅ **100% cobertura** dos Page Objects
- ✅ **Execução local** (não precisa de dispositivo)

### Execução
```bash
pytest tests/unit/ -v
```

### Documentação
📖 [Unit Tests Guide](UNIT_TESTS.md)

---

## 🔥 Camada 2: Smoke Tests

### Objetivo
Validar rapidamente se o ambiente está funcional antes dos testes E2E.

### Características
- ✅ **Rápidos** (8-10 minutos)
- ✅ **Funcionalidades críticas** apenas
- ✅ **Gate para E2E** (se falhar, não rode E2E)
- ✅ **Cobertura ~70%** das funcionalidades principais

### Testes (11 individuais + test_smoke_e2e.py consolidado)
1. App abre e driver responde
2. Login com credenciais válidas
3. Módulos visíveis na home
4. Venda consumidor (fluxo completo)
5. Venda cliente cadastrado (fluxo completo)
6. Consulta estoque produto
7. Cancelar venda vazia + navegação de saída
8. Pedido consumidor fluxo básico
9. Tela troca acessível + campo data presente
10. Borderô abre e processa relatório
11. Documentos abre e consulta executa

### Execução
```bash
pytest tests/smoke/ -v -m smoke
```

### Documentação
📖 [Smoke Tests Guide](SMOKE_TESTS.md)

---

## 🚀 Camada 3: Testes E2E

### Objetivo
Validar todas as funcionalidades do app de ponta a ponta.

### Características
- ✅ **Cobertura completa** (48 testes, 9 subpastas)
- ✅ **Cenários reais** de uso
- ✅ **Validação profunda**
- ✅ **Relatórios detalhados** (Allure)

### Módulos Testados
| Subpasta | Testes | Cobertura |
|---|---|---|
| vendas/ | 18 | Consumidor, cliente, vale presente, bônus, cancelamento, opções item |
| consultas/ | 7 | Estoque, documentos, borderô |
| pedidos/ | 6 | Pedido venda, consumidor, cliente, consulta |
| descontos/ | 6 | Desconto/acréscimo consumidor/cliente, bônus, cashback |
| cliente/ | 3 | Cadastro PF/PJ, histórico |
| trocas/ | 2 | Troca consumidor, troca cliente |
| validar/ | 2 | Validar bônus, validar cashback |
| venda_futura/ | 2 | Retirada, entrega |
| login/ | 2 | Login válido |

### Execução
```bash
pytest tests/e2e/ -v
```

### Documentação
📖 [E2E Tests Guide](E2E_TESTS.md)

---

## 🎯 Estratégia de Execução

### Desenvolvimento Local

```bash
# 1. SEMPRE executar testes unitários primeiro
pytest tests/unit/ -v

# 2. Se mudar algo nos E2E, rodar smoke test
pytest tests/smoke/ -v -m smoke

# 3. Testar funcionalidade específica
pytest tests/e2e/test_venda_consumidor.py -v
```

### Antes de Commit/PR

```bash
# 1. Testes unitários devem passar
pytest tests/unit/ -v

# 2. Smoke test deve passar
pytest tests/smoke/ -v -m smoke
```

### CI/CD Pipeline

```bash
# Stage 1: Unit Tests (sempre)
pytest tests/unit/ -v

# Stage 2: Smoke Tests (se unit passou)
pytest tests/smoke/ -v -m smoke --alluredir=logs/allure-results

# Stage 3: E2E Tests (se smoke passou)
pytest tests/e2e/ -v --alluredir=logs/allure-results

# Stage 4: Relatório
allure generate logs/allure-results
```

---

## 📈 Métricas de Qualidade

### Metas

| Métrica | Meta | Atual | Status |
|---|---|---|---|
| Cobertura de Page Objects | 100% | 100% (17/17) | ✅ |
| Testes Unitários Passando | 100% | 100% (236/236) | ✅ |
| Smoke Tests Passando | 100% | 100% | ✅ |
| Testes E2E Passando | > 90% | ~88% (última execução) | ✅ |
| Tempo Smoke Test | < 15 min | 8-10 min | ✅ |
| Tempo E2E Total | < 60 min | 30-45 min | ✅ |
| Warnings na coleta | 0 | 0 | ✅ |

---

## 🎓 Boas Práticas

### Para Desenvolvedores

1. ✅ **Sempre** rode testes unitários antes de commit
2. ✅ **Crie** testes unitários para novos Page Objects
3. ✅ **Execute** smoke test antes de criar PR
4. ✅ **Documente** novos testes criados

### Para QA

1. ✅ **Smoke test** antes de iniciar testes manuais
2. ✅ **E2E completo** antes de releases
3. ✅ **Analise** relatórios Allure regularmente
4. ✅ **Reporte** falhas intermitentes

### Para CI/CD

1. ✅ **Unit tests** em toda build
2. ✅ **Smoke tests** em branches principais
3. ✅ **E2E completo** antes de deploy em produção
4. ✅ **Armazene** relatórios históricos

---

## 🔧 Configuração

### pytest.ini

```ini
[pytest]
markers =
    smoke: Smoke tests (3-5 min)
    venda: Testes de venda
    pedido: Testes de pedido
    estoque: Testes de estoque
    troca: Testes de troca
    bonus: Testes de bonus
```

### Executar por Marcador

```bash
# Todos os testes de venda
pytest -v -m venda

# Todos os testes de pedido
pytest -v -m pedido

# Smoke tests
pytest -v -m smoke
```

---

## 📊 Relatórios

### Allure

```bash
# Gerar relatório
pytest tests/ -v --alluredir=logs/allure-results
allure serve logs/allure-results
```

### HTML

```bash
pytest tests/ -v --html=report.html --self-contained-html
```

### Console

```bash
pytest tests/ -v --tb=short
```

---

## 🎯 Roadmap

### Próximas Melhorias

- [ ] Aumentar smoke tests para 15 (adicionar validações de relatórios)
- [ ] Criar testes de performance/stress
- [ ] Integrar com CI/CD do GitLab
- [ ] Dashboard em tempo real de execução
- [ ] Testes de compatibilidade multi-dispositivo

---

## 📚 Documentação Completa

- 📖 [Getting Started](GETTING_STARTED.md) - Instalação e primeiro teste
- 📖 [Architecture](ARCHITECTURE.md) - Estrutura do projeto
- 📖 [Unit Tests](UNIT_TESTS.md) - Testes unitários detalhados
- 📖 [Smoke Tests](SMOKE_TESTS.md) - Smoke tests detalhados
- 📖 [E2E Tests](E2E_TESTS.md) - Testes E2E detalhados
- 📖 [Page Objects](PAGE_OBJECTS.md) - Referência dos Page Objects

---

**Última atualização**: 10/04/2026
**Versão**: 2.0.108
