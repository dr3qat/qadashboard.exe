"""
Test Venda Futura - Teste de venda futura com retirada em loja.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_futura_page import VendaFuturaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Venda Futura")
class TestVendaFutura:
    """Testes de venda futura."""

    @allure.title("Venda Futura - Retirada em Loja")
    @allure.description("""
Cenario: Realizar venda futura com retirada em loja

Pre-condicoes:
- Usuario logado no sistema
- Cliente cadastrado no sistema
- Produto com grade cadastrado

Dado que estou na tela inicial do PDV
Quando acesso o menu "Venda Futura"
E seleciono retirada em loja
E seleciono o vendedor
E busco cliente por CPF
E adiciono produto com tamanho "38"
E seleciono pagamento a vista em Dinheiro
E finalizo a venda
Entao a venda futura e concluida com sucesso
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda_futura", "retirada_loja", "dinheiro")
    def test_venda_futura_sucesso(self, driver_logado):
        """
        Cenario: Realizar venda futura com retirada em loja
        Dado que estou logado no app
        Quando inicio uma venda futura
        E seleciono retirada em loja
        E busco cliente por CPF
        E adiciono um produto com tamanho
        E seleciono pagamento a vista em dinheiro
        Entao a venda e realizada com sucesso
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda_futura = VendaFuturaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Venda Futura'"):
            pagina_venda_futura.clicar_venda_futura()

        with allure.step("2. Executar fluxo de venda futura"):
            pagina_venda_futura.executar_venda_futura(
                cpf=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_FUTURE_SALE,
                tamanho=test_data.PRODUCT_SIZE_FUTURE
            )

        # Assert
        with allure.step("3. Validar sucesso e concluir"):
            pagina_venda_futura.validar_sucesso_e_concluir()

        with allure.step("4. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"

