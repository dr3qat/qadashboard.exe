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
        """Deve clicar no menu Documentos usando ver_e_clicar_texto."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.ver_e_clicar_texto = MagicMock()

        page.clicar_menu_documentos()

        page.ver_e_clicar_texto.assert_called_once_with("Documentos")


class TestDocumentosPageRolarAteEncontrarTexto:
    """Testes para o método rolar_até_encontrar_texto."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_rolar_até_encontrar_texto_sucesso(self, mock_logger, mock_base_init):
        """Deve rolar até encontrar o texto 'Período'."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.rolar_ate_texto = MagicMock()

        page.rolar_até_encontrar_texto()

        page.rolar_ate_texto.assert_called_once_with("Período", max_scrolls=5)

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_rolar_até_encontrar_texto_fallback(self, mock_logger, mock_base_init):
        """Deve continuar normalmente se scroll falhar (campo já visível)."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.rolar_ate_texto = MagicMock(side_effect=Exception("não encontrado"))

        page.rolar_até_encontrar_texto()  # não deve levantar exceção


class TestDocumentosPagePreencherDataInicial:
    """Testes para o método preencher_data_inicial_com."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.BasePage.app_package', new_callable=PropertyMock, return_value="br.com.app")
    @patch('pages.documentos_page.logger')
    @patch('pages.documentos_page.time')
    def test_preencher_data_inicial_com_data_atual(self, mock_time, mock_logger, mock_app_package, mock_base_init):
        """Deve preencher data inicial com a data atual no formato dd/mm/yyyy."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()
        page._id_completo = MagicMock(return_value="br.com.app:id/textInputLayout4")
        page.driver.find_element = MagicMock(side_effect=Exception("não encontrado"))

        page.preencher_data_inicial_com()

        page.clicar_por_id.assert_called_once_with(DocumentosPage.EDT_PREENCHER_DATA_INICIAL)
        page.digitar_por_id.assert_called_once()
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
        """Deve preencher data final com a data atual no formato dd/mm/yyyy."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()
        page._id_completo = MagicMock(return_value="br.com.app:id/textInputLayout5")
        page.driver.find_element = MagicMock(side_effect=Exception("não encontrado"))

        page.preencher_data_final_com()

        page.clicar_por_id.assert_called_once_with(DocumentosPage.EDT_PREENCHER_DATA_FINAL)
        page.digitar_por_id.assert_called_once()
        data_digitada = page.digitar_por_id.call_args[0][1]
        assert len(data_digitada) == 10
        assert data_digitada[2] == '/' and data_digitada[5] == '/'


class TestDocumentosPageClicarBotaoConsultar:
    """Testes para o método clicar_botão_consultar."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_clicar_botão_consultar_sucesso(self, mock_logger, mock_base_init):
        """Deve clicar no botão Consultar via ver_e_clicar_texto."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.ver_e_clicar_texto = MagicMock()

        page.clicar_botão_consultar()

        page.ver_e_clicar_texto.assert_called_once_with("Consultar")


class TestDocumentosPageVerificarDocumentos:
    """Testes para o método verificar_que_os_documentos / clicar_primeiro_documento."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_clicar_primeiro_documento_clica_indice_zero(self, mock_logger, mock_base_init):
        """Deve clicar no primeiro ViewGroup pai (índice 0) via find_elements XPath."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page._id_completo = MagicMock(return_value="com.app:id/lbl_nf")
        mock_elem = MagicMock()
        page.driver.find_elements = MagicMock(return_value=[mock_elem, MagicMock()])

        page.clicar_primeiro_documento()

        page.driver.find_elements.assert_called_once()
        mock_elem.click.assert_called_once()

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_clicar_primeiro_documento_fallback_textview100(self, mock_logger, mock_base_init):
        """Deve usar encontrar_todos_por_id('textView100')[0] se XPath retornar lista vazia."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page._id_completo = MagicMock(return_value="com.app:id/lbl_nf")
        page.driver.find_elements = MagicMock(return_value=[])
        mock_elem = MagicMock()
        page.encontrar_todos_por_id = MagicMock(return_value=[mock_elem])

        page.clicar_primeiro_documento()

        page.encontrar_todos_por_id.assert_called_once_with("textView100")
        mock_elem.click.assert_called_once()

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_verificar_que_os_documentos_delega_para_clicar_primeiro(self, mock_logger, mock_base_init):
        """verificar_que_os_documentos deve delegar para clicar_primeiro_documento."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.clicar_primeiro_documento = MagicMock()

        page.verificar_que_os_documentos()

        page.clicar_primeiro_documento.assert_called_once()


class TestDocumentosPageClicarDetalhesDocumento:
    """Testes para o método clicar_detalhes_documento."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    @patch('pages.documentos_page.time')
    def test_clicar_detalhes_usa_encontrar_clicavel_sem_scroll(self, mock_time, mock_logger, mock_base_init):
        """Deve usar encontrar_clicavel_por_id (sem scroll) para não fechar popup."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        mock_elem = MagicMock()
        page.encontrar_clicavel_por_id = MagicMock(return_value=mock_elem)

        page.clicar_detalhes_documento()

        page.encontrar_clicavel_por_id.assert_called_once_with(
            DocumentosPage.TXT_DETALHES_DOCUMENTO, tempo_espera=10
        )
        mock_elem.click.assert_called_once()


class TestDocumentosPageVerificarQueOsDetalhes:
    """Testes para o método verificar_que_os_detalhes."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_verificar_que_os_detalhes_aguarda_txt_cliente(self, mock_logger, mock_base_init):
        """Deve aguardar txtCliente aparecer na tela de detalhes."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.encontrar_por_id = MagicMock()

        page.verificar_que_os_detalhes()

        page.encontrar_por_id.assert_called_once_with(
            DocumentosPage.TXT_CLIENTE, tempo_espera=10
        )

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_verificar_que_os_detalhes_nao_falha_se_ausente(self, mock_logger, mock_base_init):
        """Deve continuar se txtCliente não encontrado (tela já pode ter avançado)."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.encontrar_por_id = MagicMock(side_effect=Exception("não encontrado"))

        page.verificar_que_os_detalhes()  # não deve levantar exceção


