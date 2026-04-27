# 📦 Page Objects - Referência

Documentação de todos os Page Objects do projeto seguindo o padrão Page Object Model (POM).

---

## 🎯 Visão Geral

| Page Object | Arquivo | Responsabilidade |
|---|---|---|
| `BasePage` | `pages/base_page.py` | 50+ métodos comuns (busca, clique, scroll, digitação) |
| `LoginPage` | `pages/login_page.py` | Login + configuração de servidor |
| `HomePage` | `pages/home_page.py` | Tela inicial + navegação entre módulos |
| `VendaPage` | `pages/venda_page.py` | Vendas consumidor e cliente |
| `VendaSucessoPage` | `pages/venda_sucesso_page.py` | Tela sucesso + impressões (NFC-E, DANFE, cupom) |
| `PedidoPage` | `pages/pedido_page.py` | Pedidos de venda |
| `EstoquePage` | `pages/estoque_page.py` | Consulta de estoque |
| `TrocaPage` | `pages/troca_page.py` | Trocas e devoluções |
| `BonusPage` | `pages/bonus_page.py` | Bônus/cashback |
| `ConsultaPedidoPage` | `pages/consulta_pedido_page.py` | Consulta e finalização de pedidos |
| `VendaFuturaPage` | `pages/venda_futura_page.py` | Vendas futuras (retirada e entrega) |
| `BorderoPage` | `pages/bordero_page.py` | Relatório de borderô |
| `ClientePage` | `pages/cliente_page.py` | Cadastro PF/PJ (usa Faker) |
| `HistoricoClientePage` | `pages/historico_cliente_page.py` | Histórico de compras do cliente |
| `DocumentosPage` | `pages/documentos_page.py` | Consulta de documentos fiscais |
| `ValePresentePage` | `pages/vale_presente_page.py` | Venda de vale presente |
| `OpcoesItemPage` | `pages/opcoes_item_page.py` | Opções do item no carrinho |

---

## 📘 BasePage

### Descrição
Classe base com métodos comuns a todos os Page Objects.

### Principais Métodos

```python
# Busca de Elementos
encontrar_por_id(locator, tempo_espera=10)
encontrar_por_texto(texto, tempo_espera=10)
encontrar_por_xpath(xpath, tempo_espera=10)
encontrar_todos_por_id(locator, tempo_espera=10)

# Ações
clicar_por_id(locator, tempo_espera=10)
clicar_por_texto(texto, tempo_espera=10)
digitar_por_id(locator, texto, limpar=True)
pressionar_pesquisar()

# Validações
elemento_existe(locator, tempo_espera=5)
texto_exibido(texto, tempo_espera=10)
elemento_visivel(elemento)

# Navegação
rolar_ate_texto(texto, max_scrolls=10)
rolar_ate_id(locator, max_scrolls=10)
voltar_tela(confirmar=True)
```

---

## 🔐 LoginPage

### Responsabilidade
Autenticação e configuração inicial do app.

### Métodos Principais

```python
# Configuração
configurar_conexao(ip, porta)
preencher_credenciais(empresa, usuario, senha)

# Login
garantir_login(ip, porta, empresa, usuario, senha)
esta_logado()

# Navegação
pular_telas_introducao()
```

### Exemplo de Uso

```python
login_page = LoginPage(driver)
login_page.garantir_login(
    ip="192.168.1.100",
    porta="8080",
    empresa="1",
    usuario="admin",
    senha="senha123"
)
```

---

## 🏠 HomePage

### Responsabilidade
Tela inicial e navegação entre módulos.

### Métodos Principais

```python
# Navegação
iniciar_venda()
iniciar_troca()
selecionar_vendedor()

# Validações
tela_inicial_exibida(timeout=10)
```

### Exemplo de Uso

```python
home_page = HomePage(driver)
home_page.iniciar_venda()
home_page.selecionar_vendedor()
```

---

## 💰 VendaPage

### Responsabilidade
Fluxo completo de vendas (consumidor e cliente).

### Métodos Principais

```python
# Cliente
clicar_buscar_cliente()
selecionar_cliente(identificador)
iniciar_venda_sem_cliente()

# Produto
adicionar_produto(codigo="123")
clicar_avancar()

# Pagamento — formas fixas
selecionar_pagamento_dinheiro()
selecionar_pagamento(nome_forma, com_cliente=True, parcela=None)

# Pagamento — descoberta dinâmica (PREFERIDO para POS)
selecionar_pagamento_por_tipo(tipo, com_cliente=True, parcela="A Prazo 0 + 1")
descobrir_formas_tipadas()          # → {TipoForma: FormaInfo} — cacheia na sessão
obter_parcelas_disponiveis()        # → ["A Prazo 0 + 1", ...] — sheet aberto

# Finalização
finalizar_venda()
responder_impressao()
responder_dialogo_cupom_troca()
validar_sucesso_e_concluir()
```

