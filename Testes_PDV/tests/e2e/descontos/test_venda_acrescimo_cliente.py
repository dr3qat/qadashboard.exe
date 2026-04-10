"""
Test Venda Acrescimo Cliente - Venda cliente com acrescimo de R$ 10,00.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Venda com Acrescimo")
class TestVendaAcrescimoCliente:

    @allure.title("Venda Acrescimo Cliente - R$ 10,00 Dinheiro")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda", "cliente", "acrescimo", "dinheiro")
    def test_venda_acrescimo_cliente(self, driver_logado):
        """Venda cliente com acrescimo R$ 10,00 — valida restante zerado antes de finalizar."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        with allure.step("1. Acessar Iniciar Venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Venda cliente + acrescimo R$ 10,00 + DINHEIRO"):
            pagina_venda.executar_venda_cliente_com_acrescimo(
                id_cliente=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_SALE,
                acrescimo="10,00"
            )

        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
