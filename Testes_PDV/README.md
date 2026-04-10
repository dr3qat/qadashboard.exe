# 🧪 Testes Automatizados - PDV Mobile

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Appium](https://img.shields.io/badge/Appium-2.0-green)
![Pytest](https://img.shields.io/badge/Pytest-9.0-orange)
![Status](https://img.shields.io/badge/Status-Ativo-success)
![Testes](https://img.shields.io/badge/Testes-323-brightgreen)

Framework de testes automatizados para o aplicativo PDV Mobile (Android), utilizando Appium, Python e o padrão Page Object Model (POM).

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Estatísticas](#estatísticas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Execução dos Testes](#execução-dos-testes)
- [Documentação](#documentação)
- [Relatórios](#relatórios)

---

## 🎯 Sobre o Projeto

Suite completa de testes automatizados para o aplicativo PDV Mobile, cobrindo:

- **Testes Unitários**: Validação isolada dos Page Objects sem interação com o Appium
- **Smoke Tests**: Validação rápida de sanidade do ambiente (~8-10 min)
- **Testes E2E**: Testes completos de ponta a ponta de todas as funcionalidades
- **Testes Negativos**: Validação de rejeição de entradas inválidas

### Funcionalidades Testadas

- ✅ Login e Autenticação
- ✅ Vendas (Consumidor e Cliente)
- ✅ Vendas com Desconto e Acréscimo
- ✅ Pedidos de Venda
- ✅ Consulta de Estoque
- ✅ Trocas e Devoluções
- ✅ Consulta de Pedidos
- ✅ Vendas Futuras (Retirada e Entrega)
- ✅ Bônus/Cashback
- ✅ Cancelamentos
- ✅ Cadastro de Clientes (PF/PJ)
- ✅ Histórico de Clientes
- ✅ Documentos Fiscais
- ✅ Vale Presente
- ✅ Borderô
- ✅ Opções de Item no Carrinho

---

## 📊 Estatísticas

### Cobertura de Testes

| Tipo de Teste | Arquivos | Testes | Tempo Estimado | Status |
|---|---|---|---|---|
| **Unitários** | 14 | **236** | ~25 segundos | ✅ 236/236 passando |
| **Smoke** | 12 | **18** | ~8-10 minutos | ✅ Funcional |
| **E2E** | 29 | **48** | ~30-45 minutos | ✅ Funcional |
| **Negativos** | 3 | **5** | ~5 minutos | ✅ Funcional |
| **TOTAL** | **58** | **323** | | ✅ 0 warnings na coleta |

### Page Objects (17)

| Page Object | Responsabilidade |
|---|---|
| `BasePage` | 50+ métodos comuns (busca, clique, scroll, digitação) |
| `LoginPage` | Login + configuração de servidor |
| `HomePage` | Tela inicial + navegação entre módulos |
| `VendaPage` | Vendas consumidor e cliente |
| `VendaSucessoPage` | Tela de sucesso + impressões (NFC-E, DANFE, cupom) |
| `PedidoPage` | Pedidos de venda |
| `EstoquePage` | Consulta de estoque |
| `TrocaPage` | Trocas e devoluções |
| `BonusPage` | Bônus/cashback |
| `ConsultaPedidoPage` | Consulta e finalização de pedidos |
| `VendaFuturaPage` | Vendas futuras (retirada e entrega) |
| `BorderoPage` | Relatório de borderô |
| `ClientePage` | Cadastro PF/PJ (usa Faker) |
| `HistoricoClientePage` | Histórico de compras do cliente |
| `DocumentosPage` | Consulta de documentos fiscais |
| `ValePresentePage` | Venda de vale presente |
| `OpcoesItemPage` | Opções do item no carrinho |

---

## 📁 Estrutura do Projeto

```
Testes_PDV/
├── pages/                      # 17 Page Objects (POM)
│   ├── base_page.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── venda_page.py
│   ├── venda_sucesso_page.py
│   ├── pedido_page.py
│   ├── estoque_page.py
│   ├── troca_page.py
│   ├── bonus_page.py
│   ├── consulta_pedido_page.py
│   ├── venda_futura_page.py
│   ├── bordero_page.py
│   ├── cliente_page.py
│   ├── historico_cliente_page.py
│   ├── documentos_page.py
│   ├── vale_presente_page.py
│   └── opcoes_item_page.py
│
├── tests/
│   ├── unit/                   # 236 testes unitários (14 arquivos)
│   │   ├── test_base_page_unit.py
│   │   ├── test_bonus_page_unit.py
│   │   ├── test_config_unit.py
│   │   ├── test_consulta_pedido_page_unit.py
│   │   ├── test_documentos_page_unit.py
│   │   ├── test_estoque_page_unit.py
│   │   ├── test_home_page_unit.py
│   │   ├── test_locators_unit.py
│   │   ├── test_login_page_unit.py
│   │   ├── test_pedido_page_unit.py
│   │   ├── test_troca_page_unit.py
│   │   ├── test_vale_presente_page_unit.py
│   │   ├── test_venda_futura_page_unit.py
│   │   └── test_venda_page_unit.py
│   │
│   ├── smoke/                  # 18 testes (12 arquivos)
│   │   ├── test_01_app_abre.py
│   │   ├── test_02_login.py
│   │   ├── test_03_home_modulos.py
│   │   ├── test_04_venda_consumidor.py
│   │   ├── test_05_venda_cliente.py
│   │   ├── test_06_consultar_estoque.py
│   │   ├── test_07_cancelar_venda.py
│   │   ├── test_08_pedido.py
│   │   ├── test_09_troca.py
│   │   ├── test_10_bordero.py
│   │   ├── test_11_documentos.py
│   │   └── test_smoke_e2e.py   # consolidado (7 testes)
│   │
│   ├── e2e/                    # 48 testes (29 arquivos, 9 subpastas)
│   │   ├── cliente/            # 3 testes
│   │   ├── consultas/          # 7 testes
│   │   ├── descontos/          # 6 testes
│   │   ├── login/              # 2 testes
│   │   ├── pedidos/            # 6 testes
│   │   ├── trocas/             # 2 testes
│   │   ├── validar/            # 2 testes
│   │   ├── venda_futura/       # 2 testes
│   │   └── vendas/             # 18 testes
│   │
│   └── negativos/              # 5 testes (3 arquivos)
│       ├── test_login_invalido.py
│       ├── test_busca_invalida.py
│       └── test_troca_sem_resultado.py
│
├── config.py                   # Logger + configurações globais
├── conftest.py                 # Fixtures pytest (driver, driver_logado)
├── test_data.py                # Dados externalizados (IP, senha, IDs)
├── framework.py                # Utilitários Appium (legado)
├── pytest.ini                  # Configuração pytest
├── requirements.txt            # Dependências Python
└── docs/                       # Documentação detalhada
    ├── GETTING_STARTED.md
    ├── TESTS.md
    ├── UNIT_TESTS.md
    ├── SMOKE_TESTS.md
    └── PAGE_OBJECTS.md
```

---

## 🛠️ Tecnologias

- **Python 3.13** + **Appium 2.0** + **Pytest 9.0** + **Allure Reports**
- **Page Object Model (POM)** — arquitetura de testes
- **MagicMock** — isolamento nos testes unitários
- **Faker** — geração de dados nos testes de cadastro

---

## 🚀 Instalação

```bash
cd D:\PDV_AUTOMACAO\Testes_PDV
pip install -r requirements.txt

# Appium (se não tiver)
npm install -g appium
appium driver install uiautomator2
```

---

## ▶️ Execução dos Testes

```bash
cd D:\PDV_AUTOMACAO\Testes_PDV

# Unitários (sem device, ~25s)
pytest tests/unit/ -v

# Smoke (device conectado, ~8-10min)
pytest tests/smoke/ -v -m smoke

# E2E completo (device conectado, ~30-45min)
pytest tests/e2e/ -v

# Negativos
pytest tests/negativos/ -v

# Teste específico
pytest tests/e2e/vendas/test_venda_cliente.py -v

# Com relatório Allure
pytest --alluredir=logs/allure-results && allure serve logs/allure-results
```

---

## 📚 Documentação

| Arquivo | Conteúdo |
|---|---|
| `docs/GETTING_STARTED.md` | Guia de início rápido |
| `docs/TESTS.md` | Estratégia de testes |
| `docs/UNIT_TESTS.md` | Testes unitários |
| `docs/SMOKE_TESTS.md` | Smoke tests |
| `docs/PAGE_OBJECTS.md` | Referência dos Page Objects |
| `../CLAUDE.md` | Instruções completas (arquitetura, fluxos, padrões) |

---

## 📈 Relatórios

```bash
pytest -v --alluredir=logs/allure-results
allure serve logs/allure-results
```

Allure gera: histórico, gráficos, screenshots de falhas, logs por teste, categorização por severidade.

---

**Versão**: 2.0.108 | **Última atualização**: 10/04/2026
