"""
Vale Presente Page - Page Object para tela de vale presente.
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle
from test_data import test_data


class ValePresentePage(BasePage):
    """Page Object para funcionalidades de vale presente."""

    # ========== LOCATORS ==========

    # Tela inicial
    TXT_VALE_PRESENTE = "Vale Presente"

    # Tela Escolher Vendedor
    TXT_VENDEDOR_NOME = "txt_dialog_seller_name"

    # Resumo do Vale Presente
    TXT_CLIENTE = "textView194"
    TXT_NOME_VALE = "textView196"
    TXT_NUMERO_VALE = "textView197"
    TXT_VALOR_VALE = "textView198"

    # Campo de valor do vale
    EDT_VALOR = "textInputEditText"

    # Botões
    BTN_FINALIZAR = "btn_finalizar"
    BTN_PROCEED = "btn_proceed"
    BTN_FINALIZAR_PAGAMENTO = "btnFinalizar"
    BTN_CONFIRMAR_VENDA = "btn_confirmar_venda"

    # Diálogo Impressão
    BTN_NAO = "android:id/button2"
    BTN_SIM = "android:id/button1"

    # Alerta de giftback/cashback
    BTN_CONFIRMAR_CASHBACK = "md_buttonDefaultPositive"

    # ========== AÇÕES ==========

    def navegar_para_vale_presente(self):
        """Navega para a tela de Vale Presente."""
        logger.info(f"{LogStyle.ACAO} Navegando para {LogStyle.elemento('Vale Presente')}...")
        self.clicar_por_texto(self.TXT_VALE_PRESENTE)

    def selecionar_vendedor(self):
        """Seleciona o vendedor na lista."""
        logger.info(f"{LogStyle.ACAO} Selecionando vendedor...")
        self.clicar_por_id(self.TXT_VENDEDOR_NOME)

    def obter_dados_resumo_vale_presente(self) -> dict:
        """
        Extrai e valida os dados do resumo do Vale Presente.

        Returns:
            dict: Dicionário com os dados extraídos (cliente, nome_vale, numero_vale, valor)

        Raises:
            Exception: Se algum campo estiver vazio ou não for encontrado
        """
        logger.info(f"{LogStyle.VALIDAR} Extraindo dados do resumo do Vale Presente...")

        # Coleta os textos da tela usando os IDs
        cliente = self.encontrar_clicavel_por_id(self.TXT_CLIENTE, tempo_espera=5).text
        nome_vale = self.encontrar_clicavel_por_id(self.TXT_NOME_VALE, tempo_espera=2).text
        numero_vale = self.encontrar_clicavel_por_id(self.TXT_NUMERO_VALE, tempo_espera=2).text
        valor = self.encontrar_clicavel_por_id(self.TXT_VALOR_VALE, tempo_espera=2).text

        # Valida se houve alguma falha de carregamento no App
        # numero_vale pode ser vazio (PDV auto-gera após inserção do valor)
        if not cliente or not valor:
            raise Exception("Falha na validação: Um ou mais campos do resumo estão vazios!")

        # Imprime os dados capturados no log
        logger.info(f"   {LogStyle.OK} Cliente: {LogStyle.valor(cliente)}")
        logger.info(f"   {LogStyle.OK} Produto: {LogStyle.valor(nome_vale)}")
        logger.info(f"   {LogStyle.OK} Número: {LogStyle.valor(numero_vale)}")
        logger.info(f"   {LogStyle.OK} Valor: {LogStyle.valor(valor)}")

        return {
            "cliente": cliente,
            "nome_vale": nome_vale,
            "numero_vale": numero_vale,
            "valor": valor
        }

    def tratar_alerta_cashback(self):
        """Trata alerta de giftback/cashback que pode aparecer após avançar pagamento."""
        logger.info(f"{LogStyle.ACAO} Verificando alerta de cashback (giftback)...")
        if self.texto_exibido("cupons de cashback disponíveis", tempo_espera=3):
            logger.info(f"   {LogStyle.OK} Alerta de cashback detectado. Clicando em OK...")
            self.clicar_por_id(self.BTN_CONFIRMAR_CASHBACK)
            time.sleep(1)
            logger.info(f"   {LogStyle.OK} Alerta de cashback tratado com sucesso")
        else:
            logger.info(f"   {LogStyle.INFO} Alerta de cashback não apareceu")

    def inserir_valor_vale(self, valor: str = None):
        """
        Insere o valor do vale presente.
        ATENÇÃO: EDT_VALOR (textInputEditText) é um LinearLayout — send_keys falha nele.
        Estratégia: clicar no container → encontrar EditText filho pelo hint → limpar → digitar.
        """
        if valor is None:
            valor = test_data.VALE_VALUE
        logger.info(f"{LogStyle.ACAO} Inserindo valor do vale: {LogStyle.valor(valor)}...")
        # 1. Clica no container para disparar o foco no EditText interno
        self.clicar_se_existir(self.EDT_VALOR, tempo_espera=5)
        time.sleep(0.5)
        # 2. Usa o elemento atualmente focado (EditText filho do container)
        # UiSelector().hint() não existe no UIAutomator2 — active_element é mais robusto
        campo = self.driver.switch_to.active_element
        campo.clear()
        campo.send_keys(valor)
        time.sleep(0.5)
        # 3. Fecha teclado para liberar o btn_finalizar
        self.fechar_teclado()

    def clicar_finalizar(self):
        """Clica no botão FINALIZAR (usa ver_e_clicar — teclado pode cobri-lo)."""
        logger.info(f"{LogStyle.ACAO} Clicando em {LogStyle.elemento('FINALIZAR')}...")
        self.ver_e_clicar(self.BTN_FINALIZAR)

    def selecionar_pagamento_dinheiro(self):
        """Seleciona forma de pagamento dinheiro."""
        logger.info(f"{LogStyle.ACAO} Selecionando atalho de pagamento: {LogStyle.valor('DINHEIRO')}")
        time.sleep(1)  # Aguarda tela estabilizar
        self.clicar_por_texto("DINHEIRO")

    def clicar_avancar_pagamento(self):
        """Clica no botão Avançar com a forma selecionada."""
        logger.info(f"{LogStyle.ACAO} Clicando em {LogStyle.elemento('Avançar')}...")
        self.clicar_por_id(self.BTN_PROCEED)

    def finalizar_pagamento(self):
        """Clica no botão finalizar no pagamento (validar_texto_e_clicar_por_id do legado)."""
        logger.info(f"{LogStyle.ACAO} Clicando em {LogStyle.elemento('Finalizar')} no pagamento...")
        # Linha 52 do legado: validar_texto_e_clicar_por_id(driver, "Finalizar", "btnFinalizar")
        # Primeiro valida que o texto "Finalizar" está na tela, depois clica no botão
        self.aguardar_texto("Finalizar", tempo_espera=10)
        self.clicar_por_id(self.BTN_FINALIZAR_PAGAMENTO)

    def responder_impressao(self, imprimir: bool = None):
        """
        Responde ao diálogo de impressão do cupom.

        Args:
            imprimir: Se None, usa a configuração global (test_data.PRINT_CUPOM_VENDA).
                     Se True/False, sobrescreve a configuração global para este teste.
        """
        if imprimir is None:
            imprimir = test_data.PRINT_CUPOM_VENDA

        timeout = test_data.PRINT_DIALOG_TIMEOUT
        logger.info(f"{LogStyle.ACAO} Respondendo impressão cupom: {LogStyle.valor('SIM' if imprimir else 'NÃO')} (aguardando até {timeout}s)")
        btn = self.BTN_SIM if imprimir else self.BTN_NAO
        self.clicar_se_existir(btn, tempo_espera=timeout)
        time.sleep(2)  # Aguarda fechamento do diálogo

    def concluir_venda(self):
        """Clica no botão CONCLUIR VENDA após sucesso."""
        logger.info(f"{LogStyle.ACAO} Concluindo venda...")
        self.ver_e_clicar(self.BTN_CONFIRMAR_VENDA)

    # ========== VALIDAÇÕES ==========

    def venda_sucesso_exibida(self, timeout: int = 15) -> bool:
        """Verifica se a mensagem de sucesso apareceu."""
        logger.info(f"{LogStyle.VALIDAR} Aguardando mensagem de sucesso...")
        return self.texto_exibido("Venda realizada com sucesso!", timeout)

    def executar_fluxo_completo_vale_presente(self):
        """
        Executa o fluxo completo de venda de vale presente.

        Returns:
            dict: Dados extraídos do resumo do vale presente
        """
        from pages.venda_sucesso_page import VendaSucessoPage

        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda Vale Presente')}")

        self.navegar_para_vale_presente()
        self.selecionar_vendedor()

        # Valida dados do Vale Presente na tela
        dados = self.obter_dados_resumo_vale_presente()

        self.inserir_valor_vale()
        self.clicar_finalizar()
        self.selecionar_pagamento_dinheiro()
        self.clicar_avancar_pagamento()
        self.tratar_alerta_cashback()
        self.finalizar_pagamento()
        self.responder_impressao()
        time.sleep(2)  # Aguarda fechamento do diálogo de impressão

        # Tela de sucesso — processa impressões opcionais (NFC-E, DANFE, cupom troca)
        sucesso = VendaSucessoPage(self.driver)
        sucesso.processar_todas_impressoes()

        # Valida mensagem de sucesso
        assert self.venda_sucesso_exibida(), "Mensagem de sucesso não foi exibida!"

        sucesso.concluir_venda()

        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda Vale Presente concluída ✅')}")

        return dados