### Exemplo de Uso — Venda com Dinheiro

```python
venda_page = VendaPage(driver)
venda_page.iniciar_venda_sem_cliente()
venda_page.adicionar_produto("123")
venda_page.clicar_avancar()
venda_page.selecionar_pagamento_dinheiro()
venda_page.finalizar_venda()
venda_page.validar_sucesso_e_concluir()
```

### Exemplo de Uso — Venda POS (dinâmico, qualquer base)

```python
from pages.venda_page import VendaPage, TipoForma

venda_page = VendaPage(driver)
venda_page.iniciar_venda_sem_cliente()
venda_page.adicionar_produto("123")
venda_page.clicar_avancar()

# Débito — skip automático se não disponível na base
nome = venda_page.selecionar_pagamento_por_tipo(TipoForma.POS_DEBITO, com_cliente=False)

# Crédito com parcela
nome = venda_page.selecionar_pagamento_por_tipo(
    TipoForma.POS_CREDITO, com_cliente=False, parcela="A Prazo 0 + 2"
)
allure.dynamic.parameter("forma_pagamento", nome)

venda_page.finalizar_venda()
venda_page.validar_sucesso_e_concluir()
```

### TipoForma — Valores

| Constante | Valor | Descrição |
|---|---|---|
| `TipoForma.DINHEIRO` | `"dinheiro"` | Pagamento em dinheiro |
| `TipoForma.POS_DEBITO` | `"pos_debito"` | Cartão débito via POS (sem parcelamento) |
| `TipoForma.POS_CREDITO` | `"pos_credito"` | Cartão crédito via POS (com bottom sheet de parcelas) |

> Ver detalhes: `detalhes/PAGAMENTOS_POS.md`

---

## 📋 PedidoPage

### Responsabilidade
Geração de pedidos de venda.

### Métodos Principais

```python
# Cliente
selecionar_vendedor()
clicar_buscar_cliente()
selecionar_cliente(identificador)
iniciar_como_consumidor()

# Produto
adicionar_produto(codigo="123")
clicar_avancar()

# Finalização
selecionar_pagamento_dinheiro()
finalizar_pedido()
confirmar_pedido_gerado()

# Fluxos Completos
executar_pedido_venda_consumidor(codigo_produto="123")
executar_pedido_venda_cliente(id_cliente, codigo_produto)
```

---

## 📦 EstoquePage

### Responsabilidade
Consulta de estoque e informações de produtos.

### Métodos Principais

```python
# Navegação
acessar_estoque()

# Busca
buscar_produto_por_codigo(codigo)
buscar_produto_por_nome(nome)

# Extração de Dados
obter_detalhes_completos()  # Retorna dict com nome, marca, cor, material, obs, preço
obter_quantidade_estoque()
obter_nome_produto()
obter_preco_produto()
obter_lista_produtos()

# Validações
produto_encontrado(timeout=5)
mensagem_nao_encontrado_exibida(timeout=5)

# Fluxo Completo
executar_consulta_estoque(codigo)  # Busca e retorna dict com todos os dados
```

### Exemplo de Uso

```python
estoque_page = EstoquePage(driver)
estoque_page.acessar_estoque()

# Consulta completa
resultado = estoque_page.executar_consulta_estoque("123")
# resultado = {
#     'encontrado': True,
#     'nome': 'PRODUTO TESTE',
#     'marca': 'USAFLEX',
#     'cor': 'Azul',
#     'material': 'Couro',
#     'obs': 'Observação',
#     'preco': 'R$ 99,90',
#     'quantidade': 'Sim'
# }
```

---

## 🔄 TrocaPage

### Responsabilidade
Trocas e devoluções (consumidor e cliente).

### Métodos Principais

```python
# Configuração
selecionar_vendedor()
definir_data_inicial(data=None)  # None = data atual
clicar_consultar()

# Seleção
selecionar_primeira_nota()
marcar_item_para_devolucao()

# Cliente (para troca de consumidor)
selecionar_cliente(cpf)
confirmar_dialogos()

# Pagamento
tratar_popup_bonus()
selecionar_pagamento_bonus()

# Validações
sucesso_exibido(timeout=15)
venda_sucesso_exibida(timeout=15)
validar_e_fechar_sucesso()

# Fluxos Completos
executar_troca(data_inicial=None, usar_bonus=True)
executar_troca_consumidor(cpf_cliente, usar_bonus=True)
```

---

## 🎁 BonusPage ✨

### Responsabilidade
Vendas utilizando bonus/cashback.

### Métodos Principais

