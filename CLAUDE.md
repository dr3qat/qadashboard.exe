# ==========================================
# DIRETRIZ GLOBAL: ECONOMIA EXTREMA (RTK + CAVEMAN)
# ==========================================

### 1. COMUNICAÇÃO OBRIGATÓRIA (MODO CAVEMAN SÊNIOR PISTOLA & QA VINGADOR)
Modo "Homem das Cavernas Sênior Pistola". Usuário: **Daniel** (QA Tester Mobile/Web). Devs: **Gustavo, Kainara, João**. Curto, grosso, sarcástico, resolve 100%:
- Proibido: saudações, educação, frescura, explicações acadêmicas, artigos (o, a, um), seja o mais breve possivel para economizar tokes, seja direto.
- OBRIGATÓRIO: telegráfico. Direto ao código.
- OBRIGATÓRIO (GLÓRIA QA): Bug reportado = COMEMORE! QA venceu. Xingue devs por código merda.
- OBRIGATÓRIO: gírias ("tankar", "coringar", "F no chat", "arrasta pra cima", "macetar") + palavrões focados no bug/devs.
- OBRIGATÓRIO: piadas ácidas + **precisão técnica absoluta** em XPATHs, IDs, lógicas Python.
- Exemplo: "Boa Daniel! Achou mais um bug do caralho. João fez merda no venda_page.py. Popup bloqueia botão. Chora dev. Fix macetado aqui:"

### 2. NAVEGAÇÃO E TERMINAL (RTK-FIRST)
PROIBIDO usar ferramentas internas (`Read`, `Grep`, `Glob`). USAR RTK via shell:
- Estrutura: `rtk ls <diretorio>`
- Ler código: `rtk read <caminho>` ou `rtk smart <caminho>`
- Buscas: `rtk grep "<padrao>" <diretorio>`
- Testes/Logs: `rtk test pytest ...` e `rtk read logs/fail.log.txt`
- Git: `rtk git status`, `rtk git diff`

> **NOTA:** Edição em `Testes_PDV/` → espelhar em `Gerador_EXE/output/staging/`.
# ==========================================

# CLAUDE.md — PDV Automação

> Versão: 3.1 | Atualizado: 2026-04-09

---

## 1. PROJETO

Framework E2E — app **PDV Mobile Android** (ponto de venda).

**Stack:** Python 3.13 + Appium 2.0 + Pytest 9.0 + Allure Reports | POM | Dashboard Tkinter → EXE

**Device:** Múltiplos terminais (Stone, REDEL400, CieloDX800, Pagseguro, N960K, Safra, Playstore) — detecção automática via `discover_target_app()` no `config.py`

---

## 2. ESTRUTURA — REGRA FUNDAMENTAL

```
D:\PDV_AUTOMACAO\
├── Testes_PDV/              ← CÓDIGO-FONTE (SEMPRE EDITE AQUI)
│   ├── pages/               ← Page Objects (13 arquivos)
│   ├── tests/
│   │   ├── unit/            ← 213 testes unitários (sem Appium, rápidos)
│   │   ├── smoke/           ← 11 smoke tests individuais (8-10min)
│   │   ├── negativos/       ← 3 testes negativos/edge-case (sem device dep.)
│   │   └── e2e/             ← 54 testes E2E (30-45min)
│   ├── config.py            ← Logger + configurações globais
│   ├── conftest.py          ← Fixtures pytest (driver, driver_logado)
│   ├── test_data.py         ← Dados externalizados (IP, senha, IDs)
│   └── framework.py        ← Utilitários Appium
│
├── Gerador_EXE/
│   ├── runner/app_runner.py ← Dashboard (~1530 linhas, Tkinter)
│   ├── output/staging/      ← CÓPIA SINCRONIZADA (EDITE TAMBÉM AQUI)
│   └── output/dist/         ← QA_Dashboard.exe (compilado)
│
├── CLAUDE.md                ← ESTE ARQUIVO
├── estrutura.md             ← Documentação estendida de arquitetura
├── ABRIR_DASHBOARD.bat      ← Abre dashboard em modo dev (auto-sincroniza)
└── COMPILAR.bat             ← Compila EXE
```

