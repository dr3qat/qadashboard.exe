"""Test Troca Sem Resultado - Cenario negativo: data sem movimentacao."""
import time
import pytest
import allure
from pages.home_page import HomePage
from pages.troca_page import TrocaPage


@allure.epic("PDV Mobile")
@allure.feature("Trocas e Devoluções")
@allure.story("Troca Negativa")
class TestTrocaSemResultado:
    """Testa comportamento da tela de troca quando nao ha notas no periodo."""

    @allure.title("Troca - Data sem movimentacao nao exibe notas")
    @allure.description("""
Cenario: Busca de troca em periodo sem movimentacao

Pre-condicoes:
- Usuario logado
- Data futura (sem transacoes)

Dado que estou na tela de troca
Quando consulto um periodo sem movimentacao (data futura)
Entao nao devo ver lista de notas fiscais
E devo poder voltar para a tela inicial sem erro
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("troca", "negativo", "data-invalida")
    def test_troca_data_futura_sem_notas(self, driver_logado):
        """
        Cenario: Data futura → lista de notas vazia ou erro esperado.
        Usa data 01/01/2030 (definitivamente sem transacoes).
        """
        pagina_inicial = HomePage(driver_logado)
        pagina_troca = TrocaPage(driver_logado)

        DATA_SEM_MOVIMENTO = "01/01/2030"

        with allure.step("1. Acessar modulo Realizar Troca"):
            pagina_inicial.iniciar_troca()
            pagina_inicial.selecionar_vendedor()

        with allure.step(f"2. Definir data futura sem movimento ({DATA_SEM_MOVIMENTO})"):
            pagina_troca.definir_data_inicial(DATA_SEM_MOVIMENTO)

        with allure.step("3. Clicar Consultar (sem aguardar lista)"):
            pagina_troca.fechar_teclado()
            pagina_troca.ver_e_clicar(TrocaPage.BTN_CONSULTAR)
            time.sleep(8)  # Aguarda resposta do servidor para data sem dados

        with allure.step("4. Verificar que lista de notas NAO foi carregada"):
            lista_exibida = pagina_troca.elemento_existe(
                TrocaPage.ITEM_LISTA_NOTAS, tempo_espera=3
            )
            assert not lista_exibida, \
                "Lista de notas apareceu para data futura - comportamento inesperado"

        with allure.step("5. Voltar para tela inicial"):
            pagina_troca.voltar_com_confirmacao()

        with allure.step("6. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial apos troca sem resultado"
