"""
Testes unitários para VendaPage.
Utiliza mocks para evitar interação real com Appium/emulador.
"""
import pytest
from unittest.mock import MagicMock, patch


class TestVendaPageClicarBuscarCliente:
    """Testes para o método clicar_buscar_cliente."""

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    @patch('pages.venda_page.time')
    def test_clicar_buscar_cliente_versao_l400_stone(self, mock_time, mock_logger, mock_base_init):
        """
        Na versão L400/Stone, deve clicar por texto em 'Buscar Cliente'.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()

        def texto_exibido_mock(texto, tempo_espera):
            return texto in ["Selecionar Cliente", "Buscar Cliente"]

        page.texto_exibido = MagicMock(side_effect=texto_exibido_mock)
        page.clicar_por_texto = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.clicar_buscar_cliente()

        # Assert
        page.clicar_por_texto.assert_called_once_with("Buscar Cliente")
        page.clicar_por_id.assert_not_called()

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    @patch('pages.venda_page.time')
    def test_clicar_buscar_cliente_versao_playstore(self, mock_time, mock_logger, mock_base_init):
        """
        Na versão Playstore, deve clicar por ID.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=False)
        page.clicar_por_texto = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.clicar_buscar_cliente()

        # Assert
        page.clicar_por_id.assert_called_once_with(VendaPage.BTN_BUSCAR_CLIENTE)


class TestVendaPageIniciarVendaSemCliente:
    """Testes para o método iniciar_venda_sem_cliente."""

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    @patch('pages.venda_page.time')
    def test_iniciar_venda_sem_cliente_versao_l400_stone(self, mock_time, mock_logger, mock_base_init):
        """
        Na versão L400/Stone, deve clicar em 'INICIAR VENDA' por texto.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()

        def texto_exibido_mock(texto, tempo_espera):
            return texto in ["Selecionar Cliente", "INICIAR VENDA"]

        page.texto_exibido = MagicMock(side_effect=texto_exibido_mock)
        page.clicar_por_texto = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.iniciar_venda_sem_cliente()

        # Assert
        page.clicar_por_texto.assert_called_once_with(VendaPage.TXT_INICIAR_VENDA_BTN)

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    @patch('pages.venda_page.time')
    def test_iniciar_venda_sem_cliente_versao_playstore(self, mock_time, mock_logger, mock_base_init):
        """
        Na versão Playstore, deve clicar por ID (button30).
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=False)
        page.clicar_por_texto = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.iniciar_venda_sem_cliente()

        # Assert
        page.clicar_por_id.assert_called_once_with(VendaPage.BTN_INICIAR_VENDA_SEM_CLIENTE)


class TestVendaPageSelecionarCliente:
    """Testes para o método selecionar_cliente."""

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    def test_selecionar_cliente_digita_pesquisa_e_confirma(self, mock_logger, mock_base_init):
        """
        Deve digitar identificador, pesquisar e confirmar.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.digitar_por_id = MagicMock()
        page.pressionar_pesquisar = MagicMock()
        page.encontrar_por_id = MagicMock()
        page.clicar_por_id = MagicMock()

        identificador = "98765"

        # Act
        page.selecionar_cliente(identificador)

        # Assert
        page.digitar_por_id.assert_called_once_with(VendaPage.EDT_BUSCA_CLIENTE, identificador)
        page.pressionar_pesquisar.assert_called_once()
        page.clicar_por_id.assert_called_once_with(VendaPage.BTN_CONFIRMAR_CLIENTE)


class TestVendaPageAdicionarProduto:
    """Testes para o método adicionar_produto."""

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    def test_adicionar_produto_clica_digita_e_seleciona(self, mock_logger, mock_base_init):
        """
        Deve clicar em adicionar, digitar código e selecionar imagem.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()

        codigo = "789"

        # Act
        page.adicionar_produto(codigo)

        # Assert
        page.clicar_por_id.assert_any_call(VendaPage.BTN_ADICIONAR_PRODUTOS)
        page.digitar_por_id.assert_called_once_with(VendaPage.EDT_BUSCA_PRODUTO, codigo)
        page.clicar_por_id.assert_any_call(VendaPage.IMG_PRODUTO)


class TestVendaPageTratarPopupBonus:
    """Testes para o método tratar_popup_bonus."""

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    @patch('pages.venda_page.time')
    def test_tratar_popup_bonus_clica_quando_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o popup de bônus está visível, deve clicar em 'Mais tarde'.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)
        page.clicar_por_id = MagicMock()

        # Act
        page.tratar_popup_bonus()

        # Assert
        page.clicar_por_id.assert_called_once_with(VendaPage.BTN_MAIS_TARDE)

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    @patch('pages.venda_page.time')
    def test_tratar_popup_bonus_ignora_quando_nao_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o popup não está visível, não deve clicar.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=False)
        page.clicar_por_id = MagicMock()

        # Act
        page.tratar_popup_bonus()

        # Assert
        page.clicar_por_id.assert_not_called()


