"""
Testes unitários para DocumentosPage.
Utiliza mocks para evitar interação real com Appium/emulador.
"""
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from datetime import datetime


class TestDocumentosPageClicarMenuDocumentos:
    """Testes para o método clicar_menu_documentos."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_clicar_menu_documentos_sucesso(self, mock_logger, mock_base_init):
        """
        Deve clicar no menu Documentos usando texto.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_por_texto = MagicMock()

        # Act
        page.clicar_menu_documentos()

        # Assert
        page.clicar_por_texto.assert_called_once_with("Documentos")


class TestDocumentosPageRolarAteEncontrarTexto:
    """Testes para o método rolar_até_encontrar_texto."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_rolar_até_encontrar_texto_sucesso(self, mock_logger, mock_base_init):
        """
        Deve rolar até encontrar o texto 'Período'.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.rolar_ate_texto = MagicMock()

        # Act
        page.rolar_até_encontrar_texto()

        # Assert
        page.rolar_ate_texto.assert_called_once_with("Período", max_scrolls=10)


class TestDocumentosPagePreencherDataInicial:
    """Testes para o método preencher_data_inicial_com."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.BasePage.app_package', new_callable=PropertyMock, return_value="br.com.app")
    @patch('pages.documentos_page.logger')
    @patch('pages.documentos_page.time')
    def test_preencher_data_inicial_com_data_atual(self, mock_time, mock_logger, mock_app_package, mock_base_init):
        """
        Deve preencher data inicial com a data atual no formato dd/mm/yyyy.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()

        # Mock find_element para simular xpath fallback
        mock_edit_text = MagicMock()
        page.driver.find_element = MagicMock(side_effect=Exception("Elemento não encontrado"))

        # Act
        page.preencher_data_inicial_com()

        # Assert
        page.clicar_por_id.assert_called_once_with(DocumentosPage.EDT_PREENCHER_DATA_INICIAL)
        # Verifica que tentou digitar a data
        page.digitar_por_id.assert_called_once()
        # Verifica formato da data (dd/mm/yyyy)
        data_digitada = page.digitar_por_id.call_args[0][1]
        assert len(data_digitada) == 10
        assert data_digitada[2] == '/' and data_digitada[5] == '/'


class TestDocumentosPagePreencherDataFinal:
    """Testes para o método preencher_data_final_com."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.BasePage.app_package', new_callable=PropertyMock, return_value="br.com.app")
    @patch('pages.documentos_page.logger')
    @patch('pages.documentos_page.time')
    def test_preencher_data_final_com_data_atual(self, mock_time, mock_logger, mock_app_package, mock_base_init):
        """
        Deve preencher data final com a data atual no formato dd/mm/yyyy.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()

        # Mock find_element para simular xpath fallback
        page.driver.find_element = MagicMock(side_effect=Exception("Elemento não encontrado"))

        # Act
        page.preencher_data_final_com()

        # Assert
        page.clicar_por_id.assert_called_once_with(DocumentosPage.EDT_PREENCHER_DATA_FINAL)
        # Verifica que tentou digitar a data
        page.digitar_por_id.assert_called_once()
        # Verifica formato da data (dd/mm/yyyy)
        data_digitada = page.digitar_por_id.call_args[0][1]
        assert len(data_digitada) == 10
        assert data_digitada[2] == '/' and data_digitada[5] == '/'


class TestDocumentosPageClicarBotaoConsultar:
    """Testes para o método clicar_botão_consultar."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_clicar_botão_consultar_sucesso(self, mock_logger, mock_base_init):
        """
        Deve clicar no botão Consultar usando texto.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_por_texto = MagicMock()

        # Act
        page.clicar_botão_consultar()

        # Assert
        page.clicar_por_texto.assert_called_once_with("Consultar")


class TestDocumentosPageVerificarDocumentos:
    """Testes para o método verificar_que_os_documentos."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_verificar_que_os_documentos_clica_primeiro_da_lista(self, mock_logger, mock_base_init):
        """
        Deve clicar no primeiro documento da lista.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_no_primeiro_da_lista_por_id = MagicMock()

        # Act
        page.verificar_que_os_documentos()

        # Assert
        page.clicar_no_primeiro_da_lista_por_id.assert_called_once_with(
            DocumentosPage.LBL_VERIFICAR_QUE_DOCUMENTOS
        )


