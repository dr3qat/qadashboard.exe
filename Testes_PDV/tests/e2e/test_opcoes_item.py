"""
Test Opcoes Item - Teste completo do menu de ações do item produto.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from pages.opcoes_item_page import OpcoesItemPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Carrinho de Vendas")
@allure.story("Ações do Item Produto")
class TestOpcoesItem:
    """Testes do menu de ações do item produto no carrinho."""

    @allure.title("Opções Item - Remover Item do Carrinho")
    @allure.description("""
Cenário: Remover item do carrinho de vendas

Pré-condições:
- Usuário logado no sistema
- Cliente selecionado
- Produto adicionado no carrinho

Dado que estou na tela de vendas com um item no carrinho
Quando abro o menu de ações do item
E seleciono "Remover item"
E confirmo a remoção
Então o item é removido do carrinho
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("carrinho", "item", "remover")
    def test_remover_item_carrinho(self, driver_logado):
        """
        Cenário: Remover item do carrinho
        Dado que tenho um item no carrinho
        Quando removo o item
        Então o item é excluído com sucesso
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)
        opcoes_item = OpcoesItemPage(driver)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        # Act
        with allure.step("3. Remover item do carrinho"):
            opcoes_item.remover_item()

        # Assert
        with allure.step("4. Validar que item foi removido"):
            assert not opcoes_item.item_existe_no_carrinho(), \
                "Item ainda está presente no carrinho"

    @allure.title("Opções Item - Alterar Quantidade do Item")
    @allure.description("""
Cenário: Alterar quantidade do item no carrinho

Pré-condições:
- Usuário logado no sistema
- Cliente selecionado
- Produto adicionado no carrinho

Dado que estou na tela de vendas com um item no carrinho
Quando abro o menu de ações do item
E seleciono "Alterar quantidade"
E digito uma nova quantidade (ex: 3)
E confirmo
Então a quantidade do item é atualizada
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("carrinho", "item", "quantidade")
    def test_alterar_quantidade_item(self, driver_logado):
        """
        Cenário: Alterar quantidade do item
        Dado que tenho um item no carrinho
        Quando altero a quantidade para 3
        Então a quantidade é atualizada para 3
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)
        opcoes_item = OpcoesItemPage(driver)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        # Act
        with allure.step("3. Alterar quantidade para 3"):
            quantidade_atualizada = opcoes_item.alterar_quantidade("3")

        # Assert
        with allure.step("4. Validar que quantidade foi alterada"):
            assert quantidade_atualizada == "3", \
                f"Quantidade esperada '3', mas encontrou '{quantidade_atualizada}'"

    @allure.title("Opções Item - Alterar Preço do Item")
    @allure.description("""
Cenário: Alterar preço do item no carrinho

Pré-condições:
- Usuário logado no sistema
- Cliente selecionado
- Produto adicionado no carrinho

Dado que estou na tela de vendas com um item no carrinho
Quando abro o menu de ações do item
E seleciono "Alterar preço"
E digito um novo preço (ex: 15000)
E confirmo
Então o preço do item é atualizado
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("carrinho", "item", "preco")
    def test_alterar_preco_item(self, driver_logado):
        """
        Cenário: Alterar preço do item
        Dado que tenho um item no carrinho
        Quando altero o preço para 15000
        Então o preço é atualizado
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)
        opcoes_item = OpcoesItemPage(driver)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        with allure.step("3. Capturar preço original"):
            preco_original = opcoes_item.obter_preco_atual()

        # Act
        with allure.step("4. Alterar preço para 15000"):
            preco_novo = opcoes_item.alterar_preco("15000")

        # Assert
        with allure.step("5. Validar que preço foi alterado"):
            assert preco_novo != preco_original, \
                f"Preço não foi alterado! Continua: {preco_original}"

    @allure.title("Opções Item - Alterar Tamanho do Item")
    @allure.description("""
Cenário: Alterar tamanho do item no carrinho

Pré-condições:
- Usuário logado no sistema
- Cliente selecionado
- Produto com múltiplos tamanhos adicionado no carrinho

Dado que estou na tela de vendas com um item no carrinho
Quando abro o menu de ações do item
E seleciono "Alterar tamanho"
E escolho um tamanho diferente
Então o tamanho do item é atualizado
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("carrinho", "item", "tamanho")
    def test_alterar_tamanho_item(self, driver_logado):
        """
        Cenário: Alterar tamanho do item
        Dado que tenho um item com múltiplos tamanhos no carrinho
        Quando altero o tamanho
        Então o tamanho é atualizado
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)
        opcoes_item = OpcoesItemPage(driver)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        # Act
        with allure.step("3. Alterar tamanho do item"):
            tamanho_antigo, tamanho_novo = opcoes_item.alterar_tamanho()

        # Assert
        with allure.step("4. Validar que tamanho foi alterado"):
            assert tamanho_novo != tamanho_antigo, \
                f"Tamanho não foi alterado! Continua: {tamanho_antigo}"

    @allure.title("Opções Item - Alterar Vendedor do Item")
    @allure.description("""
Cenário: Alterar vendedor do item no carrinho

Pré-condições:
- Usuário logado no sistema
- Cliente selecionado
- Produto adicionado no carrinho
- Múltiplos vendedores cadastrados

