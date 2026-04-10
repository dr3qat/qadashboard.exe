"""
Test Venda Consumidor - Teste de venda para consumidor (sem cliente).
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Venda para Consumidor")
class TestVendaConsumidor:
    """Testes de venda para consumidor (sem cliente cadastrado)."""

    @allure.title("Venda Consumidor - Pagamento Dinheiro")
    @allure.description("""
Cenario: Realizar venda para consumidor final com pagamento em dinheiro

Pre-condicoes:
- Usuario logado no sistema
- Produto cadastrado no sistema

Dado que estou na tela inicial do PDV
Quando acesso o menu "Iniciar Venda"
E seleciono o vendedor
E pulo a selecao de cliente (consumidor)
E adiciono o produto codigo "123"
E seleciono pagamento em Dinheiro
E finalizo a venda
Entao a venda e concluida com sucesso
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda", "consumidor", "dinheiro")
    def test_venda_consumidor_sucesso(self, driver_logado):
        """
        Cenario: Realizar venda para consumidor
        Dado que estou logado no app
        Quando inicio uma venda
        E inicio sem selecionar cliente
        E adiciono um produto
        E finalizo com pagamento em dinheiro
        Entao a venda e realizada com sucesso
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Iniciar Venda'"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Executar fluxo de venda consumidor"):
            pagina_venda.executar_venda_consumidor(codigo_produto=test_data.PRODUCT_CODE_SALE)

        # Assert
        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
