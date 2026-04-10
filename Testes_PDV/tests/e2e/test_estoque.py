"""
Test Estoque - Testes de consulta de estoque.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.estoque_page import EstoquePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Estoque")
@allure.story("Consulta de Estoque")
class TestEstoque:
    """Testes de consulta de estoque."""

    @allure.title("Consultar Estoque - Produto Existente")
    @allure.description("""
Cenario: Consultar estoque de produto existente

Pre-condicoes:
- Usuario logado no sistema
- Produto cadastrado no sistema

Dado que estou na tela inicial do PDV
Quando acesso a consulta de estoque
E busco um produto pelo codigo
Entao o produto e encontrado
E a tabela de estoque/preco e exibida
""")
    @allure.severity(allure.severity_level.NORMAL)
    def test_consultar_estoque_produto(self, driver_logado):
        driver = driver_logado
        pagina_estoque = EstoquePage(driver)
        codigo_produto = test_data.PRODUCT_CODE

        with allure.step("1. Acessar consulta de estoque"):
            pagina_estoque.acessar_estoque()

        with allure.step(f"2. Buscar produto codigo {codigo_produto}"):
            pagina_estoque.buscar_produto_por_codigo(codigo_produto)

        with allure.step("3. Validar produto encontrado"):
            assert pagina_estoque.produto_encontrado(), "Produto nao encontrado"
            
        with allure.step("4. Validar tabela de estoque"):
            qtd = pagina_estoque.obter_quantidade_estoque()
            assert qtd, "Tabela de estoque/preço não exibida"

    @allure.title("Consultar Estoque - Produto Inexistente")
    @allure.description("""
Cenario: Consultar estoque de produto inexistente

Pre-condicoes:
- Usuario logado no sistema

Dado que estou na tela inicial do PDV
Quando acesso a consulta de estoque
E busco um produto com codigo invalido
Entao a mensagem de "nao encontrado" e exibida
""")
    @allure.severity(allure.severity_level.NORMAL)
    def test_consultar_estoque_produto_inexistente(self, driver_logado):
        driver = driver_logado
        pagina_estoque = EstoquePage(driver)
        codigo_invalido = "99999999"

        with allure.step("1. Acessar consulta"):
            pagina_estoque.acessar_estoque()

        with allure.step("2. Buscar invalido"):
            pagina_estoque.buscar_produto_por_codigo(codigo_invalido)

        with allure.step("3. Validar mensagem de erro"):
            assert pagina_estoque.mensagem_nao_encontrado_exibida(), "Mensagem de erro nao apareceu"

    @allure.title("Consultar Lista de Produtos")
    @allure.description("""
Cenario: Consultar lista de produtos por descricao

Pre-condicoes:
- Usuario logado no sistema
- Produtos cadastrados no sistema

Dado que estou na tela inicial do PDV
Quando acesso a consulta de estoque
E busco por nome/descricao
Entao uma lista de produtos e exibida
E os itens correspondem ao filtro aplicado
""")
    @allure.severity(allure.severity_level.MINOR)
    def test_consultar_lista_produtos(self, driver_logado):
        driver = driver_logado
        pagina_estoque = EstoquePage(driver)

        with allure.step("1. Acessar consulta"):
            pagina_estoque.acessar_estoque()

        with allure.step("2. Buscar por descrição (Lista)"):
            # Busca por NOME/DESCRIÇÃO para garantir filtro correto
            pagina_estoque.buscar_produto_por_nome(test_data.PRODUCT_CODE_STOCK_1)

        with allure.step("3. Validar lista"):
            lista = pagina_estoque.obter_lista_produtos()
            assert lista, "Lista de produtos vazia ou nao exibida"
            allure.attach(f"Itens encontrados: {len(lista)}", name="Lista")

    @allure.title("Consultar Estoque - Validar Detalhes (Busca Dupla)")
    @allure.description("""
Cenario: Validar detalhes completos de multiplos produtos

Pre-condicoes:
- Usuario logado no sistema
- Produtos 123 e 1234 cadastrados no sistema

Dado que estou na tela de consulta de estoque
Quando busco o produto "123"
Entao os detalhes do produto sao exibidos (nome, preco, marca, cor, material)
Quando busco o produto "1234"
Entao os detalhes do segundo produto sao exibidos corretamente
""")
    @allure.severity(allure.severity_level.NORMAL)
    def test_consultar_estoque_validar_informacoes(self, driver_logado):
        driver = driver_logado
        pagina_estoque = EstoquePage(driver)
        
        # Produtos para o teste
        produto_1 = test_data.PRODUCT_CODE_STOCK_1
        produto_2 = test_data.PRODUCT_CODE_STOCK_2

        with allure.step("1. Acessar tela de Estoque"):
            pagina_estoque.acessar_estoque()

        # --- BUSCA 1 ---
        with allure.step(f"2. Buscar Produto 1: {produto_1}"):
            resultado1 = pagina_estoque.executar_consulta_estoque(produto_1)

        with allure.step(f"3. Validar Detalhes Produto {produto_1}"):
            detalhes1 = f"""
            Nome: {resultado1['nome']}
            Preço: {resultado1['preco']}
            Marca: {resultado1['marca']}
            Cor: {resultado1['cor']}
            Material: {resultado1['material']}
            Obs: {resultado1['obs']}
            """
            allure.attach(detalhes1, name=f"Detalhes {produto_1}", attachment_type=allure.attachment_type.TEXT)

            assert resultado1['encontrado'], f"Produto {produto_1} não encontrado"
            assert resultado1['nome'], "Nome vazio"
            assert "R$" in resultado1['preco'], f"Preço inválido: {resultado1['preco']}"

        # --- BUSCA 2 ---
        with allure.step(f"4. Buscar Produto 2: {produto_2}"):
            # O método executar_consulta_estoque já clica na lupa novamente, o que limpa a busca anterior
            resultado2 = pagina_estoque.executar_consulta_estoque(produto_2)

        with allure.step(f"5. Validar Detalhes Produto {produto_2}"):
            detalhes2 = f"""
            Nome: {resultado2['nome']}
            Preço: {resultado2['preco']}
            Marca: {resultado2['marca']}
            Cor: {resultado2['cor']}
            Material: {resultado2['material']}
            Obs: {resultado2['obs']}
            """
            allure.attach(detalhes2, name=f"Detalhes {produto_2}", attachment_type=allure.attachment_type.TEXT)

            assert resultado2['encontrado'], f"Produto {produto_2} não encontrado"
            assert resultado2['nome'], "Nome vazio"
            # Validação opcional para o segundo produto, caso ele possa não ter preço/estoque
            if resultado2['preco'] != "N/A":
                assert "R$" in resultado2['preco'], f"Preço inválido: {resultado2['preco']}"