Dado que estou na tela de vendas com um item no carrinho
Quando abro o menu de ações do item
E seleciono "Alterar vendedor"
E escolho um vendedor diferente
Então o vendedor do item é atualizado
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("carrinho", "item", "vendedor")
    def test_alterar_vendedor_item(self, driver_logado):
        """
        Cenário: Alterar vendedor do item
        Dado que tenho um item no carrinho
        Quando altero o vendedor
        Então o vendedor é atualizado
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)
        opcoes_item = OpcoesItemPage(driver)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        # Act
        with allure.step("3. Alterar vendedor do item"):
            vendedor_antigo, vendedor_novo = opcoes_item.alterar_vendedor()

        # Assert
        with allure.step("4. Validar que vendedor foi alterado"):
            assert vendedor_novo != vendedor_antigo, \
                f"Vendedor não foi alterado! Continua: {vendedor_antigo}"

    @allure.title("Opções Item - Consultar Estoque do Item")
    @allure.description("""
Cenário: Consultar estoque do item no carrinho

Pré-condições:
- Usuário logado no sistema
- Cliente selecionado
- Produto adicionado no carrinho

Dado que estou na tela de vendas com um item no carrinho
Quando abro o menu de ações do item
E seleciono "Ver estoque"
Então a tela de consulta de estoque é exibida
E os detalhes do produto são mostrados (nome, marca)
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("carrinho", "item", "estoque", "consulta")
    def test_consultar_estoque_item(self, driver_logado):
        """
        Cenário: Consultar estoque do item
        Dado que tenho um item no carrinho
        Quando consulto o estoque
        Então as informações do produto são exibidas
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)
        opcoes_item = OpcoesItemPage(driver)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        # Act
        with allure.step("3. Consultar estoque do item"):
            info_produto = opcoes_item.consultar_estoque()

        # Assert
        with allure.step("4. Validar informações do produto"):
            assert info_produto["nome"], "Nome do produto está vazio"
            assert info_produto["marca"], "Marca do produto está vazia"

    @allure.title("Opções Item - Fluxo Completo de Ações")
    @allure.description("""
Cenário: Testar todas as ações do item em sequência

Pré-condições:
- Usuário logado no sistema
- Cliente selecionado
- Produto adicionado no carrinho

Dado que estou na tela de vendas com um item no carrinho
Quando executo todas as ações em sequência:
1. Alterar quantidade
2. Alterar preço
3. Alterar tamanho
4. Alterar vendedor
5. Consultar estoque
6. Remover item
Então todas as ações são executadas com sucesso
""")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("carrinho", "item", "fluxo-completo", "integracao")
    def test_opcoes_item_fluxo_completo(self, driver_logado):
        """
        Cenário: Fluxo completo de ações do item
        Dado que tenho um item no carrinho
        Quando executo todas as ações disponíveis
        Então todas são executadas com sucesso
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)
        opcoes_item = OpcoesItemPage(driver)

        with allure.step("1. Iniciar venda e selecionar cliente"):
            pagina_inicial.iniciar_venda()
            pagina_inicial.selecionar_vendedor()
            pagina_venda.clicar_buscar_cliente()
            pagina_venda.selecionar_cliente(test_data.CUSTOMER_ID)

        with allure.step("2. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(test_data.PRODUCT_CODE)

        # Act & Assert
        with allure.step("3. FASE 1: Alterar quantidade"):
            quantidade_nova = opcoes_item.alterar_quantidade("3")
            assert quantidade_nova == "3", "Falha ao alterar quantidade"

        with allure.step("4. FASE 2: Alterar preço"):
            preco_original = opcoes_item.obter_preco_atual()
            preco_novo = opcoes_item.alterar_preco("15000")
            assert preco_novo != preco_original, "Falha ao alterar preço"

        with allure.step("5. FASE 3: Alterar tamanho"):
            tamanho_antigo, tamanho_novo = opcoes_item.alterar_tamanho()
            assert tamanho_novo != tamanho_antigo, "Falha ao alterar tamanho"

        with allure.step("6. FASE 4: Alterar vendedor"):
            vendedor_antigo, vendedor_novo = opcoes_item.alterar_vendedor()
            assert vendedor_novo != vendedor_antigo, "Falha ao alterar vendedor"

        with allure.step("7. FASE 5: Consultar estoque"):
            info_produto = opcoes_item.consultar_estoque()
            assert info_produto["nome"], "Falha ao consultar estoque"
            assert info_produto["marca"], "Falha ao consultar estoque"

        with allure.step("8. FASE 6: Remover item"):
            opcoes_item.remover_item()
            assert not opcoes_item.item_existe_no_carrinho(), \
                "Falha ao remover item"

        with allure.step("9. Validar fluxo completo executado"):
            allure.attach(
                "Todas as 6 fases foram executadas com sucesso:\n"
                "1. Quantidade alterada ✅\n"
                "2. Preço alterado ✅\n"
                "3. Tamanho alterado ✅\n"
                "4. Vendedor alterado ✅\n"
                "5. Estoque consultado ✅\n"
                "6. Item removido ✅",
                name="Resumo do Fluxo",
                attachment_type=allure.attachment_type.TEXT
            )
