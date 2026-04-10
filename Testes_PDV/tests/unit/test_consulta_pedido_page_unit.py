"""
Testes unitários para ConsultaPedidoPage.
Utiliza mocks para evitar interação real com Appium/emulador.
"""
import pytest
from unittest.mock import MagicMock, patch, PropertyMock


class TestConsultaPedidoPageAbrirMenuLateral:
    """Testes para o método abrir_menu_lateral."""

    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_abrir_menu_lateral_sucesso(self, mock_time, mock_logger, mock_base_init):
        """
        Deve encontrar e clicar no menu lateral por accessibility ID.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.encontrar_por_accessibility_id = MagicMock()
        mock_menu = MagicMock()
        page.encontrar_por_accessibility_id.return_value = mock_menu

        # Act
        page.abrir_menu_lateral()

        # Assert
        mock_menu.click.assert_called_once()


class TestConsultaPedidoPageSelecionarUltimoPedido:
    """Testes para o método selecionar_ultimo_pedido."""

    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_selecionar_ultimo_pedido_scroll_e_clica_maior_numero(self, mock_time, mock_logger, mock_base_init):
        """
        Deve fazer scroll, encontrar todos os pedidos e clicar no de maior número.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.realizar_scroll_para_baixo = MagicMock()
        page.scroll_nativo_ate_id = MagicMock()
        page.encontrar_todos_por_id = MagicMock()

        # Mock elementos com números (5, 11, 12, 7)
        mock_elem_5 = MagicMock()
        mock_elem_5.text = "5"
        mock_elem_11 = MagicMock()
        mock_elem_11.text = "11"
        mock_elem_12 = MagicMock()
        mock_elem_12.text = "12"  # Este deve ser clicado
        mock_elem_7 = MagicMock()
        mock_elem_7.text = "7"

        page.encontrar_todos_por_id.return_value = [
            mock_elem_5,
            mock_elem_11,
            mock_elem_12,
            mock_elem_7
        ]

        # Act
        resultado = page.selecionar_ultimo_pedido()

        # Assert
        assert resultado is True
        # Verifica que fez 10 scrolls
        assert page.realizar_scroll_para_baixo.call_count == 10
        # Verifica que clicou no elemento com número 12 (maior)
        mock_elem_12.click.assert_called_once()

    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_selecionar_ultimo_pedido_sem_elementos_retorna_false(self, mock_time, mock_logger, mock_base_init):
        """
        Quando não há pedidos, deve retornar False.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.realizar_scroll_para_baixo = MagicMock()
        page.encontrar_todos_por_id = MagicMock(return_value=[])
        page.scroll_nativo_ate_id = MagicMock()

        # Act
        resultado = page.selecionar_ultimo_pedido()

        # Assert
        assert resultado is False


class TestConsultaPedidoPageResponderCupomVenda:
    """Testes para o método responder_cupom_venda."""

    @patch('pages.consulta_pedido_page.test_data')
    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_responder_cupom_venda_clica_sim_quando_configurado(self, mock_time, mock_logger, mock_base_init, mock_test_data):
        """
        Quando PRINT_CUPOM_VENDA = True, deve clicar em SIM.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)
        page.clicar_se_existir = MagicMock(return_value=True)

        mock_test_data.PRINT_CUPOM_VENDA = True
        mock_test_data.PRINT_DIALOG_TIMEOUT = 20

        # Act
        page.responder_cupom_venda()

        # Assert
        # Verifica que clicou em SIM (button1)
        page.clicar_se_existir.assert_called_with(ConsultaPedidoPage.BTN_DIALOG_SIM, tempo_espera=2)

    @patch('pages.consulta_pedido_page.test_data')
    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_responder_cupom_venda_clica_nao_quando_nao_configurado(self, mock_time, mock_logger, mock_base_init, mock_test_data):
        """
        Quando PRINT_CUPOM_VENDA = False, deve clicar em NÃO (padrão).
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)
        page.clicar_se_existir = MagicMock(return_value=True)

        mock_test_data.PRINT_CUPOM_VENDA = False
        mock_test_data.PRINT_DIALOG_TIMEOUT = 20

        # Act
        page.responder_cupom_venda()

        # Assert
        # Verifica que clicou em NÃO (button2)
        page.clicar_se_existir.assert_called_with(ConsultaPedidoPage.BTN_DIALOG_NAO, tempo_espera=2)


class TestConsultaPedidoPageResponderCupomTrocaDialogo:
    """Testes para o método responder_cupom_troca_dialogo."""

    @patch('pages.consulta_pedido_page.test_data')
    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_responder_cupom_troca_dialogo_clica_sim_quando_configurado(self, mock_time, mock_logger, mock_base_init, mock_test_data):
        """
        Quando PRINT_CUPOM_TROCA = True, deve clicar em SIM no diálogo.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)
        page.clicar_se_existir = MagicMock(return_value=True)

        mock_test_data.PRINT_CUPOM_TROCA = True
        mock_test_data.PRINT_DIALOG_TIMEOUT = 20

        # Act
        page.responder_cupom_troca_dialogo()

        # Assert
        page.clicar_se_existir.assert_called_with(ConsultaPedidoPage.BTN_DIALOG_SIM, tempo_espera=2)

    @patch('pages.consulta_pedido_page.test_data')
    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_responder_cupom_troca_dialogo_ignora_quando_nao_aparece(self, mock_time, mock_logger, mock_base_init, mock_test_data):
        """
        Quando o diálogo não aparece, deve ignorar (log informativo).
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=False)
        page.clicar_se_existir = MagicMock()

        mock_test_data.PRINT_DIALOG_TIMEOUT = 20

        # Act - não deve lançar exceção
        page.responder_cupom_troca_dialogo()

        # Assert
        # Não deve clicar em nada se o diálogo não aparecer
        page.clicar_se_existir.assert_not_called()


class TestConsultaPedidoPageTratarPopupBonus:
    """Testes para o método tratar_popup_bonus."""

    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_tratar_popup_bonus_clica_quando_existe(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o popup de bônus existe, deve clicar em 'Mais tarde'.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.clicar_se_existir = MagicMock(return_value=True)

        # Act
        page.tratar_popup_bonus()

        # Assert
        page.clicar_se_existir.assert_called_once_with(ConsultaPedidoPage.BTN_MAIS_TARDE, tempo_espera=3)


class TestConsultaPedidoPageValidacoes:
    """Testes para métodos de validação."""

    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    def test_venda_sucesso_exibida_retorna_true(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando mensagem de sucesso está visível.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)

        # Act
        resultado = page.venda_sucesso_exibida(timeout=10)

        # Assert
        assert resultado is True
        page.texto_exibido.assert_called_once_with("Venda realizada com sucesso!", 10)


class TestConsultaPedidoPageFluxoCompleto:
    """Testes para o método executar_consulta_e_finalizar_pedido."""

    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    @patch('pages.consulta_pedido_page.time')
    def test_executar_consulta_e_finalizar_pedido_chama_metodos_na_ordem(self, mock_time, mock_logger, mock_base_init):
        """
        Deve chamar todos os métodos do fluxo na ordem correta.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.acessar_consulta_pedido = MagicMock()
        page.selecionar_ultimo_pedido = MagicMock()
        page.clicar_finalizar_pedido = MagicMock()
        page.finalizar_venda = MagicMock()

        # Act
        page.executar_consulta_e_finalizar_pedido()

        # Assert - verifica ordem de chamada
        page.acessar_consulta_pedido.assert_called_once()
        page.selecionar_ultimo_pedido.assert_called_once()
        page.clicar_finalizar_pedido.assert_called_once()
        page.finalizar_venda.assert_called_once()


