"""
Testes unitários para VendaFuturaPage.
Utiliza mocks para evitar interação real com Appium/emulador.
"""
import pytest
from unittest.mock import MagicMock, patch


class TestVendaFuturaPageSelecionarRetiradaLoja:
    """Testes para o método selecionar_retirada_loja."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_selecionar_retirada_loja_clica_sem_scroll(self, mock_logger, mock_base_init):
        """
        Deve clicar diretamente no botão (sem scroll).
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()

        # Act
        page.selecionar_retirada_loja()

        # Assert
        page.clicar_por_id.assert_called_once_with(VendaFuturaPage.BTN_VENDA_FUTURA_LOJA)


class TestVendaFuturaPageSelecionarEntregaDomicilio:
    """Testes para o método selecionar_entrega_domicilio."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_selecionar_entrega_domicilio_clica_e_avanca_frete(self, mock_logger, mock_base_init):
        """
        Deve clicar no botão e avançar frete (sem scrolls).
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.clicar_por_texto = MagicMock()

        # Act
        page.selecionar_entrega_domicilio()

        # Assert
        page.clicar_por_id.assert_called_once_with(VendaFuturaPage.BTN_VENDA_FUTURA_DOMICILIO)
        page.clicar_por_texto.assert_called_once_with("Avançar")


class TestVendaFuturaPageBuscarClienteCpf:
    """Testes para o método buscar_cliente_cpf."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_buscar_cliente_cpf_clica_digita_e_confirma(self, mock_logger, mock_base_init):
        """
        Deve clicar no campo, digitar CPF e confirmar.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()

        cpf = "12345678901"

        # Act
        page.buscar_cliente_cpf(cpf)

        # Assert
        page.clicar_por_id.assert_any_call(VendaFuturaPage.EDT_CPF)
        page.digitar_por_id.assert_called_once_with(VendaFuturaPage.EDT_CPF, cpf)
        page.clicar_por_id.assert_any_call(VendaFuturaPage.BTN_CONFIRMAR_CPF)

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_buscar_cliente_cpf_usa_valor_padrao(self, mock_logger, mock_base_init):
        """
        Deve usar CPF padrão '1' quando não especificado.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()

        # Act
        page.buscar_cliente_cpf()

        # Assert
        page.digitar_por_id.assert_called_once_with(VendaFuturaPage.EDT_CPF, "1")


class TestVendaFuturaPageAdicionarProduto:
    """Testes para o método adicionar_produto."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_adicionar_produto_com_tamanho(self, mock_logger, mock_base_init):
        """
        Deve adicionar produto e selecionar tamanho (sem scrolls).
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()
        page.clicar_por_texto = MagicMock()

        codigo = "456"
        tamanho = "38"

        # Act
        page.adicionar_produto(codigo, tamanho)

        # Assert
        page.clicar_por_id.assert_any_call(VendaFuturaPage.BTN_ADICIONAR_PRODUTOS)
        page.digitar_por_id.assert_called_once_with(VendaFuturaPage.EDT_BUSCA_PRODUTO, codigo)
        page.clicar_por_id.assert_any_call(VendaFuturaPage.IMG_PRODUTO)
        page.clicar_por_texto.assert_called_once_with(tamanho)


class TestVendaFuturaPageSelecionarPagamentoAvista:
    """Testes para o método selecionar_pagamento_avista."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    @patch('pages.venda_futura_page.time')
    def test_selecionar_pagamento_avista_seleciona_movimento_e_plano(self, mock_time, mock_logger, mock_base_init):
        """
        Deve clicar em pagamento personalizado, selecionar A VISTA no
        Movimento de Caixa e depois A VISTA no Plano de Venda.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.contar_elementos_visiveis_por_texto = MagicMock(return_value=2)
        page.clicar_no_enesimo_texto = MagicMock()
        page.clicar_por_texto = MagicMock()

        # Act
        page.selecionar_pagamento_avista()

        # Assert
        page.clicar_por_id.assert_any_call(VendaFuturaPage.TXT_PAGAMENTO_TITULO)
        # Assert para primeira tentativa (via índice) - Movimento de Caixa
        page.clicar_no_enesimo_texto.assert_any_call("A VISTA", indice=0, tempo_espera=5)
        # Assert para clique no Plano de Venda (segundo A VISTA)
        page.clicar_no_enesimo_texto.assert_any_call("A VISTA", indice=1, tempo_espera=3)
        page.clicar_por_id.assert_any_call(VendaFuturaPage.BTN_AVANCAR)

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    @patch('pages.venda_futura_page.time')
    def test_selecionar_pagamento_avista_scroll_quando_nao_encontra(self, mock_time, mock_logger, mock_base_init):
        """
        Quando A VISTA não é encontrado imediatamente, deve fazer scroll.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.contar_elementos_visiveis_por_texto = MagicMock(side_effect=[2, 1])
        page.clicar_no_enesimo_texto = MagicMock(side_effect=[Exception("Not found"), None])
        page.rolar_ate_texto = MagicMock()
        page.clicar_por_texto = MagicMock()

        # Act
        page.selecionar_pagamento_avista()

        # Assert
        # Assert que tentou primeiro via índice (e falhou) e depois tentou novamente
        assert page.clicar_no_enesimo_texto.call_count == 2
        page.clicar_no_enesimo_texto.assert_any_call("A VISTA", indice=0, tempo_espera=5)
        page.clicar_no_enesimo_texto.assert_any_call("A VISTA", indice=0, tempo_espera=3)
        # Assert que usou fallback (scroll + clique simples) entre as tentativas
        page.rolar_ate_texto.assert_called_once_with("A VISTA")
        page.clicar_por_texto.assert_called_once_with("A VISTA")