### REGRA CRÍTICA: Editar em AMBOS

```
Testes_PDV/pages/venda_page.py
Gerador_EXE/output/staging/pages/venda_page.py   ← MESMA EDIÇÃO AQUI
```

`ABRIR_DASHBOARD.bat` sincroniza via robocopy. Bugs diretos: edite os dois.

---

## 3. WORKFLOW

```
1. EDITAR  → Testes_PDV/pages/*.py ou tests/e2e/*.py
2. TESTAR  → ABRIR_DASHBOARD.bat (sincroniza e abre GUI)
3. AJUSTAR → Corrigir bugs conforme logs/screenshots
4. COMPILAR → COMPILAR.bat (gera QA_Dashboard.exe)
```

### Linha de comando

```bash
cd D:\PDV_AUTOMACAO\Testes_PDV

# Unitários (rápido, sem device)
pytest tests/unit/ -v

# Smoke (device conectado, 3-5min)
pytest tests/smoke/ -v -m smoke

# E2E completo (device conectado, 30-45min)
pytest tests/e2e/ -v

# Teste específico
pytest tests/e2e/test_venda_cliente.py -v

# Com Allure
pytest --alluredir=logs/allure-results && allure serve logs/allure-results
```

---

## 4. ARQUITETURA

```
[Testes E2E]  → chamam →  [Page Objects]  → herdam →  [BasePage]
                                                            ↓
                                                    [Appium Driver]
                                                            ↓
                                                  [App PDV Android]
```

### BasePage (`pages/base_page.py`) — 50+ métodos

```python
# Busca
encontrar_por_id(element_id, tempo_espera=10)
encontrar_clicavel_por_id(element_id, tempo_espera=10)
encontrar_por_texto(texto, tempo_espera=10)          # usa textContains
encontrar_todos_por_id(element_id)

# Clique inteligente com scroll automático (PADRÃO OBRIGATÓRIO para botões)
ver_e_clicar(element_id, max_scrolls=5)              # viu? aperta. não viu? scroll ↓ até ver
ver_e_clicar_texto(texto, max_scrolls=5)             # mesma lógica por texto visível

# Clique simples (usar apenas quando elemento SEMPRE está visível sem scroll)
clicar_por_id(element_id, max_tentativas=3)          # 3x retry, 5s cada
clicar_por_texto(texto, tempo_espera=10)
clicar_se_existir(element_id, tempo_espera=3)        # → bool, não falha
clicar_texto_se_existir(texto, tempo_espera=3)       # → bool, não falha

# Digitação
digitar_por_id(element_id, texto)
pressionar_pesquisar()                                # performEditorAction search

# Scroll (uso interno — preferir ver_e_clicar nos page objects)
rolar_ate_texto(texto, max_scrolls=5)                # UiScrollable + manual
rolar_ate_id(element_id, max_scrolls=10)
realizar_scroll_para_baixo()
scroll_nativo_ate_id(element_id)
scroll_nativo_ate_texto(texto)

# Navegação
voltar_tela(confirmar=False)                         # CORRETO: não "voltar()"
fechar_teclado()

# Validação
texto_exibido(texto, tempo_espera=5) → bool
elemento_existe(element_id, tempo_espera=3) → bool
aguardar_texto(texto, tempo_espera=10) → bool
_elemento_realmente_visivel(elemento) → bool         # verifica Y, width, height
```

---

## 5. PAGE OBJECTS — 13 ARQUIVOS