class TestDocumentosPageClicarDetalhesDocumento:
    """Testes para o método clicar_detalhes_documento."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_clicar_detalhes_documento_sucesso(self, mock_logger, mock_base_init):
        """
        Deve clicar em detalhes do documento.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.clicar_detalhes_documento()

        # Assert
        page.clicar_por_id.assert_called_once_with(DocumentosPage.TXT_DETALHES_DOCUMENTO)


class TestDocumentosPageVerificarDetalhes:
    """Testes para o método verificar_que_os_detalhes."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_verificar_que_os_detalhes_sucesso(self, mock_logger, mock_base_init):
        """
        Deve clicar para verificar detalhes do documento.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.verificar_que_os_detalhes()

        # Assert
        page.clicar_por_id.assert_called_once_with(DocumentosPage.TXT_VERIFICAR_QUE_DETALHES)


class TestDocumentosPageValidarDadosTelaDetalhes:
    """Testes para o método validar_dados_tela_detalhes."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_validar_dados_tela_detalhes_retorna_true_quando_visivel(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando texto está visível.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)

        # Act
        resultado = page.validar_dados_tela_detalhes()

        # Assert
        assert resultado is True
        page.texto_exibido.assert_called_once_with("Validar dados da tela de Detalhes do Documento")


class TestDocumentosPageVoltarTelaDocumentos:
    """Testes para o método voltar_tela_documentos."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_voltar_tela_documentos_chama_voltar_tela(self, mock_logger, mock_base_init):
        """
        Deve chamar método voltar_tela da BasePage.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.voltar_tela = MagicMock()

        # Act
        page.voltar_tela_documentos()

        # Assert
        page.voltar_tela.assert_called_once()


class TestDocumentosPageExecutarDocumentos:
    """Testes para o método executar_documentos."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    @patch('pages.documentos_page.time')
    def test_executar_documentos_chama_metodos_na_ordem(self, mock_time, mock_logger, mock_base_init):
        """
        Deve chamar todos os métodos do fluxo na ordem correta.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page._app_package = "com.test.app"  # necessário para a propriedade app_package
        page.clicar_menu_documentos = MagicMock()
        page.rolar_até_encontrar_texto = MagicMock()
        page.preencher_data_inicial_com = MagicMock()
        page.preencher_data_final_com = MagicMock()
        page.fechar_teclado = MagicMock()
        page.clicar_botão_consultar = MagicMock()
        page.verificar_que_os_documentos = MagicMock()
        page.clicar_detalhes_documento = MagicMock()
        page.verificar_que_os_detalhes = MagicMock()
        page.validar_dados_tela_detalhes = MagicMock()
        page.voltar_tela_documentos = MagicMock()

        # Act
        page.executar_documentos()

        # Assert - verifica ordem de chamada
        page.clicar_menu_documentos.assert_called_once()
        page.rolar_até_encontrar_texto.assert_called_once()
        page.preencher_data_inicial_com.assert_called_once()
        page.preencher_data_final_com.assert_called_once()
        page.clicar_botão_consultar.assert_called_once()
        page.verificar_que_os_documentos.assert_called_once()
        page.clicar_detalhes_documento.assert_called_once()
        page.verificar_que_os_detalhes.assert_called_once()
        page.validar_dados_tela_detalhes.assert_called_once()
        # Verifica que voltar_tela_documentos foi chamado 3 vezes
        assert page.voltar_tela_documentos.call_count == 3


class TestDocumentosPageDadosTelaDetalhesExibida:
    """Testes para o método dados_tela_detalhes_exibida."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_dados_tela_detalhes_exibida_retorna_true_quando_visivel(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando texto de validação está visível.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)

        # Act
        resultado = page.dados_tela_detalhes_exibida(timeout=10)

        # Assert
        assert resultado is True
        page.texto_exibido.assert_called_once_with(
            "Validar dados da tela de Detalhes do Documento", 10
        )

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_dados_tela_detalhes_exibida_retorna_false_quando_nao_visivel(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando texto de validação não está visível.
        """
        from pages.documentos_page import DocumentosPage

        # Arrange
        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=False)

        # Act
        resultado = page.dados_tela_detalhes_exibida(timeout=5)

        # Assert
        assert resultado is False
