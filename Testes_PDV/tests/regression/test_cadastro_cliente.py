"""Test Cadastro Cliente - Regressão: cadastro PF e PJ."""
import pytest
import allure
from pages.cliente_page import ClientePage


@allure.epic("PDV Mobile")
@allure.feature("Cadastro de Cliente")
@allure.story("Cadastro de Pessoa Física")
class TestCadastroPFRegressao:
    """Regressão: cadastro de Pessoa Física."""

    @allure.title("REG: Cadastrar Pessoa Física")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "cadastro", "pf")
    @pytest.mark.regression
    def test_cadastrar_pessoa_fisica(self, driver_logado):
        """PF cadastrada com sucesso e mensagem de confirmação exibida."""
        cliente_page = ClientePage(driver_logado)

        with allure.step("1. Navegar ate Novo Cadastro"):
            cliente_page.navegar_novo_cadastro()

        with allure.step("2. Cadastrar PF"):
            dados = cliente_page.cadastrar_cliente_completo(tipo_pessoa="PF")
            allure.attach(str(dados), name="Dados PF", attachment_type=allure.attachment_type.TEXT)

        with allure.step("3. Verificar sucesso"):
            assert cliente_page.cadastro_concluido_com_sucesso(), \
                "Cadastro PF nao concluido"


@allure.epic("PDV Mobile")
@allure.feature("Cadastro de Cliente")
@allure.story("Cadastro de Pessoa Jurídica")
class TestCadastroPJRegressao:
    """Regressão: cadastro de Pessoa Jurídica."""

    @allure.title("REG: Cadastrar Pessoa Jurídica")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "cadastro", "pj")
    @pytest.mark.regression
    def test_cadastrar_pessoa_juridica(self, driver_logado):
        """PJ cadastrada com sucesso e mensagem de confirmação exibida."""
        cliente_page = ClientePage(driver_logado)

        with allure.step("1. Navegar ate Novo Cadastro"):
            cliente_page.navegar_novo_cadastro()

        with allure.step("2. Cadastrar PJ"):
            dados = cliente_page.cadastrar_cliente_completo(tipo_pessoa="PJ")
            allure.attach(str(dados), name="Dados PJ", attachment_type=allure.attachment_type.TEXT)

        with allure.step("3. Verificar sucesso"):
            assert cliente_page.cadastro_concluido_com_sucesso(), \
                "Cadastro PJ nao concluido"