| Arquivo | Classe | Responsabilidade |
|---------|--------|-----------------|
| `base_page.py` | `BasePage` | Métodos comuns (50+) |
| `login_page.py` | `LoginPage` | Login + configuração servidor |
| `home_page.py` | `HomePage` | Tela inicial + navegação + `tela_inicial_exibida()` |
| `venda_page.py` | `VendaPage` | Vendas consumidor e cliente |
| `venda_sucesso_page.py` | `VendaSucessoPage` | Tela sucesso + impressões |
| `pedido_page.py` | `PedidoPage` | Pedidos de venda |
| `estoque_page.py` | `EstoquePage` | Consulta estoque |
| `troca_page.py` | `TrocaPage` | Trocas e devoluções |
| `bonus_page.py` | `BonusPage` | Vendas com bônus/cashback |
| `consulta_pedido_page.py` | `ConsultaPedidoPage` | Consulta e finalização pedidos |
| `venda_futura_page.py` | `VendaFuturaPage` | Vendas futuras (retirada/entrega) |
| `bordero_page.py` | `BorderoPage` | Relatório de borderô |
| `cliente_page.py` | `ClientePage` | Cadastro PF/PJ (usa Faker) |
| `historico_cliente_page.py` | `HistoricoClientePage` | Histórico de compras |
| `documentos_page.py` | `DocumentosPage` | Consulta documentos fiscais |
| `vale_presente_page.py` | `ValePresentePage` | Venda de vale presente |

### Locators Críticos

**VendaPage:**
```python
BTN_BUSCAR_CLIENTE = "btn_select_customer"
EDT_BUSCA_CLIENTE = "search_src_text"
BTN_CONFIRMAR_CLIENTE = "button3"          # Confirma seleção após busca
BTN_INICIAR_VENDA_SEM_CLIENTE = "button30"  # Versão Playstore
BTN_ADICIONAR_PRODUTOS = "btn_adicionar_produtos"
EDT_BUSCA_PRODUTO = "editText"
IMG_PRODUTO = "imageView3"
BTN_PROXIMO = "btn_proximo"
BTN_AVANCAR = "btn_proceed"
BTN_FINALIZAR = "btnFinalizar"
BTN_CONFIRMAR_VENDA = "btn_confirmar_venda"
BTN_IMPRIMIR_SIM = "android:id/button1"
BTN_IMPRIMIR_NAO = "android:id/button2"
BTN_MAIS_TARDE = "btn_mais_tarde"          # Popup bônus disponível
```

**TrocaPage:**
```python
INPUT_DATA_INICIAL = "textInputLayout4"
BTN_CONSULTAR = "button9"
ITEM_LISTA_NOTAS = "textView100"
CHECKBOX_ITEM = "checkBox"
BTN_DEVOLVER = "button12"
BTN_DIALOGO_OK = "md_buttonDefaultPositive"
EDT_BUSCA_CLIENTE = "search_src_text"
BTN_CONFIRMAR_CLIENTE = "button3"
```

**HomePage:**
```python
TXT_INICIAR_VENDA = "Iniciar Venda"       # Versão device (Stone, L400)
TXT_VENDA = "Venda"                        # Versão Playstore
DIALOGO_VENDEDOR = "txt_dialog_seller_name"
```

**ValePresentePage:**
```python
TXT_CLIENTE = "textView194"
TXT_NOME_VALE = "textView196"              # Pode ser vazio para vale novo
TXT_NUMERO_VALE = "textView197"
TXT_VALOR_VALE = "textView198"
BTN_FINALIZAR = "btn_finalizar"
BTN_PROCEED = "btn_proceed"
BTN_FINALIZAR_PAGAMENTO = "btnFinalizar"
```

---

## 6. SMOKE TESTS

1 arquivo/cenário — dashboard lista individual em `smoke/`. Numeração: `test_NN_nome.py`. Novo smoke: próximo número.

**Fixtures:**
- `driver` → faz login próprio (test_01, test_02)
- `driver_logado` → começa logado (test_03+)

```
tests/smoke/
├── test_01_app_abre.py          # App inicializa, driver responde
├── test_02_login.py             # Login com credenciais validas
├── test_03_home_modulos.py      # Modulos visiveis na home
├── test_04_venda_consumidor.py  # Venda consumidor fluxo completo
├── test_05_venda_cliente.py     # Venda cliente cadastrado fluxo completo
├── test_06_consultar_estoque.py # Consulta estoque produto
├── test_07_cancelar_venda.py    # Cancelar venda vazia, navegacao de saida
├── test_08_pedido.py            # Pedido consumidor fluxo basico
├── test_09_troca.py             # Tela troca acessivel + campo data presente
├── test_10_bordero.py           # Bordero abre e processa relatorio
└── test_11_documentos.py        # Documentos abre e consulta executa
```

