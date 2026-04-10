"""
Test Venda Desconto Bonus Cliente - Venda cliente com desconto R$ 10,00 + bônus cashback.

Pre-requisito:
- Cliente deve ter bonus disponivel (gerado por troca anterior)
- Produto deve suportar 3 unidades
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Venda com Desconto e Bonus")
class TestVendaDescontoBonusCliente:

    @allure.title("Venda Cliente - Desconto R$ 10,00 + Bonus Cashback")
    @allure.description("""
Cenario: Venda cliente com desconto em reais + bonus cashback

Pre-condicoes:
- Usuario logado no sistema
- Cliente com bonus disponivel
- Produto cadastrado no sistema

Fluxo:
1. Adiciona produto + btn_increase x2 (total 3 itens)
2. Avanca para pagamento
3. Seleciona DINHEIRO, avanca, skip todos dialogs
4. Exclui pagamento DINHEIRO (imageView12 -> Excluir pagamento)
5. Aplica desconto R$ 10,00 (textView127 area, XPath[2])
6. Aplica bonus cashback (imageView19 -> Bonus -> ck_discount[1] -> Aplicar)
7. Adiciona DINHEIRO via btn_adiciona_pagamento -> btn_pagar
8. Scroll para btnFinalizar e finaliza
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda", "cliente", "desconto", "bonus", "cashback", "dinheiro")
    def test_venda_desconto_bonus_cliente(self, driver_logado):
        """Venda cliente: 3 itens + desconto R$ 10,00 + bonus cashback."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        with allure.step("1. Acessar Iniciar Venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Venda cliente: 3 itens + desconto R$ 10,00 + bonus"):
            pagina_venda.executar_venda_cliente_desconto_bonus(
                id_cliente=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_SALE,
                desconto="10,00",
                quantidade_extra=2
            )

        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
