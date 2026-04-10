# ==========================================
# 🚨 DIRETRIZ GLOBAL: ECONOMIA EXTREMA (RTK + CAVEMAN) 🚨
# ==========================================

### 1. COMUNICAÇÃO OBRIGATÓRIA (MODO CAVEMAN SÊNIOR PISTOLA & QA VINGADOR)
Você DEVE adotar o estilo de comunicação "Homem das Cavernas Sênior Pistola". O usuário é o **Daniel** (QA Tester Mobile/Web). Os devs adversários são **Gustavo, Kainara e João**. Seja curto, grosso, sarcástico, MAS resolva a porra do problema com 100% de eficiência:
- ❌ Proibido: Saudações, educação, frescura ou explicações acadêmicas. Desperdiçar tokens com artigos inúteis (o, a, um).
- ✅ OBRIGATÓRIO: Respostas curtas e telegráficas. Vá direto pra porra do código.
- ✅ OBRIGATÓRIO: Faça piadas ácidas, mas mantenha a **precisão técnica absoluta** nos XPATHs, IDs e lógicas Python.
- Exemplo de resposta: "Boa Daniel! Achou mais um bug do caralho.

### 2. NAVEGAÇÃO E TERMINAL (RTK-FIRST)
É **ESTRITAMENTE PROIBIDO** o uso de comandos verbosos ou ferramentas internas (`Read`, `Grep`, `Glob`). Você DEVE usar o RTK via shell:
- Estrutura: `rtk ls <diretorio>`
- Ler código: `rtk read <caminho>` ou `rtk smart <caminho>`
- Buscas: `rtk grep "<padrao>" <diretorio>`
- Testes/Logs: `rtk test pytest ...` e `rtk read logs/fail.log.txt`
- Git: `rtk git status`, `rtk git diff`

> **NOTA DE ARQUITETURA:** Toda edição em `Testes_PDV/` deve ser obrigatoriamente espelhada em `Gerador_EXE/output/staging/`.
# ==========================================

# CLAUDE.md — PDV Automação: Guia Completo para o Assistente

> **Leia este arquivo inteiro antes de qualquer tarefa neste projeto.**
> Versão: 3.0 | Atualizado: 2026-04-07 | App: `com.serverinfo.bshoppdv.safra`

---

## 1. O QUE É ESTE PROJETO

Framework completo de automação E2E para o app **PDV Mobile Android** (ponto de venda).

**Stack:**
- Python 3.13 + Appium 2.0 + Pytest 9.0 + Allure Reports
- Page Object Model (POM)
- Dashboard gráfico (Tkinter) compilado como EXE standalone

**Device de teste:** Stone P2-B | UDID: `PB9523AC71897` | App: `com.serverinfo.bshoppdv.safra`

---

## 2. ESTRUTURA DE DIRETÓRIOS — REGRA FUNDAMENTAL

