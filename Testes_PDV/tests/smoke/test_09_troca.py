"""Smoke 09 - Tela de troca acessivel e formulario carrega."""
import pytest
import allure
from pages.home_page import HomePage
from pages.troca_page import TrocaPage
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Troca")
@pytest.mark.smoke
class TestSmoke09Troca:

    @allure.title("SMOKE 9/11: Troca - tela acessivel e formulario carrega")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "troca", "navegacao")
    def test_09_troca_tela_acessivel(self, driver_logado):
        """
        Valida que modulo troca abre, campo data e botao consultar estao presentes.
        Nao executa troca completa (depende de dados). Apenas health-check do modulo.
        """
        pagina_inicial = HomePage(driver_logado)
        pagina_troca = TrocaPage(driver_logado)

        with allure.step("1. Acessar modulo Realizar Troca"):
            pagina_inicial.iniciar_troca()
            pagina_inicial.selecionar_vendedor()

        with allure.step("2. Verificar que campo data inicial esta presente"):
            assert pagina_troca.elemento_existe(TrocaPage.INPUT_DATA_INICIAL, tempo_espera=10), \
                "Campo data inicial nao encontrado na tela de troca"

        with allure.step("3. Verificar que botao Consultar esta presente"):
            assert pagina_troca.elemento_existe(TrocaPage.BTN_CONSULTAR, tempo_espera=5), \
                "Botao Consultar nao encontrado na tela de troca"

        with allure.step("4. Voltar para tela inicial"):
            pagina_troca.voltar_com_confirmacao()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial apos fechar troca"

        logger.info("[SMOKE 9/11] Tela troca acessivel OK")
