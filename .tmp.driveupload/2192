"""
Home Page - Page Object para tela inicial (pós-login).
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle, Cores


class HomePage(BasePage):
    """Page Object para tela inicial do app."""

    # --- Locators ---
    TXT_INICIAR_VENDA = "Iniciar Venda"
    TXT_REALIZAR_TROCA = "Realizar Troca"
    TXT_VENDA = "Venda"
    DIALOGO_VENDEDOR = "txt_dialog_seller_name"
    # Tela full-screen de seleção de vendedor (usa mesmo ID para itens da lista)
    TELA_ESCOLHER_VENDEDOR = "Escolher Vendedor"

    # --- Ações ---
    def iniciar_venda(self):
        """Inicia uma venda. Tenta 'Venda' (Playstore) ou 'Iniciar Venda' (devices)."""
        logger.info(f"{LogStyle.ACAO} Iniciando venda...")
        time.sleep(2)  # Aguarda tela estabilizar

        # Tenta clicar diretamente sem scroll (botão sempre visível na home)
        # Primeiro tenta "Iniciar Venda" (devices: Stone, L400, etc)
        logger.info(f"   {LogStyle.DEBUG} Verificando {LogStyle.elemento('Iniciar Venda')}...")
        try:
            if self.texto_exibido(self.TXT_INICIAR_VENDA, tempo_espera=5):
                logger.info(f"   {LogStyle.OK} Encontrado {LogStyle.elemento('Iniciar Venda')} (versão device)")
                self.clicar_por_texto(self.TXT_INICIAR_VENDA)
                return
        except Exception as e:
            logger.info(f"   {LogStyle.DEBUG} 'Iniciar Venda' não encontrado: {e}")

        # Depois tenta "Venda" (versão Playstore)
        logger.info(f"   {LogStyle.DEBUG} Verificando {LogStyle.elemento('Venda')}...")
        try:
            if self.texto_exibido(self.TXT_VENDA, tempo_espera=5):
                logger.info(f"   {LogStyle.OK} Encontrado {LogStyle.elemento('Venda')} (versão Playstore)")
                self.clicar_por_texto(self.TXT_VENDA)
                return
        except Exception as e:
            logger.info(f"   {LogStyle.DEBUG} 'Venda' não encontrado: {e}")

        # Última tentativa: usa scroll nativo para encontrar
        logger.info(f"   {LogStyle.DEBUG} Tentando com scroll nativo...")
        try:
            self.rolar_ate_texto(self.TXT_VENDA, max_scrolls=3)
            self.clicar_por_texto(self.TXT_VENDA)
            return
        except:
            pass

        try:
            self.rolar_ate_texto(self.TXT_INICIAR_VENDA, max_scrolls=3)
            self.clicar_por_texto(self.TXT_INICIAR_VENDA)
            return
        except:
            pass

        raise Exception(f"Não encontrou 'Venda' nem 'Iniciar Venda' na tela inicial")

    def iniciar_troca(self):
        """Inicia uma troca/devolução."""
        logger.info(f"{LogStyle.ACAO} Iniciando troca...")
        self.ver_e_clicar_texto(self.TXT_REALIZAR_TROCA)
        logger.info(f"   {LogStyle.OK} Clicou em {LogStyle.elemento('Realizar Troca')}")

    def selecionar_vendedor(self, max_tentativas: int = 3):
        """
        Seleciona vendedor no diálogo ou tela full-screen.
        Se não aparecer nenhuma tela de vendedor, continua o fluxo.
        Usa ID para clicar no primeiro vendedor da lista.
        """
        logger.info(f"{LogStyle.ACAO} Selecionando vendedor...")
        time.sleep(2)  # Aguarda tela estabilizar

        for tentativa in range(max_tentativas):
            try:
                # 1. Verifica se é tela full-screen "Escolher Vendedor" ou diálogo
                #    Ambos usam o mesmo ID para os itens: txt_dialog_seller_name
                if self.texto_exibido(self.TELA_ESCOLHER_VENDEDOR, tempo_espera=3):
                    logger.info(f"   {LogStyle.OK} Tela {LogStyle.elemento('Escolher Vendedor')} detectada")
                    # Clica no PRIMEIRO vendedor da lista por ID
                    self.clicar_no_primeiro_da_lista_por_id(self.DIALOGO_VENDEDOR)
                    logger.info(f"   {LogStyle.OK} Primeiro vendedor da lista selecionado!")
                    time.sleep(1)
                    return

                # 2. Verifica se é diálogo popup (mesmo ID)
                if self.elemento_existe(self.DIALOGO_VENDEDOR, tempo_espera=3):
                    self.clicar_por_id(self.DIALOGO_VENDEDOR)
                    logger.info(f"   {LogStyle.OK} Vendedor selecionado via diálogo!")
                    return

                # 3. Nenhuma tela de vendedor apareceu
                logger.info(f"   {LogStyle.SKIP} Nenhuma tela de vendedor detectada (versão pode não exigir)")
                return

            except Exception as e:
                if tentativa < max_tentativas - 1:
                    logger.warning(f"   {LogStyle.RETRY} Tentativa {tentativa + 1}: {e}")
                    time.sleep(1)
                else:
                    logger.warning(f"   {LogStyle.aviso('Falha ao selecionar vendedor:')} {e}. Continuando...")

    # --- Validações ---
    def tela_inicial_exibida(self, timeout: int = 10) -> bool:
        """Verifica se está na tela inicial."""
        return (
            self.texto_exibido(self.TXT_INICIAR_VENDA, timeout) or
            self.texto_exibido(self.TXT_VENDA, timeout)
        )
