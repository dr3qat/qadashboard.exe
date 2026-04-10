"""Smoke 06 - Consultar estoque de produto."""
import pytest
import allure
from pages.estoque_page import EstoquePage
from pages.home_page import HomePage
from test_data import test_data
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Estoque")
@pytest.mark.smoke
class TestSmoke06ConsultarEstoque:

    @allure.title("SMOKE 6/7: Consultar estoque de produto")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "estoque")
    def test_06_consultar_estoque(self, driver_logado):
        """
        Navega ate Consultar Estoque, busca produto pelo codigo e
        valida que foi encontrado.
        """
        pagina_estoque = EstoquePage(driver_logado)
        pagina_inicial = HomePage(driver_logado)
        codigo = test_data.PRODUCT_CODE_SALE

        with allure.step("1. Acessar modulo de estoque"):
            pagina_estoque.acessar_estoque()

        with allure.step(f"2. Buscar produto codigo {codigo}"):
            pagina_estoque.buscar_produto_por_codigo(codigo)

        with allure.step("3. Validar produto encontrado"):
            assert pagina_estoque.produto_encontrado(), \
                f"Produto {codigo} nao foi encontrado no estoque"

        with allure.step("4. Voltar para home"):
            pagina_estoque.voltar_tela()
            pagina_inicial.clicar_texto_se_existir("SIM", tempo_espera=2)

        logger.info("[SMOKE 6/7] Consultar estoque OK")
