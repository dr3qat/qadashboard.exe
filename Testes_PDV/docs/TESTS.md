# 📋 Testes - Visão Geral

Estratégia completa de testes do PDV Mobile com 3 camadas de validação.

---

## 🎯 Pirâmide de Testes

```
           /\
          /  \          E2E Tests
         / 54 \         (Testes completos de ponta a ponta)
        /______\        Tempo: 30-45 min
       /        \
      /   Smoke  \      Smoke Tests
     /    10     \     (Testes críticos de sanidade)
    /____________\     Tempo: 3-5 min
   /              \
  /   Unit Tests   \   Unit Tests
 /       200       \  (Testes isolados dos Page Objects)
/__________________\ Tempo: < 10 segundos

TOTAL: 264 TESTES
```

---

## 📊 Resumo Executivo

| Camada | Quantidade | Tempo | Quando Executar | Requer Dispositivo |
|--------|-----------|-------|----------------|-------------------|
| **Unit** | 200 | < 10s | Sempre (desenvolvimento) | ❌ Não |
| **Smoke** | 10 | 3-5 min | Antes de E2E | ✅ Sim |
| **E2E** | 54 | 30-45 min | Release/CI/CD | ✅ Sim |

---

## 🧪 Camada 1: Testes Unitários

### Objetivo
Validar Page Objects de forma isolada, sem Appium.

### Características
- ✅ **Ultra-rápidos** (< 10 segundos total)
- ✅ **Sem dependências** externas (mocks)
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
- ✅ **Rápidos** (3-5 minutos)
- ✅ **Funcionalidades críticas** apenas
- ✅ **Gate para E2E** (se falhar, não rode E2E)
- ✅ **Cobertura ~70%** das funcionalidades principais

### Testes
1. App abre corretamente
2. Login funciona
3. Elementos básicos visíveis
4. Navegação funciona
5. Servidor respondendo
6. Venda básica
7. Cancelamento
8. Pedido básico
9. Navegação entre módulos
10. Recuperação de botão back

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
- ✅ **Cobertura completa** (54 testes)
- ✅ **Cenários reais** de uso
- ✅ **Validação profunda**
- ✅ **Relatórios detalhados** (Allure)

### Módulos Testados
- Login (1 teste)
- Vendas - Consumidor (2 testes)
- Vendas - Cliente (2 testes)
- Pedidos (3 testes)
- Estoque (4 testes)
- Trocas - Consumidor (2 testes)
- Trocas - Cliente (2 testes)
- Bonus/Cashback (2 testes)
- Consulta de Pedidos (2 testes)
- Vendas Futuras (2 testes)
- Cancelamentos (6 testes)
- Outros (26 testes)

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
|---------|------|-------|--------|
| Cobertura de Page Objects | 100% | 100% | ✅ |
| Testes Unitários Passando | 100% | 98.5% | ⚠️ |
| Smoke Tests Passando | 100% | 100% | ✅ |
| Testes E2E Passando | > 95% | ~96% | ✅ |
| Tempo Smoke Test | < 5 min | 3-5 min | ✅ |
| Tempo E2E Total | < 60 min | 30-45 min | ✅ |

### Tendências

```
Testes Unitários:
  Jan 2026: 171 testes
  Feb 2026: 200 testes (+29, +17%)

Smoke Tests:
  Jan 2026: 5 testes (~30% cobertura)
  Feb 2026: 10 testes (~70% cobertura, +100%)

Page Objects Testados:
  Jan 2026: 8/9 (88.9%)
  Feb 2026: 10/10 (100%, +11.1%)
```

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

**Última atualização**: 24/02/2026
**Versão**: 2.1
