"""
Test Troca Consumidor - Teste de troca/devolução para consumidor.

IMPORTANTE: Este teste DEPENDE de test_venda_consumidor_sucesso rodar ANTES.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.troca_page import TrocaPage


@allure.epic("PDV Mobile")
@allure.feature("Trocas e Devoluções")
@allure.story("Troca para Consumidor")
class TestTrocaConsumidor:
    """Testes de troca para consumidor (com venda pos-troca)."""

    @allure.title("Troca Consumidor - Devolução com Venda Bônus")
    @allure.description("""
Cenario: Realizar troca de produto para consumidor com venda usando bonus

Pre-condicoes:
- Usuario logado no sistema
- Venda recente para consumidor (criada por test_venda_consumidor_sucesso)

Dado que estou na tela inicial do PDV
Quando acesso o menu "Realizar Troca"
E seleciono o vendedor
E defino o periodo de busca
E consulto as notas fiscais
E seleciono uma nota e marco item para devolucao
E confirmo a troca (app inicia nova venda automaticamente com bonus)
E pago com o bonus da troca
E finalizo a venda
Entao a troca e venda sao realizadas com sucesso
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("troca", "consumidor", "bonus", "devolução")
    def test_troca_consumidor_sucesso(self, driver_logado):
        """
        Cenario: Realizar troca de produto para consumidor
        Dado que estou logado no app
        Quando inicio uma troca
        E seleciono uma nota fiscal
        E marco um item para devolucao
        E realizo uma venda com o bonus da troca
        Entao a troca e venda sao realizadas com sucesso
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_troca = TrocaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Realizar Troca'"):
            pagina_inicial.iniciar_troca()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Executar fluxo de troca consumidor (com venda bônus)"):
            pagina_troca.executar_troca_consumidor()

        # Assert
        with allure.step("4. Verificar retorno à tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
