"""Smoke 03 - Modulos principais visiveis na home."""
import pytest
import allure
from pages.home_page import HomePage
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Home")
@pytest.mark.smoke
class TestSmoke03HomeModulos:

    @allure.title("SMOKE 3/7: Modulos principais visiveis na home")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "home")
    def test_03_home_modulos_visiveis(self, driver_logado):
        """Tela inicial exibe pelo menos o botao de Venda."""
        home_page = HomePage(driver_logado)

        venda_visivel = (
            home_page.texto_exibido("Venda", tempo_espera=5) or
            home_page.texto_exibido("Iniciar Venda", tempo_espera=3)
        )

        assert venda_visivel, \
            "Botao de Venda nao encontrado na home - app em estado invalido"
        logger.info("[SMOKE 3/7] Modulos visiveis na home")