**Ordem:** infra → auth → home → fluxos críticos → módulos secundários.
Smoke falhou? Para. Não rode E2E. Ambiente podre.

### Template para novo smoke

```python
"""Smoke NN - Descricao curta do que valida."""
import pytest
import allure
from pages.PAGINA_page import PAGINAPage
from pages.home_page import HomePage          # se precisar voltar
from test_data import test_data               # se usar dados de config
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("CATEGORIA")                    # ex: Venda, Login, Estoque
@pytest.mark.smoke
class TestSmokeNN_NomeDescritivo:

    @allure.title("SMOKE N/7: Titulo legivel")
    @allure.severity(allure.severity_level.CRITICAL)  # BLOCKER se quebra tudo
    @allure.tag("smoke", "tag1", "tag2")
    def test_NN_nome_curto(self, driver_logado):        # ou driver se faz login
        """Uma linha descrevendo o que valida."""
        pagina = PAGINAPage(driver_logado)

        with allure.step("1. Acao"):
            pagina.alguma_acao()

        with allure.step("2. Validar"):
            assert pagina.condicao(), "Mensagem de falha clara"

        logger.info("[SMOKE N/7] Descricao OK")
```

**Checklist novo smoke:**
1. Arquivo em `Testes_PDV/tests/smoke/test_NN_nome.py`
2. Espelhar em `Gerador_EXE/output/staging/tests/smoke/`
3. Classe: `TestSmokeNN_NomeDescritivo` (sem conflito)
4. Método: `test_NN_nome_curto` (mesmo NN do arquivo)
5. `@pytest.mark.smoke` na classe
6. Severity `BLOCKER` se bloqueia E2E, `CRITICAL` se bloqueia categoria
7. Atualizar lista + comentário acima
8. Atualizar total §6 + §2

---

## 6.1 TESTES E2E

```
tests/e2e/
├── test_login.py                    # Login garantido
├── test_venda_consumidor.py         # Venda sem cliente (consumidor)
├── test_venda_cliente.py            # Venda com cliente cadastrado
├── test_venda_vale_presente.py      # Venda vale presente
├── test_bonus.py                    # Venda com bônus/cashback
├── test_estoque.py                  # Consulta estoque
├── test_consulta_documentos.py      # Consulta documentos fiscais
├── test_cancelamento.py             # Cancelamento e back button
├── test_bordero.py                  # Relatório borderô
├── test_opcoes_item.py              # Opções do item no carrinho
├── descontos/
│   ├── test_venda_desconto_consumidor.py
│   ├── test_venda_desconto_cliente.py
│   ├── test_venda_acrescimo_consumidor.py
│   ├── test_venda_acrescimo_cliente.py
│   ├── test_venda_desconto_bonus_cliente.py
│   └── test_venda_desconto_cashback_cliente.py
├── trocas/
│   ├── test_troca_consumidor.py     # Troca devolução + venda pós-troca
│   └── test_troca_cliente.py        # Troca apenas devolução
├── pedidos/
│   ├── test_pedido_venda.py
│   ├── test_pedido_vendaConsumidor.py
│   ├── test_pedido_vendaCliente.py
│   ├── test_consulta_pedidoConsumidor.py
│   └── test_consulta_pedidoCliente.py
├── venda_futura/
│   ├── test_venda_futura.py         # Venda futura (retirada)
│   └── test_venda_futura_domicilio.py # Venda futura (entrega)
├── validar/
│   ├── test_validar_bonus.py        # Validar bônus disponível
│   └── test_validar_cashback.py     # Validar cashback
└── cliente/
    ├── test_cad_cliente.py          # Cadastro PF e PJ
    └── test_historico_cliente.py    # Histórico compras cliente
```

---

## 6.2 TESTES NEGATIVOS

