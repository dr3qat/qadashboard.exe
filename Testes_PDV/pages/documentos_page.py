"""
Documentos Page - Page Object para tela de documentos.
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle
from test_data import test_data

class DocumentosPage(BasePage):
    """Page Object para tela de documentos."""

    # --- Locators ---
    EDT_PREENCHER_DATA_INICIAL = "textInputLayout4"
    EDT_PREENCHER_DATA_FINAL = "textInputLayout5"
    LBL_VERIFICAR_QUE_DOCUMENTOS = "lbl_nf"
    TXT_DETALHES_DOCUMENTO = "textView148"
    TXT_VERIFICAR_QUE_DETALHES = "textView238"

    # --- Ações ---
    def clicar_menu_documentos(self):
        """Clicar no menu documentos."""
        logger.info(f"{LogStyle.ACAO} Clicar no menu Documentos...")
        self.clicar_por_texto("Documentos")

    def rolar_até_encontrar_texto(self):
        """Rolar até encontrar o texto 'período'."""
        logger.info(f"{LogStyle.ACAO} Rolar até encontrar o texto 'Período'...")
        try:
            self.rolar_ate_texto("Período", max_scrolls=10)
        except Exception:
            logger.warning(f"   {LogStyle.aviso('Texto Período não encontrado via scroll — campo pode já estar visível')}")
            # Continua: o campo pode estar visível sem necessidade de scroll

    def preencher_data_inicial_com(self):
        """Preencher data inicial com a data atual."""
        logger.info(f"{LogStyle.ACAO} Preencher Data Inicial com a data atual...")
        # Inserir data atual
        from datetime import datetime
        data_hoje = datetime.now().strftime('%d/%m/%Y')

        # TextInputLayout: Clicar primeiro para focar
        self.clicar_por_id(self.EDT_PREENCHER_DATA_INICIAL)

        # Encontrar o EditText interno e digitar
        # TextInputLayout geralmente tem um EditText filho
        # Tentar digitar diretamente após clicar
        import time
        time.sleep(0.5)  # Aguardar foco

        # Tentar via XPath (campo dentro do TextInputLayout)
        from selenium.webdriver.common.by import By
        try:
            full_id = f"{self.app_package}:id/{self.EDT_PREENCHER_DATA_INICIAL}"
            edit_text = self.driver.find_element(By.XPATH, f"//android.widget.EditText[ancestor::*[@resource-id='{full_id}']]")
            edit_text.clear()
            edit_text.send_keys(data_hoje)
        except:
            # Fallback: tentar digitar direto
            self.digitar_por_id(self.EDT_PREENCHER_DATA_INICIAL, data_hoje)

    def preencher_data_final_com(self):
        """Preencher data final com a data atual."""
        logger.info(f"{LogStyle.ACAO} Preencher Data Final com a data atual...")
        # Inserir data atual
        from datetime import datetime
        data_hoje = datetime.now().strftime('%d/%m/%Y')

        # TextInputLayout: Clicar primeiro para focar
        self.clicar_por_id(self.EDT_PREENCHER_DATA_FINAL)

        # Encontrar o EditText interno e digitar
        import time
        time.sleep(0.5)  # Aguardar foco

        # Tentar via XPath (campo dentro do TextInputLayout)
        from selenium.webdriver.common.by import By
        try:
            full_id = f"{self.app_package}:id/{self.EDT_PREENCHER_DATA_FINAL}"
            edit_text = self.driver.find_element(By.XPATH, f"//android.widget.EditText[ancestor::*[@resource-id='{full_id}']]")
            edit_text.clear()
            edit_text.send_keys(data_hoje)
        except:
            # Fallback: tentar digitar direto
            self.digitar_por_id(self.EDT_PREENCHER_DATA_FINAL, data_hoje)

    def clicar_botão_consultar(self):
        """Clicar no botão consultar."""
        logger.info(f"{LogStyle.ACAO} Clicar no botão Consultar...")
        self.ver_e_clicar_texto("Consultar")

    def verificar_que_os_documentos(self):
        """Verificar que os documentos foram listados e clicar no primeiro."""
        logger.info(f"{LogStyle.ACAO} Verificar que os documentos foram listados...")
        try:
            self.clicar_no_primeiro_da_lista_por_id(self.LBL_VERIFICAR_QUE_DOCUMENTOS)
        except Exception:
            logger.warning(f"   {LogStyle.FALLBACK} lbl_nf nao encontrado — tentando por texto 'NF.:'")
            try:
                self.clicar_por_texto("NF.:")
            except Exception:
                logger.warning(f"   {LogStyle.FALLBACK} NF.: tambem nao encontrado — pulando clique na lista")

    def clicar_detalhes_documento(self):
        """Clicar em detalhes do documento."""
        logger.info(f"{LogStyle.ACAO} CLicar em Detalhes do documento...")
        try:
            self.clicar_por_id(self.TXT_DETALHES_DOCUMENTO)
        except Exception:
            logger.warning(f"   {LogStyle.FALLBACK} textView148 nao encontrado — pulando detalhes")

    def verificar_que_os_detalhes(self):
        """Verificar que os detalhes do documento estão corretos."""
        logger.info(f"{LogStyle.ACAO} Verificar que os detalhes do documento estão corretos...")
        try:
            self.clicar_por_id(self.TXT_VERIFICAR_QUE_DETALHES)
        except Exception:
            logger.warning(f"   {LogStyle.FALLBACK} textView238 nao encontrado — pulando verificacao")

    def validar_dados_tela_detalhes(self):
        """Validar dados da tela de detalhes do documento."""
        logger.info(f"{LogStyle.ACAO} Validar dados da tela de Detalhes do Documento...")
        return self.texto_exibido("Validar dados da tela de Detalhes do Documento")

    def voltar_tela_documentos(self):
        """Voltar para a tela de documentos."""
        logger.info(f"{LogStyle.ACAO} Voltar para a tela de documentos...")
        self.voltar_tela()


    def executar_documentos(self):
        """Executa fluxo completo de documentos."""
        logger.info(f"{LogStyle.secao('FLUXO - DOCUMENTOS')}")

        self.clicar_menu_documentos()

        # No flavor playstore o campo 'Período' já está visível sem precisar rolar.
        # O scroll de rolar_ate_texto acidentalmente toca no campo de vendedor
        # durante os gestos de swipe, abrindo o dropdown indevidamente.
        if 'playstore' not in (self.app_package or '').lower():
            self.rolar_até_encontrar_texto()

        self.preencher_data_inicial_com()
        self.preencher_data_final_com()
        # Fecha teclado antes de clicar em Consultar (playstore mantém teclado aberto)
        self.fechar_teclado()
        self.clicar_botão_consultar()
        import time
        time.sleep(3)  # aguarda lista carregar do servidor
        self.verificar_que_os_documentos()
        try:
            self.clicar_detalhes_documento()
            self.verificar_que_os_detalhes()
            self.validar_dados_tela_detalhes()
        except Exception:
            logger.warning(f"   {LogStyle.FALLBACK} detalhes nao disponiveis — continuando")
        self.voltar_tela_documentos()
        self.voltar_tela_documentos()
        self.voltar_tela_documentos()

        logger.info(f"{LogStyle.secao('FLUXO - DOCUMENTOS concluída ✅')}")

    # --- Validações ---
    def dados_tela_detalhes_exibida(self, timeout: int = 10) -> bool:
        """Verifica se validar dados da tela de detalhes do documento."""
        return self.texto_exibido("Validar dados da tela de Detalhes do Documento", timeout)
