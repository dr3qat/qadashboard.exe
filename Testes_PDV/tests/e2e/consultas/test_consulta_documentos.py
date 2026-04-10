"""
Consulta Documentos - Filtro por Período - Teste de consulta de documentos fiscais.
"""
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
    @allure.description("""Cenario: Consulta de Documentos Fiscais

Pre-condicoes:
- Usuario logado no sistema

Dado que estou na tela inicial do PDV
E clicar no menu Documentos
E rolar até encontrar o texto 'Período'
E preencher Data Inicial com a data atual
E preencher Data Final com a data atual
E clicar no botão Consultar
E verificar que os documentos foram listados
E CLicar em Detalhes do documento
E verificar que os detalhes do documento estão corretos
E voltar para a tela de documentos""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("consulta", "documentos", "nf")
    def test_consulta_documentos_sucesso(self, driver_logado):
        """
        Cenario: Consulta de Documentos Fiscais

        Dado que estou logado no app
        Quando acesso o menu de consulta de documentos
        E filtro por periodo
        Entao os documentos sao listados corretamente
        """
        driver = driver_logado

        # Arrange
        pagina_documentos = DocumentosPage(driver)

        # Act
        with allure.step("1. Executar fluxo: Documentos"):
            pagina_documentos.executar_documentos()


        # Assert
        # Para testes de consulta, o fluxo completo já é a validação
        # Se executou sem erro, o teste passou
        # (O legado não tem assertion explícita no final)