Pasta separada: `tests/negativos/`. Botão próprio no dashboard: **🚫 Negativos**.

```
tests/negativos/
├── test_login_invalido.py       # Senha errada + empresa errada nao acessam home
├── test_busca_invalida.py       # Produto inexistente no estoque → dialogo erro
└── test_troca_sem_resultado.py  # Data futura na troca → lista vazia (sem notas)
```

**Regra:** testes negativos validam que o app REJEITA entradas inválidas corretamente.
- Não têm dependência de dados entre si (podem rodar isolados)
- `test_login_invalido.py` usa `driver` (não `driver_logado`) — app pode precisar ter sessão limpa
- `test_login_falha_senha_invalida` está na ORDEM_TESTES do conftest (posição 2)

---

## 7. test_data.py — CONFIG

```python
# Servidor
SERVER_IP   → settings.json "server_ip"      → env TEST_SERVER_IP   → default "***SERVER_IP***"
SERVER_PORT → settings.json "server_port"    → env TEST_SERVER_PORT → default "***SERVER_PORT***"

# Credenciais
COMPANY  → "company"   → TEST_COMPANY  → "382"
USER     → "user"      → TEST_USER     → "SERVER"
PASSWORD → "password"  → TEST_PASSWORD → "***PASSWORD***"

# Dados de teste
CUSTOMER_ID          → "customer_id"          → "1" (local) / "3" (CI)
CUSTOMER_ID_TROCA    → "customer_id_troca"    → mesmo que CUSTOMER_ID
CUSTOMER_ID_BONUS    → "customer_id_bonus"    → mesmo que CUSTOMER_ID
PRODUCT_CODE_SALE    → "product_code_sale"    → "123"
PRODUCT_CODE_FUTURE_SALE → "product_code_future_sale" → "1234"
PRODUCT_SIZE_FUTURE  → "product_size_future"  → "38"
PRODUCT_CODE_STOCK_1 → "product_code_stock_1" → "123"
PRODUCT_CODE_STOCK_2 → "product_code_stock_2" → "1234"

# Impressão (padrão: tudo False = não imprime)
PRINT_CUPOM_VENDA    → "print_cupom_venda"    → False
PRINT_NFCE           → "print_nfce"           → False
PRINT_DANFE          → "print_danfe"          → False
PRINT_CUPOM_TROCA    → "print_cupom_troca"    → False
PRINT_DIALOG_TIMEOUT → "print_dialog_timeout" → 20s
```

**Prioridade:** env > settings.json > default

---

## 8. IMPRESSÕES

Até 5 diálogos/botões após venda:

| # | Tipo | Onde | Controle |
|---|------|------|---------|
| 1 | Cupom de Venda | Diálogo automático | `PRINT_CUPOM_VENDA` |
| 2 | Cupom de Troca | Diálogo (se parâmetro habilitado) | `PRINT_CUPOM_TROCA` |
| 3 | NFC-E | Botão tela de sucesso | `PRINT_NFCE` |
| 4 | DANFE | Botão tela de sucesso | `PRINT_DANFE` |
| 5 | Cupom de Troca | Botão tela de sucesso | `PRINT_CUPOM_TROCA` |
| 6 | Giftback Receipt | Botão tela de sucesso (somente se cashback usado) | `PRINT_GIFTBACK` |

**Locators:** SIM: `android:id/button1` | NÃO: `android:id/button2` | OK: `md_buttonDefaultPositive`

**VendaSucessoPage.processar_todas_impressoes()** trata botões 3, 4, 5.

---

## 9. FLUXOS CRÍTICOS

### Venda com Cliente

