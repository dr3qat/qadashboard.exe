"""
Pedido Page - Page Object para tela de pedido de venda.
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle, Cores


class PedidoPage(BasePage):
    """Page Object para tela de pedido de venda."""

    # --- Locators ---
    BTN_BUSCAR_CLIENTE = "btn_select_customer"
    BTN_ADICIONAR_PRODUTOS = "btn_adicionar_produtos"
    EDT_BUSCA_PRODUTO = "editText"
    IMG_PRODUTO = "imageView3"
    BTN_PROXIMO = "btn_proximo"
    BTN_AVANCAR = "btn_proceed"
    BTN_FINALIZAR = "btnFinalizar"
    BTN_PEDIDO_GERADO = "button17"

    # Busca cliente
    EDT_BUSCA_CLIENTE = "search_src_text"
    BTN_CONFIRMAR_CLIENTE = "button3"
    BTN_INICIAR_VENDA = "button30"  # Botão para consumidor (sem cliente)
    TXT_VENDEDOR = "txt_dialog_seller_name"

    # Popup de bonus
    BTN_MAIS_TARDE = "btn_mais_tarde"
    TXT_BONUS_DISPONIVEL = "BÔNUS DISPONÍVEL"

    # Alerta de cashback (após selecionar pagamento)
    TXT_ALERTA_CASHBACK = "Cliente possui 1 cupons de cashback disponíveis para uso!\nNovos pontos de cashback só serão gerados após a utilização dos cupons já disponíveis."
    BTN_CONFIRMAR_CASHBACK = "md_buttonDefaultPositive"

    # --- Ações ---
    def selecionar_vendedor(self):
        """Seleciona o vendedor."""
        logger.info(f"{LogStyle.ACAO} Selecionando vendedor...")
        self.clicar_por_id(self.TXT_VENDEDOR)

    def clicar_buscar_cliente(self):
        """Clica no botão buscar cliente."""
        logger.info(f"{LogStyle.ACAO} Clicando em {LogStyle.elemento('Buscar Cliente')}...")
        self.clicar_por_id(self.BTN_BUSCAR_CLIENTE)

    def iniciar_como_consumidor(self):
        """Inicia pedido sem selecionar cliente (consumidor final).

        Após selecionar vendedor, clica direto em 'Iniciar Venda' (button30).
        """
        logger.info(f"{LogStyle.ACAO} Iniciando como consumidor (sem cliente)...")
        self.ver_e_clicar(self.BTN_INICIAR_VENDA)

    def selecionar_cliente(self, identificador: str):
        """Seleciona cliente pelo identificador."""
        logger.info(f"{LogStyle.ACAO} Selecionando cliente: {LogStyle.valor(identificador)}")
        self.digitar_por_id(self.EDT_BUSCA_CLIENTE, identificador)
        self.pressionar_pesquisar()
        time.sleep(5)  # Resultados carregam assincronamente — button3 falha sem espera
        self.clicar_por_id(self.BTN_CONFIRMAR_CLIENTE)

    def adicionar_produto(self, codigo: str = "123"):
        """Adiciona produto pelo código."""
        logger.info(f"{LogStyle.ACAO} Adicionando produto: {LogStyle.valor(codigo)}")
        time.sleep(2)  # Aguarda tela carregar após selecionar cliente
        self.ver_e_clicar(self.BTN_ADICIONAR_PRODUTOS)

        self.digitar_por_id(self.EDT_BUSCA_PRODUTO, codigo)
        self.clicar_por_id(self.IMG_PRODUTO)

    def clicar_avancar(self):
        """Clica no botão avançar."""
        logger.info(f"{LogStyle.ACAO} Clicando em {LogStyle.elemento('Avançar')}...")
        elemento = self.encontrar_clicavel_por_id(self.BTN_PROXIMO)
        time.sleep(1.5)  # Estabiliza transição de tela (padrão venda_page)
        elemento.click()

    def selecionar_pagamento_dinheiro(self, com_cliente: bool = True):
        """
        Seleciona forma de pagamento dinheiro.

        Args:
            com_cliente: Se True, verifica alerta de cashback após avançar.
                        Se False (consumidor), não verifica.
        """
        logger.info(f"{LogStyle.ACAO} Selecionando pagamento: {LogStyle.valor('DINHEIRO')}")
        self.ver_e_clicar_texto("DINHEIRO")
        self.ver_e_clicar(self.BTN_AVANCAR)

        # Trata alerta de cashback (somente para pedidos com cliente)
        if com_cliente:
            self.tratar_alerta_cashback()

    def tratar_popup_bonus(self):
        """Trata popup de BÔNUS DISPONÍVEL se aparecer."""
        if self.texto_exibido(self.TXT_BONUS_DISPONIVEL, tempo_espera=3):
            logger.info(f"{LogStyle.ACAO} Popup {LogStyle.elemento('BÔNUS DISPONÍVEL')} detectado. Clicando em 'Mais tarde'...")
            self.clicar_por_id(self.BTN_MAIS_TARDE)
            time.sleep(1)

    def tratar_alerta_cashback(self):
        """
        Trata alerta de cashback que pode aparecer após selecionar forma de pagamento.

        Este alerta aparece SOMENTE para clientes com cashback disponível:
        - Valida o texto do alerta
        - Clica no botão confirmar (md_buttonDefaultPositive)
        - Se não aparecer, não bloqueia o teste (é opcional)
        """
        logger.info(f"{LogStyle.ACAO} Verificando alerta de cashback...")

        # Verifica se o alerta apareceu (timeout curto para não atrasar o teste)
        if self.texto_exibido("cupons de cashback disponíveis", tempo_espera=3):
            logger.info(f"{LogStyle.OK} Alerta de cashback detectado. Validando mensagem...")

            # Valida que a mensagem completa está presente
            texto_esperado_parte1 = "Cliente possui 1 cupons de cashback disponíveis para uso!"
            texto_esperado_parte2 = "Novos pontos de cashback só serão gerados após a utilização dos cupons já disponíveis"

            if self.texto_exibido(texto_esperado_parte1, tempo_espera=1):
                logger.info(f"   {LogStyle.VALIDAR} Mensagem validada: {LogStyle.valor('Cashback disponível')}")

            # Clica no botão confirmar
            logger.info(f"   {LogStyle.ACAO} Clicando em {LogStyle.elemento('Confirmar')}...")
            self.clicar_por_id(self.BTN_CONFIRMAR_CASHBACK)
            time.sleep(1)
            logger.info(f"   {LogStyle.OK} Alerta de cashback tratado com sucesso")
        else:
            logger.info(f"   {LogStyle.INFO} Alerta de cashback não apareceu (cliente sem cashback ou já utilizado)")

    def finalizar_pedido(self):
        """Finaliza o pedido."""
        logger.info(f"{LogStyle.ACAO} Finalizando pedido...")
        self.tratar_popup_bonus()
        self.ver_e_clicar(self.BTN_FINALIZAR)

    def confirmar_pedido_gerado(self):
        """Confirma o pedido gerado."""
        logger.info(f"{LogStyle.VALIDAR} Aguardando {LogStyle.elemento('Pedido gerado com sucesso!')}")
        self.aguardar_texto("Pedido gerado com sucesso!")
        self.ver_e_clicar(self.BTN_PEDIDO_GERADO)

    def executar_pedido_venda_consumidor(self, codigo_produto: str = "123"):
        """Executa fluxo completo de pedido de venda para consumidor (sem cliente)."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Pedido de venda (CONSUMIDOR)')}")

        self.selecionar_vendedor()
        self.iniciar_como_consumidor()
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=False)  # Consumidor não tem cashback
        self.finalizar_pedido()
        self.confirmar_pedido_gerado()

        logger.info(f"{LogStyle.secao('📋 FLUXO - Pedido (CONSUMIDOR) concluído ✅')}")

    def executar_pedido_venda_cliente(self, id_cliente: str = "1", codigo_produto: str = "123"):
        """Executa fluxo completo de pedido de venda para cliente cadastrado."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Pedido de venda (CLIENTE)')}")

        self.selecionar_vendedor()
        self.clicar_buscar_cliente()
        self.selecionar_cliente(id_cliente)
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=True)  # Verifica cashback
        self.finalizar_pedido()
        self.confirmar_pedido_gerado()

        logger.info(f"{LogStyle.secao('📋 FLUXO - Pedido (CLIENTE) concluído ✅')}")

    def executar_pedido_venda(self, id_cliente: str = "1", codigo_produto: str = "123"):
        """Executa fluxo completo de pedido de venda (mantido para compatibilidade)."""
        self.executar_pedido_venda_cliente(id_cliente, codigo_produto)

    # --- Validações ---
    def pedido_sucesso_exibido(self, timeout: int = 10) -> bool:
        """Verifica se mensagem de sucesso apareceu."""
        return self.texto_exibido("Pedido gerado com sucesso!", timeout)
