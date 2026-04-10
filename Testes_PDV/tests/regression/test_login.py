"""Test Login - Regressão: garantir acesso ao sistema."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Autenticação")
@allure.story("Login")
class TestLoginRegressao:
    """Regressão: login e sessão ativa."""

    @allure.title("REG: Login - Garantir acesso ao sistema")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("regression", "login", "critico")
    @pytest.mark.regression
    def test_garantir_login(self, driver):
        """Dado o app instalado, quando faço login, então estou na tela inicial."""
        pagina_login = LoginPage(driver)
        pagina_inicial = HomePage(driver)

        with allure.step("Garantir login"):
            pagina_login.garantir_login(
                ip=test_data.SERVER_IP,
                porta=test_data.SERVER_PORT,
                empresa=test_data.COMPANY,
                usuario=test_data.USER,
                senha=test_data.PASSWORD
            )

        with allure.step("Verificar tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(timeout=30), \
                "Tela inicial nao exibida apos login"