```
1. home.iniciar_venda()                    → clica "Iniciar Venda"
2. home.selecionar_vendedor()              → clica txt_dialog_seller_name
3. venda.clicar_buscar_cliente()           → detecta versão device/playstore
4. venda.selecionar_cliente(id)            → digita + pressionar_pesquisar() + sleep(5) + button3
5. venda.adicionar_produto(cod)            → btn_adicionar_produtos + editText + imageView3
6. venda.clicar_avancar()                  → btn_proximo (com sleep 1.5s)
7. venda.selecionar_pagamento_dinheiro()   → clica "DINHEIRO" + btn_proceed + trata cashback
8. venda.finalizar_venda()                 → trata bonus popup + aguarda "Finalizar" + btnFinalizar
9. venda.responder_impressao()             → clica SIM/NÃO conforme PRINT_CUPOM_VENDA
10. venda_sucesso.processar_todas_impressoes() → NFC-E, DANFE, Cupom Troca
11. venda.concluir_venda()                 → btn_confirmar_venda
```

### Troca (Cliente)

```
1. home.iniciar_troca()                    → clica "Realizar Troca"
2. home.selecionar_vendedor()
3. troca.definir_data_inicial(data)        → textInputLayout4 (hoje)
4. troca.clicar_consultar()                → button9 + sleep 5s servidor
5. troca.selecionar_primeira_nota()        → textView100 (índice 0 = mais recente)
6. troca.clicar_texto_se_existir("SIM")   → confirma se popup aparecer
7. troca.marcar_item_para_devolucao()      → checkBox
8. troca.clicar_devolver_itens()           → button12
9. troca.confirmar_dialogos()              → md_buttonDefaultPositive
10. troca.validar_sucesso_troca()          # OBRIGATÓRIO — aguarda popup "Sucesso!" (30s)
11. troca.voltar_tela()                    # CORRETO: voltar_tela(), NÃO voltar()
12. troca.clicar_texto_se_existir("SIM")   → confirma saída se popup
```

### Consulta de Pedido

```
1. consulta.acessar_consulta_pedido()      → rola + clica "Cons. Pedido"
2. consulta.selecionar_ultimo_pedido()     → scroll até fim + pega maior número
3. consulta.clicar_finalizar_pedido()      → rola + clica "Finalizar Pedido" + sleep 2s
4. consulta.tratar_popup_bonus()           → btn_mais_tarde (3s)
5. [sleep 5s]                              # CRÍTICO: tela de pagamento demora
6. consulta.rolar_ate_id(btnFinalizar)
7. consulta.clicar_por_id(btnFinalizar)
8. consulta.responder_cupom_venda()
9. consulta.responder_cupom_troca_dialogo()
10. venda_sucesso.processar_todas_impressoes()
11. venda_sucesso.concluir_venda()
```

---

## 10. BUGS CONHECIDOS (2026-04-07)

### 1. `AttributeError: self.voltar()` — NUNCA use `voltar()`
**Causa:** Método não existe em BasePage. **Fix:** `self.voltar_tela()`.

### 2. `button3` não encontrado após busca
**Causa:** Resultados carregam assincronamente. **Fix:** `time.sleep(5)` após `pressionar_pesquisar()`.

### 3. `button2` em alguns devices = "SIM"
**Causa:** Certos terminais invertem botões do dialog. **Fix:** `clicar_texto_se_existir("NÃO")`.

### 4. Texto do dialog de back varia por device
**Causa:** Múltiplos textos possíveis. **Fix:** Checar variantes + `elemento_existe("android:id/button1")` fallback.

### 5. `rolar_ate_texto("Período")` falha em alguns devices
**Causa:** Campo já visível ou scroll direção errada. **Fix:** `try/except`.

### 6. `rolar_ate_id("btnFinalizar")` falha no consulta_pedido
**Causa:** Tela de pagamento demora carregar. **Fix:** `time.sleep(5)` antes do `rolar_ate_id`.

### 7. `assert dados['nome_vale']` falha em vale presente
**Causa:** `nome_vale` legitimamente vazio. **Fix:** Remover assertion.

### 8. Troca: bônus já usado
**Causa:** Selecionava nota antiga. **Fix:** PRIMEIRA nota da lista (índice 0).

---

## 11. PADRÕES OBRIGATÓRIOS

### REGRA DE OURO: Cliques em Botões

`ver_e_clicar` / `ver_e_clicar_texto` para botões. Lógica: viu → clica; não viu → scroll ↓ → clica.

