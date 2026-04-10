"""
Testes unitários para HomePage.
Utiliza mocks para evitar interação real com Appium/emulador.
"""
import pytest
from unittest.mock import MagicMock, patch


class TestHomePageIniciarVenda:
    """Testes para o método iniciar_venda."""

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    @patch('pages.home_page.time')
    def test_iniciar_venda_quando_iniciar_venda_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o texto 'Iniciar Venda' está visível,
        deve clicar nele e retornar (versão device).
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(side_effect=lambda texto, tempo_espera: texto == "Iniciar Venda")
        home_page.clicar_por_texto = MagicMock()
        home_page.rolar_ate_texto = MagicMock()

        # Act
        home_page.iniciar_venda()

        # Assert
        home_page.clicar_por_texto.assert_called_once_with(HomePage.TXT_INICIAR_VENDA)

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    @patch('pages.home_page.time')
    def test_iniciar_venda_quando_venda_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Quando 'Iniciar Venda' não existe mas 'Venda' está visível,
        deve clicar em 'Venda' (versão Playstore).
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()

        def texto_exibido_mock(texto, tempo_espera):
            return texto == "Venda"

        home_page.texto_exibido = MagicMock(side_effect=texto_exibido_mock)
        home_page.clicar_por_texto = MagicMock()
        home_page.rolar_ate_texto = MagicMock()

        # Act
        home_page.iniciar_venda()

        # Assert
        home_page.clicar_por_texto.assert_called_once_with(HomePage.TXT_VENDA)

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    @patch('pages.home_page.time')
    def test_iniciar_venda_usa_scroll_quando_nao_encontra(self, mock_time, mock_logger, mock_base_init):
        """
        Quando nenhum texto visível diretamente, usa scroll para encontrar.
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(return_value=False)
        home_page.clicar_por_texto = MagicMock()
        home_page.rolar_ate_texto = MagicMock()

        # Act
        home_page.iniciar_venda()

        # Assert - deve tentar scroll
        home_page.rolar_ate_texto.assert_called()

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    @patch('pages.home_page.time')
    def test_iniciar_venda_lanca_excecao_quando_nenhum_botao_encontrado(self, mock_time, mock_logger, mock_base_init):
        """
        Quando nenhum botão de venda é encontrado,
        deve lançar exceção.
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(return_value=False)
        home_page.clicar_por_texto = MagicMock()
        home_page.rolar_ate_texto = MagicMock(side_effect=Exception("Não encontrou"))

        # Act & Assert
        with pytest.raises(Exception, match="Não encontrou"):
            home_page.iniciar_venda()


class TestHomePageIniciarTroca:
    """Testes para o método iniciar_troca."""

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    @patch('pages.home_page.time')
    def test_iniciar_troca_rola_e_clica(self, mock_time, mock_logger, mock_base_init):
        """
        Deve usar ver_e_clicar_texto para 'Realizar Troca' (scroll automatico se necessario).
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.ver_e_clicar_texto = MagicMock()

        # Act
        home_page.iniciar_troca()

        # Assert
        home_page.ver_e_clicar_texto.assert_called_once_with(HomePage.TXT_REALIZAR_TROCA)


class TestHomePageSelecionarVendedor:
    """Testes para o método selecionar_vendedor."""

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    @patch('pages.home_page.time')
    def test_selecionar_vendedor_tela_full_screen(self, mock_time, mock_logger, mock_base_init):
        """
        Quando a tela 'Escolher Vendedor' está visível,
        deve clicar no primeiro vendedor da lista.
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(side_effect=lambda texto, tempo_espera: texto == "Escolher Vendedor")
        home_page.clicar_no_primeiro_da_lista_por_id = MagicMock()
        home_page.elemento_existe = MagicMock(return_value=False)
        home_page.clicar_por_id = MagicMock()

        # Act
        home_page.selecionar_vendedor()

        # Assert
        home_page.clicar_no_primeiro_da_lista_por_id.assert_called_once_with(HomePage.DIALOGO_VENDEDOR)

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    @patch('pages.home_page.time')
    def test_selecionar_vendedor_dialogo_popup(self, mock_time, mock_logger, mock_base_init):
        """
        Quando apenas o diálogo popup de vendedor aparece,
        deve clicar por ID.
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(return_value=False)
        home_page.elemento_existe = MagicMock(return_value=True)
        home_page.clicar_por_id = MagicMock()
        home_page.clicar_no_primeiro_da_lista_por_id = MagicMock()

        # Act
        home_page.selecionar_vendedor()

        # Assert
        home_page.clicar_por_id.assert_called_once_with(HomePage.DIALOGO_VENDEDOR)

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    @patch('pages.home_page.time')
    def test_selecionar_vendedor_nenhuma_tela_detectada(self, mock_time, mock_logger, mock_base_init):
        """
        Quando nenhuma tela de vendedor aparece,
        deve simplesmente retornar (versão pode não exigir).
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(return_value=False)
        home_page.elemento_existe = MagicMock(return_value=False)
        home_page.clicar_por_id = MagicMock()
        home_page.clicar_no_primeiro_da_lista_por_id = MagicMock()

        # Act - não deve lançar exceção
        home_page.selecionar_vendedor()

        # Assert - não deve ter clicado em nada
        home_page.clicar_por_id.assert_not_called()
        home_page.clicar_no_primeiro_da_lista_por_id.assert_not_called()


class TestHomePageTelaInicialExibida:
    """Testes para o método tela_inicial_exibida."""

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    def test_tela_inicial_exibida_quando_iniciar_venda_visivel(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando 'Iniciar Venda' está visível.
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(side_effect=lambda texto, timeout: texto == "Iniciar Venda")

        # Act
        resultado = home_page.tela_inicial_exibida(timeout=10)

        # Assert
        assert resultado is True

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    def test_tela_inicial_exibida_quando_venda_visivel(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando 'Venda' está visível.
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(side_effect=lambda texto, timeout: texto == "Venda")

        # Act
        resultado = home_page.tela_inicial_exibida(timeout=10)

        # Assert
        assert resultado is True

    @patch('pages.home_page.BasePage.__init__', return_value=None)
    @patch('pages.home_page.logger')
    def test_tela_inicial_exibida_retorna_false_quando_nenhum(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando nenhum texto está visível.
        """
        from pages.home_page import HomePage

        # Arrange
        home_page = HomePage.__new__(HomePage)
        home_page.driver = MagicMock()
        home_page.texto_exibido = MagicMock(return_value=False)

        # Act
        resultado = home_page.tela_inicial_exibida(timeout=10)

        # Assert
        assert resultado is False
