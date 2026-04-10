"""
Test Pedido Venda Cliente - Testes de pedido de venda com cliente cadastrado.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.pedido_page import PedidoPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Pedido de Venda")
@allure.story("Gerar Pedido - Cliente")
class TestPedidoVendaCliente:
    """Testes de pedido de venda para cliente cadastrado."""

    @allure.title("Pedido Venda - Cliente cadastrado")
    @allure.description("""
Cenario: Realizar pedido de venda para cliente cadastrado

Pre-condicoes:
- Usuario logado no sistema
- Cliente cadastrado no sistema
- Produto cadastrado no sistema

Dado que estou na tela inicial do PDV
Quando acesso o menu "Pedido Venda"
E seleciono o vendedor
E busco e seleciono um cliente cadastrado
E adiciono o produto codigo "123"
E seleciono pagamento em Dinheiro
E finalizo e confirmo o pedido
Entao o pedido e gerado com sucesso
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("pedido", "venda", "cliente", "dinheiro")
    def test_pedido_venda_cliente_sucesso(self, driver_logado):
        """
        Cenario: Realizar pedido de venda para cliente
        Dado que estou logado no app
        Quando inicio um pedido de venda
        E seleciono um cliente cadastrado
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

        with allure.step("2. Executar fluxo de pedido para cliente"):
            pagina_pedido.executar_pedido_venda_cliente(
                id_cliente=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_SALE
            )

        # Assert
        with allure.step("3. Verificar retorno à tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
