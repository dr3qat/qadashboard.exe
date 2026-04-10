"""Smoke 11 - Documentos fiscais tela acessivel e consulta executa."""
import time
import pytest
import allure
from pages.documentos_page import DocumentosPage
from pages.home_page import HomePage
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Documentos")
@pytest.mark.smoke
class TestSmoke11Documentos:

    @allure.title("SMOKE 11/11: Documentos - tela abre e consulta executa")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "documentos", "fiscal")
    def test_11_documentos_tela_e_consulta(self, driver_logado):
        """
        Valida que modulo documentos abre, aceita periodo e executa consulta.
        Nao valida conteudo da lista (dia pode nao ter documentos).
        """
        pagina_inicial = HomePage(driver_logado)
        documentos = DocumentosPage(driver_logado)

        with allure.step("1. Acessar menu Documentos"):
            documentos.clicar_menu_documentos()

        with allure.step("2. Preencher periodo (data atual)"):
            if 'playstore' not in (documentos.app_package or '').lower():
                documentos.rolar_até_encontrar_texto()
            documentos.preencher_data_inicial_com()
            documentos.preencher_data_final_com()
            documentos.fechar_teclado()

        with allure.step("3. Executar consulta"):
            documentos.clicar_botão_consultar()
            time.sleep(3)  # Aguarda resposta servidor

        with allure.step("4. Voltar para tela inicial"):
            documentos.voltar_tela_documentos()
            documentos.voltar_tela_documentos()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial apos fechar documentos"

        logger.info("[SMOKE 11/11] Documentos tela e consulta OK")
