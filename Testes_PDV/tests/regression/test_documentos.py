"""Test Documentos - Regressão: consulta de documentos fiscais."""
import pytest
import allure
from pages.documentos_page import DocumentosPage


@allure.epic("PDV Mobile")
@allure.feature("Consultas")
@allure.story("Consulta de Documentos Fiscais")
class TestDocumentosRegressao:
    """Regressão: consulta de documentos fiscais por período."""

    @allure.title("REG: Consulta Documentos - Filtro por Período")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "documentos", "consulta")
    @pytest.mark.regression
    def test_consulta_documentos_sucesso(self, driver_logado):
        """Documentos fiscais consultados sem erro no fluxo completo."""
        pagina_documentos = DocumentosPage(driver_logado)

        with allure.step("1. Executar fluxo consulta documentos"):
            pagina_documentos.executar_documentos()
