"""Test Busca Invalida - Cenarios negativos de busca de produto no estoque."""
import pytest
import allure
from pages.home_page import HomePage
from pages.estoque_page import EstoquePage


@allure.epic("PDV Mobile")
@allure.feature("Estoque")
@allure.story("Busca Negativa")
class TestBuscaInvalida:
    """Testes de busca com codigos/descricoes inexistentes."""

    @allure.title("Estoque - Produto inexistente exibe mensagem de nao encontrado")
    @allure.description("""
Cenario: Busca por codigo de produto que nao existe no sistema

Pre-condicoes:
- Usuario logado
- Codigo de produto inexistente

Dado que estou na consulta de estoque
Quando busco por codigo inexistente
Entao devo ver mensagem de produto nao encontrado
E nao devo ver detalhes de produto
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("estoque", "negativo", "busca")
    def test_produto_inexistente_exibe_nao_encontrado(self, driver_logado):
        """
        Cenario: Codigo invalido → dialogo 'Produto nao encontrado'.
        """
        pagina_inicial = HomePage(driver_logado)
        estoque = EstoquePage(driver_logado)

        with allure.step("1. Acessar consulta de estoque"):
            estoque.acessar_estoque()

        with allure.step("2. Buscar codigo de produto inexistente"):
            estoque.buscar_produto_por_codigo("XXXXINVALIDO99999")

        with allure.step("3. Verificar que produto NAO foi encontrado"):
            encontrado = estoque.produto_encontrado(timeout=5)
            # produto_encontrado() ja dispensa dialogo de erro se existir
            assert not encontrado, \
                "App exibiu produto para codigo invalido - locator ou validacao com bug"

        with allure.step("4. Voltar para tela inicial"):
            estoque.voltar_tela()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial apos busca invalida no estoque"

    @allure.title("Estoque - Descricao inexistente exibe lista vazia ou nao encontrado")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("estoque", "negativo", "busca", "descricao")
    def test_descricao_inexistente_sem_resultado(self, driver_logado):
        """
        Cenario: Descricao sem match → sem resultados ou mensagem.
        """
        pagina_inicial = HomePage(driver_logado)
        estoque = EstoquePage(driver_logado)

        with allure.step("1. Acessar consulta de estoque"):
            estoque.acessar_estoque()

        with allure.step("2. Buscar descricao de produto que nao existe"):
            estoque.buscar_produto_por_nome("PRODUTO ZZZINEXISTENTE XYZQQA999")

        with allure.step("3. Verificar que produto NAO foi encontrado"):
            encontrado = estoque.produto_encontrado(timeout=5)
            assert not encontrado, \
                "App exibiu produto para descricao invalida"

        with allure.step("4. Voltar para tela inicial"):
            estoque.voltar_tela()

        with allure.step("5. Verificar retorno"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial"
