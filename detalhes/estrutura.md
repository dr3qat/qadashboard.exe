# 📘 Estrutura Completa - PDV Automação

**Versão**: 3.0
**Última Atualização**: 10/03/2026
**Propósito**: Documentação completa de 100% do projeto para referência rápida

---

## 📑 Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Arquitetura Completa](#arquitetura-completa)
3. [Estrutura de Diretórios](#estrutura-de-diretórios)
4. [Workflow de Desenvolvimento](#workflow-de-desenvolvimento)
5. [Sistema de Testes](#sistema-de-testes)
6. [Sistema de Impressões](#sistema-de-impressões)
7. [Build e Compilação](#build-e-compilação)
8. [Conversão de Testes Legados](#conversão-de-testes-legados)
9. [Dashboard (Runner)](#dashboard-runner)
10. [Padrões e Boas Práticas](#padrões-e-boas-práticas)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral do Projeto

### O Que É?

**PDV Automação** é um framework completo de automação de testes E2E para aplicativo mobile PDV (Android) usando:

- **Appium 2.0** - Automação mobile
- **Python 3.13** - Linguagem de programação
- **Pytest 9.0** - Framework de testes
- **Page Object Model (POM)** - Padrão de design
- **Allure Reports** - Relatórios interativos
- **PyInstaller** - Compilação para EXE standalone

### Componentes Principais

```
┌──────────────────────────────────────────────────────────────┐
│                    PDV AUTOMAÇÃO                             │
├──────────────────────────────────────────────────────────────┤
│  1. Testes_PDV/         → Código-fonte dos testes            │
│  2. Gerador_EXE/        → Sistema de build/compilação        │
│  3. QA Dashboard.exe    → Aplicação standalone compilada     │
├──────────────────────────────────────────────────────────────┤
│  TESTES: 264 (200 unit + 10 smoke + 54 E2E)                 │
│  PAGE OBJECTS: 11 (100% cobertura)                           │
│  TELAS: 14 funcionalidades do PDV                            │
└──────────────────────────────────────────────────────────────┘
```

### Estatísticas do Projeto

| Categoria | Quantidade | Status |
|-----------|-----------|--------|
| **Testes Unitários** | 200 | ✅ 197/200 passando |
| **Smoke Tests** | 10 | ✅ Funcional |
| **Testes E2E** | 54 | ✅ Funcional |
| **Page Objects** | 11 | ✅ 100% cobertura |
| **Linhas de Código (app_runner.py)** | ~1530 | ✅ Otimizado |

---

## 🏗️ Arquitetura Completa

### Pirâmide Arquitetural (5 Camadas)

```
                    ┌─────────────────────┐
                    │   5. TESTES E2E     │  (tests/e2e/)
                    │   (54 testes)       │
                    └──────────┬──────────┘
                               │
            ┌──────────────────┴──────────────────┐
            │   4. PAGE OBJECTS (POM)             │  (pages/)
            │   (11 Page Objects)                 │
            └──────────────────┬──────────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │   3. FRAMEWORK E UTILITÁRIOS                │
        │   (config.py, framework.py, conftest.py)    │
        └──────────────────────┬──────────────────────┘
                               │
    ┌──────────────────────────┴──────────────────────────┐
    │   2. APPIUM + SELENIUM WEBDRIVER                    │
    │   (Automação Mobile)                                │
    └──────────────────────────┬──────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────┐
│   1. APLICATIVO PDV ANDROID (Target Under Test)             │
└──────────────────────────────────────────────────────────────┘
```

### Camada 1: Base Page (50+ métodos)

**Arquivo**: `Testes_PDV/pages/base_page.py`

**Responsabilidade**: Métodos comuns compartilhados por todos os Page Objects.

**Principais Métodos**:
```python
# Busca de Elementos
encontrar_por_id(locator, tempo_espera=10)
encontrar_clicavel_por_id(element_id, tempo_espera=10)
encontrar_por_texto(texto, tempo_espera=10)
encontrar_todos_por_id(locator)

# Ações
clicar_por_id(locator, max_tentativas=3)
clicar_por_texto(texto, tempo_espera=10)
clicar_se_existir(element_id, tempo_espera=3)
digitar_por_id(locator, texto)
limpar_campo_por_id(element_id)

# Navegação
rolar_ate_texto(texto, max_scrolls=10)
rolar_ate_id(locator, max_scrolls=10)
realizar_scroll_para_baixo()
voltar_tela(confirmar=True)

# Validações
elemento_existe(locator, tempo_espera=5)
texto_exibido(texto, tempo_espera=10)
elemento_visivel(elemento)
obter_texto_por_id(element_id)

# Teclado
pressionar_pesquisar()
pressionar_enter()
pressionar_voltar()
fechar_teclado()
```

### Camada 2: Page Objects (11 arquivos)

| Page Object | Responsabilidade | Métodos | Arquivo |
|-------------|------------------|---------|---------|
| **LoginPage** | Autenticação e configuração inicial | 8 | `login_page.py` |
| **HomePage** | Tela inicial e navegação | 6 | `home_page.py` |
| **VendaPage** | Vendas (consumidor e cliente) | 12 | `venda_page.py` |
| **VendaSucessoPage** | Tela de sucesso + impressões | 15 | `venda_sucesso_page.py` |
| **PedidoPage** | Pedidos de venda | 11 | `pedido_page.py` |
| **EstoquePage** | Consulta de estoque | 15 | `estoque_page.py` |
| **TrocaPage** | Trocas e devoluções | 18 | `troca_page.py` |
| **BonusPage** | Vendas com bonus/cashback | 17 | `bonus_page.py` |
| **ConsultaPedidoPage** | Consulta de pedidos | 8 | `consulta_pedido_page.py` |
| **VendaFuturaPage** | Vendas futuras (retirada/entrega) | 14 | `venda_futura_page.py` |
| **BorderoPage** | Relatório de borderô | 8 | `bordero_page.py` |
| **ClientePage** | Cadastro de clientes (PF/PJ) | 10 | `cliente_page.py` |
| **HistoricoClientePage** | Histórico de compras do cliente | 7 | `historico_cliente_page.py` |

### Camada 3: Framework e Utilitários

**Arquivo**: `Testes_PDV/config.py`
- Logger customizado com cores e estilos
- Configurações globais (timeouts, diretórios)
- Classe `LogStyle` para formatação de logs
- Símbolos ASCII para logs amigáveis

**Arquivo**: `Testes_PDV/framework.py`
- Gerenciamento de Appium Server
- Multi-device support
- Utilitários de rede e processos

**Arquivo**: `Testes_PDV/conftest.py`
- Fixtures pytest (driver, driver_logado)
- Hooks de setup/teardown
- Configuração de relatórios Allure

**Arquivo**: `Testes_PDV/test_data.py`
- Dados de teste externalizados
- Configurações de servidor (IP, porta)
- Credenciais (empresa, usuário, senha)
- IDs de teste (cliente, produto)

### Camada 4: Testes E2E (54 testes)

**Estrutura**:
```
tests/
├── unit/                      # 200 testes unitários
│   ├── test_base_page_unit.py
│   ├── test_bonus_page_unit.py
│   ├── test_estoque_page_unit.py
│   └── ...
├── smoke/                     # 10 smoke tests (3-5min)
│   └── test_smoke_e2e.py
└── e2e/                       # 54 testes E2E (30-45min)
    ├── test_login.py
    ├── test_venda_consumidor.py
    ├── test_venda_cliente.py
    ├── test_pedido_vendaConsumidor.py
    ├── test_pedido_vendaCliente.py
    ├── test_estoque.py
    ├── test_troca_consumidor.py
    ├── test_troca_cliente.py
    ├── test_bonus.py
    ├── test_consulta_pedidoConsumidor.py
    ├── test_consulta_pedidoCliente.py
    ├── test_venda_futura.py
    ├── test_venda_futura_domicilio.py
    ├── test_cancelamento.py
    ├── test_bordero.py
    ├── test_cad_cliente.py
    └── test_historico_cliente.py
```

### Camada 5: Dashboard (Runner)

**Arquivo**: `Gerador_EXE/runner/app_runner.py` (~1530 linhas)

**Componentes**:
1. Interface Tkinter (abas, campos, botões)
2. Executor de testes (threading)
3. Gerenciador de logs (streaming)
4. Sistema de configurações (import/export settings.json)
5. Controle de Appium Server (auto-start/stop)
6. Multi-device selector
7. Sistema de impressões configurável (4 tipos)

---

## 📂 Estrutura de Diretórios

```
D:\PDV_AUTOMACAO\
│
├── 📁 Testes_PDV/                    ← CÓDIGO-FONTE (EDITE AQUI)
│   ├── pages/                        # Page Objects
│   │   ├── __init__.py
│   │   ├── base_page.py             # 50+ métodos comuns
│   │   ├── login_page.py
│   │   ├── home_page.py
│   │   ├── venda_page.py
│   │   ├── venda_sucesso_page.py    # ⭐ Controle de impressões
│   │   ├── pedido_page.py
│   │   ├── estoque_page.py
│   │   ├── troca_page.py
│   │   ├── bonus_page.py
│   │   ├── consulta_pedido_page.py
│   │   ├── venda_futura_page.py
│   │   ├── bordero_page.py          # ⭐ Relatório de borderô
│   │   ├── cliente_page.py          # ⭐ Cadastro PF/PJ + Faker
│   │   └── historico_cliente_page.py # ⭐ Histórico de compras
│   │
│   ├── tests/                        # Testes
│   │   ├── unit/                    # 200 testes unitários
│   │   │   ├── test_base_page_unit.py
│   │   │   ├── test_bonus_page_unit.py
│   │   │   └── ...
│   │   ├── smoke/                   # 10 smoke tests
│   │   │   └── test_smoke_e2e.py
│   │   └── e2e/                     # 54 testes E2E
│   │       ├── test_login.py
│   │       ├── test_venda_consumidor.py
│   │       ├── test_pedido_vendaConsumidor.py
│   │       ├── test_bordero.py      # ⭐ NOVO
│   │       ├── test_cad_cliente.py  # ⭐ NOVO
│   │       └── test_historico_cliente.py # ⭐ NOVO
│   │
│   ├── docs/                         # Documentação dos testes
│   │   ├── GETTING_STARTED.md
│   │   ├── ARCHITECTURE.md
│   │   ├── TESTS.md
│   │   ├── UNIT_TESTS.md
│   │   ├── SMOKE_TESTS.md
│   │   ├── E2E_TESTS.md
│   │   └── PAGE_OBJECTS.md
│   │
│   ├── config.py                     # Configurações globais + Logger
│   ├── conftest.py                   # Fixtures pytest
│   ├── test_data.py                  # Dados de teste externalizados
│   ├── framework.py                  # Framework Appium
│   ├── pytest.ini                    # Configuração pytest
│   ├── requirements.txt              # Dependências Python
│   ├── VERSION                       # Versão do projeto (ex: 2.0.21)
│   ├── run_normal.bat                # Executar todos os testes
│   └── run_debug.bat                 # Executar com debug
│
├── 📁 Gerador_EXE/                   ← BUILD E COMPILAÇÃO
│   ├── runner/
│   │   └── app_runner.py            # Dashboard principal (~1530 linhas)
│   │
│   ├── build/
│   │   └── builder_pro.py           # Build pipeline PyInstaller
│   │
│   ├── scripts/
│   │   ├── instalar_python.bat      # Auto-instalador Python + deps
│   │   └── instalar_appium.bat      # Auto-instalador Appium + Node
│   │
│   ├── output/
│   │   ├── staging/                 # ⚙️ Sincronizado automaticamente
│   │   │   ├── config.py            # (cópia de Testes_PDV)
│   │   │   ├── pages/
│   │   │   └── tests/
│   │   │
│   │   └── dist/                    # 📦 EXE final compilado
│   │       ├── QA_Dashboard.exe
│   │       ├── settings.json
│   │       └── _internal/           # Dependências empacotadas
│   │
│   └── resources/
│       └── icon.ico                 # Ícone do EXE
│
├── 📁 claude/qa/                     ← SKILLS E COMANDOS
│   ├── commands/
│   │   ├── modelappium.md           # Skill desenvolvimento Appium
│   │   └── converterLegado.md       # ⭐ Workflow conversão legado→POM
│   └── skills/
│       ├── qa-test-analyze/
│       ├── qa-test-impl/
│       ├── qa-ci-configure/
│       └── ...
│
├── 📄 ABRIR_DASHBOARD.bat            ← 🚀 EXECUTAR PARA TESTAR (modo dev)
├── 📄 COMPILAR.bat                   ← Atalho para compilação
│
├── 📘 ARQUITETURA_COMPLETA.md        # Documentação arquitetura
├── 📘 README_DESENVOLVIMENTO.md      # Guia de desenvolvimento
├── 📘 CONFIGURACAO_IMPRESSAO.md      # Sistema de impressões
├── 📘 estrutura.md                   # ⭐ ESTE ARQUIVO
└── 📘 converterLegado.md             # ⭐ Workflow conversão testes
```

---

## 🔄 Workflow de Desenvolvimento

### 1️⃣ Desenvolver e Testar (ANTES de compilar)

```bash
┌─────────────────────────────────────────────────────────┐
│  1. EDITAR código em Testes_PDV/                        │
│     - pages/*.py                                         │
│     - tests/e2e/*.py                                     │
│     - config.py, test_data.py                           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│  2. TESTAR executando ABRIR_DASHBOARD.bat               │
│     → Sincroniza automaticamente                        │
│     → Abre Dashboard em modo dev                        │
│     → Simula ambiente do EXE                            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│  3. AJUSTAR código se necessário (volta para passo 1)   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│  4. COMPILAR quando tudo estiver funcionando            │
│     → COMPILAR.bat ou                                   │
│     → cd Gerador_EXE\build                              │
│     → python builder_pro.py                             │
└─────────────────────────────────────────────────────────┘
```

### O Que o ABRIR_DASHBOARD.bat Faz?

1. **Sincroniza** todos os arquivos de `Testes_PDV` para `Gerador_EXE\output\staging`
2. **Copia**:
   - config.py, test_data.py, framework.py, conftest.py, VERSION
   - Todos os Page Objects (pages/)
   - Todos os Testes (tests/e2e, tests/smoke, tests/unit)
3. **Executa** o Dashboard usando o staging (simula o EXE)

### 2️⃣ Compilar (DEPOIS de testar)

```bash
cd Gerador_EXE\build
python builder_pro.py
```

**Saída**: `Gerador_EXE\output\dist\QA_Dashboard.exe`

---

## 🧪 Sistema de Testes

### Tipos de Testes

| Tipo | Quantidade | Tempo | Propósito |
|------|-----------|-------|-----------|
| **Unitários** | 200 | < 10s | Testar Page Objects isoladamente (mocks) |
| **Smoke** | 10 | 3-5min | Validação rápida de sanidade |
| **E2E** | 54 | 30-45min | Testes completos de ponta a ponta |

### Estrutura de Teste Unitário

```python
"""Test Nome Page - Testes unitários para NomePage."""
import pytest
from unittest.mock import MagicMock, patch

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
"""Test Nome - Testes E2E para funcionalidade X."""
import pytest
import allure
from pages.nome_page import NomePage
from test_data import test_data

@allure.epic("PDV Mobile")
@allure.feature("Nome da Feature")
@allure.story("História do Usuário")
class TestNome:
    """Testes E2E para funcionalidade X."""

    @allure.title("Título do Teste")
    @allure.description("""
    Cenário: Descrição do cenário

    Pré-condições:
    - Usuário logado no sistema

    Passos:
    1. Primeiro passo
    2. Segundo passo
    3. Terceiro passo

    Resultado esperado:
    - Resultado esperado 1
    - Resultado esperado 2
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("tag1", "tag2", "tag3")
    def test_nome_teste(self, driver_logado):
        """
        Cenário: [descrição BDD]
        Dado que [pré-condição]
        Quando [ação]
        Então [resultado esperado]
        """
        # Arrange
        page = NomePage(driver_logado)

        # Act
        with allure.step("1. Primeiro passo"):
            page.acao_1()

        with allure.step("2. Segundo passo"):
            page.acao_2()

        with allure.step("3. Validação"):
            resultado = page.validacao()

        # Assert
        with allure.step("4. Verificação final"):
            assert resultado, "Mensagem de erro"

            allure.attach(
                str(resultado),
                name="Dados Coletados",
                attachment_type=allure.attachment_type.TEXT
            )
```

### Execução de Testes

**Testes Unitários**:
```bash
pytest tests/unit/ -v
pytest tests/unit/test_bonus_page_unit.py -v
```

**Smoke Tests**:
```bash
pytest tests/smoke/ -v -m smoke
```

**Testes E2E**:
```bash
pytest tests/e2e/ -v
pytest tests/e2e/test_venda_consumidor.py -v
pytest tests/e2e/ -v -m venda
```

**Com Relatório Allure**:
```bash
pytest -v --alluredir=logs/allure-results
allure serve logs/allure-results
```

### Fixtures Disponíveis

**`driver`** - Driver Appium básico (app limpo)
```python
def test_exemplo(self, driver):
    login_page = LoginPage(driver)
    # Teste com app limpo
```

**`driver_logado`** - Driver com usuário já logado (mais comum)
```python
def test_exemplo(self, driver_logado):
    venda_page = VendaPage(driver_logado)
    # Teste com usuário já autenticado
```

---

## 🖨️ Sistema de Impressões

### Tipos de Impressão Disponíveis

| Tipo | Quando Aparece | Controle Dashboard | Padrão |
|------|----------------|-------------------|--------|
| **1. Cupom de Venda** | Diálogo automático após finalizar venda | `print_cupom_venda` | ☐ false (clica NÃO) |
| **2. Cupom de Troca (Diálogo)** | Pode aparecer ANTES da tela de sucesso* | `print_cupom_troca` | ☐ false (clica NÃO) |
| **3. NFC-E** | Botão na tela de sucesso | `print_nfce` | ☐ false (não clica) |
| **4. DANFE** | Botão na tela de sucesso | `print_danfe` | ☐ false (não clica) |
| **5. Cupom de Troca (Botão)** | Botão na tela de sucesso** | `print_cupom_troca` | ☐ false (não clica) |

\* *Depende de parâmetro no sistema. Se habilitado, aparece como diálogo antes da tela de sucesso.*
\*\* *Se não foi perguntado antes, o botão pode aparecer na tela de sucesso.*

### Fluxo Completo de Venda com Impressões

```
1. VENDA EXECUTADA
   ↓
2. CUPOM DE VENDA (diálogo automático)
   ☐ Desmarcado → Clica NÃO
   ✓ Marcado → Clica SIM
   ↓
3. CUPOM DE TROCA (diálogo - se parâmetro habilitado)
   ☐ Desmarcado → Clica NÃO
   ✓ Marcado → Clica SIM
   ↓
4. TELA DE SUCESSO
   ↓
5. PROCESSAMENTO AUTOMÁTICO (ordem XML):
   5.1. NFC-E (primeiro botão)
   5.2. DANFE (segundo botão)
   5.3. CUPOM TROCA (terceiro botão - se não foi antes)
   ↓
6. CONCLUIR VENDA
```

### Configuração no settings.json

```json
{
  "print_cupom_venda": false,
  "print_nfce": false,
  "print_danfe": false,
  "print_cupom_troca": false,
  "print_dialog_timeout": 20
}
```

### Page Objects Responsáveis

| Page Object | Responsabilidade |
|-------------|------------------|
| **VendaPage** | Responde diálogos: Cupom Venda + Cupom Troca (antes da tela) |
| **BonusPage** | Responde diálogos: Cupom Venda + Cupom Troca (antes da tela) |
| **VendaFuturaPage** | Responde diálogos: Cupom Venda + Cupom Troca (antes da tela) |
| **VendaSucessoPage** | Processa botões NA ORDEM: NFC-E, DANFE, Cupom Troca |

### Uso no Teste

```python
from pages.venda_page import VendaPage
from pages.venda_sucesso_page import VendaSucessoPage

def test_venda_completa_com_impressoes(self, driver_logado):
    venda_page = VendaPage(driver_logado)
    sucesso_page = VendaSucessoPage(driver_logado)

    # 1. Executa venda (diálogos respondidos automaticamente)
    venda_page.executar_venda_consumidor()

    # 2. Valida sucesso
    assert sucesso_page.tela_sucesso_exibida()

    # 3. Processa TODAS as impressões na ORDEM CORRETA
    sucesso_page.processar_todas_impressoes()

    # 4. Confirma venda
    sucesso_page.concluir_venda()
```

---

## 🔨 Build e Compilação

### Arquivos Envolvidos

1. **builder_pro.py** - Pipeline de build principal
2. **instalar_python.bat** - Instalador Python + dependências
3. **instalar_appium.bat** - Instalador Appium + Node.js

### Pipeline de Build (builder_pro.py)

**9 Etapas**:
```
1. Validar Dependências     → Verifica Python, pytest, appium, allure
2. Preparar Staging         → Copia arquivos de Testes_PDV para staging
3. Validar Testes           → Executa pytest em staging
4. Gerar spec.py            → Cria arquivo de configuração PyInstaller
5. Compilar com PyInstaller → Gera EXE standalone
6. Copiar Assets            → Copia settings.json, ícone, scripts
7. Validar EXE              → Testa se EXE abre e fecha corretamente
8. Limpar Build Cache       → Remove arquivos temporários
9. Gerar Relatório Final    → Cria BUILD_LOG.txt com resumo
```

### Configurações Críticas do PyInstaller

**Hidden Imports** (Importações Dinâmicas):
```python
hidden_imports = [
    "pytest", "pluggy", "_pytest", "iniconfig",
    "pytest_html", "pytest_metadata",
    "allure_pytest", "allure_commons",
    "appium", "selenium",
    "faker", "faker.providers", "faker.providers.person.pt_BR",
    "faker.providers.address.pt_BR", "faker.providers.company.pt_BR",
    "requests", "requests.adapters", "urllib3",
    # ... outros
]
```

**Collect-All Packages** (Incluir Todos os Submódulos):
```python
collect_all_packages = [
    "pytest", "pluggy", "_pytest", "iniconfig",
    "pytest_html", "allure_pytest",
    "appium", "selenium",
    "faker", "requests"
]
```

**Critical Packages** (Validação Obrigatória):
```python
critical_packages = [
    "pytest", "pluggy", "_pytest", "iniconfig",
    "pytest_html", "pytest_metadata",
    "allure_pytest", "allure_commons",
    "appium", "selenium",
    "faker", "requests",
]
```

### Adicionar Nova Biblioteca ao Build

Quando adicionar uma nova dependência Python que será usada no EXE, você DEVE atualizar **5 locais**:

#### 1. requirements.txt
```txt
pytest==9.0.0
appium-python-client==4.2.0
Faker==33.5.1  # ← ADICIONAR AQUI
requests==2.31.0  # ← ADICIONAR AQUI
```

#### 2. builder_pro.py - critical_packages (linha ~239)
```python
critical_packages = [
    "pytest", "appium", "selenium",
    "faker", "requests",  # ← ADICIONAR AQUI
]
```

#### 3. builder_pro.py - hidden_imports (linha ~338)
```python
hidden_imports = [
    "pytest", "appium", "selenium",
    "faker", "faker.providers", "faker.providers.person.pt_BR",  # ← ADICIONAR AQUI
    "faker.providers.address.pt_BR", "faker.providers.company.pt_BR",  # ← ADICIONAR AQUI
    "requests", "requests.adapters", "urllib3",  # ← ADICIONAR AQUI
]
```

#### 4. builder_pro.py - collect_all_packages (linha ~354)
```python
collect_all_packages = [
    "pytest", "appium", "selenium",
    "faker", "requests",  # ← ADICIONAR AQUI
]
```

#### 5. instalar_python.bat - Duas Localizações

**Localização 1** (linha ~198 - instalação manual):
```batch
echo    Instalando Faker...
"!PYTHON_PATH!" -m pip install Faker --quiet

echo    Instalando requests...
"!PYTHON_PATH!" -m pip install requests --quiet
```

**Localização 2** (linha ~218 - fallback essencial):
```batch
"!PYTHON_PATH!" -m pip install pytest Appium-Python-Client allure-pytest Faker requests --quiet
```

### Execução do Build

```bash
# Via atalho
COMPILAR.bat

# Manualmente
cd Gerador_EXE\build
python builder_pro.py
```

**Saída**:
- `Gerador_EXE\output\dist\QA_Dashboard.exe` (~80 MB)
- `Gerador_EXE\output\dist\_internal\` (dependências)
- `Gerador_EXE\output\dist\settings.json` (configurações)
- `Gerador_EXE\build\BUILD_LOG.txt` (log detalhado)

---

## 🔄 Conversão de Testes Legados

### Workflow Completo (9 Passos)

Baseado em `claude/qa/commands/converterLegado.md`:

```
1. LER ARQUIVOS LEGADOS       → Entender funcionalidade atual
2. VERIFICAR PROJETO          → Identificar Page Object existente
3. CRIAR/ATUALIZAR POM        → Implementar Page Object
4. CRIAR TESTES E2E          → Implementar testes POM
5. ATUALIZAR requirements.txt → Adicionar novas dependências
6. ATUALIZAR builder_pro.py   → 3 localizações (critical, hidden, collect)
7. ATUALIZAR instalar_python.bat → 2 localizações (manual + fallback)
8. TESTAR                     → ABRIR_DASHBOARD.bat
9. COMPILAR E VALIDAR         → python builder_pro.py
```

### Checklist de Conversão

#### ✅ SEMPRE Fazer:

- **Usar test_data.py**: Nunca valores fixos no código
  ```python
  # ✅ CORRETO
  cliente_id = test_data.CUSTOMER_ID

  # ❌ ERRADO
  cliente_id = "4225455"
  ```

- **Listar TODOS os campos no terminal**: Logs detalhados com formatação
  ```python
  logger.info("=" * 60)
  logger.info("DADOS COLETADOS")
  logger.info("=" * 60)
  logger.info(f"   Campo 1: {valor1}")
  logger.info(f"   Campo 2: {valor2}")
  logger.info("=" * 60)
  ```

- **Seguir estrutura do legado**: Mesmo número de testes, mesma ordem

- **Page Object herda BasePage**: Sempre
  ```python
  from pages.base_page import BasePage

  class NovoPage(BasePage):
      def __init__(self, driver):
          super().__init__(driver)
  ```

- **Organizar locators no topo**: Constantes maiúsculas
  ```python
  class NovoPage(BasePage):
      # ========== LOCATORS ==========
      BTN_EXEMPLO = "btn_exemplo_id"
      TXT_TITULO = "Título da Tela"
      EDT_CAMPO = "edt_campo_id"
  ```

#### ❌ NUNCA Fazer:

- Hardcoded IDs, CPFs, CNPJs, códigos de produtos
- Criar mais testes do que o legado tinha
- Adicionar funcionalidades não solicitadas
- Usar `log_tecnico()` para dados visíveis (usar `logger.info()`)
- Esquecer de atualizar build files quando adicionar libs

### Exemplo de Conversão: Borderô

**Legado** (bordero.py):
```python
def test_bordero():
    # ... código procedural com 150 linhas
    driver.find_element(By.ID, "btn_bordero").click()
    # ... mais código inline
```

**Convertido** (bordero_page.py + test_bordero.py):

**bordero_page.py**:
```python
class BorderoPage(BasePage):
    # ========== LOCATORS ==========
    TXT_BORDERO = "Borderô"
    BTN_GERAR = "btn_gerar_bordero"

    def navegar_ate_bordero(self):
        """Navega até a tela de Borderô."""
        self.rolar_ate_texto(self.TXT_BORDERO)
        self.clicar_por_texto(self.TXT_BORDERO)

    def gerar_bordero(self):
        """Gera o borderô."""
        self.clicar_por_id(self.BTN_GERAR)

    def validar_dados_bordero(self) -> dict:
        """Valida e coleta todos os dados do borderô."""
        logger.info("=" * 70)
        logger.info("DADOS DO BORDERÔ")
        logger.info("=" * 70)

        dados = {}
        dados['fundo_caixa'] = self._ler_campo("Fundo de Caixa", "txt_fundo")
        # ... coletar todos os 12 campos

        logger.info("=" * 70)
        logger.info("RESUMO DOS DADOS COLETADOS")
        logger.info("=" * 70)
        logger.info(f"   Fundo de Caixa: {dados['fundo_caixa']}")
        # ... listar todos os 12 campos

        return dados
```

**test_bordero.py**:
```python
@allure.title("Gerar Borderô com Data Atual")
@allure.severity(allure.severity_level.CRITICAL)
def test_gerar_bordero_data_atual(self, driver_logado):
    # Arrange
    bordero_page = BorderoPage(driver_logado)

    # Act
    with allure.step("Navegar até menu Borderô"):
        bordero_page.navegar_ate_bordero()

    with allure.step("Gerar borderô"):
        bordero_page.gerar_bordero()

    with allure.step("Validar dados do borderô"):
        dados = bordero_page.validar_dados_bordero()

    # Assert
    assert bordero_page.bordero_gerado_com_sucesso(dados)

    allure.attach(str(dados), name="Dados do Borderô")
```

---

## 🎛️ Dashboard (Runner)

### Arquivo: app_runner.py (~1530 linhas)

### Componentes Principais

```
app_runner.py
├── Classe AppiumTestRunner
│   ├── __init__()                  # Inicialização UI
│   ├── _criar_interface()          # Build interface Tkinter
│   ├── _criar_aba_config()         # Aba Configurações
│   ├── _criar_aba_testes()         # Aba Testes
│   ├── _criar_aba_logs()           # Aba Logs
│   │
│   ├── _executar_testes()          # Thread executor pytest
│   ├── _processar_logs()           # Streaming logs em tempo real
│   ├── _detectar_modo_execucao()   # Frozen vs Dev mode
│   │
│   ├── _salvar_settings()          # Persistir configurações
│   ├── _carregar_settings()        # Carregar configurações
│   ├── _exportar_settings()        # Exportar para .json
│   ├── _importar_settings()        # Importar de .json
│   │
│   ├── _iniciar_appium()           # Auto-start Appium Server
│   ├── _parar_appium()             # Stop Appium Server
│   ├── _listar_dispositivos()      # Multi-device selector
│   │
│   └── _on_closing()               # Cleanup ao fechar
│
└── main()                          # Entry point
```

### Interface (Abas)

**Aba 1: Configurações**
- Servidor (IP, Porta)
- Credenciais (Empresa, Usuário, Senha)
- IDs de teste (Cliente, Produto, Tamanho)
- **Configurações de Impressão** (4 checkboxes + timeout)
- Device Selector (multi-device)
- Appium (caminho, porta, auto-start)
- Botões: Salvar, Exportar Settings, Importar Settings

**Aba 2: Testes**
- Seleção de testes (checkbox tree)
- Seleção de suite (Unit, Smoke, E2E, Todos)
- Botão "Executar Testes Selecionados"
- Barra de progresso

**Aba 3: Logs**
- Área de texto com scroll
- Checkbox "Mostrar logs técnicos (debug)"
- Botão "Limpar Logs"
- Streaming em tempo real

### Funcionalidades Especiais

**1. Frozen Detection**
```python
def _detectar_modo_execucao(self) -> str:
    if getattr(sys, 'frozen', False):
        return "FROZEN"  # EXE compilado
    else:
        return "DEV"     # Desenvolvimento
```

**2. Settings Multi-Ambiente**
```json
settings_homolog.json    → Homologação
settings_prod.json       → Produção
settings_qa.json         → QA
```

**3. Worker Mode**
- Testes executam em thread separada (não trava UI)
- Logs processados em lotes de 5 linhas (performance)
- Filtros automáticos de ruído (Selenium, urllib3)

**4. Logger com Modo Debug Otimizado**
```
┌─────────────────────────────────────────────────┐
│ Checkbox Desmarcado (Modo Normal)              │
│  → Mostra: ações, botões clicados             │
│  → Oculta: stack traces, logs técnicos        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Checkbox Marcado (Modo Debug)                  │
│  → Mostra: ações + stack traces EM ERROS       │
│  → Filtra: logs de bibliotecas (Selenium, etc) │
│  → Ignora: linhas > 500 caracteres             │
└─────────────────────────────────────────────────┘
```

**5. Multi-Device Support**
```python
def _listar_dispositivos(self):
    result = subprocess.run(['adb', 'devices'], capture_output=True)
    devices = [linha.split()[0] for linha in linhas if '\tdevice' in linha]
    # Popula dropdown com devices
```

---

## 📋 Padrões e Boas Práticas

### Nomenclatura

**Page Objects**:
```python
# Arquivo: nome_page.py
class NomePage(BasePage):  # PascalCase
    pass
```

**Locators**:
```python
# Constantes MAIÚSCULAS
BTN_CONFIRMAR = "btn_confirmar"
EDT_USUARIO = "edt_usuario"
TXT_TITULO = "Título da Tela"
```

**Métodos**:
```python
# snake_case descritivo
def navegar_ate_tela_principal(self):
    pass

def selecionar_produto_por_codigo(self, codigo: str):
    pass
```

**Testes**:
```python
# test_nome_funcionalidade.py
def test_nome_cenario_resultado_esperado(self, driver_logado):
    pass

# Exemplo:
def test_login_credenciais_validas_sucesso(self, driver_logado):
    pass
```

### Organização de Código

**Page Object**:
```python
"""
NomePage - Page Object para tela de [funcionalidade].
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle, SimbolosASCII

class NomePage(BasePage):
    """Page Object para [funcionalidade]."""

    # ========== LOCATORS ==========
    BTN_EXEMPLO = "btn_exemplo"
    TXT_TITULO = "Título"

    # ========== ACOES ==========
    def metodo_acao(self):
        """Descrição da ação."""
        pass

    # ========== VALIDACOES ==========
    def metodo_validacao(self) -> bool:
        """Valida condição."""
        return True

    # ========== FLUXOS COMPLETOS ==========
    def executar_fluxo_completo(self):
        """Executa fluxo completo."""
        pass
```

### Logs e Mensagens

**Símbolos ASCII Disponíveis** (config.py):
```python
class SimbolosASCII:
    OK = "[✅]"
    ERRO = "[❌]"
    AVISO = "[⚠️]"
    INFO = "[ℹ️]"
    CLICK = "[🔘]"
    TYPE = "[⌨️]"
    SCROLL = "[📜]"
    BUSCA = "[🔍]"
    VALIDAR = "[✔️]"
```

**Uso**:
```python
logger.info(f"{SimbolosASCII.OK} Login realizado com sucesso")
logger.warning(f"{SimbolosASCII.AVISO} Campo vazio detectado")
logger.error(f"{SimbolosASCII.ERRO} Falha na validação")
```

**Formatação de Seções**:
```python
logger.info("=" * 60)
logger.info("TÍTULO DA SEÇÃO")
logger.info("=" * 60)
logger.info(f"   Campo 1: {valor1}")
logger.info(f"   Campo 2: {valor2}")
logger.info("=" * 60)
```

### Esperas e Timeouts

**Usar Esperas Explícitas**:
```python
# ✅ BOM
elemento = self.encontrar_clicavel_por_id("btn_exemplo", tempo_espera=10)

# ❌ RUIM
elemento = self.driver.find_element(By.ID, "btn_exemplo")
time.sleep(5)  # Espera fixa
```

**Timeouts Padrão** (config.py):
```python
DEFAULT_WAIT = 30  # Segundos
RETRY_ATTEMPTS = 2  # Tentativas de retry
```

### Tratamento de Erros

**Em Page Objects**:
```python
def metodo_que_pode_falhar(self):
    """Método com tratamento de erro."""
    try:
        self.clicar_por_id("btn_exemplo")
        return True
    except Exception as e:
        logger.error(f"Erro ao clicar: {e}")
        return False
```

**Em Testes**:
```python
def test_exemplo(self, driver_logado):
    """Teste com validação clara."""
    page = ExemploPage(driver_logado)

    with allure.step("Executar ação"):
        page.executar_acao()

    with allure.step("Validar resultado"):
        assert page.validar_resultado(), \
            "Resultado esperado não foi alcançado"
```

### Dados de Teste

**Sempre usar test_data.py**:
```python
# ✅ CORRETO
from test_data import test_data

def test_exemplo(self, driver_logado):
    page = ExemploPage(driver_logado)
    page.selecionar_cliente(test_data.CUSTOMER_ID)
    page.adicionar_produto(test_data.PRODUCT_CODE)

# ❌ ERRADO
def test_exemplo(self, driver_logado):
    page = ExemploPage(driver_logado)
    page.selecionar_cliente("1234567")  # Hardcoded
    page.adicionar_produto("ABC123")    # Hardcoded
```

### Anexos Allure

**Anexar dados coletados**:
```python
with allure.step("Coletar dados"):
    dados = page.coletar_dados()

allure.attach(
    str(dados),
    name="Dados Coletados",
    attachment_type=allure.attachment_type.TEXT
)
```

**Anexar screenshot em falha** (automático via conftest.py):
```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver') or item.funcargs.get('driver_logado')
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_falha",
                attachment_type=allure.attachment_type.PNG
            )
```

---

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. ModuleNotFoundError ao compilar

**Erro**: `ModuleNotFoundError: No module named 'faker'`

**Solução**: Atualizar 5 locais (veja seção [Build e Compilação](#build-e-compilação)):
1. requirements.txt
2. builder_pro.py - critical_packages
3. builder_pro.py - hidden_imports
4. builder_pro.py - collect_all_packages
5. instalar_python.bat - 2 localizações

#### 2. Appium não conecta ao dispositivo

**Erro**: `SessionNotCreatedException: Could not start a new session`

**Soluções**:
```bash
# Verificar dispositivos
adb devices

# Reiniciar ADB
adb kill-server
adb start-server

# Verificar Appium
appium --version

# Reinstalar driver
appium driver install uiautomator2
```

#### 3. Testes falhando intermitentemente

**Possíveis Causas**:
- Timeouts muito curtos
- Conexão instável com servidor
- Memória do dispositivo cheia
- App travando

**Soluções**:
```python
# Aumentar timeouts em config.py
DEFAULT_WAIT = 30  # Aumentar para 45 se necessário

# Usar esperas condicionais
self.encontrar_clicavel_por_id("btn", tempo_espera=15)

# Adicionar retry em ações críticas
self.clicar_por_id("btn", max_tentativas=5)
```

#### 4. Dashboard não abre após compilar

**Erro**: EXE abre e fecha imediatamente

**Soluções**:
```bash
# Executar via CMD para ver erros
cd Gerador_EXE\output\dist
QA_Dashboard.exe

# Verificar BUILD_LOG.txt
type Gerador_EXE\build\BUILD_LOG.txt

# Recompilar com validação
cd Gerador_EXE\build
python builder_pro.py
```

#### 5. Settings não importa

**Erro**: Settings não carregam do JSON

**Soluções**:
- Verificar sintaxe do JSON (usar editor como VS Code)
- Verificar encoding do arquivo (deve ser UTF-8)
- Verificar se todas as chaves obrigatórias existem:
  ```json
  {
    "server_ip": "...",
    "server_port": "...",
    "company": "...",
    "user": "...",
    "password": "...",
    "customer_id": "...",
    "product_code": "...",
    "print_cupom_venda": false,
    "print_nfce": false,
    "print_danfe": false,
    "print_cupom_troca": false
  }
  ```

#### 6. Logs não aparecem no Dashboard

**Problema**: Teste executando mas logs não aparecem

**Soluções**:
- Verificar se checkbox "Mostrar logs técnicos" está configurado corretamente
- Limpar cache de logs (botão "Limpar Logs")
- Reabrir o Dashboard
- Verificar se `logger.info()` está sendo usado (não `print()`)

#### 7. Testes unitários falhando após mudanças

**Erro**: Testes unitários que passavam agora falham

**Soluções**:
```bash
# Ver traceback completo
pytest tests/unit/ -v --tb=long

# Atualizar mocks após mudanças
# Verificar se assinaturas de métodos mudaram
# Verificar se novos métodos precisam de mocks
```

#### 8. Import errors após sincronização

**Erro**: `ImportError: cannot import name 'X' from 'pages.Y'`

**Soluções**:
```bash
# Limpar cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar se arquivo existe em staging
ls Gerador_EXE\output\staging\pages\
```

---

## 📚 Referências Rápidas

### Comandos Úteis

```bash
# === TESTES ===
# Unit tests
pytest tests/unit/ -v

# Smoke tests
pytest tests/smoke/ -v -m smoke

# E2E tests
pytest tests/e2e/ -v

# Teste específico
pytest tests/e2e/test_venda_consumidor.py::TestVendaConsumidor::test_venda_consumidor_sucesso -v

# Com Allure
pytest -v --alluredir=logs/allure-results
allure serve logs/allure-results

# === DESENVOLVIMENTO ===
# Testar mudanças
ABRIR_DASHBOARD.bat

# Compilar
COMPILAR.bat

# === APPIUM ===
# Listar dispositivos
adb devices

# Reiniciar ADB
adb kill-server && adb start-server

# Iniciar Appium
appium

# === LIMPEZA ===
# Limpar cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Limpar allure results
rm -rf logs/allure-results/*
```

### Arquivos Importantes

| Arquivo | Propósito | Localização |
|---------|-----------|-------------|
| **config.py** | Configurações globais + Logger | Testes_PDV/ |
| **test_data.py** | Dados de teste externalizados | Testes_PDV/ |
| **conftest.py** | Fixtures pytest | Testes_PDV/ |
| **base_page.py** | Classe base (50+ métodos) | Testes_PDV/pages/ |
| **app_runner.py** | Dashboard principal | Gerador_EXE/runner/ |
| **builder_pro.py** | Pipeline de build | Gerador_EXE/build/ |
| **settings.json** | Configurações do usuário | output/dist/ |
| **VERSION** | Versão do projeto | Testes_PDV/ |
| **converterLegado.md** | Workflow conversão testes | claude/qa/commands/ |
| **estrutura.md** | Esta documentação | D:\PDV_AUTOMACAO\ |

### Dependências Principais

```txt
# Core
Python==3.13
pytest==9.0.0
appium-python-client==4.2.0
selenium==4.x

# Relatórios
allure-pytest==2.13.5
pytest-html==4.1.1

# Utilitários
Faker==33.5.1
requests==2.31.0

# Build
pyinstaller==6.11.1
```

### Variáveis de Ambiente Úteis

```bash
# CI/CD
set CI=true

# Test Data Overrides
set TEST_SERVER_IP=192.168.1.100
set TEST_SERVER_PORT=8080
set TEST_COMPANY=382
set TEST_USER=admin
set TEST_PASSWORD=senha123
set TEST_CUSTOMER_ID=1
set TEST_PRODUCT_CODE=123
set TEST_TIMEOUT=30
```

---

## 📝 Histórico de Versões

### [3.0] - 2026-03-10
- ✨ Criação do `estrutura.md` - Documentação completa unificada
- 📚 Consolidação de ARQUITETURA_COMPLETA.md, README_DESENVOLVIMENTO.md, CONFIGURACAO_IMPRESSAO.md
- 📘 Integração de converterLegado.md no workflow
- 🔧 Documentação completa do sistema de build (5 locais de atualização)

### [2.0.21] - 2026-03-03
- ✨ Sistema de impressões configurável via Dashboard (4 tipos)
- 📦 Page Object VendaSucessoPage para gerenciar impressões
- 🔄 Estrutura de testes reorganizada (separação consumidor/cliente)
- ⚡ Performance otimizada na interface do Dashboard

### [2.1.0] - 2026-02-24
- ✨ Testes Unitários para BonusPage (29 novos testes)
- 🧪 Expansão dos Smoke Tests (5 → 10 testes)
- 🔧 Correção: EstoquePage ausente impedindo coleta de testes
- 📊 Cobertura de Page Objects: 88.9% → 100%

### [2.0.5] - 2026-02-03
- ✨ VendaSucessoPage - Novo Page Object para tela de sucesso
- 📁 Reorganização dos testes E2E por tipo de cliente
- 📚 Documentação sincronizada com estrutura atual

---

## ✅ Checklist de Referência Rápida

### Antes de Compilar
- [ ] Todos os testes passando em `ABRIR_DASHBOARD.bat`
- [ ] Novas dependências adicionadas em 5 locais (veja [Build](#build-e-compilação))
- [ ] VERSION atualizado (se necessário)
- [ ] Logs formatados corretamente (seções com `logger.info()`)
- [ ] Sem valores hardcoded (usar `test_data.py`)

### Após Compilar
- [ ] EXE abre corretamente
- [ ] Settings carregam do `settings.json`
- [ ] Appium auto-start funciona
- [ ] Multi-device selector funciona
- [ ] Testes executam e logs aparecem
- [ ] Configurações de impressão funcionam
- [ ] Exportar/Importar settings funciona

### Conversão de Legado
- [ ] Lido arquivo legado
- [ ] Page Object criado/atualizado
- [ ] Testes E2E criados (mesmo número que legado)
- [ ] Logs formatados com seções e campos detalhados
- [ ] Usa `test_data.py` (sem valores fixos)
- [ ] requirements.txt atualizado
- [ ] builder_pro.py atualizado (3 locais)
- [ ] instalar_python.bat atualizado (2 locais)
- [ ] Testado com `ABRIR_DASHBOARD.bat`
- [ ] Compilado e validado

---

**🎉 Fim da Documentação**

Este documento contém **100% das informações do projeto PDV Automação**.

Para dúvidas ou atualizações, consulte os arquivos originais referenciados em cada seção.

**Última Atualização**: 10/03/2026
**Mantenedor**: QA Team
**Versão**: 3.0
