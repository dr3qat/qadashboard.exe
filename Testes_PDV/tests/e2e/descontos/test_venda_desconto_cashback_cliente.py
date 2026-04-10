"""
Test Venda Desconto Cashback Cliente - Venda cliente com cashback + desconto R$ 10,00.

Pre-requisito:
- Cliente deve ter cashback disponivel
- Produto deve suportar 3 unidades
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Venda com Desconto e Cashback")
class TestVendaDescontoCashbackCliente:

    @allure.title("Venda Cliente - Cashback + Desconto R$ 10,00 Dinheiro")
    @allure.description("""
Cenario: Venda cliente com cashback ativado via flag + desconto em reais

Pre-condicoes:
- Usuario logado no sistema
- Cliente com cashback disponivel
- Produto cadastrado no sistema

Fluxo:
1. Adiciona produto + btn_increase x2 (total 3 itens)
2. Avanca para seleção de pagamento
3. Marca flag cashback (switch_cashback)
4. Seleciona DINHEIRO, avanca, skip todos dialogs
5. Aplica desconto R$ 10,00 (textView127 area, XPath[2])
6. Scroll para btnFinalizar e finaliza
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda", "cliente", "desconto", "cashback", "dinheiro")
    def test_venda_desconto_cashback_cliente(self, driver_logado):
        """Venda cliente: 3 itens + cashback flag + desconto R$ 10,00."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        with allure.step("1. Acessar Iniciar Venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Venda cliente: 3 itens + cashback + desconto R$ 10,00"):
            pagina_venda.executar_venda_cliente_desconto_cashback(
                id_cliente=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_SALE,
                desconto="10,00",
                quantidade_extra=2
            )

        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
