# 🧪 Testes Automatizados - PDV Mobile

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Appium](https://img.shields.io/badge/Appium-2.0-green)
![Pytest](https://img.shields.io/badge/Pytest-9.0-orange)
![Status](https://img.shields.io/badge/Status-Ativo-success)

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

Este projeto contém a suite completa de testes automatizados para o aplicativo PDV Mobile, cobrindo:

- **Testes Unitários**: Validação isolada dos Page Objects sem interação com o Appium
- **Smoke Tests**: Validação rápida de sanidade do ambiente (3-5 min)
- **Testes E2E**: Testes completos de ponta a ponta de todas as funcionalidades

### Funcionalidades Testadas

- ✅ Login e Autenticação
- ✅ Vendas (Consumidor e Cliente)
- ✅ Pedidos de Venda
- ✅ Consulta de Estoque
- ✅ Trocas e Devoluções
- ✅ Consulta de Pedidos
- ✅ Vendas Futuras
- ✅ Bonus/Cashback
- ✅ Cancelamentos

---

## 📊 Estatísticas

### Cobertura de Testes

| Tipo de Teste | Quantidade | Tempo Estimado | Status |
|--------------|-----------|---------------|--------|
| **Testes Unitários** | 200 | < 10 segundos | ✅ 197/200 passando |
| **Smoke Tests** | 10 | 3-5 minutos | ✅ Funcional |
| **Testes E2E** | 54 | 30-45 minutos | ✅ Funcional |
| **TOTAL** | **264** | **~40 minutos** | ✅ |

### Page Objects

| Page Object | Testes Unitários | Testes E2E | Status |
|------------|-----------------|-----------|--------|
| BasePage | 23 | - | ✅ 100% |
| LoginPage | 7 | 1 | ✅ 100% |
| HomePage | 7 | - | ✅ 100% |
| VendaPage | 15 | 2 | ✅ 100% |
| PedidoPage | 10 | 4 | ✅ 100% |
| EstoquePage | 23 | 4 | ✅ 100% |
| TrocaPage | 19 | 4 | ✅ 100% |
| BonusPage | 29 | 2 | ✅ 100% |
| ConsultaPedidoPage | 7 | 4 | ✅ 100% |
| VendaFuturaPage | 20 | 2 | ✅ 100% |
| VendaSucessoPage | - | - | ✅ 100% |
| **TOTAL** | **160** | **23** | **11/11 (100%)** |

---

## 📁 Estrutura do Projeto

```
Testes_PDV/
├── 📂 pages/                    # Page Objects (POM)
│   ├── base_page.py            # Classe base com métodos comuns
│   ├── login_page.py
│   ├── home_page.py
│   ├── venda_page.py
│   ├── venda_sucesso_page.py   # ⭐ NOVO - Tela de sucesso
│   ├── pedido_page.py
│   ├── estoque_page.py
│   ├── troca_page.py
│   ├── bonus_page.py
│   ├── consulta_pedido_page.py
│   └── venda_futura_page.py
│
├── 📂 tests/                    # Testes
│   ├── 📂 unit/                # Testes unitários (200 testes)
│   │   ├── test_base_page_unit.py
│   │   ├── test_bonus_page_unit.py (✨ NOVO - 29 testes)
│   │   ├── test_estoque_page_unit.py
│   │   ├── test_login_page_unit.py
│   │   ├── test_venda_page_unit.py
│   │   └── ...
│   │
│   ├── 📂 smoke/               # Smoke tests (10 testes)
│   │   └── test_smoke_e2e.py  (✨ EXPANDIDO - 5→10 testes)
│   │
│   └── 📂 e2e/                 # Testes E2E (14 arquivos)
│       ├── test_login.py
│       ├── test_venda_consumidor.py
│       ├── test_venda_cliente.py
│       ├── test_pedido_vendaConsumidor.py  # ⭐ SEPARADO
│       ├── test_pedido_vendaCliente.py     # ⭐ SEPARADO
│       ├── test_estoque.py
│       ├── test_troca_consumidor.py
│       ├── test_troca_cliente.py
│       ├── test_bonus.py
│       ├── test_consulta_pedidoConsumidor.py  # ⭐ SEPARADO
│       ├── test_consulta_pedidoCliente.py     # ⭐ SEPARADO
│       ├── test_venda_futura.py
│       ├── test_venda_futura_domicilio.py
│       └── test_cancelamento.py
│
├── 📂 logs/                     # Logs de execução
│   └── allure-results/         # Resultados Allure
│
├── 📂 docs/                     # Documentação
│   ├── GETTING_STARTED.md      # Guia de início rápido
│   ├── ARCHITECTURE.md         # Arquitetura do projeto
│   ├── TESTS.md                # Visão geral dos testes
│   ├── UNIT_TESTS.md           # Documentação dos testes unitários
│   ├── SMOKE_TESTS.md          # Documentação dos smoke tests
│   ├── E2E_TESTS.md            # Documentação dos testes E2E
│   └── PAGE_OBJECTS.md         # Documentação dos Page Objects
│
├── config.py                   # Configurações globais
├── conftest.py                 # Fixtures do pytest
├── test_data.py                # Dados de teste
├── framework.py                # Framework Appium
├── pytest.ini                  # Configuração pytest
├── requirements.txt            # Dependências Python
├── run_normal.bat              # Executar todos os testes
└── run_debug.bat               # Executar com debug
```

---

## 🛠️ Tecnologias

### Core
- **Python 3.13** - Linguagem de programação
- **Appium 2.0** - Automação mobile
- **Pytest 9.0** - Framework de testes
- **Selenium 4.x** - WebDriver

### Relatórios e Visualização
- **Allure** - Relatórios interativos
- **pytest-html** - Relatórios HTML
- **Logging customizado** - Logs coloridos e detalhados

### Padrões e Arquitetura
- **Page Object Model (POM)** - Organização dos elementos
- **AAA Pattern** - Arrange-Act-Assert nos testes
- **Fixtures** - Reutilização de setup/teardown
- **Mocks** - Testes unitários isolados

---

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.8+** instalado
2. **Java JDK 11+** instalado (para Appium)
3. **Node.js 16+** instalado
4. **Android SDK** configurado
5. **Appium Server 2.0+** instalado

### Passo a Passo

```bash
# 1. Clone o repositório
cd D:\PDV_AUTOMACAO\Testes_PDV

# 2. Crie um ambiente virtual (opcional mas recomendado)
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Instale o Appium (se não tiver)
npm install -g appium
appium driver install uiautomator2

# 5. Configure o test_data.py com seus dados
# Edite test_data.py com IP do servidor, credenciais, etc.
```

### Verificação da Instalação

```bash
# Verificar Python
python --version

# Verificar Appium
appium --version

# Verificar ADB
adb version

# Listar dispositivos conectados
adb devices
```

---

## ▶️ Execução dos Testes

### Testes Unitários (Rápido - <10s)

```bash
# Executar todos os testes unitários
pytest tests/unit/ -v

# Executar testes de um Page Object específico
pytest tests/unit/test_bonus_page_unit.py -v

# Ver duração dos testes
pytest tests/unit/ -v --durations=10
```

### Smoke Tests (3-5 minutos)

```bash
# Executar smoke tests
pytest tests/smoke/ -v -m smoke

# Com relatório Allure
pytest tests/smoke/ -v -m smoke --alluredir=logs/allure-results
allure serve logs/allure-results
```

### Testes E2E (30-45 minutos)

```bash
# Executar todos os testes E2E
pytest tests/e2e/ -v

# Executar teste específico
pytest tests/e2e/test_venda_consumidor.py -v

# Executar com tag específica
pytest tests/e2e/ -v -m venda
```

### Executar Tudo

```bash
# Windows
run_normal.bat

# Linux/Mac
pytest -v --alluredir=logs/allure-results
```

### Com Relatório Allure

```bash
# Executar testes e gerar relatório
pytest -v --alluredir=logs/allure-results
allure serve logs/allure-results
```

---

## 📚 Documentação

Documentação detalhada disponível na pasta `docs/`:

- **[Getting Started](docs/GETTING_STARTED.md)** - Guia completo de instalação e primeiro teste
- **[Arquitetura](docs/ARCHITECTURE.md)** - Estrutura e padrões do projeto
- **[Testes](docs/TESTS.md)** - Visão geral da estratégia de testes
- **[Testes Unitários](docs/UNIT_TESTS.md)** - Como criar e executar testes unitários
- **[Smoke Tests](docs/SMOKE_TESTS.md)** - Documentação dos smoke tests
- **[Testes E2E](docs/E2E_TESTS.md)** - Guia completo dos testes E2E
- **[Page Objects](docs/PAGE_OBJECTS.md)** - Referência dos Page Objects

---

## 📈 Relatórios

### Allure Reports

Os relatórios Allure fornecem visualização rica dos resultados:

- ✅ Histórico de execuções
- ✅ Gráficos de sucesso/falha
- ✅ Screenshots de falhas
- ✅ Logs detalhados
- ✅ Categorização por severidade
- ✅ Tempo de execução

```bash
# Gerar e visualizar relatório
pytest -v --alluredir=logs/allure-results
allure serve logs/allure-results
```

### Logs

Logs detalhados são gerados em:
- **Console**: Saída colorida em tempo real
- **Allure**: Logs anexados aos testes

---

## 🎯 Padrões de Código

### Estrutura de Teste Unitário

```python
class TestNomePageMetodo:
    """Testes para o método metodo_exemplo."""

    @patch('pages.nome_page.BasePage.__init__', return_value=None)
    @patch('pages.nome_page.logger')
    def test_metodo_cenario_resultado_esperado(self, mock_logger, mock_base_init):
        """Descrição do teste."""
        from pages.nome_page import NomePage

        # Arrange
        page = NomePage.__new__(NomePage)
        page.driver = MagicMock()
        page.metodo_mock = MagicMock(return_value=valor_esperado)

        # Act
        resultado = page.metodo_testado()

        # Assert
        assert resultado == valor_esperado
        page.metodo_mock.assert_called_once()
```

### Estrutura de Teste E2E

```python
@allure.title("Título do Teste")
@allure.description("Descrição detalhada")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("tag1", "tag2")
def test_nome_teste(self, driver_logado):
    """Cenário do teste em formato BDD."""
    driver = driver_logado
    page = NomePage(driver)

    with allure.step("1. Primeiro passo"):
        page.acao_1()

    with allure.step("2. Segundo passo"):
        page.acao_2()

    with allure.step("3. Validação"):
        assert page.validacao()
```

---

## 🐛 Troubleshooting

### Problemas Comuns

**1. Appium não conecta ao dispositivo**
```bash
# Verificar dispositivos
adb devices

# Reiniciar ADB
adb kill-server
adb start-server
```

**2. Testes falhando intermitentemente**
- Aumentar tempos de espera em `config.py`
- Verificar estabilidade da conexão com servidor
- Verificar memória do dispositivo

**3. Import errors**
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

**4. Testes unitários falhando após mudanças**
- Verificar se os mocks estão atualizados
- Verificar nomenclatura dos métodos
- Executar: `pytest tests/unit/ -v --tb=short`

---

## 📝 Changelog

### [2.0.5] - 2026-03-03

#### ✨ Adicionado
- **VendaSucessoPage** - Novo Page Object dedicado à tela de sucesso de vendas
- **Reorganização dos testes E2E** - Separação por tipo de cliente:
  - test_pedido_vendaConsumidor.py e test_pedido_vendaCliente.py
  - test_consulta_pedidoConsumidor.py e test_consulta_pedidoCliente.py

#### 🔧 Atualizado
- Documentação sincronizada com estrutura atual de arquivos
- Contagem de Page Objects: 10 → **11**
- Estrutura de testes E2E mais organizada e modular

#### 📊 Estatísticas Atualizadas
- **Page Objects:** 11 (100% cobertos)
- **Testes E2E:** 14 arquivos
- **Testes Unitários:** 12 arquivos
- **Testes Smoke:** 1 arquivo

### [2.1.0] - 2026-02-24

#### ✨ Adicionado
- **Testes Unitários para BonusPage** (29 novos testes)
  - Cobertura completa de todos os métodos
  - Testes para bonus_disponivel, ativar_bonus, bonus_foi_aplicado
  - Testes para métodos de pagamento e validações

- **Expansão dos Smoke Tests** (5 → 10 testes)
  - Teste de conectividade com servidor
  - Teste de venda básica completa
  - Teste de cancelamento com confirmação
  - Teste de geração de pedido
  - Teste de navegação entre módulos
  - Teste de recuperação de botão back

#### 🔧 Corrigido
- EstoquePage ausente na pasta pages/ (impedindo coleta de testes)
- Smoke tests agora validam módulos principais (Pedido, Estoque, Troca)
- Documentação atualizada com números corretos

#### 📊 Estatísticas
- Testes Unitários: 171 → **200** (+29)
- Smoke Tests: 5 → **10** (+5)
- Cobertura de Page Objects: 88.9% → **100%**

---

## 👥 Equipe

- **QA Mobile Team** - Desenvolvimento e manutenção dos testes
- **Servidor QA Mobile** - Infraestrutura e CI/CD

---

## 📄 Licença

Projeto interno - Todos os direitos reservados

---

## 🔗 Links Úteis

- [Appium Documentation](https://appium.io/docs/en/2.0/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Reports](https://docs.qameta.io/allure/)
- [Page Object Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

---

**Última atualização**: 03/03/2026
**Versão**: 2.0.5
