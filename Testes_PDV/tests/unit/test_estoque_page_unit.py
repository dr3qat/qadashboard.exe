"""
Testes unitarios para EstoquePage.
Utiliza mocks para evitar interacao real com Appium/emulador.
"""
import pytest
from unittest.mock import MagicMock, patch
from pages.estoque_page import EstoquePage

# Define a dummy package for app_package as per GEMINI.md
DUMMY_APP_PACKAGE = "com.dummy"


class TestEstoquePageAcessarEstoque:
    """Testes para o metodo acessar_estoque."""

    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time')
    def test_acessar_estoque_clica_estoque(self, mock_time, mock_logger, mock_base_init):
        """
        Deve usar ver_e_clicar_texto com TXT_ESTOQUE (scroll automatico se necessario).
        O texto e sempre 'Estoque' em qualquer device.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE
        estoque_page.ver_e_clicar_texto = MagicMock()

        # Act
        estoque_page.acessar_estoque()

        # Assert
        estoque_page.ver_e_clicar_texto.assert_called_once_with(EstoquePage.TXT_ESTOQUE)

    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time')
    def test_acessar_estoque_lanca_excecao_quando_nao_encontrado(self, mock_time, mock_logger, mock_base_init):
        """
        Quando modulo nao e encontrado, deve propagar excecao de ver_e_clicar_texto.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE
        estoque_page.ver_e_clicar_texto = MagicMock(side_effect=Exception("Nao encontrou"))

        # Act & Assert
        with pytest.raises(Exception, match="Nao encontrou"):
            estoque_page.acessar_estoque()


