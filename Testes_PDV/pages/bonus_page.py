"""
Bonus Page - Page Object para tela de bonus/cashback durante pagamento.
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle
from test_data import test_data


class BonusPage(BasePage):
    """Page Object para funcionalidades de bonus/cashback."""

    # ========== LOCATORS ==========

    # Tela inicial
    TXT_INICIAR_VENDA = "Iniciar Venda"

    # Tela Escolher Vendedor
    RCW_VENDEDORES = "rcv_sellers"
    TXT_VENDEDOR_NOME = "txt_dialog_seller_name"

    # Tela Selecionar Cliente
    BTN_BUSCAR_CLIENTE = "btn_select_customer"
    BTN_NOVO_CADASTRO = "btn_novo_cadastro"
    EDT_CPF = "edtCpf"
    EDT_NOME = "edtNome"
    CHK_SEM_CPF = "chk_sem_cpf"
    BTN_INICIAR_VENDA = "button30"

    # Tela Carrinho
    CARD_USER_INFO = "card_user_info"
    BTN_ADICIONAR_PRODUTOS = "btn_adicionar_produtos"
    BTN_PROXIMO = "btn_proximo"

    # Tela Forma de Pagamento COM BONUS
    CASHBACK_CONTAINER = "cashback_promotion_container"
    TXT_MAX_BONUS = "txt_max_bonus"
    SWITCH_BONUS = "switch_bonus"
    TXT_BONUS_COMPACT = "txt_bonus_compact"
    TXT_FINAL_AMOUNT = "txt_final_amount"
    BTN_PROCEED = "btn_proceed"

    # Cashback
    ICON_CASHBACK = "icon_cashback"
    VALOR_CASHBACK = "valor_cashback"
    
    # Botoes Finais
    BTN_FINALIZAR = "btnFinalizar" 
    BTN_CONFIRMAR_VENDA = "btn_confirmar_venda"

    # Alerta de cashback
    BTN_CONFIRMAR_CASHBACK = "md_buttonDefaultPositive"

    # Dialogo Impressao
    BTN_NAO = "android:id/button2"
    BTN_SIM = "android:id/button1"

    # ========== ACOES BONUS ==========

    def bonus_disponivel(self, tempo_espera: int = 5) -> bool:
        """Verifica se o bonus esta disponivel na tela de pagamento."""
        logger.info(f"{LogStyle.VALIDAR} Verificando se bonus esta disponivel...")
        return self.elemento_existe(self.SWITCH_BONUS, tempo_espera)

    def obter_valor_bonus(self) -> str:
        """Obtem o valor maximo do bonus disponivel."""
        try:
            elemento = self.encontrar_por_id(self.TXT_MAX_BONUS)
            valor = elemento.text
            logger.info(f"   {LogStyle.OK} Valor do bonus: {LogStyle.valor(valor)}")
            return valor
        except:
            return "N/A"

    def bonus_ativado(self) -> bool:
        """Verifica se o switch de bonus esta ativado."""
        try:
            elemento = self.encontrar_por_id(self.SWITCH_BONUS, tempo_espera=3)
            return elemento.get_attribute("checked") == "true"
        except:
            return False

    def ativar_bonus(self):
        """Ativa o bonus se estiver disponivel e desativado."""
        logger.info(f"{LogStyle.ACAO} Ativando bonus...")
        if not self.bonus_ativado():
            self.clicar_por_id(self.SWITCH_BONUS)
            logger.info("   [WAIT] Aguardando recalculo...")
            time.sleep(2)
            # Poll: aguarda TXT_FINAL_AMOUNT ter valor válido (até +3s)
            for _ in range(6):
                try:
                    el = self.encontrar_por_id(self.TXT_FINAL_AMOUNT, tempo_espera=0)
                    if el and el.text and el.text.strip() not in ("", "R$ 0,00"):
                        break
                except Exception:
                    pass
                time.sleep(0.5)
            logger.info(f"   {LogStyle.OK} Bonus ativado!")
        else:
            logger.info(f"   {LogStyle.SKIP} Bonus ja estava ativado")

    def obter_valor_final(self) -> str:
        """Obtem o valor final apos aplicar bonus."""
        try:
            elemento = self.encontrar_por_id(self.TXT_FINAL_AMOUNT, tempo_espera=3)
            valor = elemento.text
            logger.info(f"   {LogStyle.OK} Valor final: {LogStyle.valor(valor)}")
            return valor
        except:
            return "N/A"

    def obter_desconto_bonus(self) -> str:
        """Obtem o texto do desconto de bonus aplicado."""
        try:
            elemento = self.encontrar_por_id(self.TXT_BONUS_COMPACT, tempo_espera=3)
            texto = elemento.text
            logger.info(f"   {LogStyle.OK} Desconto bonus: {LogStyle.valor(texto)}")
            return texto
        except:
            return "N/A"

    # ========== ACOES CASHBACK ==========

    def cashback_disponivel(self, tempo_espera: int = 5) -> bool:
        """Verifica se o cashback esta disponivel na tela."""
        logger.info(f"{LogStyle.VALIDAR} Verificando se cashback esta disponivel...")
        return self.elemento_existe(self.ICON_CASHBACK, tempo_espera)

    def obter_valor_cashback(self) -> str:
        """
        Obtem o valor do cashback disponivel e valida sua presenca.

        Returns:
            str: Valor do cashback (ex: "R$ 50,00")

        Raises:
            Exception: Se o icone ou valor do cashback nao for encontrado ou estiver vazio
        """
        logger.info(f"{LogStyle.VALIDAR} Validando saldo de cashback...")

        # 1. Valida se o ícone do cashback está na tela
        if not self.elemento_existe(self.ICON_CASHBACK, tempo_espera=5):
            raise Exception("Ícone de cashback (icon_cashback) não foi encontrado na tela")

        logger.info(f"   {LogStyle.OK} Ícone de cashback (icon_cashback) encontrado na tela")

        # 2. Busca o elemento de texto do valor do cashback
        elemento_valor = self.encontrar_clicavel_por_id(self.VALOR_CASHBACK, tempo_espera=3)

        # 3. Extrai o texto (ex: "R$ 50,00")
        valor_texto = elemento_valor.text

        # 4. Valida se está vazio ou com espaços em branco
        if not valor_texto or valor_texto.strip() == "":
            raise Exception("Falha: O campo de cashback (valor_cashback) está visível, mas está VAZIO!")

        # 5. Imprime o valor encontrado no terminal/relatório
        logger.info(f"   {LogStyle.OK} Valor de cashback disponível carregado: {LogStyle.valor(valor_texto)}")

        return valor_texto

    # ========== ACOES CASHBACK ==========

    def tratar_alerta_cashback(self):
        """Trata alerta de cashback que pode aparecer após avançar no pagamento com cliente."""
        logger.info(f"{LogStyle.ACAO} Verificando alerta de cashback...")
        if self.texto_exibido("cupons de cashback disponíveis", tempo_espera=3):
            logger.info(f"   {LogStyle.OK} Alerta de cashback detectado. Clicando em OK...")
            self.clicar_por_id(self.BTN_CONFIRMAR_CASHBACK)
            time.sleep(0.5)
            logger.info(f"   {LogStyle.OK} Alerta de cashback tratado com sucesso")
        else:
            logger.info(f"   {LogStyle.INFO} Alerta de cashback não apareceu")

    # ========== ACOES PAGAMENTO ==========

    def clicar_avancar_pagamento(self):
        """
        Clica no botao Avancar na tela de pagamento e usa o scroll funcional (rolar_ate_texto).
        """
        logger.info(f"{LogStyle.ACAO} Clicando em Avancar...")
        self.clicar_por_id(self.BTN_PROCEED)
        self.tratar_alerta_cashback()

        logger.info("   [SCROLL] Rolando até encontrar botão de Finalizar...")
        # Usa o método que já existe na BasePage
        # "Finalizar" é o texto provável do botão btnFinalizar
        try:
            self.rolar_ate_texto("Finalizar")
        except:
            # Tenta texto alternativo comum caso o primeiro não ache
            try:
                self.rolar_ate_texto("Confirmar")
            except:
                pass 

    # ========== ACOES CARRINHO ==========

    def adicionar_produto(self, codigo: str = "123"):
        logger.info(f"{LogStyle.ACAO} Adicionando produto: {LogStyle.valor(codigo)}")
        self.clicar_por_id(self.BTN_ADICIONAR_PRODUTOS)
        self.digitar_por_id("editText", codigo)
        self.clicar_por_id("imageView3")

    def clicar_avancar_carrinho(self):
        logger.info(f"{LogStyle.ACAO} Avancando do carrinho...")
        elemento = self.encontrar_clicavel_por_id(self.BTN_PROXIMO)
        time.sleep(0.5)
        elemento.click()

    # ========== ACOES CLIENTE ==========

    def buscar_cliente_por_cpf(self, cpf: str):
        logger.info(f"{LogStyle.ACAO} Buscando cliente por CPF: {LogStyle.valor(cpf)}")
        self.clicar_por_id(self.BTN_BUSCAR_CLIENTE)
        self.digitar_por_id("search_src_text", cpf)
        self.pressionar_pesquisar()
        self.clicar_por_id("button3")

    def iniciar_venda_com_cliente(self):
        logger.info(f"{LogStyle.ACAO} Iniciando venda com cliente...")
        self.clicar_por_id(self.BTN_INICIAR_VENDA)

    # ========== ACOES DIALOGO ==========

    def responder_impressao(self, imprimir: bool = None):
        """
        Event-driven: trata dialogs de impressão ao aparecer e aguarda tela de sucesso.
        Budget único 45s — sem timeouts fixos por dialog.
        """
        if imprimir is None:
            imprimir = test_data.PRINT_CUPOM_VENDA
        logger.info(f"{LogStyle.ACAO} Aguardando resultado (event-driven, cupom={'SIM' if imprimir else 'NAO'})...")
        self._aguardar_sucesso_event_driven(imprimir_cupom=imprimir, timeout=45)

    def responder_dialogo_cupom_troca(self, imprimir: bool = None):
        """Mantido para compatibilidade — event-driven já trata cupom troca em responder_impressao."""
        pass

    # ========== VALIDACOES ==========

    def tela_pagamento_exibida(self, timeout: int = 10) -> bool:
        return self.texto_exibido("Forma de Pagamento", timeout)

    def bonus_foi_aplicado(self) -> bool:
        logger.info(f"{LogStyle.VALIDAR} Verificando aplicação do bonus...")
        for i in range(5):
            try:
                valor_final = self.obter_valor_final()
                if "0,00" in valor_final or "0.00" in valor_final:
                    logger.info(f"   ✅ [OK] Valor final zerado: {valor_final}")
                    return True
                
                desconto = self.obter_desconto_bonus()
                if desconto and desconto != "N/A":
                    logger.info(f"   ✅ [OK] Desconto aplicado visível: {desconto}")
                    return True

                logger.info(f"   ⏳ Tentativa {i+1}: Valor ainda é {valor_final}. Aguardando...")
                time.sleep(1.5)
            except:
                pass
        logger.error(f"   ❌ [ERRO] Bonus não aplicado após tentativas.")
        return False

    def venda_sucesso_exibida(self, timeout: int = 15) -> bool:
        return (
            self.texto_exibido("Venda realizada com sucesso!", timeout) or
            self.texto_exibido("sucesso", timeout)
        )

    def concluir_venda(self):
        """Clica em concluir venda apos sucesso."""
        logger.info(f"{LogStyle.ACAO} Concluindo venda...")
        try:
            self.ver_e_clicar(self.BTN_CONFIRMAR_VENDA)
        except Exception:
            self.ver_e_clicar(self.BTN_FINALIZAR)