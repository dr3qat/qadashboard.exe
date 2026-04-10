"""
Test Venda Desconto Cliente - Venda cliente com desconto de R$ 10,00.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Venda com Desconto")
class TestVendaDescontoCliente:

    @allure.title("Venda Desconto Cliente - R$ 10,00 Dinheiro")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda", "cliente", "desconto", "dinheiro")
    def test_venda_desconto_cliente(self, driver_logado):
        """Venda cliente com desconto R$ 10,00 — valida restante zerado antes de finalizar."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        with allure.step("1. Acessar Iniciar Venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Venda cliente + desconto R$ 10,00 + DINHEIRO"):
            pagina_venda.executar_venda_cliente_com_desconto(
                id_cliente=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_SALE,
                desconto="10,00"
            )

        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