class TestVendaPageResponderImpressao:
    """Testes para o método responder_impressao."""

    @patch('pages.venda_page.test_data')
    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    @patch('pages.venda_page.time')
    def test_responder_impressao_sim(self, mock_time, mock_logger, mock_base_init, mock_test_data):
        """
        Quando imprimir=True, deve clicar no botão SIM.
        """
        from pages.venda_page import VendaPage

        # Arrange
        mock_test_data.PRINT_DIALOG_TIMEOUT = 20
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.clicar_se_existir = MagicMock()

        # Act
        page.responder_impressao(imprimir=True)

        # Assert
        page.clicar_se_existir.assert_called_once_with(VendaPage.BTN_IMPRIMIR_SIM, tempo_espera=20)

    @patch('pages.venda_page.test_data')
    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    @patch('pages.venda_page.time')
    def test_responder_impressao_nao(self, mock_time, mock_logger, mock_base_init, mock_test_data):
        """
        Quando imprimir=False, deve clicar no botão NÃO.
        """
        from pages.venda_page import VendaPage

        # Arrange
        mock_test_data.PRINT_DIALOG_TIMEOUT = 20
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.clicar_se_existir = MagicMock()

        # Act
        page.responder_impressao(imprimir=False)

        # Assert
        page.clicar_se_existir.assert_called_once_with(VendaPage.BTN_IMPRIMIR_NAO, tempo_espera=20)


class TestVendaPageValidacoes:
    """Testes para métodos de validação."""

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    def test_venda_sucesso_exibida_retorna_true(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando mensagem de sucesso está visível.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)

        # Act
        resultado = page.venda_sucesso_exibida(timeout=10)

        # Assert
        assert resultado is True
        page.texto_exibido.assert_called_once_with("Venda realizada com sucesso!", 10)

    @patch('pages.venda_sucesso_page.VendaSucessoPage')
    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    def test_validar_sucesso_e_concluir(self, mock_logger, mock_base_init, mock_sucesso_class):
        """
        Deve aguardar texto de sucesso, processar impressões e concluir venda.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.aguardar_texto = MagicMock()
        page.concluir_venda = MagicMock()

        mock_sucesso_instance = MagicMock()
        mock_sucesso_class.return_value = mock_sucesso_instance

        # Act
        page.validar_sucesso_e_concluir()

        # Assert
        page.aguardar_texto.assert_called_once_with("Venda realizada com sucesso!")
        mock_sucesso_instance.processar_todas_impressoes.assert_called_once()
        page.concluir_venda.assert_called_once()


class TestVendaPageFluxoCliente:
    """Testes para o método executar_venda_cliente."""

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    def test_executar_venda_cliente_chama_metodos_na_ordem(self, mock_logger, mock_base_init):
        """
        Deve chamar todos os métodos do fluxo na ordem correta.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.clicar_buscar_cliente = MagicMock()
        page.selecionar_cliente = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_dinheiro = MagicMock()
        page.finalizar_venda = MagicMock()
        page.responder_impressao = MagicMock()
        page.responder_dialogo_cupom_troca = MagicMock()

        id_cliente = "42"
        codigo_produto = "888"

        # Act
        page.executar_venda_cliente(id_cliente, codigo_produto)

        # Assert
        page.clicar_buscar_cliente.assert_called_once()
        page.selecionar_cliente.assert_called_once_with(id_cliente)
        page.adicionar_produto.assert_called_once_with(codigo_produto)
        page.clicar_avancar.assert_called_once()
        page.selecionar_pagamento_dinheiro.assert_called_once()
        page.finalizar_venda.assert_called_once()
        page.responder_impressao.assert_called_once()
        page.responder_dialogo_cupom_troca.assert_called_once()


class TestVendaPageFluxoConsumidor:
    """Testes para o método executar_venda_consumidor."""

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    def test_executar_venda_consumidor_chama_metodos_na_ordem(self, mock_logger, mock_base_init):
        """
        Deve chamar todos os métodos do fluxo na ordem correta.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.iniciar_venda_sem_cliente = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_dinheiro = MagicMock()
        page.finalizar_venda = MagicMock()
        page.responder_impressao = MagicMock()
        page.responder_dialogo_cupom_troca = MagicMock()

        codigo_produto = "999"

        # Act
        page.executar_venda_consumidor(codigo_produto)

        # Assert
        page.iniciar_venda_sem_cliente.assert_called_once()
        page.adicionar_produto.assert_called_once_with(codigo_produto)
        page.clicar_avancar.assert_called_once()
        page.selecionar_pagamento_dinheiro.assert_called_once()
        page.finalizar_venda.assert_called_once()
        page.responder_impressao.assert_called_once()
        page.responder_dialogo_cupom_troca.assert_called_once()

    @patch('pages.venda_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_page.logger')
    def test_executar_venda_consumidor_usa_codigo_padrao(self, mock_logger, mock_base_init):
        """
        Deve usar código de produto padrão quando não especificado.
        """
        from pages.venda_page import VendaPage

        # Arrange
        page = VendaPage.__new__(VendaPage)
        page.driver = MagicMock()
        page.iniciar_venda_sem_cliente = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_dinheiro = MagicMock()
        page.finalizar_venda = MagicMock()
        page.responder_impressao = MagicMock()
        page.responder_dialogo_cupom_troca = MagicMock()

        # Act
        page.executar_venda_consumidor()

        # Assert
        page.adicionar_produto.assert_called_once_with("123")
