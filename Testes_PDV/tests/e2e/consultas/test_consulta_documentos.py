"""
Consulta Documentos - Filtro por Período - Teste de consulta de documentos fiscais.
"""
import time
import pytest
import allure
from pages.documentos_page import DocumentosPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Consultas")
@allure.story("Consulta de Documentos Fiscais")
class TestConsultaDocumentos:
    """Testes de consulta de documentos fiscais."""

    @allure.title("Consulta Documentos - Filtro por Período")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("consulta", "documentos", "nf")
    def test_consulta_documentos_sucesso(self, driver_logado):
        """
        Cenario: Consulta de Documentos Fiscais
        Dado que estou logado no app
        Quando acesso documentos, filtro por periodo e abro o primeiro doc
        Entao consigo ver os detalhes do documento
        """
        driver = driver_logado
        pagina_documentos = DocumentosPage(driver)

        with allure.step("1. Acessar Documentos e preencher período"):
            pagina_documentos.clicar_menu_documentos()
            if 'playstore' not in (pagina_documentos.app_package or '').lower():
                pagina_documentos.rolar_até_encontrar_texto()
            pagina_documentos.preencher_data_inicial_com()
            pagina_documentos.fechar_teclado()
            pagina_documentos.preencher_data_final_com()
            pagina_documentos.fechar_teclado()
            pagina_documentos.clicar_botão_consultar()
            pagina_documentos.aguardar_resultado_consulta()

        with allure.step("2. Clicar no primeiro documento da lista"):
            pagina_documentos.clicar_primeiro_documento()
            time.sleep(0.5)

        with allure.step("3. Clicar em Detalhes (1ª opção do bottom sheet)"):
            pagina_documentos.clicar_detalhes_documento()

        with allure.step("4. Aguardar dados do documento carregarem"):
            assert pagina_documentos.elemento_existe("txtCliente", tempo_espera=10) or \
                   pagina_documentos.texto_exibido("Detalhes Documento", tempo_espera=10), \
                   "Tela Detalhes Documento não carregou"

        with allure.step("5. Voltar para home"):
            pagina_documentos.voltar_tela_documentos()
            time.sleep(0.2)
            pagina_documentos.voltar_tela_documentos()
            time.sleep(0.2)
            pagina_documentos.voltar_tela_documentos()