class TestDocumentosPageValidarDadosTelaDetalhes:
    """Testes para o método validar_dados_tela_detalhes."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    @patch('pages.documentos_page.time')
    def test_validar_dados_retorna_true_quando_campos_presentes(self, mock_time, mock_logger, mock_base_init):
        """Deve retornar True quando txtCliente e txtStatus existem."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)
        page.realizar_scroll_para_baixo = MagicMock()

        resultado = page.validar_dados_tela_detalhes()

        assert resultado is True
        assert page.realizar_scroll_para_baixo.call_count == 2

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    @patch('pages.documentos_page.time')
    def test_validar_dados_retorna_false_quando_cliente_ausente(self, mock_time, mock_logger, mock_base_init):
        """Deve retornar False se txtCliente não existe."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=False)
        page.realizar_scroll_para_baixo = MagicMock()

        resultado = page.validar_dados_tela_detalhes()

        assert resultado is False


class TestDocumentosPageVoltarTelaDocumentos:
    """Testes para o método voltar_tela_documentos."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_voltar_tela_documentos_chama_voltar_tela(self, mock_logger, mock_base_init):
        """Deve chamar voltar_tela da BasePage."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.voltar_tela = MagicMock()

        page.voltar_tela_documentos()

        page.voltar_tela.assert_called_once()


class TestDocumentosPageExecutarDocumentos:
    """Testes para o método executar_documentos."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    @patch('pages.documentos_page.time')
    def test_executar_documentos_chama_metodos_na_ordem(self, mock_time, mock_logger, mock_base_init):
        """Deve chamar todos os métodos do fluxo na ordem correta."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page._app_package = "com.test.app"
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

        page.executar_documentos()

        page.clicar_menu_documentos.assert_called_once()
        page.rolar_até_encontrar_texto.assert_called_once()
        page.preencher_data_inicial_com.assert_called_once()
        page.preencher_data_final_com.assert_called_once()
        page.fechar_teclado.assert_called_once()
        page.clicar_botão_consultar.assert_called_once()
        page.verificar_que_os_documentos.assert_called_once()
        page.clicar_detalhes_documento.assert_called_once()
        page.verificar_que_os_detalhes.assert_called_once()
        page.validar_dados_tela_detalhes.assert_called_once()
        assert page.voltar_tela_documentos.call_count == 3


class TestDocumentosPageDadosTelaDetalhesExibida:
    """Testes para o método dados_tela_detalhes_exibida."""

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_retorna_true_quando_txt_cliente_existe(self, mock_logger, mock_base_init):
        """Deve retornar True quando txtCliente está presente."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)
        page.texto_exibido = MagicMock(return_value=False)

        resultado = page.dados_tela_detalhes_exibida(timeout=10)

        assert resultado is True

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_retorna_true_via_texto_detalhes_documento(self, mock_logger, mock_base_init):
        """Deve retornar True via texto 'Detalhes Documento' se txtCliente ausente."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=False)
        page.texto_exibido = MagicMock(return_value=True)

        resultado = page.dados_tela_detalhes_exibida(timeout=5)

        assert resultado is True

    @patch('pages.documentos_page.BasePage.__init__', return_value=None)
    @patch('pages.documentos_page.logger')
    def test_retorna_false_quando_nenhum_campo_presente(self, mock_logger, mock_base_init):
        """Deve retornar False quando nenhum campo está presente."""
        from pages.documentos_page import DocumentosPage

        page = DocumentosPage.__new__(DocumentosPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=False)
        page.texto_exibido = MagicMock(return_value=False)

        resultado = page.dados_tela_detalhes_exibida()

        assert resultado is False
