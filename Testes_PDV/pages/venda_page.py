"""
Venda Page - Page Object para tela de venda.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from config import logger, LogStyle, Cores
from test_data import test_data


class VendaPage(BasePage):
    """Page Object para tela de venda."""

    # --- Locators ---
    BTN_BUSCAR_CLIENTE = "btn_select_customer"
    BTN_INICIAR_VENDA_SEM_CLIENTE = "button30"  # Versão Playstore
    BTN_ADICIONAR_PRODUTOS = "btn_adicionar_produtos"
    EDT_BUSCA_PRODUTO = "editText"
    IMG_PRODUTO = "imageView3"
    BTN_PROXIMO = "btn_proximo"
    BTN_AVANCAR = "btn_proceed"
    BTN_FINALIZAR = "btnFinalizar"
    BTN_CONFIRMAR_VENDA = "btn_confirmar_venda"
    BTN_IMPRIMIR_SIM = "android:id/button1"
    BTN_IMPRIMIR_NAO = "android:id/button2"

    # Busca cliente
    EDT_BUSCA_CLIENTE = "search_src_text"
    BTN_CONFIRMAR_CLIENTE = "button3"

    # Tela "Selecionar Cliente" (versão L400/Stone)
    TELA_SELECIONAR_CLIENTE = "Selecionar Cliente"
    TXT_INICIAR_VENDA_BTN = "INICIAR VENDA"

    # Popup de bonus
    BTN_MAIS_TARDE = "btn_mais_tarde"
    TXT_BONUS_DISPONIVEL = "BÔNUS DISPONÍVEL"

    # Alerta de cashback (após selecionar pagamento)
    TXT_ALERTA_CASHBACK = "Cliente possui 1 cupons de cashback disponíveis para uso!\nNovos pontos de cashback só serão gerados após a utilização dos cupons já disponíveis."
    BTN_CONFIRMAR_CASHBACK = "md_buttonDefaultPositive"

    # Carrinho — quantidade
    BTN_AUMENTAR_QTDE = "btn_increase"

    # Tela forma de pagamento — flags de bônus/cashback
    SWITCH_BONUS     = "switch_bonus"
    SWITCH_CASHBACK  = "switch_cashback"

    # Desconto / Acréscimo / Restante (tela forma de pagamento — após btn_proceed)
    TXT_DESCONTO_AREA = "textView127"       # âncora de scroll para área de desconto/acréscimo
    TXT_RESTANTE = "textView153"
    # Dois campos com mesmo resource-id: [1]=acréscimo, [2]=desconto
    # contains() funciona em qualquer flavor/device sem hardcode de pacote
    XPATH_ACRESCIMO_REAIS  = '(//android.widget.EditText[contains(@resource-id,"edt_desconto_item_reais")])[1]'
    XPATH_DESCONTO_REAIS   = '(//android.widget.EditText[contains(@resource-id,"edt_desconto_item_reais")])[2]'

    # Pagamentos — seção (para excluir/reconfigurar pagamento)
    TXT_PAGAMENTOS_HEADER  = "textView131"   # header "Pagamentos"
    BTN_EXCLUIR_PAGAMENTO  = "imageView12"   # ícone trash/delete dentro do card de pagamento
    BTN_TIPO_PAGAMENTO     = "imageView19"   # abre seletor de tipos: Bônus, DINHEIRO, etc.
    BTN_ADICIONAR_PAG      = "btn_adiciona_pagamento"
    BTN_PAGAR              = "btn_pagar"
    XPATH_BONUS_CHECKBOX   = '(//android.widget.CheckBox[contains(@resource-id,"ck_discount")])[1]'

    # --- Ações ---
    def clicar_buscar_cliente(self):
        """Clica no botão buscar cliente."""
        logger.info(f"{LogStyle.ACAO} Clicando em {LogStyle.elemento('Buscar Cliente')}...")

        # Versão L400/Stone: Tela "Selecionar Cliente" com botão "Buscar Cliente" por texto
        if self.texto_exibido(self.TELA_SELECIONAR_CLIENTE, tempo_espera=3):
            logger.info(f"   {LogStyle.OK} Tela {LogStyle.elemento('Selecionar Cliente')} detectada")
            if self.texto_exibido("Buscar Cliente", tempo_espera=2):
                self.clicar_por_texto("Buscar Cliente")
                logger.info(f"   {LogStyle.OK} Clicou em {LogStyle.elemento('Buscar Cliente')}")
                return

        # Versão Playstore: ID btn_select_customer
        logger.info(f"   {LogStyle.INFO} Tentando versão Playstore (ID)...")
        self.clicar_por_id(self.BTN_BUSCAR_CLIENTE)

    def iniciar_venda_sem_cliente(self):
        """Inicia venda sem selecionar cliente (consumidor)."""
        logger.info(f"{LogStyle.ACAO} Iniciando venda sem cliente...")

        # Versão L400/Stone: Tela "Selecionar Cliente" com botão "INICIAR VENDA"
        if self.texto_exibido(self.TELA_SELECIONAR_CLIENTE, tempo_espera=3):
            logger.info(f"   {LogStyle.OK} Tela {LogStyle.elemento('Selecionar Cliente')} detectada (versão L400/Stone)")
            if self.texto_exibido(self.TXT_INICIAR_VENDA_BTN, tempo_espera=3):
                self.clicar_por_texto(self.TXT_INICIAR_VENDA_BTN)
                logger.info(f"   {LogStyle.OK} Clicou em {LogStyle.elemento('INICIAR VENDA')}")
                return

        # Versão Playstore: botão button30
        logger.info(f"   {LogStyle.INFO} Tentando versão Playstore (button30)...")
        self.clicar_por_id(self.BTN_INICIAR_VENDA_SEM_CLIENTE)

    def selecionar_cliente(self, identificador: str):
        """Seleciona cliente pelo identificador."""
        logger.info(f"{LogStyle.ACAO} Selecionando cliente: {LogStyle.valor(identificador)}")
        self.digitar_por_id(self.EDT_BUSCA_CLIENTE, identificador)
        self.pressionar_pesquisar()
        self.encontrar_por_id(self.BTN_CONFIRMAR_CLIENTE, tempo_espera=10)  # Aguarda servidor retornar resultados
        self.clicar_por_id(self.BTN_CONFIRMAR_CLIENTE)

    def adicionar_produto(self, codigo: str = "123"):
        """Adiciona produto pelo código."""
        logger.info(f"{LogStyle.ACAO} Adicionando produto: {LogStyle.valor(codigo)}")
        self.clicar_por_id(self.BTN_ADICIONAR_PRODUTOS)
        self.digitar_por_id(self.EDT_BUSCA_PRODUTO, codigo)
        self.clicar_por_id(self.IMG_PRODUTO)

    def clicar_avancar(self):
        """Clica no botão avançar."""
        logger.info(f"{LogStyle.ACAO} Clicando em {LogStyle.elemento('Avançar')}...")
        # Espera extra para estabilizar transição
        elemento = self.encontrar_clicavel_por_id(self.BTN_PROXIMO)
        time.sleep(1.5)
        elemento.click()

    def selecionar_pagamento_dinheiro(self, com_cliente: bool = True):
        """
        Seleciona forma de pagamento dinheiro.

        Args:
            com_cliente: Se True, verifica alerta de cashback após avançar.
                        Se False (consumidor), não verifica.
        """
        logger.info(f"{LogStyle.ACAO} Selecionando pagamento: {LogStyle.valor('DINHEIRO')}")
        self.clicar_por_texto("DINHEIRO")
        self.clicar_por_id(self.BTN_AVANCAR)

        # Trata alerta de cashback (somente para vendas com cliente)
        if com_cliente:
            self.tratar_alerta_cashback()

    def tratar_popup_bonus(self):
        """Trata popup de BÔNUS DISPONÍVEL se aparecer."""
        if self.texto_exibido(self.TXT_BONUS_DISPONIVEL, tempo_espera=3):
            logger.info(f"{LogStyle.ACAO} Popup {LogStyle.elemento('BÔNUS DISPONÍVEL')} detectado. Clicando em 'Mais tarde'...")
            self.clicar_por_id(self.BTN_MAIS_TARDE)

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
            logger.info(f"   {LogStyle.OK} Alerta de cashback tratado com sucesso")
        else:
            logger.info(f"   {LogStyle.INFO} Alerta de cashback não apareceu (cliente sem cashback ou já utilizado)")

    def finalizar_venda(self):
        """Finaliza a venda."""
        logger.info(f"{LogStyle.ACAO} Finalizando venda...")
        self.tratar_popup_bonus()  # Trata popup de bonus se aparecer
        self.aguardar_texto("Finalizar")
        self.clicar_por_id(self.BTN_FINALIZAR)

    def responder_impressao(self, imprimir: bool = None):
        """
        Responde ao diálogo de impressão do cupom de venda.

        Args:
            imprimir: Se None, usa a configuração global (test_data.PRINT_CUPOM_VENDA).
                     Se True/False, sobrescreve a configuração global para este teste.
        """
        # Usa configuração global se não especificado
        if imprimir is None:
            imprimir = test_data.PRINT_CUPOM_VENDA

        timeout = test_data.PRINT_DIALOG_TIMEOUT
        logger.info(f"{LogStyle.ACAO} Respondendo impressão cupom venda: {LogStyle.valor('SIM' if imprimir else 'NÃO')} (config: {test_data.PRINT_CUPOM_VENDA})")
        btn = self.BTN_IMPRIMIR_SIM if imprimir else self.BTN_IMPRIMIR_NAO
        self.clicar_se_existir(btn, tempo_espera=timeout)
        time.sleep(2)  # Aguarda fechamento do diálogo

    def responder_dialogo_cupom_troca(self, imprimir: bool = None):
        """
        Responde ao diálogo de cupom de troca que pode aparecer ANTES da tela de sucesso.
        Este diálogo só aparece se o sistema tiver parâmetro habilitado.

        Args:
            imprimir: Se None, usa a configuração global (test_data.PRINT_CUPOM_TROCA).
                     Se True/False, sobrescreve a configuração global para este teste.
        """
        # Usa configuração global se não especificado
        if imprimir is None:
            imprimir = test_data.PRINT_CUPOM_TROCA

        timeout = test_data.PRINT_DIALOG_TIMEOUT
        logger.info(f"{LogStyle.ACAO} Verificando diálogo cupom troca (antes da tela sucesso)...")

        # Tenta responder ao diálogo (pode não aparecer)
        if self.clicar_se_existir(self.BTN_IMPRIMIR_SIM if imprimir else self.BTN_IMPRIMIR_NAO, tempo_espera=3):
            logger.info(f"{LogStyle.OK} Diálogo cupom troca respondido: {LogStyle.valor('SIM' if imprimir else 'NÃO')}")
            time.sleep(2)
        else:
            logger.info(f"{LogStyle.INFO} Diálogo cupom troca não apareceu (parâmetro pode estar desabilitado)")

    def concluir_venda(self):
        """Clica em concluir venda após sucesso."""
        logger.info(f"{LogStyle.ACAO} Concluindo venda...")
        self.ver_e_clicar(self.BTN_CONFIRMAR_VENDA)

    def executar_venda_cliente(self, id_cliente: str = "1", codigo_produto: str = "123"):
        """Executa fluxo completo de venda para cliente."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda para cliente')}")

        self.clicar_buscar_cliente()
        self.selecionar_cliente(id_cliente)
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=True)  # Verifica cashback
        self.finalizar_venda()
        self.responder_impressao()  # Cupom de venda (diálogo automático)
        self.responder_dialogo_cupom_troca()  # Cupom de troca (pode aparecer antes da tela)

        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente concluída ✅')}")

    def executar_venda_consumidor(self, codigo_produto: str = "123"):
        """Executa fluxo completo de venda para consumidor (sem cliente)."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda consumidor')}")

        self.iniciar_venda_sem_cliente()
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=False)  # Consumidor não tem cashback
        self.finalizar_venda()
        self.responder_impressao()  # Cupom de venda (diálogo automático)
        self.responder_dialogo_cupom_troca()  # Cupom de troca (pode aparecer antes da tela)

        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda consumidor concluída ✅')}")

    def aumentar_quantidade(self, vezes: int = 1):
        """Clica btn_increase N vezes para aumentar quantidade do produto no carrinho."""
        logger.info(f"{LogStyle.ACAO} Aumentando quantidade: {LogStyle.valor(f'+{vezes}x')}")
        for _ in range(vezes):
            self.clicar_por_id(self.BTN_AUMENTAR_QTDE)

    def ativar_flag_bonus(self):
        """Ativa o switch de bônus na tela de forma de pagamento."""
        logger.info(f"{LogStyle.ACAO} Ativando flag de {LogStyle.valor('bônus')}...")
        self.clicar_se_existir(self.SWITCH_BONUS, tempo_espera=5)

    def ativar_flag_cashback(self):
        """Ativa o switch/checkbox de cashback na tela de seleção de pagamento."""
        logger.info(f"{LogStyle.ACAO} Ativando flag de {LogStyle.valor('cashback')}...")
        self.clicar_se_existir(self.SWITCH_CASHBACK, tempo_espera=5)

    def _interagir_xpath(self, xpath: str, valor: str):
        """Scroll até âncora, clica no elemento por XPath e digita valor."""
        self.scroll_nativo_ate_id(self.TXT_DESCONTO_AREA)
        elemento = self.driver.find_element(AppiumBy.XPATH, xpath)
        elemento.click()
        elemento.clear()
        elemento.send_keys(valor)
        self.realizar_scroll_para_baixo()  # fecha teclado

    def aplicar_desconto_reais(self, valor: str = "10,00"):
        """Aplica desconto em reais. XPath[2] = campo desconto (XPath[1] é acréscimo)."""
        logger.info(f"{LogStyle.ACAO} Aplicando desconto: {LogStyle.valor(f'R$ {valor}')}")
        self._interagir_xpath(self.XPATH_DESCONTO_REAIS, valor)

    def aplicar_acrescimo_reais(self, valor: str = "10,00"):
        """Aplica acréscimo em reais. XPath[1] = campo acréscimo (XPath[2] é desconto)."""
        logger.info(f"{LogStyle.ACAO} Aplicando acréscimo: {LogStyle.valor(f'R$ {valor}')}")
        self._interagir_xpath(self.XPATH_ACRESCIMO_REAIS, valor)

    def validar_restante_zerado(self) -> bool:
        """Valida textView153 = R$ 0,00 (nenhum valor faltando, tudo pago)."""
        logger.info(f"{LogStyle.VALIDAR} Validando restante zerado ({LogStyle.elemento('textView153')})...")
        try:
            self.rolar_ate_id(self.TXT_RESTANTE, max_scrolls=3)
        except Exception:
            pass  # Pode já estar visível
        elemento = self.encontrar_por_id(self.TXT_RESTANTE, tempo_espera=5)
        if elemento:
            logger.info(f"   {LogStyle.INFO} Restante: {LogStyle.valor(elemento.text)}")
            return "0,00" in elemento.text
        return False

    def finalizar_venda_com_desconto(self):
        """Valida restante R$ 0,00 e clica btnFinalizar (com scroll). Chamado após aplicar desconto."""
        logger.info(f"{LogStyle.ACAO} Finalizando venda com desconto...")
        assert self.validar_restante_zerado(), "Restante não é R$ 0,00 — desconto não aplicado corretamente"
        self.tratar_popup_bonus()
        # ver_e_clicar: scroll automático até enxergar btnFinalizar
        self.ver_e_clicar(self.BTN_FINALIZAR)

    def executar_venda_consumidor_com_desconto(self, codigo_produto: str = "123", desconto: str = "10,00"):
        """Executa fluxo completo de venda consumidor com desconto em reais."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda consumidor com desconto')}")
        self.iniciar_venda_sem_cliente()
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=False)  # DINHEIRO + btn_proceed
        # Tela auto-scrolla pro fundo após btn_proceed
        self.tratar_popup_bonus()                              # bonus aparece → mais tarde
        # Scroll pra cima até textView127, aplica desconto, fecha teclado
        self.aplicar_desconto_reais(desconto)
        assert self.validar_restante_zerado(), "Restante não é R$ 0,00 — desconto não aplicado"
        # ver_e_clicar scrolla pro fundo até btnFinalizar
        self.ver_e_clicar(self.BTN_FINALIZAR)
        self.responder_impressao()
        self.responder_dialogo_cupom_troca()
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda consumidor com desconto concluída ✅')}")

    def executar_venda_cliente_com_desconto(self, id_cliente: str = "1", codigo_produto: str = "123", desconto: str = "10,00"):
        """Executa fluxo completo de venda cliente com desconto em reais."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente com desconto')}")
        self.clicar_buscar_cliente()
        self.selecionar_cliente(id_cliente)
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=True)   # DINHEIRO + btn_proceed + cashback → OK
        # Tela auto-scrolla pro fundo após cashback
        self.tratar_popup_bonus()                              # bonus aparece após cashback → mais tarde
        # Scroll pra cima até textView127, aplica desconto, fecha teclado
        self.aplicar_desconto_reais(desconto)
        assert self.validar_restante_zerado(), "Restante não é R$ 0,00 — desconto não aplicado"
        # ver_e_clicar scrolla pro fundo até btnFinalizar
        self.ver_e_clicar(self.BTN_FINALIZAR)
        self.responder_impressao()
        self.responder_dialogo_cupom_troca()
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente com desconto concluída ✅')}")

    def excluir_primeiro_pagamento(self):
        """Scroll (qualquer direcao via UiScrollable) ate imageView12 e confirma excluir."""
        logger.info(f"{LogStyle.ACAO} Excluindo pagamento existente...")
        # scroll_nativo_ate_id usa UiScrollable.scrollIntoView que busca nas 2 direções
        self.scroll_nativo_ate_id(self.BTN_EXCLUIR_PAGAMENTO)
        self.clicar_por_id(self.BTN_EXCLUIR_PAGAMENTO)
        self.clicar_por_texto("Excluir pagamento")

    def aplicar_bonus_cashback(self):
        """Scroll até imageView19, abre seletor → Bônus → ck_discount[1] → Aplicar."""
        logger.info(f"{LogStyle.ACAO} Aplicando bônus cashback...")
        self.scroll_nativo_ate_id(self.BTN_TIPO_PAGAMENTO)
        self.clicar_por_id(self.BTN_TIPO_PAGAMENTO)
        self.clicar_por_texto("Bônus")
        xpath_cb = '(//android.widget.CheckBox[contains(@resource-id,"ck_discount")])[1]'
        elemento = self.driver.find_element(AppiumBy.XPATH, xpath_cb)
        elemento.click()
        self.clicar_por_texto("Aplicar")

    def adicionar_dinheiro_pagamento(self):
        """btn_adiciona_pagamento → DINHEIRO → btn_pagar."""
        logger.info(f"{LogStyle.ACAO} Adicionando DINHEIRO como pagamento...")
        self.clicar_por_id(self.BTN_ADICIONAR_PAG)
        self.clicar_por_texto("DINHEIRO")
        self.clicar_por_id(self.BTN_PAGAR)

    def executar_venda_cliente_desconto_bonus(self, id_cliente: str = "1", codigo_produto: str = "123", desconto: str = "10,00", quantidade_extra: int = 2):
        """
        Venda cliente: qtde +2 (total 3), DINHEIRO → excluir, desconto + bônus, DINHEIRO + btn_pagar.
        Fluxo: add produto → +2 → avançar → DINHEIRO/skip dialogs → excluir pag →
               desconto 10,00 → bônus → DINHEIRO → btnFinalizar.
        """
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente desconto + bônus')}")
        self.clicar_buscar_cliente()
        self.selecionar_cliente(id_cliente)
        self.adicionar_produto(codigo_produto)
        self.aumentar_quantidade(quantidade_extra)             # btn_increase ×2 → total 3
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=True)   # DINHEIRO + btn_proceed + cashback(OK)
        self.tratar_popup_bonus()                              # popup bônus → mais tarde
        # Safety net: cashback dialog pode aparecer com delay depois do popup de bonus
        self.clicar_se_existir(self.BTN_CONFIRMAR_CASHBACK, tempo_espera=6)
        # Tela scrollada pro fundo — reprocessa: excluir DINHEIRO, aplicar desconto+bônus, readicionar
        self.excluir_primeiro_pagamento()                      # scroll UiScrollable → imageView12 → Excluir
        self.aplicar_desconto_reais(desconto)                  # scroll ↑ textView127 → XPath[2] → 10,00
        self.aplicar_bonus_cashback()                          # imageView19 → Bônus → ck_discount[1] → Aplicar
        self.adicionar_dinheiro_pagamento()                    # btn_adiciona_pagamento → DINHEIRO → btn_pagar
        self.ver_e_clicar(self.BTN_FINALIZAR)                  # scroll ↓ → clica
        self.responder_impressao()
        self.responder_dialogo_cupom_troca()
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente desconto + bônus concluída ✅')}")

    def executar_venda_cliente_desconto_cashback(self, id_cliente: str = "1", codigo_produto: str = "123", desconto: str = "10,00", quantidade_extra: int = 2):
        """
        Venda cliente: qtde +2 (total 3), marca cashback → DINHEIRO/skip dialogs → desconto → finalizar.
        Diferente do bônus: nao remove DINHEIRO; cashback aplicado via flag antes de selecionar pagamento.
        """
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente desconto + cashback')}")
        self.clicar_buscar_cliente()
        self.selecionar_cliente(id_cliente)
        self.adicionar_produto(codigo_produto)
        self.aumentar_quantidade(quantidade_extra)             # btn_increase ×2 → total 3
        self.clicar_avancar()
        self.ativar_flag_cashback()                            # switch_cashback na tela seleção pagamento
        self.selecionar_pagamento_dinheiro(com_cliente=True)   # DINHEIRO + btn_proceed + cashback(OK)
        self.tratar_popup_bonus()                              # popup bônus → mais tarde
        self.clicar_se_existir(self.BTN_CONFIRMAR_CASHBACK, tempo_espera=6)  # safety net cashback dialog
        self.aplicar_desconto_reais(desconto)                  # scroll ↑ textView127 → XPath[2] → 10,00
        self.ver_e_clicar(self.BTN_FINALIZAR)                  # scroll ↓ → clica
        self.responder_impressao()
        self.responder_dialogo_cupom_troca()
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente desconto + cashback concluída ✅')}")

    def executar_venda_consumidor_com_acrescimo(self, codigo_produto: str = "123", acrescimo: str = "10,00"):
        """Executa fluxo completo de venda consumidor com acréscimo em reais."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda consumidor com acréscimo')}")
        self.iniciar_venda_sem_cliente()
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=False)
        self.tratar_popup_bonus()
        self.aplicar_acrescimo_reais(acrescimo)
        assert self.validar_restante_zerado(), "Restante não é R$ 0,00 — acréscimo não aplicado"
        self.ver_e_clicar(self.BTN_FINALIZAR)
        self.responder_impressao()
        self.responder_dialogo_cupom_troca()
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda consumidor com acréscimo concluída ✅')}")

    def executar_venda_cliente_com_acrescimo(self, id_cliente: str = "1", codigo_produto: str = "123", acrescimo: str = "10,00"):
        """Executa fluxo completo de venda cliente com acréscimo em reais."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente com acréscimo')}")
        self.clicar_buscar_cliente()
        self.selecionar_cliente(id_cliente)
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=True)
        self.tratar_popup_bonus()
        self.aplicar_acrescimo_reais(acrescimo)
        assert self.validar_restante_zerado(), "Restante não é R$ 0,00 — acréscimo não aplicado"
        self.ver_e_clicar(self.BTN_FINALIZAR)
        self.responder_impressao()
        self.responder_dialogo_cupom_troca()
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente com acréscimo concluída ✅')}")

    # --- Validações ---
    def venda_sucesso_exibida(self, timeout: int = 10) -> bool:
        """Verifica se mensagem de sucesso apareceu."""
        return self.texto_exibido("Venda realizada com sucesso!", timeout)

    def validar_sucesso_e_concluir(self):
        """
        Valida sucesso, processa impressões da tela e conclui venda.

        IMPORTANTE: Este método processa TODAS as impressões configuradas no Dashboard:
        - NFC-E (se habilitado)
        - DANFE (se habilitado)
        - Cupom de Troca botão (se habilitado e não foi perguntado antes)
        """
        from pages.venda_sucesso_page import VendaSucessoPage

        logger.info(f"{LogStyle.VALIDAR} Aguardando {LogStyle.elemento('Venda realizada com sucesso!')}")
        self.aguardar_texto("Venda realizada com sucesso!")

        # Processa TODAS as impressões da tela de sucesso (ordem XML)
        sucesso_page = VendaSucessoPage(self.driver)
        sucesso_page.processar_todas_impressoes()

        # Concluir venda
        self.concluir_venda()
