"""Test Borderô - Regressão: geração de borderô."""
import pytest
import allure
from pages.bordero_page import BorderoPage


@allure.epic("PDV Mobile")
@allure.feature("Borderô")
@allure.story("Geração de Borderô")
class TestBorderoRegressao:
    """Regressão: borderô do dia atual."""

    @allure.title("REG: Gerar Borderô - Data Atual")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "bordero", "relatorio")
    @pytest.mark.regression
    def test_gerar_bordero_data_atual(self, driver_logado):
        """Borderô do dia gerado e dados carregados corretamente."""
        bordero_page = BorderoPage(driver_logado)

        with allure.step("1. Navegar ate Borderô"):
            bordero_page.navegar_ate_bordero()

        with allure.step("2. Inserir data atual"):
            bordero_page.inserir_data_inicial()

        with allure.step("3. Gerar borderô"):
            bordero_page.gerar_bordero()

        with allure.step("4. Validar dados"):
            dados_bordero = bordero_page.validar_dados_bordero()
            assert bordero_page.bordero_gerado_com_sucesso(dados_bordero), \
                "Borderô nao gerado ou dados nao carregados"
            allure.attach(str(dados_bordero), name="Dados do Borderô",
                          attachment_type=allure.attachment_type.TEXT)
