"""Test Histórico Cliente - Regressão: consulta de histórico."""
import pytest
import allure
from pages.historico_cliente_page import HistoricoClientePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Histórico Cliente")
@allure.story("Consulta de Histórico")
class TestHistoricoClienteRegressao:
    """Regressão: histórico de compras do cliente."""

    @allure.title("REG: Consultar Histórico de Cliente")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "historico", "cliente")
    @pytest.mark.regression
    def test_consultar_historico_cliente(self, driver_logado):
        """Histórico carregado com dados do cliente."""
        historico_page = HistoricoClientePage(driver_logado)
        codigo_cliente = test_data.CUSTOMER_ID

        with allure.step("1. Navegar ate Histórico Cliente"):
            historico_page.navegar_ate_historico_cliente()

        with allure.step(f"2. Selecionar cliente {codigo_cliente}"):
            historico_page.selecionar_cliente(codigo_cliente)

        with allure.step("3. Validar histórico"):
            dados = historico_page.validar_resumo_historico()
            assert historico_page.historico_carregado_com_sucesso(), \
                "Histórico nao carregado"
            allure.attach(str(dados), name=f"Histórico {codigo_cliente}",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("4. Voltar"):
            historico_page.voltar_tela_anterior()
