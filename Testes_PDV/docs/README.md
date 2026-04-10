# 📚 Documentação - PDV Mobile Testes

Bem-vindo à documentação completa do framework de testes automatizados do PDV Mobile.

---

## 📖 Índice da Documentação

### 🚀 Para Começar

- **[Getting Started](GETTING_STARTED.md)**
  - Instalação completa do ambiente
  - Configuração de pré-requisitos
  - Executando seu primeiro teste
  - Troubleshooting de problemas comuns
  - Checklist de verificação

### 🏗️ Arquitetura e Visão Geral

- **[Testes - Visão Geral](TESTS.md)**
  - Pirâmide de testes (Unit → Smoke → E2E)
  - Estratégia de execução
  - Métricas de qualidade
  - Boas práticas

### 🧪 Tipos de Testes

- **[Testes Unitários](UNIT_TESTS.md)**
  - Estrutura e padrões
  - AAA Pattern (Arrange-Act-Assert)
  - Técnicas de mocking
  - Exemplos completos
  - 200 testes | < 10 segundos

- **[Smoke Tests](SMOKE_TESTS.md)**
  - 10 testes críticos
  - Validação de ambiente
  - Gate para testes E2E
  - 3-5 minutos

### 📦 Referências

- **[Page Objects](PAGE_OBJECTS.md)**
  - Referência completa de todos os Page Objects
  - Métodos disponíveis
  - Exemplos de uso
  - Boas práticas
  - 10 Page Objects documentados

---

## 🎯 Guia Rápido

### Novo no Projeto?

1. Leia [Getting Started](GETTING_STARTED.md)
2. Execute testes unitários: `pytest tests/unit/ -v`
3. Execute smoke tests: `pytest tests/smoke/ -v -m smoke`
4. Explore a [Visão Geral dos Testes](TESTS.md)

### Desenvolvedor?

1. [Testes Unitários](UNIT_TESTS.md) - Como criar testes para Page Objects
2. [Page Objects](PAGE_OBJECTS.md) - Referência de métodos
3. [Testes](TESTS.md) - Estratégia de execução

### QA Engineer?

1. [Smoke Tests](SMOKE_TESTS.md) - Validação rápida de ambiente
2. [Testes](TESTS.md) - Overview completo
3. [Getting Started](GETTING_STARTED.md) - Setup do ambiente

---

## 📊 Status do Projeto

| Componente | Status | Documentação |
|-----------|--------|--------------|
| Testes Unitários | ✅ 197/200 (98.5%) | [UNIT_TESTS.md](UNIT_TESTS.md) |
| Smoke Tests | ✅ 10/10 (100%) | [SMOKE_TESTS.md](SMOKE_TESTS.md) |
| Testes E2E | ✅ ~96% | - |
| Page Objects | ✅ 10/10 (100%) | [PAGE_OBJECTS.md](PAGE_OBJECTS.md) |
| Documentação | ✅ Completa | Você está aqui! |

---

## 🔗 Links Úteis

### Projeto

- [README Principal](../README.md) - Raiz do projeto
- [Configuração](../config.py) - Config global
- [Dados de Teste](../test_data.py) - Dados para testes

### Executar Testes

```bash
# Testes Unitários (rápido)
pytest tests/unit/ -v

# Smoke Tests (3-5 min)
pytest tests/smoke/ -v -m smoke

# Todos com relatório
pytest -v --alluredir=logs/allure-results
allure serve logs/allure-results
```

### Recursos Externos

- [Appium Documentation](https://appium.io/docs/en/2.0/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Reports](https://docs.qameta.io/allure/)
- [Page Object Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

---

## 📝 Histórico de Atualizações

### Versão 2.1 (24/02/2026)

#### ✨ Novidades
- **BonusPage**: 29 novos testes unitários adicionados
- **Smoke Tests**: Expandido de 5 para 10 testes (+100%)
- **EstoquePage**: Corrigido e adicionado ao projeto
- **Documentação**: 6 novos documentos criados

#### 📊 Estatísticas
- Testes Unitários: 171 → **200** (+17%)
- Smoke Tests: 5 → **10** (+100%)
- Cobertura Page Objects: 88.9% → **100%**
- Cobertura Smoke: 30% → **70%**

#### 📚 Documentação Criada
1. README.md principal
2. docs/GETTING_STARTED.md
3. docs/TESTS.md
4. docs/UNIT_TESTS.md
5. docs/SMOKE_TESTS.md
6. docs/PAGE_OBJECTS.md

---

## 🤝 Contribuindo

### Adicionando Nova Documentação

1. Crie o arquivo `.md` na pasta `docs/`
2. Adicione ao índice deste README
3. Mantenha formato consistente
4. Use emojis para melhor visualização

### Atualizando Documentação

1. Atualize o documento relevante
2. Atualize a data no rodapé
3. Adicione ao [Histórico de Atualizações](#-histórico-de-atualizações)

---

## 📞 Suporte

Precisa de ajuda?

1. Consulte [Getting Started - Troubleshooting](GETTING_STARTED.md#-problemas-comuns)
2. Verifique os logs em `logs/allure-results`
3. Entre em contato com a equipe de QA Mobile

---

**Última atualização**: 24/02/2026
**Versão da Documentação**: 2.1
**Total de Documentos**: 6 + README principal
