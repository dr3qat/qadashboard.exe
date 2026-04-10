"""Smoke 07 - Cancelar venda vazia, navegacao de saida funciona."""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Cancelamento")
@pytest.mark.smoke
class TestSmoke07CancelarVenda:

    @allure.title("SMOKE 7/7: Cancelar venda vazia - navegacao funciona")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "cancelamento", "navegacao")
    def test_07_cancelar_venda_vazia(self, driver_logado):
        """
        Abre tela de venda sem adicionar produtos e volta para home.
        Valida que a navegacao de saida funciona.
        """
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        with allure.step("1. Iniciar venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Entrar no carrinho sem cliente"):
            pagina_venda.iniciar_venda_sem_cliente()

        with allure.step("4. Voltar sem adicionar produtos"):
            pagina_venda.voltar_tela(confirmar=True)

        with allure.step("5. Verificar retorno a tela inicial"):
            if not pagina_inicial.tela_inicial_exibida(timeout=5):
                pagina_venda.voltar_tela(confirmar=True)
            assert pagina_inicial.tela_inicial_exibida(timeout=10), \
                "Nao voltou para tela inicial apos cancelar venda"

        logger.info("[SMOKE 7/7] Cancelar venda OK")
