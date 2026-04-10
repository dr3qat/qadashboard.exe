"""
Test Venda Futura Domicilio - Teste de venda futura com entrega em domicilio.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_futura_page import VendaFuturaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Venda Futura")
class TestVendaFuturaDomicilio:

    @allure.title("Venda Futura - Entrega em Domicílio")
    @allure.description("""
Cenario: Realizar venda futura com entrega em domicilio

Pre-condicoes:
- Usuario logado no sistema
- Cliente cadastrado no sistema com endereco
- Produto com grade cadastrado

Dado que estou na tela inicial do PDV
Quando acesso o menu "Venda Futura"
E seleciono entrega em domicilio
E confirmo o frete padrao
E seleciono o vendedor
E busco cliente por CPF
E adiciono produto com tamanho "38"
E seleciono pagamento a vista em Dinheiro
E finalizo a venda
Entao a venda futura e concluida com sucesso
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda_futura", "domicilio", "dinheiro")
    def test_venda_futura_domicilio_sucesso(self, driver_logado):
        """
        Cenario: Realizar venda futura com entrega em domicilio
        Dado que estou logado no app
        Quando inicio uma venda futura
        E seleciono entrega em domicilio
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

        with allure.step("2. Executar fluxo de venda futura domicilio"):
            pagina_venda_futura.executar_venda_futura_domicilio(
                cpf=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_FUTURE_SALE,
                tamanho=test_data.PRODUCT_SIZE_FUTURE
            )

        # Assert
        with allure.step("3. Validar sucesso e concluir"):
            pagina_venda_futura.validar_sucesso_e_concluir()

        with allure.step("4. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
