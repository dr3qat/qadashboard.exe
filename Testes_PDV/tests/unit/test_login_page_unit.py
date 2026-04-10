"""
Testes unitários para LoginPage.
Utiliza mocks para evitar interação real com Appium/emulador.
"""
import pytest
from unittest.mock import MagicMock, patch


class TestLoginPageConfigurarConexao:
    """Testes para o método configurar_conexao_se_necessario."""

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_configurar_conexao_quando_botao_existe_retorna_true(self, mock_logger, mock_base_init):
        """
        Quando o botão de configurar conexão existe e é clicável,
        deve configurar IP/porta e retornar True.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()

        # Mock dos métodos herdados de BasePage
        login_page.clicar_se_existir = MagicMock(return_value=True)
        login_page.digitar_por_id = MagicMock()
        login_page.clicar_por_id = MagicMock()

        ip = "192.168.1.100"
        porta = "8080"

        # Act
        resultado = login_page.configurar_conexao_se_necessario(ip, porta)

        # Assert
        assert resultado is True
        login_page.clicar_se_existir.assert_called_once_with(
            LoginPage.BTN_CONFIGURAR_CONEXAO, tempo_espera=3
        )
        login_page.digitar_por_id.assert_any_call(LoginPage.EDT_IP_SERVIDOR, ip)
        login_page.digitar_por_id.assert_any_call(LoginPage.EDT_GATEWAY_SERVIDOR, porta)
        login_page.clicar_por_id.assert_called_once_with(LoginPage.BTN_SALVAR_DIALOGO)

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_configurar_conexao_quando_botao_nao_existe_retorna_false(self, mock_logger, mock_base_init):
        """
        Quando o botão de configurar conexão NÃO existe,
        deve retornar False sem tentar configurar.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()

        # Botão não existe
        login_page.clicar_se_existir = MagicMock(return_value=False)
        login_page.digitar_por_id = MagicMock()
        login_page.clicar_por_id = MagicMock()

        ip = "192.168.1.100"
        porta = "8080"

        # Act
        resultado = login_page.configurar_conexao_se_necessario(ip, porta)

        # Assert
        assert resultado is False
        login_page.clicar_se_existir.assert_called_once()
        login_page.digitar_por_id.assert_not_called()
        login_page.clicar_por_id.assert_not_called()


class TestLoginPageGarantirLogin:
    """Testes para o método garantir_login."""

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_garantir_login_quando_ja_logado_retorna_true_imediatamente(self, mock_logger, mock_base_init):
        """
        Quando o usuário JÁ está logado (esta_logado retorna True),
        deve retornar True imediatamente sem executar o fluxo de login.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()

        # Usuário já está logado
        login_page.esta_logado = MagicMock(return_value=True)
        login_page.pular_telas_introducao = MagicMock()
        login_page.configurar_conexao_se_necessario = MagicMock()
        login_page.preencher_credenciais = MagicMock()
        login_page.clicar_entrar = MagicMock()

        # Act
        resultado = login_page.garantir_login(
            ip="192.168.1.100",
            porta="8080",
            empresa="EMPRESA",
            usuario="USUARIO",
            senha="SENHA"
        )

        # Assert
        assert resultado is True
        login_page.esta_logado.assert_called_once_with(timeout=5)
        # Não deve chamar o fluxo de login
        login_page.pular_telas_introducao.assert_not_called()
        login_page.configurar_conexao_se_necessario.assert_not_called()
        login_page.preencher_credenciais.assert_not_called()
        login_page.clicar_entrar.assert_not_called()

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_garantir_login_quando_nao_logado_executa_fluxo_completo(self, mock_logger, mock_base_init):
        """
        Quando o usuário NÃO está logado,
        deve executar o fluxo completo de login.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()

        # Usuário NÃO está logado
        login_page.esta_logado = MagicMock(return_value=False)
        login_page.pular_telas_introducao = MagicMock()
        login_page.configurar_conexao_se_necessario = MagicMock()
        login_page.preencher_credenciais = MagicMock()
        login_page.clicar_entrar = MagicMock()

        ip = "192.168.1.100"
        porta = "8080"
        empresa = "EMPRESA"
        usuario = "USUARIO"
        senha = "SENHA"

        # Act
        resultado = login_page.garantir_login(
            ip=ip,
            porta=porta,
            empresa=empresa,
            usuario=usuario,
            senha=senha
        )

        # Assert
        assert resultado is True
        login_page.esta_logado.assert_called_once_with(timeout=5)
        # Deve chamar todo o fluxo de login
        login_page.pular_telas_introducao.assert_called_once()
        login_page.configurar_conexao_se_necessario.assert_called_once_with(ip, porta)
        login_page.preencher_credenciais.assert_called_once_with(empresa, usuario, senha)
        login_page.clicar_entrar.assert_called_once()


