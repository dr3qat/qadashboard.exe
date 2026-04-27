"""
Testes unitários para BonusPage.
Valida métodos de gerenciamento de bonus/cashback sem depender do Appium.
"""
import pytest
from unittest.mock import MagicMock, patch


class TestBonusPageBonusDisponivel:
    """Testes para o método bonus_disponivel."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_bonus_disponivel_retorna_true_quando_elemento_existe(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando o switch de bonus está presente.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)

        # Act
        resultado = page.bonus_disponivel(tempo_espera=5)

        # Assert
        assert resultado is True
        page.elemento_existe.assert_called_once_with(BonusPage.SWITCH_BONUS, 5)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_bonus_disponivel_retorna_false_quando_elemento_nao_existe(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando o switch de bonus não está presente.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=False)

        # Act
        resultado = page.bonus_disponivel(tempo_espera=3)

        # Assert
        assert resultado is False
        page.elemento_existe.assert_called_once_with(BonusPage.SWITCH_BONUS, 3)


class TestBonusPageObterValorBonus:
    """Testes para o método obter_valor_bonus."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_valor_bonus_retorna_texto_do_elemento(self, mock_logger, mock_base_init):
        """
        Deve retornar o texto do elemento quando encontrado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        mock_elemento = MagicMock()
        mock_elemento.text = "R$ 50,00"
        page.encontrar_por_id = MagicMock(return_value=mock_elemento)

        # Act
        valor = page.obter_valor_bonus()

        # Assert
        assert valor == "R$ 50,00"
        page.encontrar_por_id.assert_called_once_with(BonusPage.TXT_MAX_BONUS)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_valor_bonus_retorna_na_quando_erro(self, mock_logger, mock_base_init):
        """
        Deve retornar 'N/A' quando ocorre erro ao buscar elemento.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.encontrar_por_id = MagicMock(side_effect=Exception("Elemento não encontrado"))

        # Act
        valor = page.obter_valor_bonus()

        # Assert
        assert valor == "N/A"


class TestBonusPageBonusAtivado:
    """Testes para o método bonus_ativado."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_bonus_ativado_retorna_true_quando_checked_true(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando o switch está marcado como 'true'.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        mock_elemento = MagicMock()
        mock_elemento.get_attribute.return_value = "true"
        page.encontrar_por_id = MagicMock(return_value=mock_elemento)

        # Act
        resultado = page.bonus_ativado()

        # Assert
        assert resultado is True
        page.encontrar_por_id.assert_called_once_with(BonusPage.SWITCH_BONUS, tempo_espera=3)
        mock_elemento.get_attribute.assert_called_once_with("checked")

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_bonus_ativado_retorna_false_quando_checked_false(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando o switch está marcado como 'false'.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        mock_elemento = MagicMock()
        mock_elemento.get_attribute.return_value = "false"
        page.encontrar_por_id = MagicMock(return_value=mock_elemento)

        # Act
        resultado = page.bonus_ativado()

        # Assert
        assert resultado is False

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_bonus_ativado_retorna_false_quando_erro(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando ocorre erro ao verificar estado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.encontrar_por_id = MagicMock(side_effect=Exception("Elemento não encontrado"))

        # Act
        resultado = page.bonus_ativado()

        # Assert
        assert resultado is False


class TestBonusPageAtivarBonus:
    """Testes para o método ativar_bonus."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_ativar_bonus_clica_quando_desativado(self, mock_time, mock_logger, mock_base_init):
        """
        Deve clicar no switch quando o bonus está desativado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page._app_package = "com.test"
        page.bonus_ativado = MagicMock(return_value=False)
        page.clicar_por_id = MagicMock()
        mock_el = MagicMock()
        mock_el.text = "R$ 10,00"
        page.encontrar_por_id = MagicMock(return_value=mock_el)

        # Act
        page.ativar_bonus()

        # Assert
        page.bonus_ativado.assert_called_once()
        page.clicar_por_id.assert_called_once_with(BonusPage.SWITCH_BONUS)
        mock_time.sleep.assert_called_once_with(2)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_ativar_bonus_nao_clica_quando_ja_ativado(self, mock_time, mock_logger, mock_base_init):
        """
        Não deve clicar no switch quando o bonus já está ativado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.bonus_ativado = MagicMock(return_value=True)
        page.clicar_por_id = MagicMock()

        # Act
        page.ativar_bonus()

        # Assert
        page.bonus_ativado.assert_called_once()
        page.clicar_por_id.assert_not_called()


