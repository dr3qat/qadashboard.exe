"""Test Login Invalido - Cenarios negativos de autenticacao."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Autenticação")
@allure.story("Login Negativo")
class TestLoginInvalido:
    """Testes de login com credenciais invalidas."""

    @allure.title("Login - Senha invalida nao acessa o sistema")
    @allure.description("""
Cenario: Tentativa de login com senha incorreta deve ser bloqueada

Pre-condicoes:
- App recém iniciado (driver fixture = forceAppLaunch)
- Servidor acessivel

Dado que estou na tela de login
Quando informo senha incorreta
Entao nao devo ser direcionado a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("login", "negativo", "seguranca")
    def test_login_falha_senha_invalida(self, driver_limpo):
        """
        Cenario: Senha invalida nao deve conceder acesso.
        Nome do metodo obrigatorio (ORDEM_TESTES no conftest).
        """
        pagina_login = LoginPage(driver_limpo)
        pagina_inicial = HomePage(driver_limpo)

        with allure.step("1. Preparar tela de login"):
            pagina_login.pular_telas_introducao()
            pagina_login.configurar_conexao_se_necessario(
                test_data.SERVER_IP, test_data.SERVER_PORT
            )

        with allure.step("2. Preencher credenciais com senha invalida"):
            pagina_login.preencher_credenciais(
                empresa=test_data.COMPANY,
                usuario=test_data.USER,
                senha="SENHA_INVALIDA_QA_999"
            )

        with allure.step("3. Tentar entrar"):
            pagina_login.clicar_entrar()

        with allure.step("4. Verificar que NAO chegou na tela inicial"):
            chegou_na_home = pagina_inicial.tela_inicial_exibida(timeout=10)
            assert not chegou_na_home, \
                "FALHA DE SEGURANCA: app aceitou senha invalida e acessou tela inicial"

    @allure.title("Login - Empresa invalida nao acessa o sistema")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("login", "negativo")
    def test_login_empresa_invalida_nao_entra(self, driver_limpo):
        """
        Cenario: Empresa inexistente nao deve conceder acesso.
        """
        pagina_login = LoginPage(driver_limpo)
        pagina_inicial = HomePage(driver_limpo)

        with allure.step("1. Preparar tela de login"):
            pagina_login.pular_telas_introducao()
            pagina_login.configurar_conexao_se_necessario(
                test_data.SERVER_IP, test_data.SERVER_PORT
            )

        with allure.step("2. Preencher com empresa inexistente"):
            pagina_login.preencher_credenciais(
                empresa="EMPRESA_INEXISTENTE_00000",
                usuario=test_data.USER,
                senha=test_data.PASSWORD
            )

        with allure.step("3. Tentar entrar"):
            pagina_login.clicar_entrar()

        with allure.step("4. Verificar que NAO chegou na tela inicial"):
            chegou_na_home = pagina_inicial.tela_inicial_exibida(timeout=10)
            assert not chegou_na_home, \
                "App aceitou empresa invalida e acessou tela inicial"
