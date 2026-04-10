"""Smoke 08 - Pedido de venda consumidor fluxo basico."""
import pytest
import allure
from pages.home_page import HomePage
from pages.pedido_page import PedidoPage
from test_data import test_data
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Pedido")
@pytest.mark.smoke
class TestSmoke08Pedido:

    @allure.title("SMOKE 8/11: Pedido venda consumidor - fluxo basico")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "pedido", "consumidor")
    def test_08_pedido_consumidor(self, driver_logado):
        """Pedido consumidor: acessa modulo + cria pedido + confirma pedido gerado."""
        pagina_inicial = HomePage(driver_logado)
        pagina_pedido = PedidoPage(driver_logado)

        with allure.step("1. Acessar modulo Pedido Venda"):
            pagina_inicial.rolar_ate_texto("Pedido Venda", max_scrolls=3)
            pagina_inicial.clicar_por_texto("Pedido Venda")

        with allure.step("2. Executar pedido consumidor"):
            pagina_pedido.executar_pedido_venda_consumidor(
                codigo_produto=test_data.PRODUCT_CODE_SALE
            )

        with allure.step("3. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial apos pedido consumidor"

        logger.info("[SMOKE 8/11] Pedido consumidor OK")