class TestBonusPageObterValorFinal:
    """Testes para o método obter_valor_final."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_valor_final_retorna_texto_do_elemento(self, mock_logger, mock_base_init):
        """
        Deve retornar o texto do valor final quando encontrado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        mock_elemento = MagicMock()
        mock_elemento.text = "R$ 0,00"
        page.encontrar_por_id = MagicMock(return_value=mock_elemento)

        # Act
        valor = page.obter_valor_final()

        # Assert
        assert valor == "R$ 0,00"
        page.encontrar_por_id.assert_called_once_with(BonusPage.TXT_FINAL_AMOUNT, tempo_espera=3)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_valor_final_retorna_na_quando_erro(self, mock_logger, mock_base_init):
        """
        Deve retornar 'N/A' quando ocorre erro ao buscar elemento.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.encontrar_por_id = MagicMock(side_effect=Exception("Elemento não encontrado"))

        # Act
        valor = page.obter_valor_final()

        # Assert
        assert valor == "N/A"


class TestBonusPageObterDescontoBonus:
    """Testes para o método obter_desconto_bonus."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_desconto_bonus_retorna_texto_do_elemento(self, mock_logger, mock_base_init):
        """
        Deve retornar o texto do desconto quando encontrado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        mock_elemento = MagicMock()
        mock_elemento.text = "- R$ 50,00"
        page.encontrar_por_id = MagicMock(return_value=mock_elemento)

        # Act
        texto = page.obter_desconto_bonus()

        # Assert
        assert texto == "- R$ 50,00"
        page.encontrar_por_id.assert_called_once_with(BonusPage.TXT_BONUS_COMPACT, tempo_espera=3)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_desconto_bonus_retorna_na_quando_erro(self, mock_logger, mock_base_init):
        """
        Deve retornar 'N/A' quando ocorre erro ao buscar elemento.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.encontrar_por_id = MagicMock(side_effect=Exception("Elemento não encontrado"))

        # Act
        texto = page.obter_desconto_bonus()

        # Assert
        assert texto == "N/A"


class TestBonusPageBonusFoiAplicado:
    """Testes para o método bonus_foi_aplicado."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_bonus_foi_aplicado_retorna_true_quando_valor_zerado(self, mock_time, mock_logger, mock_base_init):
        """
        Deve retornar True quando valor final está zerado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.obter_valor_final = MagicMock(return_value="R$ 0,00")
        page.obter_desconto_bonus = MagicMock(return_value="- R$ 50,00")

        # Act
        resultado = page.bonus_foi_aplicado()

        # Assert
        assert resultado is True

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_bonus_foi_aplicado_retorna_true_quando_desconto_visivel(self, mock_time, mock_logger, mock_base_init):
        """
        Deve retornar True quando desconto está visível.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.obter_valor_final = MagicMock(return_value="R$ 10,00")
        page.obter_desconto_bonus = MagicMock(return_value="- R$ 40,00")

        # Act
        resultado = page.bonus_foi_aplicado()

        # Assert
        assert resultado is True

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_bonus_foi_aplicado_retorna_false_quando_nao_aplicado(self, mock_time, mock_logger, mock_base_init):
        """
        Deve retornar False quando bonus não foi aplicado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.obter_valor_final = MagicMock(return_value="R$ 55,99")
        page.obter_desconto_bonus = MagicMock(return_value="N/A")

        # Act
        resultado = page.bonus_foi_aplicado()

        # Assert
        assert resultado is False


