"""
Test Pedido Venda Consumidor - Testes de pedido de venda sem cliente.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.pedido_page import PedidoPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Pedido de Venda")
@allure.story("Gerar Pedido - Consumidor")
class TestPedidoVendaConsumidor:
    """Testes de pedido de venda para consumidor (sem cliente)."""

    @allure.title("Pedido Venda - Consumidor (sem cliente)")
    @allure.description("""
Cenario: Realizar pedido de venda para consumidor final

Pre-condicoes:
- Usuario logado no sistema
- Produto cadastrado no sistema

Dado que estou na tela inicial do PDV
Quando acesso o menu "Pedido Venda"
E seleciono o vendedor
E inicio sem selecionar cliente (consumidor)
E adiciono o produto codigo "123"
E seleciono pagamento em Dinheiro
E finalizo e confirmo o pedido
Entao o pedido e gerado com sucesso
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("pedido", "venda", "consumidor", "dinheiro")
    def test_pedido_venda_consumidor_sucesso(self, driver_logado):
        """
        Cenario: Realizar pedido de venda para consumidor
        Dado que estou logado no app
        Quando inicio um pedido de venda
        E NÃO seleciono cliente (consumidor final)
        E adiciono um produto
        E finalizo com pagamento em dinheiro
        Entao o pedido e gerado com sucesso
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_pedido = PedidoPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Pedido Venda'"):
            pagina_inicial.rolar_ate_texto("Pedido Venda", max_scrolls=3)
            pagina_inicial.clicar_por_texto("Pedido Venda")

        with allure.step("2. Executar fluxo de pedido para consumidor"):
            pagina_pedido.executar_pedido_venda_consumidor(codigo_produto=test_data.PRODUCT_CODE_SALE)

        # Assert
        with allure.step("3. Verificar retorno à tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
