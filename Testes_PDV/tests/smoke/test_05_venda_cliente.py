"""Smoke 05 - Venda cliente cadastrado fluxo completo."""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Venda")
@pytest.mark.smoke
class TestSmoke05VendaCliente:

    @allure.title("SMOKE 5/7: Venda cliente - fluxo completo")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "venda", "cliente")
    def test_05_venda_cliente_completa(self, driver_logado):
        """
        Fluxo completo de venda para cliente cadastrado:
        Iniciar Venda → vendedor → buscar cliente → produto → DINHEIRO → finalizar → home.
        """
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        with allure.step("1. Iniciar venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Executar fluxo cliente (busca + produto + dinheiro + finalizar)"):
            pagina_venda.executar_venda_cliente(
                id_cliente=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_SALE
            )

        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial apos venda cliente"

        logger.info("[SMOKE 5/7] Venda cliente OK")
