"""
Test Login - Testes de autenticacao.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Autenticação")
@allure.story("Login e Sessão")
class TestLogin:
    """Testes de login no aplicativo."""

    @allure.title("Login - Garantir Acesso ao Sistema")
    @allure.description("""
Cenario: Garantir que o usuario esta logado no sistema

Pre-condicoes:
- App instalado no dispositivo
- Servidor Appium ativo

Dado que o app esta instalado no dispositivo
Quando verifico o estado de configuracao do app
E configuro o servidor se necessario
E realizo login com credenciais validas
Entao devo estar logado e ver a tela inicial
""")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("login", "autenticação", "crítico")
    def test_garantir_login(self, driver):
        """
        Cenario: Garantir que o usuario esta logado
        Dado que o app esta instalado
        Quando verifico o estado de login
        Entao devo estar logado (faz login se necessario)
        """
        # Arrange
        pagina_login = LoginPage(driver)
        pagina_inicial = HomePage(driver)

        # Act
        with allure.step("Garantir login (executa se necessario)"):
            pagina_login.garantir_login(
                ip=test_data.SERVER_IP,
                porta=test_data.SERVER_PORT,
                empresa=test_data.COMPANY,
                usuario=test_data.USER,
                senha=test_data.PASSWORD
            )

        # Assert
        with allure.step("Verificar se esta na tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(timeout=30), \
                "Tela inicial nao foi exibida apos login"

    @allure.title("Verificar se ja esta logado")
    @allure.severity(allure.severity_level.NORMAL)
    def test_verificar_sessao_ativa(self, driver):
        """
        Cenario: Verificar sessao ativa
        Dado que ja fiz login anteriormente
        Quando abro o app
        Entao devo estar na tela inicial (ou login)
        """
        pagina_login = LoginPage(driver)
        pagina_inicial = HomePage(driver)

        # Garante login primeiro
        pagina_login.garantir_login(
            ip=test_data.SERVER_IP,
            porta=test_data.SERVER_PORT,
            empresa=test_data.COMPANY,
            usuario=test_data.USER,
            senha=test_data.PASSWORD
        )

        # Verifica estado atual
        if pagina_inicial.tela_inicial_exibida(timeout=5):
            allure.attach("Usuario logado com sucesso", name="Status", attachment_type=allure.attachment_type.TEXT)
            assert True
        else:
            allure.attach("Falha no login", name="Status", attachment_type=allure.attachment_type.TEXT)
            assert False, "Usuario nao esta logado"