class TestLoginPageEstaLogado:
    """Testes para o método esta_logado."""

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_esta_logado_retorna_true_quando_iniciar_venda_visivel(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando texto 'Iniciar Venda' está visível.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()

        # "Iniciar Venda" está visível
        login_page.texto_exibido = MagicMock(side_effect=lambda texto, timeout: texto == "Iniciar Venda")

        # Act
        resultado = login_page.esta_logado(timeout=5)

        # Assert
        assert resultado is True

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_esta_logado_retorna_true_quando_venda_visivel(self, mock_logger, mock_base_init):
        """
        Deve retornar True quando texto 'Venda' está visível (segunda condição).
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()

        # "Iniciar Venda" não está visível, mas "Venda" está
        def texto_exibido_mock(texto, timeout):
            return texto == "Venda"

        login_page.texto_exibido = MagicMock(side_effect=texto_exibido_mock)

        # Act
        resultado = login_page.esta_logado(timeout=5)

        # Assert
        assert resultado is True

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_esta_logado_retorna_false_quando_nenhum_texto_visivel(self, mock_logger, mock_base_init):
        """
        Deve retornar False quando nenhum texto de login está visível.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()

        # Nenhum texto está visível
        login_page.texto_exibido = MagicMock(return_value=False)

        # Act
        resultado = login_page.esta_logado(timeout=5)

        # Assert
        assert resultado is False


class TestLoginPageOutrosMetodos:
    """Testes para outros métodos da LoginPage."""

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_pular_telas_introducao_clica_nos_botoes_se_existirem(self, mock_logger, mock_base_init):
        """
        Deve tentar clicar nos botões de introdução se existirem.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()
        login_page.clicar_se_existir = MagicMock(return_value=True)

        # Act
        login_page.pular_telas_introducao()

        # Assert
        assert login_page.clicar_se_existir.call_count == 2
        login_page.clicar_se_existir.assert_any_call(LoginPage.BTN_PROXIMO_INTRO, tempo_espera=3)
        login_page.clicar_se_existir.assert_any_call(LoginPage.BTN_CONCLUIR_INTRO, tempo_espera=3)

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_preencher_credenciais_digita_todos_os_campos(self, mock_logger, mock_base_init):
        """
        Deve digitar em todos os campos de credenciais e fechar o teclado.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()
        login_page.digitar_por_id = MagicMock()
        login_page.fechar_teclado = MagicMock()

        empresa = "EMPRESA_TESTE"
        usuario = "USUARIO_TESTE"
        senha = "SENHA_TESTE"

        # Act
        login_page.preencher_credenciais(empresa, usuario, senha)

        # Assert
        login_page.digitar_por_id.assert_any_call(LoginPage.EDT_EMPRESA, empresa)
        login_page.digitar_por_id.assert_any_call(LoginPage.EDT_USUARIO, usuario)
        login_page.digitar_por_id.assert_any_call(LoginPage.EDT_SENHA, senha)
        login_page.fechar_teclado.assert_called_once()

    @patch('pages.login_page.BasePage.__init__', return_value=None)
    @patch('pages.login_page.logger')
    def test_clicar_entrar_clica_no_botao_entrar(self, mock_logger, mock_base_init):
        """
        Deve clicar no botão de entrar.
        """
        from pages.login_page import LoginPage

        # Arrange
        login_page = LoginPage.__new__(LoginPage)
        login_page.driver = MagicMock()
        login_page.clicar_por_id = MagicMock()

        # Act
        login_page.clicar_entrar()

        # Assert
        login_page.clicar_por_id.assert_called_once_with(LoginPage.BTN_ENTRAR)