class TestBonusPageClicarAvancarPagamento:
    """Testes para o método clicar_avancar_pagamento."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_clicar_avancar_pagamento_clica_e_rola_ate_finalizar(self, mock_time, mock_logger, mock_base_init):
        """
        Deve clicar no botão e rolar até encontrar 'Finalizar'.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.rolar_ate_texto = MagicMock()

        # Act
        page.clicar_avancar_pagamento()

        # Assert
        page.clicar_por_id.assert_called_once_with(BonusPage.BTN_PROCEED)
        page.rolar_ate_texto.assert_called_once_with("Finalizar")

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_clicar_avancar_pagamento_tenta_confirmar_se_finalizar_falha(self, mock_time, mock_logger, mock_base_init):
        """
        Deve tentar 'Confirmar' se 'Finalizar' não for encontrado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.rolar_ate_texto = MagicMock(side_effect=[Exception("Não encontrado"), None])

        # Act
        page.clicar_avancar_pagamento()

        # Assert
        assert page.rolar_ate_texto.call_count == 2
        page.rolar_ate_texto.assert_any_call("Finalizar")
        page.rolar_ate_texto.assert_any_call("Confirmar")


class TestBonusPageAdicionarProduto:
    """Testes para o método adicionar_produto."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_adicionar_produto_usa_codigo_informado(self, mock_logger, mock_base_init):
        """
        Deve adicionar produto com código informado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()

        codigo = "456"

        # Act
        page.adicionar_produto(codigo)

        # Assert
        page.clicar_por_id.assert_any_call(BonusPage.BTN_ADICIONAR_PRODUTOS)
        page.digitar_por_id.assert_called_once_with("editText", codigo)
        page.clicar_por_id.assert_any_call("imageView3")

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_adicionar_produto_usa_codigo_padrao(self, mock_logger, mock_base_init):
        """
        Deve usar código padrão '123' quando não especificado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()

        # Act
        page.adicionar_produto()

        # Assert
        page.digitar_por_id.assert_called_once_with("editText", "123")


class TestBonusPageClicarAvancarCarrinho:
    """Testes para o método clicar_avancar_carrinho."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_clicar_avancar_carrinho_encontra_e_clica(self, mock_time, mock_logger, mock_base_init):
        """
        Deve encontrar elemento clicável e clicar.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        mock_elemento = MagicMock()
        page.encontrar_clicavel_por_id = MagicMock(return_value=mock_elemento)

        # Act
        page.clicar_avancar_carrinho()

        # Assert
        page.encontrar_clicavel_por_id.assert_called_once_with(BonusPage.BTN_PROXIMO)
        mock_elemento.click.assert_called_once()


class TestBonusPageBuscarClientePorCpf:
    """Testes para o método buscar_cliente_por_cpf."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_buscar_cliente_por_cpf_executa_fluxo_completo(self, mock_time, mock_logger, mock_base_init):
        """
        Deve executar fluxo completo de busca de cliente.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.clicar_por_id = MagicMock()
        page.digitar_por_id = MagicMock()
        page.pressionar_pesquisar = MagicMock()

        cpf = "12345678900"

        # Act
        page.buscar_cliente_por_cpf(cpf)

        # Assert
        page.clicar_por_id.assert_any_call(BonusPage.BTN_BUSCAR_CLIENTE)
        page.digitar_por_id.assert_called_once_with("search_src_text", cpf)
        page.pressionar_pesquisar.assert_called_once()
        page.clicar_por_id.assert_any_call("button3")


class TestBonusPageResponderImpressao:
    """Testes para o método responder_impressao."""

    @patch('pages.bonus_page.test_data')
    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_responder_impressao_sim(self, mock_logger, mock_base_init, mock_test_data):
        """Quando imprimir=True, deve delegar ao event-driven com imprimir_cupom=True."""
        from pages.bonus_page import BonusPage

        mock_test_data.PRINT_CUPOM_VENDA = True
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page._aguardar_sucesso_event_driven = MagicMock()

        page.responder_impressao(imprimir=True)

        page._aguardar_sucesso_event_driven.assert_called_once_with(imprimir_cupom=True, timeout=45)

    @patch('pages.bonus_page.test_data')
    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_responder_impressao_nao(self, mock_logger, mock_base_init, mock_test_data):
        """Quando imprimir=False, deve delegar ao event-driven com imprimir_cupom=False."""
        from pages.bonus_page import BonusPage

        mock_test_data.PRINT_CUPOM_VENDA = False
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page._aguardar_sucesso_event_driven = MagicMock()

        page.responder_impressao(imprimir=False)

        page._aguardar_sucesso_event_driven.assert_called_once_with(imprimir_cupom=False, timeout=45)


