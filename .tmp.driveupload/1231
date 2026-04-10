"""
Testes unitários para PedidoPage.
Utiliza mocks para evitar interação real com Appium/emulador.
"""
import pytest
from unittest.mock import MagicMock, patch, call


class TestPedidoPageSelecionarCliente:
    """Testes para o método selecionar_cliente."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    def test_selecionar_cliente_digita_busca_e_confirma(self, mock_logger, mock_base_init):
        """
        Deve digitar o identificador, pesquisar e confirmar.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.digitar_por_id = MagicMock()
        page.pressionar_pesquisar = MagicMock()
        page.clicar_por_id = MagicMock()

        identificador = "12345"

        # Act
        page.selecionar_cliente(identificador)

        # Assert
        page.digitar_por_id.assert_called_once_with(PedidoPage.EDT_BUSCA_CLIENTE, identificador)
        page.pressionar_pesquisar.assert_called_once()
        page.clicar_por_id.assert_called_once_with(PedidoPage.BTN_CONFIRMAR_CLIENTE)


class TestPedidoPageIniciarComoConsumidor:
    """Testes para o método iniciar_como_consumidor."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    def test_iniciar_como_consumidor_rola_e_clica(self, mock_logger, mock_base_init):
        """
        Deve usar ver_e_clicar para 'Iniciar Venda' (scroll automatico se necessario).
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.ver_e_clicar = MagicMock()

        # Act
        page.iniciar_como_consumidor()

        # Assert
        page.ver_e_clicar.assert_called_once_with(PedidoPage.BTN_INICIAR_VENDA)


class TestPedidoPageAdicionarProduto:
    """Testes para o método adicionar_produto."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    @patch('pages.pedido_page.time')
    def test_adicionar_produto_clica_digita_e_seleciona(self, mock_time, mock_logger, mock_base_init):
        """
        Deve clicar em adicionar produtos, digitar código e selecionar.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()
        page.rolar_ate_id = MagicMock()

        codigo = "456"

        # Act
        page.adicionar_produto(codigo)

        # Assert
        page.clicar_por_id.assert_any_call(PedidoPage.BTN_ADICIONAR_PRODUTOS)
        page.digitar_por_id.assert_called_once_with(PedidoPage.EDT_BUSCA_PRODUTO, codigo)
        page.clicar_por_id.assert_any_call(PedidoPage.IMG_PRODUTO)

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    @patch('pages.pedido_page.time')
    def test_adicionar_produto_usa_ver_e_clicar_para_scroll_automatico(self, mock_time, mock_logger, mock_base_init):
        """
        ver_e_clicar gerencia scroll automaticamente — basta verificar que e chamado.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.ver_e_clicar = MagicMock()
        page.digitar_por_id = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.adicionar_produto("123")

        # Assert - ver_e_clicar e chamado para o botao (scroll automatico se necessario)
        page.ver_e_clicar.assert_called_once_with(PedidoPage.BTN_ADICIONAR_PRODUTOS)


class TestPedidoPageTratarPopupBonus:
    """Testes para o método tratar_popup_bonus."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    @patch('pages.pedido_page.time')
    def test_tratar_popup_bonus_clica_quando_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o popup de bônus está visível, deve clicar em 'Mais tarde'.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)
        page.clicar_por_id = MagicMock()

        # Act
        page.tratar_popup_bonus()

        # Assert
        page.texto_exibido.assert_called_once_with(PedidoPage.TXT_BONUS_DISPONIVEL, tempo_espera=3)
        page.clicar_por_id.assert_called_once_with(PedidoPage.BTN_MAIS_TARDE)

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    @patch('pages.pedido_page.time')
    def test_tratar_popup_bonus_ignora_quando_nao_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o popup de bônus não está visível, não deve clicar.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=False)
        page.clicar_por_id = MagicMock()

        # Act
        page.tratar_popup_bonus()

        # Assert
        page.clicar_por_id.assert_not_called()