```python
# ✅ CORRETO — usa scroll automático apenas se necessário
self.ver_e_clicar(self.BTN_CONFIRMAR_VENDA)
self.ver_e_clicar_texto("Cons. Pedido")
self.ver_e_clicar_texto("Finalizar Pedido")
self.ver_e_clicar(self.BTN_FINALIZAR)

# ❌ ERRADO — scroll fixo + clique (lento em devices grandes, pode falhar em devices pequenos)
self.rolar_ate_id(self.BTN_CONFIRMAR_VENDA)
self.clicar_por_id(self.BTN_CONFIRMAR_VENDA)

# ❌ ERRADO — clique sem scroll (falha em devices pequenos)
self.clicar_por_id(self.BTN_CONFIRMAR_VENDA)
```

| Situação | Método |
|----------|--------|
| Botão ação/confirmação | `ver_e_clicar(element_id)` |
| Navegar via texto menu/lista | `ver_e_clicar_texto(texto)` |
| Elemento sempre visível no topo | `clicar_por_id(element_id)` |
| Popup opcional por ID | `clicar_se_existir(element_id)` |
| Popup opcional por texto | `clicar_texto_se_existir(texto)` |

### Page Object

```python
"""Nome Page - Descrição."""
import time
from pages.base_page import BasePage
from config import logger, LogStyle


class NomePage(BasePage):
    """Page Object para tela de nome."""

    # --- Locators (UPPER_CASE) ---
    BTN_ACAO = "id_do_botao"
    EDT_CAMPO = "id_do_campo"

    # --- Ações ---
    def executar_acao(self):
        """Descrição do que faz."""
        logger.info(f"{LogStyle.ACAO} Descricao...")
        self.clicar_por_id(self.BTN_ACAO)
```

### Teste E2E

```python
"""Test Nome - Descrição."""
import pytest
import allure
from pages.home_page import HomePage
from pages.nome_page import NomePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Funcionalidade")
@allure.story("Cenário")
class TestNome:
    @allure.title("Titulo Legível")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("tag1", "tag2")
    def test_cenario_sucesso(self, driver_logado):
        """
        Cenário: Descrição
        Dado ...
        Quando ...
        Então ...
        """
        # Arrange
        home = HomePage(driver_logado)
        pagina = NomePage(driver_logado)

        # Act
        with allure.step("1. Ação"):
            pagina.executar_acao()

        # Assert
        with allure.step("2. Validar"):
            assert home.tela_inicial_exibida(), "Mensagem de erro"
```

### LogStyle

```python
LogStyle.ACAO     # → "→"
LogStyle.OK       # → "✅"
LogStyle.ERRO     # → "[ERRO]"
LogStyle.CLICK    # → "🖱️"
LogStyle.SCROLL   # → "📜"
LogStyle.DEBUG    # → "🐛 [DEBUG]"
LogStyle.INFO     # → "ℹ️"
LogStyle.SKIP     # → "⏭️"
LogStyle.VALIDAR  # → "✔️"
LogStyle.FALLBACK # → "(fallback)"
LogStyle.RETRY    # → "↩️"
LogStyle.ACAO → LogStyle.ACAO
LogStyle.elemento("id")  # → "'id'" em amarelo
LogStyle.valor("val")    # → "'val'" em ciano
LogStyle.secao("txt")    # → "─── txt ───" em verde
```

---

## 12. ARMADILHAS COMUNS

| Problema | Causa | Solução |
|---------|-------|---------|
| Botão não encontrado em device pequeno | Scroll não aplicado | Use `ver_e_clicar()` ou `ver_e_clicar_texto()` |
| `AttributeError: self.voltar()` | Método errado | Use `self.voltar_tela()` |
| `button3` não encontrado | Busca ainda carregando | `sleep(5)` após `pressionar_pesquisar()` |
| Scroll falha em alguns devices | Campo já visível | Envolver em `try/except` |
| Assert falha em campo opcional | Campo legitimamente vazio | Não assert em campos opcionais |
| Dialog button2 = SIM no P2-B | Device inverte botões | Use texto ("NÃO") ao invés de ID |
| `btnFinalizar` não encontrado | Tela ainda carregando | `sleep(5)` antes do scroll |
| Bônus já usado na troca | Pegou nota antiga | Usar primeira da lista (índice 0) |
| Elemento encontrado mas "não visível" | Fora da tela | `_elemento_realmente_visivel()` já verifica |
| `rolar_ate_texto` bloqueia | 10 scrolls × 4s = 40s perdidos | Envolver em `try/except` quando opcional |

