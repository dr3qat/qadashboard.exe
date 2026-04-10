"""
Consulta Pedido Page - Page Object para tela de consulta de pedidos.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from pages.venda_sucesso_page import VendaSucessoPage
from config import logger, LogStyle, Cores
from test_data import test_data


class ConsultaPedidoPage(BasePage):
    """Page Object para tela de consulta de pedidos."""

    # --- Locators ---
    # Menu lateral
    ACCESSIBILITY_MENU = "Open navigation drawer"

    # Lista de pedidos
    TXT_ITEM_PEDIDO = "textView230"

    # Botões
    BTN_FINALIZAR = "btnFinalizar"
    BTN_MAIS_TARDE = "btn_mais_tarde"

    # Alerta de cashback
    BTN_CONFIRMAR_CASHBACK = "md_buttonDefaultPositive"

    # Diálogos de impressão
    BTN_DIALOG_SIM = "android:id/button1"
    BTN_DIALOG_NAO = "android:id/button2"

    # --- Ações de Configuração ---
    def abrir_menu_lateral(self):
        """Abre o menu lateral (navigation drawer)."""
        logger.info(f"{LogStyle.ACAO} Abrindo menu lateral...")
        try:
            menu = self.encontrar_por_accessibility_id(self.ACCESSIBILITY_MENU)
            menu.click()
            time.sleep(1)
            logger.info(f"   {LogStyle.OK} Menu lateral aberto")
        except Exception as e:
            logger.warning(f"   {LogStyle.aviso('Erro ao abrir menu:')} {e}")
            raise

    def acessar_configuracoes(self):
        """Acessa tela de configurações."""
        logger.info(f"{LogStyle.ACAO} Acessando {LogStyle.elemento('Configurações')}...")
        self.clicar_por_texto("Configurações")

    def garantir_flag_buscar_todos_pedidos(self):
        """Garante que a flag 'Buscar todos os pedidos' está ativa."""
        logger.info(f"{LogStyle.ACAO} Verificando flag {LogStyle.elemento('Buscar todos os pedidos')}...")

        # Rola até encontrar o texto
        self.rolar_ate_texto("Buscar todos os pedidos")

        # Encontra o switch associado
        try:
            # Busca o texto e depois o switch próximo
            elementos = self.encontrar_todos_por_uiautomator(
                'new UiSelector().text("Buscar todos os pedidos")',
                tempo_espera=3
            )

            if elementos:
                # Pega o parent e busca o switch
                parent = elementos[0]
                # Tenta encontrar switch no mesmo container
                switches = self.encontrar_todos_por_classe(
                    "android.widget.Switch",
                    tempo_espera=3
                )

                for switch in switches:
                    try:
                        # Verifica se o switch está na mesma linha (próximo ao texto)
                        if switch.is_displayed():
                            checked = switch.get_attribute("checked")
                            if checked == "false":
                                logger.info(f"   {LogStyle.INFO} Flag desativada, ativando...")
                                switch.click()
                            else:
                                logger.info(f"   {LogStyle.OK} Flag já está ativa")
                            return True
                    except:
                        continue

            # Fallback: clica no texto para alternar
            logger.info(f"   {LogStyle.FALLBACK} Clicando no texto para alternar...")
            self.clicar_por_texto("Buscar todos os pedidos")
            return True

        except Exception as e:
            logger.warning(f"   {LogStyle.aviso('Erro ao configurar flag:')} {e}")
            return False

    def voltar_para_home(self):
        """Volta para a tela inicial."""
        logger.info(f"{LogStyle.ACAO} Voltando para Home...")
        self.driver.back()
        time.sleep(1)

    def configurar_buscar_todos_pedidos(self):
        """Fluxo completo para configurar flag de buscar todos os pedidos."""
        logger.info(f"{LogStyle.secao('⚙️  CONFIG - Configurando busca de pedidos')}")
        self.abrir_menu_lateral()
        self.acessar_configuracoes()
        self.garantir_flag_buscar_todos_pedidos()
        self.voltar_para_home()
        logger.info(f"{LogStyle.secao('⚙️  CONFIG - Configuração concluída')}")

    # --- Ações de Consulta ---
    def acessar_consulta_pedido(self):
        """Acessa a tela de consulta de pedidos."""
        logger.info(f"{LogStyle.ACAO} Acessando {LogStyle.elemento('Cons. Pedido')}...")
        self.ver_e_clicar_texto("Cons. Pedido")
        # Lista carregada em selecionar_ultimo_pedido via encontrar_todos_por_id

    def selecionar_ultimo_pedido(self):
        """Seleciona o pedido mais recente (último da lista, novos vão pro fundo)."""
        logger.info(f"{LogStyle.ACAO} Selecionando pedido mais recente (último da lista)...")

        # Scroll até o final para revelar os pedidos mais recentes
        logger.info(f"   {LogStyle.SCROLL} Rolando até o final da lista...")
        for _ in range(10):
            self.realizar_scroll_para_baixo()
            time.sleep(0.3)

        # Pega elementos visíveis no fundo — não rolar mais para não perder referência
        elementos = self.encontrar_todos_por_id(self.TXT_ITEM_PEDIDO, tempo_espera=10)
        if not elementos:
            logger.warning(f"   {LogStyle.aviso('Nenhum pedido encontrado na lista')}")
            return False

        # Pedido mais recente = maior número (numeração sequencial crescente)
        def _safe_int(el):
            try:
                return int(el.text.strip())
            except (ValueError, TypeError):
                return -1

        ultimo = max(elementos, key=_safe_int)
        numero_pedido = ultimo.text.strip()
        logger.info(f"   {LogStyle.CLICK} Clicando no pedido Nº {numero_pedido} (maior número)")
        ultimo.click()
        # Aguarda BottomSheet aparecer via clicar_finalizar_pedido(tempo_espera=15)
        logger.info(f"   {LogStyle.OK} Pedido Nº {numero_pedido} selecionado")
        return True

    def clicar_finalizar_pedido(self):
        """Clica em 'Finalizar Pedido' no BottomSheet."""
        logger.info(f"{LogStyle.ACAO} Clicando em {LogStyle.elemento('Finalizar Pedido')}...")
        # NÃO usar ver_e_clicar_texto: scroll fecha o BottomSheet.
        # tempo_espera=15 aguarda BottomSheet aparecer (substitui sleep(5) anterior)
        self.clicar_por_texto("Finalizar Pedido", tempo_espera=15)

    def tratar_popup_bonus(self):
        """Trata popup de bônus se aparecer."""
        logger.info(f"{LogStyle.ACAO} Verificando popup de bônus...")
        if self.clicar_se_existir(self.BTN_MAIS_TARDE, tempo_espera=3):
            logger.info(f"   {LogStyle.OK} Popup de bônus fechado")
        else:
            logger.info(f"   {LogStyle.SKIP} Nenhum popup de bônus")

    def tratar_alerta_cashback(self):
        """Trata alerta de cashback que pode aparecer após finalizar pedido de cliente."""
        logger.info(f"{LogStyle.ACAO} Verificando alerta de cashback...")
        if self.texto_exibido("cupons de cashback disponíveis", tempo_espera=3):
            logger.info(f"   {LogStyle.OK} Alerta de cashback detectado. Clicando em OK...")
            self.clicar_por_id(self.BTN_CONFIRMAR_CASHBACK)
            time.sleep(1)
            logger.info(f"   {LogStyle.OK} Alerta de cashback tratado com sucesso")
        else:
            logger.info(f"   {LogStyle.INFO} Alerta de cashback não apareceu")

    def responder_cupom_venda(self):
        """
        Responde ao diálogo de Cupom de Venda (automático após finalizar).
        Conforme CONFIGURACAO_IMPRESSAO.md - Item 1.
        """
        logger.info(f"{LogStyle.ACAO} Verificando diálogo de Cupom de Venda...")

        timeout = test_data.PRINT_DIALOG_TIMEOUT

        # Aguarda diálogo aparecer
        if self.elemento_existe(self.BTN_DIALOG_NAO, tempo_espera=timeout):
            if test_data.PRINT_CUPOM_VENDA:
                # Configuração marcada: Clica SIM
                logger.info(f"   {LogStyle.INFO} Config PRINT_CUPOM_VENDA = True → Clicando SIM")
                self.clicar_se_existir(self.BTN_DIALOG_SIM, tempo_espera=2)
                logger.info(f"   {LogStyle.OK} Cupom de Venda: SIM")
            else:
                # Configuração desmarcada: Clica NÃO (padrão)
                logger.info(f"   {LogStyle.INFO} Config PRINT_CUPOM_VENDA = False → Clicando NÃO")
                self.clicar_se_existir(self.BTN_DIALOG_NAO, tempo_espera=2)
                logger.info(f"   {LogStyle.OK} Cupom de Venda: NÃO")
            time.sleep(1)
        else:
            logger.info(f"   {LogStyle.SKIP} Nenhum diálogo de Cupom de Venda apareceu")

    def responder_cupom_troca_dialogo(self):
        """
        Responde ao diálogo de Cupom de Troca (pode aparecer ANTES da tela de sucesso).
        Conforme CONFIGURACAO_IMPRESSAO.md - Item 2 (Situação A).

        IMPORTANTE: Só aparece se sistema tiver parâmetro habilitado.
        Se não aparecer, o botão estará na tela de sucesso.
        """
        logger.info(f"{LogStyle.ACAO} Verificando diálogo de Cupom de Troca...")

        timeout = test_data.PRINT_DIALOG_TIMEOUT

        # Aguarda diálogo aparecer (pode não aparecer)
        if self.elemento_existe(self.BTN_DIALOG_NAO, tempo_espera=timeout):
            if test_data.PRINT_CUPOM_TROCA:
                # Configuração marcada: Clica SIM
                logger.info(f"   {LogStyle.INFO} Config PRINT_CUPOM_TROCA = True → Clicando SIM")
                self.clicar_se_existir(self.BTN_DIALOG_SIM, tempo_espera=2)
                logger.info(f"   {LogStyle.OK} Cupom de Troca (diálogo): SIM")
            else:
                # Configuração desmarcada: Clica NÃO (padrão)
                logger.info(f"   {LogStyle.INFO} Config PRINT_CUPOM_TROCA = False → Clicando NÃO")
                self.clicar_se_existir(self.BTN_DIALOG_NAO, tempo_espera=2)
                logger.info(f"   {LogStyle.OK} Cupom de Troca (diálogo): NÃO")
            time.sleep(1)
        else:
            logger.info(f"   {LogStyle.SKIP} Nenhum diálogo de Cupom de Troca (será tratado na tela de sucesso)")

    def finalizar_venda(self):
        """
        Finaliza a venda do pedido (clica no botão Finalizar da tela de pagamento).

        Fluxo de impressões (conforme CONFIGURACAO_IMPRESSAO.md):
        1. Cupom de Venda (diálogo automático)
        2. Cupom de Troca (diálogo - se parâmetro habilitado)
        3. Tela de Sucesso (botões: NFC-E, DANFE, Cupom Troca)
        """
        logger.info(f"{LogStyle.ACAO} Finalizando venda...")
        self.tratar_popup_bonus()
        self.tratar_alerta_cashback()
        self.tratar_popup_bonus()  # Bonus pode aparecer APOS cashback ser fechado
        # Aguarda tela de pagamento carregar (servidor processa pedido)
        self.encontrar_clicavel_por_id(self.BTN_FINALIZAR, tempo_espera=15)
        self.ver_e_clicar(self.BTN_FINALIZAR)

        # IMPRESSÃO 1: Cupom de Venda (diálogo automático)
        self.responder_cupom_venda()

        # IMPRESSÃO 2: Cupom de Troca (diálogo - pode ou não aparecer)
        self.responder_cupom_troca_dialogo()

        time.sleep(1)  # Aguarda carregar tela de sucesso


    def executar_consulta_e_finalizar_pedido(self):
        """Executa fluxo completo de consulta e finalização de pedido.

        Fluxo:
        1. Acessar Cons. Pedido
        2. Selecionar último pedido (número maior)
        3. Clicar em "Finalizar Pedido" (BottomSheet)
        4. Se aparecer popup de bônus, clicar "Mais tarde"
        5. Clicar em "Finalizar" (tela de pagamento)
        6. Clicar em "CONCLUIR VENDA" (tela de sucesso/impressões)
        """
        logger.info(f"{LogStyle.secao('📋 FLUXO - Consulta e finalização de pedido')}")

        self.acessar_consulta_pedido()
        self.selecionar_ultimo_pedido()
        self.clicar_finalizar_pedido()
        self.finalizar_venda()

        logger.info(f"{LogStyle.secao('📋 FLUXO - Consulta e finalização executadas')}")

    # --- Validações ---
    def venda_sucesso_exibida(self, timeout: int = 10) -> bool:
        """Verifica se mensagem de sucesso apareceu."""
        return self.texto_exibido("Venda realizada com sucesso!", timeout)

    def validar_sucesso_e_concluir(self):
        """
        Valida sucesso da venda e processa todas as impressões.

        Fluxo completo (conforme CONFIGURACAO_IMPRESSAO.md):
        1. Valida mensagem "Venda realizada com sucesso!"
        2. Processa impressões da tela de sucesso (NFC-E, DANFE, Cupom Troca)
        3. Clica em CONCLUIR VENDA
        """
        logger.info(f"{LogStyle.VALIDAR} Aguardando {LogStyle.elemento('Venda realizada com sucesso!')}")
        if not self.aguardar_texto("Venda realizada com sucesso!", tempo_espera=10):
            raise AssertionError("Mensagem de sucesso não apareceu após finalizar pedido")
        logger.info(f"   {LogStyle.OK} Mensagem de sucesso exibida")

        # Usa VendaSucessoPage para processar impressões da tela de sucesso
        sucesso_page = VendaSucessoPage(self.driver)

        # IMPRESSÕES 3, 4, 5: Botões na tela de sucesso (NFC-E, DANFE, Cupom Troca)
        sucesso_page.processar_todas_impressoes()

        # Concluir venda
        sucesso_page.concluir_venda()
