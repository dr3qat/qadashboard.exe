"""Test Opções Item - Regressão: ações do item no carrinho."""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from pages.opcoes_item_page import OpcoesItemPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Carrinho de Vendas")
@allure.story("Ações do Item Produto")
class TestOpcoesItemRegressao:
    """Regressão: menu de ações do item no carrinho."""

    @allure.title("REG: Opções Item - Remover do Carrinho")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "carrinho", "remover")
    @pytest.mark.regression
    def test_remover_item_carrinho(self, driver_logado):
        """Item removido do carrinho com sucesso."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)
        opcoes_item = OpcoesItemPage(driver_logado)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        with allure.step("3. Remover item"):
            opcoes_item.remover_item()

        with allure.step("4. Validar remoção"):
            assert not opcoes_item.item_existe_no_carrinho(), \
                "Item ainda no carrinho"

    @allure.title("REG: Opções Item - Alterar Quantidade")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "carrinho", "quantidade")
    @pytest.mark.regression
    def test_alterar_quantidade_item(self, driver_logado):
        """Quantidade do item atualizada para valor informado."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)
        opcoes_item = OpcoesItemPage(driver_logado)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        with allure.step("3. Alterar quantidade para 3"):
            qtd = opcoes_item.alterar_quantidade("3")

        with allure.step("4. Validar quantidade"):
            assert qtd == "3", f"Quantidade esperada '3', obteve '{qtd}'"