class TestBonusPageCashbackDisponivel:
    """Testes para o método cashback_disponivel."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_cashback_disponivel_retorna_true_quando_elemento_existe(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando o ícone de cashback está presente.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)

        # Act
        resultado = page.cashback_disponivel(tempo_espera=5)

        # Assert
        assert resultado is True
        page.elemento_existe.assert_called_once_with(BonusPage.ICON_CASHBACK, 5)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_cashback_disponivel_retorna_false_quando_elemento_nao_existe(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando o ícone de cashback não está presente.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=False)

        # Act
        resultado = page.cashback_disponivel(tempo_espera=3)

        # Assert
        assert resultado is False
        page.elemento_existe.assert_called_once_with(BonusPage.ICON_CASHBACK, 3)


class TestBonusPageObterValorCashback:
    """Testes para o método obter_valor_cashback."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_valor_cashback_retorna_texto_quando_encontrado(self, mock_logger, mock_base_init):
        """
        Deve retornar o valor do cashback quando encontrado.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)
        mock_elemento = MagicMock()
        mock_elemento.text = "R$ 25,00"
        page.encontrar_clicavel_por_id = MagicMock(return_value=mock_elemento)

        # Act
        valor = page.obter_valor_cashback()

        # Assert
        assert valor == "R$ 25,00"
        page.elemento_existe.assert_called_once_with(BonusPage.ICON_CASHBACK, tempo_espera=5)
        page.encontrar_clicavel_por_id.assert_called_once_with(BonusPage.VALOR_CASHBACK, tempo_espera=3)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_valor_cashback_lanca_erro_quando_icone_nao_existe(self, mock_logger, mock_base_init):
        """
        Deve lançar exceção quando ícone não está presente.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=False)

        # Act & Assert
        with pytest.raises(Exception, match="Ícone de cashback .* não foi encontrado"):
            page.obter_valor_cashback()

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_obter_valor_cashback_lanca_erro_quando_valor_vazio(self, mock_logger, mock_base_init):
        """
        Deve lançar exceção quando valor está vazio.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.elemento_existe = MagicMock(return_value=True)
        mock_elemento = MagicMock()
        mock_elemento.text = ""
        page.encontrar_clicavel_por_id = MagicMock(return_value=mock_elemento)

        # Act & Assert
        with pytest.raises(Exception, match="campo de cashback .* está VAZIO"):
            page.obter_valor_cashback()


class TestBonusPageValidacoes:
    """Testes para métodos de validação."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_tela_pagamento_exibida_retorna_true(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando tela de pagamento está visível.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)

        # Act
        resultado = page.tela_pagamento_exibida(timeout=10)

        # Assert
        assert resultado is True
        page.texto_exibido.assert_called_once_with("Forma de Pagamento", 10)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_venda_sucesso_exibida_retorna_true_com_mensagem_completa(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando mensagem completa de sucesso está visível.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(return_value=True)

        # Act
        resultado = page.venda_sucesso_exibida(timeout=15)

        # Assert
        assert resultado is True

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    def test_venda_sucesso_exibida_retorna_true_com_mensagem_parcial(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando palavra 'sucesso' está visível.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.texto_exibido = MagicMock(side_effect=[False, True])

        # Act
        resultado = page.venda_sucesso_exibida(timeout=15)

        # Assert
        assert resultado is True

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_concluir_venda_clica_em_confirmar_venda(self, mock_time, mock_logger, mock_base_init):
        """
        Deve usar ver_e_clicar para clicar em confirmar venda (scroll automático se necessário).
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.ver_e_clicar = MagicMock()

        # Act
        page.concluir_venda()

        # Assert
        page.ver_e_clicar.assert_called_once_with(BonusPage.BTN_CONFIRMAR_VENDA)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_concluir_venda_clica_em_finalizar_se_confirmar_falha(self, mock_time, mock_logger, mock_base_init):
        """
        Deve tentar clicar em BTN_FINALIZAR se BTN_CONFIRMAR_VENDA falhar.
        """
        from pages.bonus_page import BonusPage

        # Arrange
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.rolar_ate_texto = MagicMock()
        page.clicar_por_id = MagicMock(side_effect=[Exception("Não encontrado"), None])

        # Act
        page.concluir_venda()

        # Assert
        assert page.clicar_por_id.call_count == 2
        page.clicar_por_id.assert_any_call(BonusPage.BTN_CONFIRMAR_VENDA)
        page.clicar_por_id.assert_any_call(BonusPage.BTN_FINALIZAR)