class TestPedidoPageSelecaonasPagamentoDinheiro:
    """Testes para o método selecionar_pagamento_dinheiro."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    @patch('pages.pedido_page.time')
    def test_selecionar_pagamento_dinheiro_rola_clica_e_avanca(self, mock_time, mock_logger, mock_base_init):
        """
        Deve usar ver_e_clicar_texto para DINHEIRO e ver_e_clicar para avancar.
        Com cliente (padrao), deve verificar cashback ao final.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.ver_e_clicar_texto = MagicMock()
        page.ver_e_clicar = MagicMock()
        page.tratar_alerta_cashback = MagicMock()

        # Act
        page.selecionar_pagamento_dinheiro()

        # Assert
        page.ver_e_clicar_texto.assert_called_once_with("DINHEIRO")
        page.ver_e_clicar.assert_called_once_with(PedidoPage.BTN_AVANCAR)
        page.tratar_alerta_cashback.assert_called_once()

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    @patch('pages.pedido_page.time')
    def test_selecionar_pagamento_dinheiro_sem_cliente_nao_verifica_cashback(self, mock_time, mock_logger, mock_base_init):
        """
        Sem cliente (consumidor), não deve verificar cashback.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.rolar_ate_texto = MagicMock()
        page.clicar_por_texto = MagicMock()
        page.rolar_ate_id = MagicMock()
        page.clicar_por_id = MagicMock()
        page.tratar_alerta_cashback = MagicMock()

        # Act
        page.selecionar_pagamento_dinheiro(com_cliente=False)

        # Assert
        page.tratar_alerta_cashback.assert_not_called()


class TestPedidoPageFinalizarPedido:
    """Testes para o método finalizar_pedido."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    def test_finalizar_pedido_trata_bonus_e_finaliza(self, mock_logger, mock_base_init):
        """
        Deve tratar popup de bônus e clicar em finalizar.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.tratar_popup_bonus = MagicMock()
        page.rolar_ate_texto = MagicMock()
        page.rolar_ate_id = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.finalizar_pedido()

        # Assert
        page.tratar_popup_bonus.assert_called_once()
        page.clicar_por_id.assert_called_once_with(PedidoPage.BTN_FINALIZAR)


class TestPedidoPageValidacoes:
    """Testes para métodos de validação."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    def test_pedido_sucesso_exibido_retorna_true(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando mensagem de sucesso está visível.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)

        # Act
        resultado = page.pedido_sucesso_exibido(timeout=10)

        # Assert
        assert resultado is True
        page.texto_exibido.assert_called_once_with("Pedido gerado com sucesso!", 10)

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    def test_pedido_sucesso_exibido_retorna_false(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando mensagem de sucesso não está visível.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=False)

        # Act
        resultado = page.pedido_sucesso_exibido(timeout=10)

        # Assert
        assert resultado is False


class TestPedidoPageFluxoConsumidor:
    """Testes para o método executar_pedido_venda_consumidor."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    def test_executar_pedido_venda_consumidor_chama_metodos_na_ordem(self, mock_logger, mock_base_init):
        """
        Deve chamar todos os métodos do fluxo na ordem correta.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.selecionar_vendedor = MagicMock()
        page.iniciar_como_consumidor = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_dinheiro = MagicMock()
        page.finalizar_pedido = MagicMock()
        page.confirmar_pedido_gerado = MagicMock()

        codigo_produto = "999"

        # Act
        page.executar_pedido_venda_consumidor(codigo_produto)

        # Assert - verifica ordem de chamada
        page.selecionar_vendedor.assert_called_once()
        page.iniciar_como_consumidor.assert_called_once()
        page.adicionar_produto.assert_called_once_with(codigo_produto)
        page.clicar_avancar.assert_called_once()
        page.selecionar_pagamento_dinheiro.assert_called_once()
        page.finalizar_pedido.assert_called_once()
        page.confirmar_pedido_gerado.assert_called_once()


class TestPedidoPageFluxoCliente:
    """Testes para o método executar_pedido_venda_cliente."""

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    def test_executar_pedido_venda_cliente_chama_metodos_na_ordem(self, mock_logger, mock_base_init):
        """
        Deve chamar todos os métodos do fluxo na ordem correta.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.selecionar_vendedor = MagicMock()
        page.clicar_buscar_cliente = MagicMock()
        page.selecionar_cliente = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_dinheiro = MagicMock()
        page.finalizar_pedido = MagicMock()
        page.confirmar_pedido_gerado = MagicMock()

        id_cliente = "42"
        codigo_produto = "888"

        # Act
        page.executar_pedido_venda_cliente(id_cliente, codigo_produto)

        # Assert - verifica ordem de chamada
        page.selecionar_vendedor.assert_called_once()
        page.clicar_buscar_cliente.assert_called_once()
        page.selecionar_cliente.assert_called_once_with(id_cliente)
        page.adicionar_produto.assert_called_once_with(codigo_produto)
        page.clicar_avancar.assert_called_once()
        page.selecionar_pagamento_dinheiro.assert_called_once()
        page.finalizar_pedido.assert_called_once()
        page.confirmar_pedido_gerado.assert_called_once()

    @patch('pages.pedido_page.BasePage.__init__', return_value=None)
    @patch('pages.pedido_page.logger')
    def test_executar_pedido_venda_usa_valores_padrao(self, mock_logger, mock_base_init):
        """
        Deve usar valores padrão quando não especificados.
        """
        from pages.pedido_page import PedidoPage

        # Arrange
        page = PedidoPage.__new__(PedidoPage)
        page.driver = MagicMock()
        page.selecionar_vendedor = MagicMock()
        page.clicar_buscar_cliente = MagicMock()
        page.selecionar_cliente = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_dinheiro = MagicMock()
        page.finalizar_pedido = MagicMock()
        page.confirmar_pedido_gerado = MagicMock()

        # Act - usa método de compatibilidade
        page.executar_pedido_venda()

        # Assert - verifica valores padrão
        page.selecionar_cliente.assert_called_once_with("1")
        page.adicionar_produto.assert_called_once_with("123")