class TestEstoquePageBuscarProduto:
    """Testes para os metodos de busca de produto."""

    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time')
    def test_buscar_produto_por_codigo(self, mock_time, mock_logger, mock_base_init):
        """
        Deve digitar o codigo e pressionar pesquisar.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        estoque_page.digitar_por_id = MagicMock()
        estoque_page.pressionar_pesquisar = MagicMock()
        estoque_page.clicar_pesquisar = MagicMock() # Mock the internal call
        estoque_page.garantir_filtro = MagicMock() # Mock the internal call

        # Act
        estoque_page.buscar_produto_por_codigo("123")

        # Assert
        estoque_page.clicar_pesquisar.assert_called_once()
        estoque_page.garantir_filtro.assert_called_once_with(EstoquePage.OPCAO_CODIGO)
        estoque_page.digitar_por_id.assert_called_once_with(EstoquePage.EDT_BUSCA_PRODUTO, "123")
        estoque_page.pressionar_pesquisar.assert_called_once()

    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time')
    def test_buscar_produto_por_codigo_fallback(self, mock_time, mock_logger, mock_base_init):
        """
        Quando EDT_BUSCA_PRODUTO falha, deve usar EDT_CODIGO_PRODUTO.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        estoque_page.clicar_pesquisar = MagicMock()
        estoque_page.garantir_filtro = MagicMock()

        estoque_page.digitar_por_id = MagicMock(side_effect=[Exception("Elemento nao encontrado"), None])
        estoque_page.pressionar_pesquisar = MagicMock()

        # Act
        estoque_page.buscar_produto_por_codigo("456")

        # Assert - deve ter tentado ambos os campos
        estoque_page.clicar_pesquisar.assert_called_once()
        estoque_page.garantir_filtro.assert_called_once_with(EstoquePage.OPCAO_CODIGO)
        assert estoque_page.digitar_por_id.call_count == 2
        # Check specific calls for raw IDs
        estoque_page.digitar_por_id.assert_any_call(EstoquePage.EDT_BUSCA_PRODUTO, "456")
        estoque_page.digitar_por_id.assert_any_call(EstoquePage.EDT_CODIGO_PRODUTO, "456")
        estoque_page.pressionar_pesquisar.assert_called_once()


    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time')
    def test_buscar_produto_por_nome(self, mock_time, mock_logger, mock_base_init):
        """
        Deve digitar o nome e pressionar pesquisar.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        estoque_page.digitar_por_id = MagicMock()
        estoque_page.pressionar_pesquisar = MagicMock()
        estoque_page.clicar_pesquisar = MagicMock()
        estoque_page.garantir_filtro = MagicMock()

        # Act
        estoque_page.buscar_produto_por_nome("Camiseta")

        # Assert
        estoque_page.clicar_pesquisar.assert_called_once()
        estoque_page.garantir_filtro.assert_called_once_with(EstoquePage.OPCAO_DESCRICAO)
        estoque_page.digitar_por_id.assert_called_once_with(EstoquePage.EDT_BUSCA_PRODUTO, "Camiseta")
        estoque_page.pressionar_pesquisar.assert_called_once()


class TestEstoquePageObterDados:
    """Testes para os metodos de obtencao de dados."""

    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    def test_obter_quantidade_estoque(self, mock_logger, mock_base_init):
        """
        Deve retornar 'Disponivel' quando produto esta na tela.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE
        estoque_page.elemento_existe = MagicMock(return_value=True)

        # Act
        resultado = estoque_page.obter_quantidade_estoque()

        # Assert
        assert resultado == "Disponível"
        estoque_page.elemento_existe.assert_called_once_with(EstoquePage.TXT_NOME_PRODUTO, 5)


    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    def test_obter_quantidade_estoque_retorna_vazio_quando_erro(self, mock_logger, mock_base_init):
        """
        Deve retornar string vazia quando elemento nao encontrado.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE
        estoque_page.elemento_existe = MagicMock(side_effect=Exception("nao encontrado"))

        # Act
        resultado = estoque_page.obter_quantidade_estoque()

        # Assert
        assert resultado == ""


    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time') # Add time mock
    def test_obter_nome_produto(self, mock_time, mock_logger, mock_base_init): # Add time mock param
        """
        Deve retornar o nome do produto do elemento encontrado.
        Refatorado para o novo metodo de obter_nome_produto.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package

        # Mock para driver.find_element que é chamado por _get_text
        mock_el_nome = MagicMock()
        mock_el_nome.text = "Camiseta Azul"
        estoque_page.driver.find_element.return_value = mock_el_nome
        
        # Act
        resultado = estoque_page.obter_nome_produto()

        # Assert
        assert resultado == "Camiseta Azul"
        estoque_page.driver.find_element.assert_called_once_with("xpath", f"//*[@resource-id='{EstoquePage.TXT_NOME_PRODUTO}']")


    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time') # Add time mock
    def test_obter_preco_produto(self, mock_time, mock_logger, mock_base_init): # Add time mock param
        """
        Deve retornar o preco do produto do elemento encontrado.
        Refatorado para o novo metodo de obter_preco_produto.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        
        # Mock para driver.find_element que é chamado por _get_text
        mock_el_preco = MagicMock()
        mock_el_preco.text = "R$ 99,90"
        estoque_page.driver.find_element.return_value = mock_el_preco

        # Act
        resultado = estoque_page.obter_preco_produto()

        # Assert
        assert resultado == "R$ 99,90"
        estoque_page.driver.find_element.assert_called_once_with("xpath", EstoquePage.XPATH_PRECO_VALOR)


    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    def test_obter_lista_produtos(self, mock_logger, mock_base_init):
        """
        Deve retornar lista de produtos encontrados.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        mock_produtos = [MagicMock(), MagicMock(), MagicMock()]
        estoque_page.encontrar_todos_por_id = MagicMock(return_value=mock_produtos)

        # Act
        resultado = estoque_page.obter_lista_produtos()

        # Assert
        assert len(resultado) == 3
        estoque_page.encontrar_todos_por_id.assert_called_once_with(EstoquePage.ITEM_PRODUTO, tempo_espera=5)


    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    def test_obter_lista_produtos_retorna_lista_vazia_quando_erro(self, mock_logger, mock_base_init):
        """
        Deve retornar lista vazia quando nao encontra produtos.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        estoque_page.encontrar_todos_por_id = MagicMock(side_effect=Exception("Nao encontrou"))

        # Act
        resultado = estoque_page.obter_lista_produtos()

        # Assert
        assert resultado == []
        estoque_page.encontrar_todos_por_id.assert_called_once_with(EstoquePage.ITEM_PRODUTO, tempo_espera=5)


class TestEstoquePageValidacoes:
    """Testes para os metodos de validacao."""





    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    def test_produto_encontrado_quando_nome_produto_existe(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando elemento de nome do produto existe.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        # Mock elemento_existe to return False for TXT_PRODUTO_NAO_ENCONTRADO (first check)
        # and then True for TXT_NOME_PRODUTO (second check in the `return` statement)
        estoque_page.elemento_existe = MagicMock(side_effect=[False, True])
        estoque_page.clicar_por_id = MagicMock() # Mock BTN_OK_ERRO if called by produto_encontrado

        # Act
        resultado = estoque_page.produto_encontrado(timeout=5)

        # Assert
        assert resultado is True
        estoque_page.elemento_existe.assert_any_call(EstoquePage.TXT_PRODUTO_NAO_ENCONTRADO, 2) # First call for error msg
        estoque_page.elemento_existe.assert_any_call(EstoquePage.TXT_NOME_PRODUTO, 5) # Second call for product name


    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    def test_produto_encontrado_retorna_false_quando_mensagem_nao_encontrado(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando mensagem 'Produto nao encontrado' aparece.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        # Mock elemento_existe to return True for TXT_PRODUTO_NAO_ENCONTRADO
        estoque_page.elemento_existe = MagicMock(return_value=True)
        estoque_page.clicar_por_id = MagicMock() # Mock BTN_OK_ERRO

        # Act
        resultado = estoque_page.produto_encontrado(timeout=5)

        # Assert
        assert resultado is False
        estoque_page.elemento_existe.assert_called_once_with(EstoquePage.TXT_PRODUTO_NAO_ENCONTRADO, 2)
        estoque_page.clicar_por_id.assert_called_once_with(EstoquePage.BTN_OK_ERRO)








    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    def test_mensagem_nao_encontrado_exibida(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando mensagem de nao encontrado aparece.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        # Mock elemento_existe to return True for TXT_PRODUTO_NAO_ENCONTRADO
        estoque_page.elemento_existe = MagicMock(return_value=True)

        # Act
        resultado = estoque_page.mensagem_nao_encontrado_exibida(timeout=5)

        # Assert
        assert resultado is True
        estoque_page.elemento_existe.assert_called_once_with(EstoquePage.TXT_PRODUTO_NAO_ENCONTRADO, 5)


class TestEstoquePageFluxoCompleto:
    """Testes para o fluxo completo de consulta."""

    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time')
    def test_executar_consulta_estoque_produto_encontrado(self, mock_time, mock_logger, mock_base_init):
        """
        Deve retornar dict com informacoes quando produto e encontrado.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        estoque_page.buscar_produto_por_codigo = MagicMock()
        estoque_page.produto_encontrado = MagicMock(return_value=True)
        estoque_page.obter_detalhes_completos = MagicMock(return_value={
            'nome': "Camiseta",
            'marca': "Marca X",
            'cor': "Azul",
            'material': "Algodao",
            'obs': "Nenhuma",
            'preco': "R$ 50,00"
        })
        # Mock produto_encontrado's internal calls
        estoque_page.elemento_existe = MagicMock(side_effect=[False, True]) # First for TXT_PRODUTO_NAO_ENCONTRADO, then for TXT_NOME_PRODUTO

        # Act
        resultado = estoque_page.executar_consulta_estoque("123")

        # Assert
        assert resultado['encontrado'] is True
        assert resultado['nome'] == "Camiseta"
        assert resultado['quantidade'] == "Sim" # New logic from estoque_page.py
        assert resultado['preco'] == "R$ 50,00"
        assert resultado['marca'] == "Marca X"
        assert resultado['cor'] == "Azul"
        assert resultado['material'] == "Algodao"
        assert resultado['obs'] == "Nenhuma"


    @patch('pages.estoque_page.BasePage.__init__', return_value=None)
    @patch('pages.estoque_page.logger')
    @patch('pages.estoque_page.time')
    def test_executar_consulta_estoque_produto_nao_encontrado(self, mock_time, mock_logger, mock_base_init):
        """
        Deve retornar dict com encontrado=False quando produto nao existe.
        """
        # Arrange
        estoque_page = EstoquePage.__new__(EstoquePage)
        estoque_page.driver = MagicMock()
        estoque_page._app_package = DUMMY_APP_PACKAGE # Set dummy app_package
        estoque_page.buscar_produto_por_codigo = MagicMock()
        estoque_page.produto_encontrado = MagicMock(return_value=False)
        estoque_page.obter_detalhes_completos = MagicMock(return_value={
            'nome': "N/A",
            'marca': "N/A",
            'cor': "N/A",
            'material': "N/A",
            'obs': "N/A",
            'preco': "N/A"
        })
        # Mock produto_encontrado's internal calls
        estoque_page.elemento_existe = MagicMock(return_value=True, side_effect=lambda id, timeout: id == EstoquePage.TXT_PRODUTO_NAO_ENCONTRADO) # Raw ID

        # Act
        resultado = estoque_page.executar_consulta_estoque("99999")

        # Assert
        assert resultado['encontrado'] is False
        assert resultado['nome'] == "N/A"
        assert resultado['quantidade'] == "Não" # New logic from estoque_page.py
        assert resultado['preco'] == "N/A"
        assert resultado['marca'] == "N/A"
        assert resultado['cor'] == "N/A"
        assert resultado['material'] == "N/A"
        assert resultado['obs'] == "N/A"