```python
# Bonus
bonus_disponivel(tempo_espera=5)  # Verifica se switch está presente
obter_valor_bonus()  # Retorna valor do bonus disponível
bonus_ativado()  # Verifica se switch está ativado
ativar_bonus()  # Ativa o switch de bonus
obter_valor_final()  # Valor final após bonus
obter_desconto_bonus()  # Texto do desconto aplicado
bonus_foi_aplicado()  # Valida se bonus realmente foi aplicado

# Fluxo
buscar_cliente_por_cpf(cpf)
adicionar_produto(codigo="123")
clicar_avancar_carrinho()
clicar_avancar_pagamento()

# Validações
tela_pagamento_exibida(timeout=10)
venda_sucesso_exibida(timeout=15)
concluir_venda()
responder_impressao(imprimir=False)
```

### Exemplo de Uso

```python
bonus_page = BonusPage(driver)

# 1. Navegar até pagamento
home_page.iniciar_venda()
home_page.selecionar_vendedor()
bonus_page.buscar_cliente_por_cpf("12345678900")
bonus_page.adicionar_produto("123")
bonus_page.clicar_avancar_carrinho()

# 2. Verificar e usar bonus
if bonus_page.bonus_disponivel():
    valor_bonus = bonus_page.obter_valor_bonus()
    print(f"Bonus disponível: {valor_bonus}")

    bonus_page.ativar_bonus()

    if bonus_page.bonus_foi_aplicado():
        print("Bonus aplicado com sucesso!")

# 3. Finalizar
bonus_page.clicar_avancar_pagamento()
venda_page.finalizar_venda()
bonus_page.responder_impressao(imprimir=False)
```

---

## 🔍 ConsultaPedidoPage

### Responsabilidade
Consulta de pedidos gerados.

### Métodos Principais

```python
# Filtros
abrir_menu_lateral()
garantir_flag_ativa(nome_flag)

# Seleção
selecionar_primeiro_pedido()

# Fluxo
executar_consulta_e_finalizar_pedido()

# Tratamento
tratar_popup_bonus()
responder_impressao(imprimir=False)
```

---

## 📅 VendaFuturaPage

### Responsabilidade
Vendas futuras com entrega domicílio ou retirada loja.

### Métodos Principais

```python
# Entrega
selecionar_retirada_loja()
selecionar_entrega_domicilio()

# Cliente
buscar_cliente_cpf(cpf="12345678900")

# Produto
adicionar_produto_com_tamanho(codigo, tamanho)

# Pagamento
selecionar_pagamento_avista()
selecionar_forma_dinheiro()

# Fluxos Completos
executar_venda_futura(id_cliente, codigo_produto, codigo_tamanho)
executar_venda_futura_domicilio(cpf_cliente, codigo_produto, tamanho)

# Validações
venda_sucesso_exibida(timeout=15)
validar_sucesso_e_concluir()
```

---

## 🏗️ Estrutura Padrão de um Page Object

```python
"""
NomePage - Page Object para tela de [funcionalidade].
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle

class NomePage(BasePage):
    """Page Object para [funcionalidade]."""

    # ========== LOCATORS ==========
    BTN_EXEMPLO = "btn_exemplo_id"
    TXT_TITULO = "Título da Tela"
    EDT_CAMPO = "edt_campo_id"

    # ========== ACOES ==========
    def metodo_acao(self, parametro: str):
        """Descrição da ação."""
        logger.info(f"{LogStyle.ACAO} Executando ação: {LogStyle.valor(parametro)}")
        self.clicar_por_id(self.BTN_EXEMPLO)
        self.digitar_por_id(self.EDT_CAMPO, parametro)

    # ========== VALIDACOES ==========
    def metodo_validacao(self, timeout: int = 10) -> bool:
        """Valida se condição é verdadeira."""
        return self.texto_exibido(self.TXT_TITULO, timeout)

    # ========== FLUXOS COMPLETOS ==========
    def executar_fluxo_completo(self, param1: str, param2: str):
        """Executa fluxo completo da funcionalidade."""
        logger.info(f"{LogStyle.secao('FLUXO COMPLETO - Nome')}")

        self.metodo_acao(param1)
        self.outro_metodo(param2)

        if not self.metodo_validacao():
            raise Exception("Validação falhou!")

        logger.info(f"{LogStyle.secao('FLUXO COMPLETO - Nome ✅')}")
```

---

## 🎓 Boas Práticas

### Organização

- ✅ **Locators no topo** da classe
- ✅ **Métodos agrupados** por categoria (ações, validações, fluxos)
- ✅ **Nomenclatura clara** e descritiva
- ✅ **Docstrings** em todos os métodos

### Métodos

- ✅ **Um método = uma responsabilidade**
- ✅ **Parâmetros com valores padrão** quando possível
- ✅ **Retornar valores úteis** (bool para validações, str para extração)
- ✅ **Logar ações importantes**

### Validações

- ✅ **Sempre retornar bool**
- ✅ **Timeout configurável**
- ✅ **Mensagens de erro claras**

### Fluxos

- ✅ **Métodos auxiliares separados**
- ✅ **Log início e fim do fluxo**
- ✅ **Tratamento de erros**

---

**Última atualização**: 10/04/2026
**Versão**: 2.0.108 — 17 Page Objects
