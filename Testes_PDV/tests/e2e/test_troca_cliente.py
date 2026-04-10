"""
Test Troca Cliente - Teste de troca/devolução para cliente.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.troca_page import TrocaPage


@allure.epic("PDV Mobile")
@allure.feature("Trocas e Devoluções")
@allure.story("Troca para Cliente")
class TestTrocaCliente:
    """Testes de troca para cliente cadastrado."""

    @allure.title("Troca Cliente - Devolução de Produto")
    @allure.description("""
Cenario: Realizar troca de produto para cliente cadastrado (apenas devolução)

Pre-condicoes:
- Usuario logado no sistema
- Venda recente para o cliente (nota fiscal disponivel)

Dado que estou na tela inicial do PDV
Quando acesso o menu "Realizar Troca"
E seleciono o vendedor
E defino o periodo de busca
E consulto as notas fiscais
E seleciono uma nota e marco item para devolucao
E confirmo a troca
Entao a troca e realizada com sucesso (popup "Sucesso!")
E retorno a tela inicial (sem venda pos-troca)
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("troca", "cliente", "devolução")
    def test_troca_cliente_sucesso(self, driver_logado):
        """
        Cenário: Realizar troca de produto para cliente (apenas devolução)
        Dado que estou logado no app
        Quando inicio uma troca
        E seleciono uma nota fiscal
        E marco um item para devolução
        Então a troca é realizada com sucesso (popup "Sucesso!")
        E retorno à tela inicial (sem venda pós-troca)
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

        with allure.step("3. Executar fluxo de troca (devolução)"):
            pagina_troca.executar_troca()

        # Assert
        with allure.step("4. Verificar retorno à tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