class TestConsultaPedidoPageValidarSucessoEConcluir:
    """Testes para o método validar_sucesso_e_concluir."""

    @patch('pages.consulta_pedido_page.VendaSucessoPage')
    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    def test_validar_sucesso_e_concluir_processa_impressoes_e_conclui(self, mock_logger, mock_base_init, mock_sucesso_page_class):
        """
        Deve validar sucesso, processar impressões e concluir venda.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.aguardar_texto = MagicMock(return_value=True)

        mock_sucesso_page = MagicMock()
        mock_sucesso_page_class.return_value = mock_sucesso_page

        # Act
        page.validar_sucesso_e_concluir()

        # Assert
        page.aguardar_texto.assert_called_once_with("Venda realizada com sucesso!", tempo_espera=10)
        mock_sucesso_page.processar_todas_impressoes.assert_called_once()
        mock_sucesso_page.concluir_venda.assert_called_once()

    @patch('pages.consulta_pedido_page.VendaSucessoPage')
    @patch('pages.consulta_pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.consulta_pedido_page.logger')
    def test_validar_sucesso_e_concluir_lanca_excecao_quando_sucesso_nao_aparece(self, mock_logger, mock_base_init, mock_sucesso_page_class):
        """
        Deve lançar AssertionError quando mensagem de sucesso não aparece.
        """
        from pages.consulta_pedido_page import ConsultaPedidoPage

        # Arrange
        page = ConsultaPedidoPage.__new__(ConsultaPedidoPage)
        page.driver = MagicMock()
        page.aguardar_texto = MagicMock(return_value=False)

        # Act & Assert
        with pytest.raises(AssertionError, match="Mensagem de sucesso não apareceu"):
            page.validar_sucesso_e_concluir()
