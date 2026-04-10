"""
Login Page - Page Object para tela de login.
"""
from pages.base_page import BasePage
from config import logger


class LoginPage(BasePage):
    """Page Object para tela de login."""

    # --- Locators ---
    BTN_PROXIMO_INTRO = "btn_next_intro"
    BTN_CONCLUIR_INTRO = "btn_done_intro"
    BTN_CONFIGURAR_CONEXAO = "btn_config_connection"
    EDT_IP_SERVIDOR = "edt_config_conn_ip_server"
    EDT_GATEWAY_SERVIDOR = "edt_config_conn_gateway_server"
    BTN_SALVAR_DIALOGO = "md_buttonDefaultPositive"
    EDT_EMPRESA = "edt_company_login"
    EDT_USUARIO = "edt_user_login"
    EDT_SENHA = "edt_password_login"
    BTN_ENTRAR = "btn_enter_login"

    # --- Ações ---
    def pular_telas_introducao(self):
        """Pula telas de introducao se existirem."""
        self.clicar_se_existir(self.BTN_PROXIMO_INTRO, tempo_espera=3)
        self.clicar_se_existir(self.BTN_CONCLUIR_INTRO, tempo_espera=3)

    def configurar_conexao_se_necessario(self, ip: str, porta: str):
        """Configura conexao com servidor apenas se o botao existir."""
        if self.clicar_se_existir(self.BTN_CONFIGURAR_CONEXAO, tempo_espera=3):
            logger.info("   Configurando conexao...")
            self.digitar_por_id(self.EDT_IP_SERVIDOR, ip)
            self.digitar_por_id(self.EDT_GATEWAY_SERVIDOR, porta)
            self.clicar_por_id(self.BTN_SALVAR_DIALOGO)
            return True
        logger.info("   Conexao ja configurada, pulando...")
        return False

    def preencher_credenciais(self, empresa: str, usuario: str, senha: str):
        """Preenche credenciais de login."""
        logger.info("   Preenchendo credenciais...")
        self.digitar_por_id(self.EDT_EMPRESA, empresa)
        self.digitar_por_id(self.EDT_USUARIO, usuario)
        self.digitar_por_id(self.EDT_SENHA, senha)
        # Fecha o teclado
        self.fechar_teclado()

    def clicar_entrar(self):
        """Clica no botao entrar."""
        logger.info("   Clicando em ENTRAR...")
        self.clicar_por_id(self.BTN_ENTRAR)

    def garantir_login(self, ip: str, porta: str, empresa: str, usuario: str, senha: str):
        """
        Garante que o usuario esta logado.
        Se ja estiver logado, nao faz nada.
        Se nao estiver, executa o fluxo de login.
        """
        logger.info("--- [PRE-CONDICAO] Verificando login ---")

        # Verifica se ja esta logado
        if self.esta_logado(timeout=5):
            logger.info("   Usuario ja esta logado!")
            return True

        logger.info("   Usuario nao esta logado. Executando login...")

        # Pula telas de intro se existirem
        self.pular_telas_introducao()

        # Configura conexao se necessario
        self.configurar_conexao_se_necessario(ip, porta)

        # Preenche credenciais
        self.preencher_credenciais(empresa, usuario, senha)

        # Clica em entrar
        self.clicar_entrar()

        logger.info("--- [PRE-CONDICAO] Login concluido ---")
        return True

    # --- Validações ---
    def esta_logado(self, timeout: int = 5) -> bool:
        """Verifica se usuario esta logado."""
        return (
            self.texto_exibido("Iniciar Venda", timeout) or
            self.texto_exibido("Venda", timeout)
        )