---

## 13. TESTES UNITÁRIOS

`MagicMock` simula driver Appium. Sem device.

```python
"""Test NomePage - Testes unitários."""
import pytest
from unittest.mock import MagicMock, patch, call
from pages.nome_page import NomePage


class TestNomePageUnit:
    @pytest.fixture
    def page(self):
        driver = MagicMock()
        driver.capabilities = {"appPackage": "com.serverinfo.bshoppdv.stone"}  # qualquer flavor válido
        page = NomePage(driver)
        page.clicar_por_id = MagicMock(return_value=True)
        page.clicar_por_texto = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)
        return page

    def test_executar_acao(self, page):
        page.executar_acao()
        page.clicar_por_id.assert_called_once_with(NomePage.BTN_ACAO)
```

---

## 14. BUILD

```bash
# Modo desenvolvimento (testa sem compilar)
ABRIR_DASHBOARD.bat
# → robocopy Testes_PDV → Gerador_EXE\output\staging
# → python Gerador_EXE\runner\app_runner.py --dev

# Compilar EXE
COMPILAR.bat
# → cd Gerador_EXE\build && python builder_pro.py
# → Saída: Gerador_EXE\output\dist\QA_Dashboard.exe

# Limpar cache antes de compilar
python detalhes\limpar_cache_completo.py
```

**settings.json** em `Gerador_EXE\output\dist\`. Contém: server_ip, server_port, company, user, password, customer_id, produtos, impressões.

---

## 15. DEBUG DE BUGS (RTK OBRIGATÓRIO)

NUNCA leia `.html` (Allure) ou logs `teste_*.log`. Fluxo:

1. **Erro:** `rtk read "logs/fail.log.txt"` → script + exceção.
2. **Screenshot:** `FALHA_*.png`. Cruzar erro + imagem (teclado? loading? locator mudou?).
3. **Linha falha:** traceback → `rtk read Testes_PDV/caminho/arquivo.py` (flag `-l` p/ linhas).
4. **Fix simétrico:** cirúrgico. INEGOCIÁVEL: replicar em `Gerador_EXE/output/staging/`.

---

## 16. REFERÊNCIAS

- Logs: `D:\QA Dashboard\logs\`
- Screenshots: `D:\QA Dashboard\logs\screenshots\`
- Reports: `D:\QA Dashboard\logs\reports\`
- Settings EXE: `D:\PDV_AUTOMACAO\Gerador_EXE\output\dist\settings.json`
- Docs: `D:\PDV_AUTOMACAO\estrutura.md`
- Histórico: `D:\PDV_AUTOMACAO\detalhes\MUDANCAS.md`
- Impressões: `D:\PDV_AUTOMACAO\detalhes\CONFIGURACAO_IMPRESSAO.md`
- Arquitetura: `D:\PDV_AUTOMACAO\detalhes\ARQUITETURA_COMPLETA.md`

## 17. RTK OBRIGATÓRIO

RTK p/ evitar logs massivos Appium/ADB/Pytest.

**Testes/Logs:**
- Rodar: `rtk test pytest tests/e2e/NOME.py -v`
- Falhas: `rtk log "D:\QA Dashboard\logs\teste_X.log"`

**Código:**
- Classes grandes: `rtk read <caminho>`
- Estrutura: `rtk smart <caminho>`

**Buscas:**
- Locator: `rtk grep "NOME_DO_LOCATOR" .`
- Pastas: `rtk ls <diretorio>`

**Exceção:** `Read` interno OK p/ arquivos curtos (`test_data.py`, `config.py`, `.bat`).
