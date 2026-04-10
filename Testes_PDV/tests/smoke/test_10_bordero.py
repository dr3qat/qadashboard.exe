"""Smoke 10 - Bordero acessivel e relatorio processado."""
import pytest
import allure
from pages.bordero_page import BorderoPage
from pages.home_page import HomePage
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Bordero")
@pytest.mark.smoke
class TestSmoke10Bordero:

    @allure.title("SMOKE 10/11: Bordero - tela abre e relatorio processado")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "bordero", "relatorio")
    def test_10_bordero_tela_e_geracao(self, driver_logado):
        """
        Valida que modulo bordero abre, aceita data e processa relatorio.
        Nao assertamos conteudo dos dados (dia pode nao ter movimentacao).
        """
        pagina_inicial = HomePage(driver_logado)
        bordero = BorderoPage(driver_logado)

        with allure.step("1. Navegar ate Bordero"):
            bordero.navegar_ate_bordero()

        with allure.step("2. Inserir data atual"):
            bordero.inserir_data_inicial()

        with allure.step("3. Gerar bordero"):
            bordero.gerar_bordero()

        with allure.step("4. Verificar que tela de resultado carregou"):
            dados = bordero.validar_dados_bordero()
            assert dados is not None, "validar_dados_bordero retornou None"

        logger.info("[SMOKE 10/11] Bordero tela e geracao OK")