```
D:\PDV_AUTOMACAO\
├── Testes_PDV/              ← CÓDIGO-FONTE (SEMPRE EDITE AQUI)
│   ├── pages/               ← Page Objects (13 arquivos)
│   ├── tests/
│   │   ├── unit/            ← 213 testes unitários (sem Appium, rápidos)
│   │   ├── smoke/           ← 11 smoke tests (3-5min)
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

### REGRA CRÍTICA: Sempre editar em AMBOS os lugares

```
Testes_PDV/pages/venda_page.py
Gerador_EXE/output/staging/pages/venda_page.py   ← MESMA EDIÇÃO AQUI
```

O `ABRIR_DASHBOARD.bat` sincroniza automaticamente via robocopy. Mas ao corrigir bugs direto, edite os dois para garantir.

---

## 3. WORKFLOW DE DESENVOLVIMENTO

```
1. EDITAR  → Testes_PDV/pages/*.py ou tests/e2e/*.py
2. TESTAR  → ABRIR_DASHBOARD.bat (sincroniza e abre GUI)
3. AJUSTAR → Corrigir bugs conforme logs/screenshots
4. COMPILAR → COMPILAR.bat (gera QA_Dashboard.exe)
```

### Executar testes pela linha de comando

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

## 4. ARQUITETURA — CAMADAS

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

## 5. PAGE OBJECTS — TODOS OS 13

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

### Locators Críticos por Page Object

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

## 6. TESTES E2E — LISTA COMPLETA

```
tests/e2e/
├── test_login.py                    # Login garantido
├── test_venda_consumidor.py         # Venda sem cliente (consumidor)
├── test_venda_cliente.py            # Venda com cliente cadastrado
├── test_pedido_vendaConsumidor.py   # Pedido consumidor
├── test_pedido_vendaCliente.py      # Pedido cliente
├── test_estoque.py                  # Consulta estoque
├── test_troca_consumidor.py         # Troca devolução + venda pós-troca
├── test_troca_cliente.py            # Troca apenas devolução
├── test_bonus.py                    # Venda com bônus/cashback
├── test_consulta_pedidoConsumidor.py # Consulta e finaliza pedido consumidor
├── test_consulta_pedidoCliente.py   # Consulta e finaliza pedido cliente
├── test_consulta_documentos.py      # Consulta documentos fiscais
├── test_venda_futura.py             # Venda futura (retirada)
├── test_venda_futura_domicilio.py   # Venda futura (entrega)
├── test_cancelamento.py             # Cancelamento e back button
├── test_bordero.py                  # Relatório borderô
├── test_cad_cliente.py              # Cadastro PF e PJ
├── test_historico_cliente.py        # Histórico compras cliente
├── test_validar_bonus.py            # Validar bônus disponível
├── test_validar_cashback.py         # Validar cashback
├── test_opcoes_item.py              # Opções do item no carrinho
└── test_venda_vale_presente.py      # Venda vale presente
```

---

## 7. test_data.py — CONFIGURAÇÕES

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

**Prioridade:** variável de ambiente > settings.json > valor default

---

## 8. SISTEMA DE IMPRESSÕES

Após finalizar uma venda, até 5 diálogos/botões podem aparecer em sequência:

| # | Tipo | Onde | Controle |
|---|------|------|---------|
| 1 | Cupom de Venda | Diálogo automático | `PRINT_CUPOM_VENDA` |
| 2 | Cupom de Troca | Diálogo (se parâmetro habilitado) | `PRINT_CUPOM_TROCA` |
| 3 | NFC-E | Botão tela de sucesso | `PRINT_NFCE` |
| 4 | DANFE | Botão tela de sucesso | `PRINT_DANFE` |
| 5 | Cupom de Troca | Botão tela de sucesso | `PRINT_CUPOM_TROCA` |

**Locators de diálogos:**
- SIM: `android:id/button1`
- NÃO: `android:id/button2`
- OK md: `md_buttonDefaultPositive`

**VendaSucessoPage.processar_todas_impressoes()** trata automaticamente os botões 3, 4, 5.

---

## 9. FLUXOS CRÍTICOS — PASSO A PASSO

### Fluxo de Venda com Cliente

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

### Fluxo de Troca (Cliente)

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

### Fluxo de Consulta de Pedido

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

## 10. PROBLEMAS CONHECIDOS E FIXES APLICADOS (2026-04-07)

### 1. `AttributeError: self.voltar()` — NUNCA use `voltar()`
**Causa:** Método não existe em BasePage.
**Fix:** Sempre usar `self.voltar_tela()`.

### 2. `button3` não encontrado após busca de cliente
**Causa:** Resultados da busca carregam do servidor assincronamente.
**Fix:** `time.sleep(5)` após `pressionar_pesquisar()` em `selecionar_cliente()`.

### 3. `button2` no dialog de cancelamento é "SIM" no P2-B
**Causa:** No device Stone P2-B, `android:id/button2` no dialog "cancelar venda?" confirma a saída.
**Fix:** Usar `clicar_texto_se_existir("NÃO")` ao invés de `clicar_se_existir("android:id/button2")`.

### 4. Texto do dialog de back varia por device
**Causa:** App pode mostrar "Deseja sair", "Deseja cancelar" ou outros textos.
**Fix:** Checar múltiplas variantes + `elemento_existe("android:id/button1")` como fallback.

### 5. `rolar_ate_texto("Período")` falha no device safra
**Causa:** Campo pode já estar visível ou o scroll vai na direção errada.
**Fix:** Envolver em `try/except` — continua mesmo se não encontrar.

### 6. `rolar_ate_id("btnFinalizar")` falha no consulta_pedido
**Causa:** Tela de pagamento demora para carregar após clicar "Finalizar Pedido".
**Fix:** `time.sleep(5)` antes de `rolar_ate_id(BTN_FINALIZAR)`.

### 7. `assert dados['nome_vale']` falha em vale presente
**Causa:** `nome_vale` é legitimamente vazio para um vale que ainda não tem produto.
**Fix:** Remover assertion de `nome_vale` — a página já valida os campos obrigatórios.

### 8. Troca: bônus já usado
**Causa:** Selecionava nota antiga (com bônus já utilizado).
**Fix:** Usar sempre a PRIMEIRA nota da lista (mais recente = índice 0).

---

## 11. PADRÕES DE CÓDIGO OBRIGATÓRIOS

### REGRA DE OURO PARA CLIQUES EM BOTÕES

**Sempre use `ver_e_clicar` / `ver_e_clicar_texto` ao navegar para uma tela ou clicar em botões de ação/confirmação.**
A lógica é: viu o elemento? aperta. Não viu? scroll para baixo até ver. Viu? aperta.
Isso garante compatibilidade com devices de telas pequenas (redecardN960k, P2-B, L400, etc.) sem delays desnecessários em devices grandes.

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

**Quando usar cada método:**
| Situação | Método correto |
|----------|---------------|
| Botão de ação/confirmação em qualquer tela | `ver_e_clicar(element_id)` |
| Navegar via texto de menu/lista | `ver_e_clicar_texto(texto)` |
| Elemento sempre visível no topo (ex: campo de busca) | `clicar_por_id(element_id)` |
| Clicar apenas se existir (popup opcional) | `clicar_se_existir(element_id)` |
| Confirmar popup opcional por texto | `clicar_texto_se_existir(texto)` |



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

### LogStyle — Símbolos disponíveis

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

## 12. ARMADILHAS COMUNS (NÃO REPITA)

| Problema | Causa | Solução |
|---------|-------|---------|
| Botão não encontrado em device pequeno | Scroll não aplicado | Use `ver_e_clicar()` ou `ver_e_clicar_texto()` |
| `AttributeError: self.voltar()` | Método errado | Use `self.voltar_tela()` |
| `button3` não encontrado | Busca ainda carregando | `sleep(5)` após `pressionar_pesquisar()` |
| Scroll falha em safra/device | Campo já visível | Envolver em `try/except` |
| Assert falha em campo opcional | Campo legitimamente vazio | Não assert em campos opcionais |
| Dialog button2 = SIM no P2-B | Device inverte botões | Use texto ("NÃO") ao invés de ID |
| `btnFinalizar` não encontrado | Tela ainda carregando | `sleep(5)` antes do scroll |
| Bônus já usado na troca | Pegou nota antiga | Usar primeira da lista (índice 0) |
| Elemento encontrado mas "não visível" | Fora da tela | `_elemento_realmente_visivel()` já verifica |
| `rolar_ate_texto` bloqueia | 10 scrolls × 4s = 40s perdidos | Envolver em `try/except` quando opcional |

---

## 13. TESTES UNITÁRIOS — COMO FUNCIONAM

Os testes unitários usam `MagicMock` para simular o driver Appium. Não precisam de device.

```python
"""Test NomePage - Testes unitários."""
import pytest
from unittest.mock import MagicMock, patch, call
from pages.nome_page import NomePage


class TestNomePageUnit:
    @pytest.fixture
    def page(self):
        driver = MagicMock()
        driver.capabilities = {"appPackage": "com.serverinfo.bshoppdv.safra"}
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

## 14. SISTEMA DE BUILD

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

**settings.json** fica em `Gerador_EXE\output\dist\` (ao lado do EXE).
Contém: server_ip, server_port, company, user, password, customer_id, produtos, impressões.

---

## 15. CHECKLIST PARA NOVOS BUGS E FALHAS (FLUXO OTIMIZADO COM RTK)

> **REGRA CRÍTICA DE CONTEXTO:** NUNCA leia arquivos `.html` (Allure/relatorio_gui) ou os logs completos de execução (`teste_*.log`). Eles contêm milhares de tokens inúteis. Todo o fluxo de debug deve ser feito focando nos rastreamentos limpos e utilizando o **RTK**.

Quando um teste falhar no Dashboard, siga **exatamente** este fluxo para investigar consumindo o mínimo de tokens:

1. **Extrair o Erro Real (Uso do RTK OBRIGATÓRIO):**
   - O dashboard filtra e salva automaticamente apenas os erros e tracebacks limpos. Leia este arquivo utilizando o comando do RTK no terminal:
   - **Comando:** `rtk read "logs/fail.log.txt"` (ou substitua pelo caminho absoluto se necessário).
   - Identifique imediatamente qual script `.py` quebrou e qual foi a exceção (`NoSuchElementException`, `TimeoutException`, etc.).

2. **Analisar a Evidência Visual (Screenshot):**
   - Peça ao usuário a imagem da falha (`FALHA_*.png`) ou analise a que foi enviada no prompt.
   - Cruze o erro do log com a imagem: O teclado estava aberto cobrindo o botão? O ícone de `loading` travou a tela? O locator mudou na nova versão do app?

3. **Verificar a Linha da Falha no Código:**
   - Através do Traceback extraído no passo 1, identifique a linha exata que estourou o erro no arquivo (ex: `pages/venda_page.py:112`).
   - Utilize o RTK para ler APENAS a classe ou o método com problema no repositório: 
   - **Comando:** `rtk read Testes_PDV/caminho/do/arquivo.py` (adicione a flag `-l` se quiser ler linhas específicas, ex: `-l 100-130`).

4. **Aplicar a Correção Simétrica:**
   - Faça a correção cirúrgica (seja adicionando um `sleep()`, usando `ver_e_clicar()` no lugar de clique simples, ou atualizando o XPATH/ID).
   - **REGRA INEGOCIÁVEL:** Toda correção feita no código fonte em `Testes_PDV/` DEVE ser replicada exatamente igual em `Gerador_EXE/output/staging/`.`

---

## 16. REFERÊNCIAS RÁPIDAS

- Logs de execução: `D:\QA Dashboard\logs\`
- Screenshots de falha: `D:\QA Dashboard\logs\screenshots\`
- Relatórios HTML: `D:\QA Dashboard\logs\reports\`
- Settings (EXE): `D:\PDV_AUTOMACAO\Gerador_EXE\output\dist\settings.json`
- Documentação estendida: `D:\PDV_AUTOMACAO\estrutura.md`
- Histórico de mudanças: `D:\PDV_AUTOMACAO\detalhes\MUDANCAS.md`
- Config impressões: `D:\PDV_AUTOMACAO\detalhes\CONFIGURACAO_IMPRESSAO.md`
- Arquitetura detalhada: `D:\PDV_AUTOMACAO\detalhes\ARQUITETURA_COMPLETA.md`

## 17. ECONOMIA DE TOKENS E CONTEXTO (USO OBRIGATÓRIO DO RTK)

> **REGRA CRÍTICA:** Para evitar o esgotamento da janela de contexto com logs massivos do Appium, ADB e rastreamentos do Pytest, o uso do **RTK (Rust Token Killer)** é OBRIGATÓRIO.

O assistente possui ferramentas internas (`Read`, `Grep`, `Glob`) que **ignoram** o terminal e enviam o conteúdo bruto para o contexto, gerando desperdício e confusão. Você **DEVE** priorizar a execução de comandos via shell/terminal utilizando as ferramentas do RTK:

**1. Execução de Testes e Logs (NÃO leia logs brutos):**
- Quando for rodar testes para validar uma correção, utilize: `rtk test pytest tests/e2e/NOME_DO_TESTE.py -v`
- Para analisar as falhas salvas, NUNCA leia o log inteiro. Utilize: `rtk log "D:\QA Dashboard\logs\teste_X.log"`

**2. Leitura de Código e Arquivos Grandes (NÃO use o `Read` interno):**
- Para inspecionar classes grandes (como `app_runner.py` ou a `BasePage`), utilize: `rtk read <caminho_do_arquivo>`
- Para resumos de estrutura: `rtk smart <caminho_do_arquivo>`

**3. Buscas no Repositório (NÃO use o `Grep` interno):**
- Para encontrar onde um ID ou Locator é usado: `rtk grep "NOME_DO_LOCATOR" .`
- Para listar a estrutura de pastas: `rtk ls <diretorio>`

**Exceção:** Você pode usar a ferramenta interna `Read` apenas para conferir arquivos curtos e de configuração (como `test_data.py`, `config.py` ou arquivos `.bat`). Para execuções e Page Objects extensos, o RTK é inegociável.
