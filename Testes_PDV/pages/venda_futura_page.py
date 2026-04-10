"""
Venda Futura Page - Page Object para tela de venda futura.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from config import logger, LogStyle, Cores, log_acao, log_passo_teste, log_tecnico, SimbolosASCII
from test_data import test_data


class VendaFuturaPage(BasePage):
    """Page Object para tela de venda futura."""

    # --- Locators ---
    BTN_VENDA_FUTURA_LOJA = "btn_venda_futura_loja"
    BTN_VENDA_FUTURA_DOMICILIO = "btn_venda_futura_domicilio"
    TXT_VENDEDOR = "txt_dialog_seller_name"
    EDT_CPF = "edtCpf"
    BTN_CONFIRMAR_CPF = "button30"
    BTN_ADICIONAR_PRODUTOS = "btn_adicionar_produtos"
    EDT_BUSCA_PRODUTO = "editText"
    IMG_PRODUTO = "imageView3"
    BTN_PROXIMO = "btn_proximo"
    BTN_AVANCAR = "btn_proceed"
    TXT_PAGAMENTO_TITULO = "txt_payment_title"
    TXT_OPCAO_TITULO = "txt_option_title"
    TXT_CAMPO_PAGAMENTO = "textView170"         # valor a pagar (mostra R$ 0 quando sem forma)
    IMG_PAGAMENTOS = "imageView19"
    BTN_PAGAR = "btn_pagar"
    TXT_VALOR_PAGO = "txt_checkout_total_pay3"       # total pago
    TXT_TOTAL_VENDA = "txt_checkout_total_payments3" # total da venda
    BTN_FINALIZAR = "btnFinalizar"
    BTN_CONFIRMAR_VENDA = "btn_confirmar_venda"
    BTN_IMPRIMIR_NAO = "android:id/button2"
    BTN_MAIS_TARDE = "btn_mais_tarde"

    # Alerta de giftback/cashback (após selecionar pagamento)
    BTN_CONFIRMAR_CASHBACK = "md_buttonDefaultPositive"

    # --- Ações ---
    def clicar_venda_futura(self):
        """Clica no botão Venda Futura na tela inicial."""
        self.clicar_por_texto("Venda Futura")

    def selecionar_retirada_loja(self):
        """Seleciona opção 'Retirada em loja'."""
        self.clicar_por_id(self.BTN_VENDA_FUTURA_LOJA)

    def selecionar_entrega_domicilio(self):
        """Seleciona opção 'Entrega em Domicílio' e avança Frete."""
        self.clicar_por_id(self.BTN_VENDA_FUTURA_DOMICILIO)
        self.clicar_por_texto("Avançar")

    def avancar_tipo_entrega(self):
        """Avança na tela de tipo de entrega."""
        self.clicar_por_texto("Avançar")

    def selecionar_vendedor(self):
        """Seleciona o vendedor."""
        self.clicar_por_id(self.TXT_VENDEDOR)

    def buscar_cliente_cpf(self, cpf: str = "1"):
        """Busca cliente pelo CPF."""
        self.clicar_por_id(self.EDT_CPF)
        self.digitar_por_id(self.EDT_CPF, cpf)
        self.clicar_por_id(self.BTN_CONFIRMAR_CPF)

    def adicionar_produto(self, codigo: str = "1234", tamanho: str = "38"):
        """Adiciona produto com tamanho específico."""
        self.clicar_por_id(self.BTN_ADICIONAR_PRODUTOS)
        self.digitar_por_id(self.EDT_BUSCA_PRODUTO, codigo)
        self.clicar_por_id(self.IMG_PRODUTO)
        self.clicar_por_texto(tamanho)

    def clicar_avancar(self):
        """Clica no botão avançar."""
        log_tecnico("-> Clicando em Avançar (com espera)...", "info")
        elemento = self.encontrar_clicavel_por_id(self.BTN_PROXIMO)
        time.sleep(1.5)
        elemento.click()

    def selecionar_pagamento_avista(self):
        """Seleciona pagamento: Movimento de Caixa A VISTA + Plano de Venda A VISTA."""
        log_tecnico("-> Selecionando pagamento à vista...", "info")
        time.sleep(3)

        # 1. Clica em pagamento personalizado
        self.clicar_por_id(self.TXT_PAGAMENTO_TITULO)
        time.sleep(2)  # Aguarda opções de Movimento de Caixa carregarem

        # 2. Movimento de Caixa: A VISTA (primeiro elemento com texto "A VISTA")
        log_tecnico("   -> Movimento de Caixa: selecionando 1º A VISTA...", "info")
        count_antes = self.contar_elementos_visiveis_por_texto("A VISTA")
        log_tecnico(f"   [DEBUG] Elementos 'A VISTA' visíveis antes do clique: {count_antes}", "info")

        try:
            # Tenta clicar no primeiro "A VISTA" visível (índice 0)
            self.clicar_no_enesimo_texto("A VISTA", indice=0, tempo_espera=5)
            log_tecnico("   [OK] Movimento de Caixa A VISTA selecionado", "info")
        except Exception as e:
            # Fallback: tenta scroll e clique simples
            log_tecnico(f"   [AVISO] Método de índice falhou: {e}. Tentando scroll...", "warning")
            self.rolar_ate_texto("A VISTA")
            self.clicar_por_texto("A VISTA")
            log_tecnico("   [OK] Movimento de Caixa A VISTA selecionado (via scroll)", "info")

        time.sleep(3)  # Aguarda Plano de Venda ser liberado e Movimento de Caixa fechar

        # 3. Plano de Venda: A VISTA (segundo elemento, ou único se dropdown fechou)
        log_tecnico("   -> Plano de Venda: selecionando A VISTA...", "info")
        count_depois = self.contar_elementos_visiveis_por_texto("A VISTA")
        log_tecnico(f"   [DEBUG] Elementos 'A VISTA' visíveis agora: {count_depois}", "info")

        try:
            if count_depois >= 2:
                log_tecnico("   [INFO] 2 elementos 'A VISTA' visíveis. Clicando no 2º (Plano de Venda)...", "info")
                self.clicar_no_enesimo_texto("A VISTA", indice=1, tempo_espera=3)
                log_tecnico("   [OK] Plano de Venda A VISTA selecionado (2º elemento)", "info")
            elif count_depois == 1:
                log_tecnico("   [INFO] 1 elemento 'A VISTA' visível. Clicando nele (Plano de Venda)...", "info")
                self.clicar_no_enesimo_texto("A VISTA", indice=0, tempo_espera=3)
                log_tecnico("   [OK] Plano de Venda A VISTA selecionado (único elemento)", "info")
            else:
                raise Exception(f"Nenhum elemento 'A VISTA' encontrado para Plano de Venda")
        except Exception as e:
            log_tecnico(f"   [ERRO] Falha ao selecionar Plano de Venda: {e}", "error")
            raise

        # 4. Avança
        time.sleep(1)
        log_tecnico("   -> Clicando em Avançar (btn_proceed)...", "info")
        self.clicar_por_id(self.BTN_AVANCAR)

    def tratar_alerta_cashback(self):
        """Trata alerta de giftback/cashback que pode aparecer após selecionar pagamento."""
        log_tecnico("-> Verificando alerta de cashback (giftback)...", "info")
        if self.texto_exibido("cupons de cashback disponíveis", tempo_espera=3):
            log_tecnico("   [OK] Alerta de cashback detectado. Clicando em OK...", "info")
            self.clicar_por_id(self.BTN_CONFIRMAR_CASHBACK)
            time.sleep(1)
            log_tecnico("   [OK] Alerta de cashback tratado com sucesso", "info")
        else:
            log_tecnico("   [INFO] Alerta de cashback não apareceu", "info")

    def tratar_popup_bonus(self):
        """Trata popup de bônus se aparecer."""
        log_tecnico("-> Verificando popup de bônus...", "info")
        time.sleep(3)

        if self.clicar_se_existir(self.BTN_MAIS_TARDE, tempo_espera=2):
            log_tecnico("   [OK] Popup de bônus fechado", "info")
            time.sleep(2)
        else:
            log_tecnico("   [INFO] Nenhum popup de bônus", "info")

    def selecionar_forma_dinheiro(self):
        """Seleciona forma de pagamento DINHEIRO.
        Scroll nativo até textView170 (campo pagamento = R$ 0) para garantir que
        imageView19 esteja visível, independente do estado do scroll da tela.
        """
        self.scroll_nativo_ate_id(self.TXT_CAMPO_PAGAMENTO)
        self.clicar_por_id(self.IMG_PAGAMENTOS)
        self.clicar_por_texto("DINHEIRO")
        self.clicar_por_id(self.BTN_PAGAR)

    def finalizar_venda(self):
        """Scroll até btnFinalizar. Valida pago == total antes de clicar."""
        try:
            pago = self.encontrar_por_id(self.TXT_VALOR_PAGO, tempo_espera=3).text
            total = self.encontrar_por_id(self.TXT_TOTAL_VENDA, tempo_espera=3).text
            log_tecnico(f"   [VALIDAR] Pago={pago} | Total={total}", "info")
            if pago != total:
                log_tecnico(f"   [AVISO] Pago != Total — forma de pagamento pode estar incompleta", "warning")
        except Exception:
            pass
        log_acao(f"{SimbolosASCII.SCROLL} Localizando botão Finalizar")
        self.ver_e_clicar(self.BTN_FINALIZAR)

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
        log_tecnico(f"-> Respondendo impressão cupom venda: {'SIM' if imprimir else 'NÃO'} (config: {test_data.PRINT_CUPOM_VENDA})", "info")
        btn = "android:id/button1" if imprimir else self.BTN_IMPRIMIR_NAO
        self.clicar_se_existir(btn, tempo_espera=timeout)
        time.sleep(2)

    def responder_dialogo_cupom_troca(self, imprimir: bool = None):
        """
        Responde ao diálogo de cupom de troca que pode aparecer ANTES da tela de sucesso.

        Args:
            imprimir: Se None, usa a configuração global (test_data.PRINT_CUPOM_TROCA).
                     Se True/False, sobrescreve a configuração global para este teste.
        """
        if imprimir is None:
            imprimir = test_data.PRINT_CUPOM_TROCA

        timeout = test_data.PRINT_DIALOG_TIMEOUT
        log_tecnico("-> Verificando diálogo cupom troca (antes da tela sucesso)...", "info")

        btn = "android:id/button1" if imprimir else self.BTN_IMPRIMIR_NAO
        if self.clicar_se_existir(btn, tempo_espera=3):
            log_tecnico(f"   [OK] Diálogo cupom troca respondido: {'SIM' if imprimir else 'NÃO'}", "info")
            time.sleep(2)
        else:
            log_tecnico("   [INFO] Diálogo cupom troca não apareceu", "info")

    def concluir_venda(self):
        """Clica em concluir venda após sucesso."""
        self.ver_e_clicar(self.BTN_CONFIRMAR_VENDA)

    def executar_venda_futura(self, cpf: str = "1", codigo_produto: str = "1234", tamanho: str = "38"):
        """Executa fluxo completo de venda futura com retirada em loja."""
        log_passo_teste("Iniciando Venda Futura - Retirada em Loja")
        log_tecnico("--- [FLUXO] Iniciando venda futura (retirada loja) ---", "info")

        log_acao("Selecionando tipo de entrega: Retirada em Loja")
        self.selecionar_retirada_loja()

        log_acao("Avançando para próxima etapa")
        self.avancar_tipo_entrega()

        log_acao("Selecionando vendedor")
        self.selecionar_vendedor()

        log_acao(f"Buscando cliente CPF: {cpf}")
        self.buscar_cliente_cpf(cpf)

        log_acao(f"Adicionando produto {codigo_produto} tamanho {tamanho}")
        self.adicionar_produto(codigo_produto, tamanho)

        log_acao("Avançando para pagamento")
        self.clicar_avancar()

        log_acao("Configurando pagamento à vista")
        self.selecionar_pagamento_avista()

        log_acao("Verificando alerta de cashback (giftback)")
        self.tratar_alerta_cashback()

        log_acao("Verificando popup de bônus")
        self.tratar_popup_bonus()

        log_acao("Selecionando forma de pagamento: Dinheiro")
        self.selecionar_forma_dinheiro()

        log_acao("Finalizando venda")
        self.finalizar_venda()

        log_acao("Respondendo diálogo de impressão cupom venda")
        self.responder_impressao()  # Cupom de venda (diálogo automático)

        log_passo_teste("Venda Futura Concluída")
        log_tecnico("--- [FLUXO] Venda futura (retirada loja) executada ---", "info")

    def executar_venda_futura_domicilio(self, cpf: str = "1", codigo_produto: str = "1234", tamanho: str = "38"):
        """Executa fluxo completo de venda futura com entrega em domicílio."""
        log_passo_teste("Iniciando Venda Futura - Entrega em Domicílio")
        log_tecnico("--- [FLUXO] Iniciando venda futura (domicílio) ---", "info")

        log_acao("Selecionando tipo de entrega: Domicílio")
        self.selecionar_entrega_domicilio()  # Já inclui avançar frete

        log_acao("Selecionando vendedor")
        self.selecionar_vendedor()

        log_acao(f"Buscando cliente CPF: {cpf}")
        self.buscar_cliente_cpf(cpf)

        log_acao(f"Adicionando produto {codigo_produto} tamanho {tamanho}")
        self.adicionar_produto(codigo_produto, tamanho)

        log_acao("Avançando para pagamento")
        self.clicar_avancar()

        log_acao("Configurando pagamento à vista")
        self.selecionar_pagamento_avista()

        log_acao("Verificando alerta de cashback (giftback)")
        self.tratar_alerta_cashback()

        log_acao("Verificando popup de bônus")
        self.tratar_popup_bonus()

        log_acao("Selecionando forma de pagamento: Dinheiro")
        self.selecionar_forma_dinheiro()

        log_acao("Finalizando venda")
        self.finalizar_venda()

        log_acao("Respondendo diálogo de impressão cupom venda")
        self.responder_impressao()  # Cupom de venda (diálogo automático)

        log_passo_teste("Venda Futura Domicílio Concluída")
        log_tecnico("--- [FLUXO] Venda futura (domicílio) executada ---", "info")

    # --- Validações ---
    def venda_sucesso_exibida(self, timeout: int = 10) -> bool:
        """Verifica se mensagem de sucesso apareceu."""
        return self.texto_exibido("Venda realizada com sucesso!", timeout)

    def validar_sucesso_e_concluir(self):
        """Valida sucesso e conclui venda."""
        self.aguardar_texto("Venda realizada com sucesso!")
        self.concluir_venda()
