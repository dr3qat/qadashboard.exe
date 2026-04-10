"""Smoke 02 - Login com credenciais validas."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from test_data import test_data
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Login")
@pytest.mark.smoke
class TestSmoke02Login:

    @allure.title("SMOKE 2/7: Login funciona")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "login")
    def test_02_login(self, driver):
        """Login com credenciais validas leva a tela inicial."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        login_page.garantir_login(
            ip=test_data.SERVER_IP,
            porta=test_data.SERVER_PORT,
            empresa=test_data.COMPANY,
            usuario=test_data.USER,
            senha=test_data.PASSWORD
        )

        assert home_page.tela_inicial_exibida(timeout=30), \
            "Tela inicial nao apareceu apos login"
        logger.info("[SMOKE 2/7] Login OK")
