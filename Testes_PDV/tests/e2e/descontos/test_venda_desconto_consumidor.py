"""
Test Venda Desconto Consumidor - Venda consumidor com desconto de R$ 10,00.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Venda com Desconto")
class TestVendaDescontoConsumidor:

    @allure.title("Venda Desconto Consumidor - R$ 10,00 Dinheiro")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda", "consumidor", "desconto", "dinheiro")
    def test_venda_desconto_consumidor(self, driver_logado):
        """Venda consumidor com desconto R$ 10,00 — valida restante zerado antes de finalizar."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        with allure.step("1. Acessar Iniciar Venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Venda consumidor + desconto R$ 10,00 + DINHEIRO"):
            pagina_venda.executar_venda_consumidor_com_desconto(
                codigo_produto=test_data.PRODUCT_CODE_SALE,
                desconto="10,00"
            )

        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