class TestVendaFuturaPageTratarAlertaCashback:
    """Testes para o método tratar_alerta_cashback."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    @patch('pages.venda_futura_page.time')
    def test_tratar_alerta_cashback_clica_ok_quando_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o alerta de cashback está visível, deve clicar em OK.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)
        page.clicar_por_id = MagicMock()

        # Act
        page.tratar_alerta_cashback()

        # Assert
        page.clicar_por_id.assert_called_once_with(VendaFuturaPage.BTN_CONFIRMAR_CASHBACK)

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    @patch('pages.venda_futura_page.time')
    def test_tratar_alerta_cashback_ignora_quando_nao_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o alerta não está visível, não deve clicar.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=False)
        page.clicar_por_id = MagicMock()

        # Act
        page.tratar_alerta_cashback()

        # Assert
        page.clicar_por_id.assert_not_called()


class TestVendaFuturaPageTratarPopupBonus:
    """Testes para o método tratar_popup_bonus."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    @patch('pages.venda_futura_page.time')
    def test_tratar_popup_bonus_clica_quando_existe(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o popup existe, deve clicar em 'Mais tarde'.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_se_existir = MagicMock(return_value=True)

        # Act
        page.tratar_popup_bonus()

        # Assert
        page.clicar_se_existir.assert_called_once_with(VendaFuturaPage.BTN_MAIS_TARDE, tempo_espera=4)

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    @patch('pages.venda_futura_page.time')
    def test_tratar_popup_bonus_ignora_quando_nao_existe(self, mock_time, mock_logger, mock_base_init):
        """
        Quando o popup não existe, deve apenas logar.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_se_existir = MagicMock(return_value=False)

        # Act - não deve lançar exceção
        page.tratar_popup_bonus()

        # Assert
        page.clicar_se_existir.assert_called_once()


class TestVendaFuturaPageSelecionarFormaDinheiro:
    """Testes para o método selecionar_forma_dinheiro."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_selecionar_forma_dinheiro_clica_sem_scroll(self, mock_logger, mock_base_init):
        """
        Deve selecionar forma DINHEIRO e clicar em Pagar (sem scrolls).
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.clicar_por_texto = MagicMock()

        # Act
        page.selecionar_forma_dinheiro()

        # Assert
        page.clicar_por_id.assert_any_call(VendaFuturaPage.IMG_PAGAMENTOS)
        page.clicar_por_texto.assert_called_once_with("DINHEIRO")
        page.clicar_por_id.assert_any_call(VendaFuturaPage.BTN_PAGAR)


class TestVendaFuturaPageValidacoes:
    """Testes para métodos de validação."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_venda_sucesso_exibida_retorna_true(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando mensagem de sucesso está visível.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)

        # Act
        resultado = page.venda_sucesso_exibida(timeout=10)

        # Assert
        assert resultado is True
        page.texto_exibido.assert_called_once_with("Venda realizada com sucesso!", 10)

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_validar_sucesso_e_concluir(self, mock_logger, mock_base_init):
        """
        Deve aguardar texto e chamar concluir_venda.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.aguardar_texto = MagicMock()
        page.concluir_venda = MagicMock()

        # Act
        page.validar_sucesso_e_concluir()

        # Assert
        page.aguardar_texto.assert_called_once_with("Venda realizada com sucesso!")
        page.concluir_venda.assert_called_once()


class TestVendaFuturaPageFluxoRetiradaLoja:
    """Testes para o método executar_venda_futura."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_executar_venda_futura_chama_metodos_na_ordem(self, mock_logger, mock_base_init):
        """
        Deve chamar todos os métodos do fluxo na ordem correta.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.selecionar_retirada_loja = MagicMock()
        page.avancar_tipo_entrega = MagicMock()
        page.selecionar_vendedor = MagicMock()
        page.buscar_cliente_cpf = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_avista = MagicMock()
        page.tratar_alerta_cashback = MagicMock()
        page.tratar_popup_bonus = MagicMock()
        page.selecionar_forma_dinheiro = MagicMock()
        page.finalizar_venda = MagicMock()
        page.responder_impressao = MagicMock()

        cpf = "98765"
        codigo = "111"
        tamanho = "40"

        # Act
        page.executar_venda_futura(cpf, codigo, tamanho)

        # Assert
        page.selecionar_retirada_loja.assert_called_once()
        page.avancar_tipo_entrega.assert_called_once()
        page.selecionar_vendedor.assert_called_once()
        page.buscar_cliente_cpf.assert_called_once_with(cpf)
        page.adicionar_produto.assert_called_once_with(codigo, tamanho)
        page.clicar_avancar.assert_called_once()
        page.selecionar_pagamento_avista.assert_called_once()
        page.tratar_alerta_cashback.assert_called_once()
        page.tratar_popup_bonus.assert_called_once()
        page.selecionar_forma_dinheiro.assert_called_once()
        page.finalizar_venda.assert_called_once()
        page.responder_impressao.assert_called_once()


class TestVendaFuturaPageFluxoDomicilio:
    """Testes para o método executar_venda_futura_domicilio."""

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_executar_venda_futura_domicilio_chama_metodos_na_ordem(self, mock_logger, mock_base_init):
        """
        Deve chamar todos os métodos do fluxo domicílio na ordem correta.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.selecionar_entrega_domicilio = MagicMock()
        page.selecionar_vendedor = MagicMock()
        page.buscar_cliente_cpf = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_avista = MagicMock()
        page.tratar_alerta_cashback = MagicMock()
        page.tratar_popup_bonus = MagicMock()
        page.selecionar_forma_dinheiro = MagicMock()
        page.finalizar_venda = MagicMock()
        page.responder_impressao = MagicMock()

        cpf = "12345"
        codigo = "222"
        tamanho = "42"

        # Act
        page.executar_venda_futura_domicilio(cpf, codigo, tamanho)

        # Assert
        page.selecionar_entrega_domicilio.assert_called_once()
        page.selecionar_vendedor.assert_called_once()
        page.buscar_cliente_cpf.assert_called_once_with(cpf)
        page.adicionar_produto.assert_called_once_with(codigo, tamanho)
        page.clicar_avancar.assert_called_once()
        page.selecionar_pagamento_avista.assert_called_once()
        page.tratar_alerta_cashback.assert_called_once()
        page.tratar_popup_bonus.assert_called_once()
        page.selecionar_forma_dinheiro.assert_called_once()
        page.finalizar_venda.assert_called_once()
        page.responder_impressao.assert_called_once()

    @patch('pages.venda_futura_page.BasePage.__init__', return_value=None)
    @patch('pages.venda_futura_page.logger')
    def test_executar_venda_futura_domicilio_usa_valores_padrao(self, mock_logger, mock_base_init):
        """
        Deve usar valores padrão quando não especificados.
        """
        from pages.venda_futura_page import VendaFuturaPage

        # Arrange
        page = VendaFuturaPage.__new__(VendaFuturaPage)
        page.driver = MagicMock()
        page.selecionar_entrega_domicilio = MagicMock()
        page.selecionar_vendedor = MagicMock()
        page.buscar_cliente_cpf = MagicMock()
        page.adicionar_produto = MagicMock()
        page.clicar_avancar = MagicMock()
        page.selecionar_pagamento_avista = MagicMock()
        page.tratar_alerta_cashback = MagicMock()
        page.tratar_popup_bonus = MagicMock()
        page.selecionar_forma_dinheiro = MagicMock()
        page.finalizar_venda = MagicMock()
        page.responder_impressao = MagicMock()

        # Act
        page.executar_venda_futura_domicilio()

        # Assert - verifica valores padrão
        page.buscar_cliente_cpf.assert_called_once_with("1")
        page.adicionar_produto.assert_called_once_with("1234", "38")
