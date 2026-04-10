"""Test Estoque - Regressão: consulta de estoque."""
import pytest
import allure
from pages.estoque_page import EstoquePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Estoque")
@allure.story("Consulta de Estoque")
class TestEstoqueRegressao:
    """Regressão: consulta de estoque."""

    @allure.title("REG: Consultar Estoque - Produto Existente")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "estoque", "consulta")
    @pytest.mark.regression
    def test_consultar_estoque_produto(self, driver_logado):
        """Produto encontrado e tabela de estoque exibida."""
        pagina_estoque = EstoquePage(driver_logado)
        codigo_produto = test_data.PRODUCT_CODE

        with allure.step("1. Acessar consulta de estoque"):
            pagina_estoque.acessar_estoque()

        with allure.step(f"2. Buscar produto {codigo_produto}"):
            pagina_estoque.buscar_produto_por_codigo(codigo_produto)

        with allure.step("3. Validar produto encontrado"):
            assert pagina_estoque.produto_encontrado(), "Produto nao encontrado"

        with allure.step("4. Validar tabela de estoque"):
            qtd = pagina_estoque.obter_quantidade_estoque()
            assert qtd, "Tabela de estoque/preco nao exibida"

    @allure.title("REG: Consultar Estoque - Produto Inexistente")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("regression", "estoque", "inexistente")
    @pytest.mark.regression
    def test_consultar_estoque_produto_inexistente(self, driver_logado):
        """Mensagem de nao encontrado exibida para codigo invalido."""
        pagina_estoque = EstoquePage(driver_logado)

        with allure.step("1. Acessar consulta"):
            pagina_estoque.acessar_estoque()

        with allure.step("2. Buscar codigo invalido"):
            pagina_estoque.buscar_produto_por_codigo("99999999")

        with allure.step("3. Validar mensagem de nao encontrado"):
            assert pagina_estoque.mensagem_nao_encontrado_exibida(), \
                "Mensagem de nao encontrado nao apareceu"
