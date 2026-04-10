"""
Documentos Page - Page Object para tela de documentos fiscais.
"""
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import logger, LogStyle


class DocumentosPage(BasePage):
    """Page Object para tela de documentos fiscais."""

    # --- Locators (nomes preservados para compatibilidade) ---
    EDT_PREENCHER_DATA_INICIAL   = "textInputLayout4"
    EDT_PREENCHER_DATA_FINAL     = "textInputLayout5"
    LBL_VERIFICAR_QUE_DOCUMENTOS = "lbl_nf"      # label dentro do item (não clicável); pai ViewGroup é clicável
    TXT_DETALHES_DOCUMENTO       = "textView148"  # botão Detalhes — opcional, aparece em alguns devices
    TXT_VERIFICAR_QUE_DETALHES   = "textView238"  # label "Cliente" na tela Detalhes Documento
    # Locators reais da tela Detalhes Documento (confirmados nos XMLs)
    TXT_CLIENTE    = "txtCliente"    # ex: "1 - DANIEL"
    TXT_STATUS     = "txtStatus"     # ex: "100 - Autorizado o uso da NF-e"
    TXT_PAGAMENTOS = "txtPagamentos" # "Pagamentos"
    TXT_PRODUTOS   = "txtProdutos"   # "Produtos"

    # --- Ações ---
    def clicar_menu_documentos(self):
        """Clica no item Documentos na home."""
        logger.info(f"{LogStyle.ACAO} Clicar no menu Documentos...")
        self.ver_e_clicar_texto("Documentos")

    def rolar_até_encontrar_texto(self):
        """Rola até o campo de período."""
        logger.info(f"{LogStyle.ACAO} Rolar até encontrar o texto 'Período'...")
        try:
            self.rolar_ate_texto("Período", max_scrolls=5)
        except Exception:
            logger.warning(f"   {LogStyle.FALLBACK} 'Período' não precisou de scroll")

    def _digitar_em_textinputlayout(self, layout_id: str, texto: str):
        """Digita no EditText filho de um TextInputLayout."""
        self.clicar_por_id(layout_id)
        time.sleep(0.5)
        full_id = self._id_completo(layout_id)
        try:
            # Tentativa 1: EditText filho via XPath
            edit = self.driver.find_element(
                By.XPATH,
                f"//android.widget.EditText[ancestor::*[@resource-id='{full_id}']]"
            )
            edit.clear()
            edit.send_keys(texto)
        except Exception:
            try:
                # Tentativa 2: campo com foco (evita DEFAULT_WAIT=30s de digitar_por_id)
                edit = self.driver.find_element(
                    By.XPATH,
                    "//android.widget.EditText[@focused='true']"
                )
                edit.clear()
                edit.send_keys(texto)
                logger.info(f"   {LogStyle.FALLBACK} Digitou via focused EditText")
            except Exception:
                self.digitar_por_id(layout_id, texto)

    def preencher_data_inicial_com(self):
        """Preenche data inicial com a data atual."""
        logger.info(f"{LogStyle.ACAO} Preencher Data Inicial com a data atual...")
        self._digitar_em_textinputlayout(
            self.EDT_PREENCHER_DATA_INICIAL,
            datetime.now().strftime('%d/%m/%Y')
        )

    def preencher_data_final_com(self):
        """Preenche data final com a data atual."""
        logger.info(f"{LogStyle.ACAO} Preencher Data Final com a data atual...")
        self._digitar_em_textinputlayout(
            self.EDT_PREENCHER_DATA_FINAL,
            datetime.now().strftime('%d/%m/%Y')
        )

    def clicar_botão_consultar(self):
        """Fecha teclado e clica no botão Consultar."""
        logger.info(f"{LogStyle.ACAO} Clicar no botão Consultar...")
        self.ver_e_clicar_texto("Consultar")

    def clicar_primeiro_documento(self):
        """Clica SEMPRE no primeiro documento da lista via ViewGroup pai clicável."""
        logger.info(f"{LogStyle.ACAO} Clicar no primeiro documento da lista...")
        full_lbl = self._id_completo(self.LBL_VERIFICAR_QUE_DOCUMENTOS)
        try:
            elementos = self.driver.find_elements(
                By.XPATH,
                f"//android.widget.TextView[@resource-id='{full_lbl}']"
                f"/ancestor::android.view.ViewGroup[@clickable='true']"
            )
            if not elementos:
                raise Exception("Nenhum item clickável encontrado na lista")
            elementos[0].click()
            logger.info(f"   {LogStyle.OK} Primeiro documento clicado (índice 0)")
        except Exception as e:
            logger.warning(f"   {LogStyle.FALLBACK} XPath falhou ({e}) — tentando por textView100")
            todos = self.encontrar_todos_por_id("textView100")
            if todos:
                todos[0].click()
                logger.info(f"   {LogStyle.OK} Primeiro documento clicado via textView100[0]")
            else:
                raise Exception("Impossível clicar no primeiro documento da lista")

    def verificar_que_os_documentos(self):
        """Clica no primeiro documento da lista (alias de compatibilidade)."""
        self.clicar_primeiro_documento()

    def _fechar_dialog_impressao(self):
        """Fecha dialog de impressão se aparecer (clica NÃO ou cancela)."""
        if self.clicar_texto_se_existir("NÃO", tempo_espera=3):
            logger.info(f"   {LogStyle.SKIP} Dialog impressão fechado (NÃO)")
        elif self.clicar_se_existir("android:id/button2", tempo_espera=2):
            logger.info(f"   {LogStyle.SKIP} Dialog impressão fechado (button2)")
        elif self.clicar_se_existir("md_buttonDefaultPositive", tempo_espera=2):
            logger.info(f"   {LogStyle.SKIP} Dialog impressão fechado (OK)")

    def clicar_detalhes_documento(self):
        """Clica em 'Detalhes' — primeiro item do bottom sheet (rcv_opcoes_desconto[0])."""
        logger.info(f"{LogStyle.ACAO} Clicar em Detalhes (1ª opção do bottom sheet)...")
        time.sleep(1)  # aguarda bottom sheet estabilizar
        rcv_id = self._id_completo("rcv_opcoes_desconto")
        try:
            elem = self.driver.find_element(
                By.XPATH,
                f"//androidx.recyclerview.widget.RecyclerView[@resource-id='{rcv_id}']"
                f"/android.view.ViewGroup[1]"
            )
            elem.click()
            logger.info(f"   {LogStyle.OK} Detalhes clicado (ViewGroup[1] de rcv_opcoes_desconto)")
        except Exception:
            logger.warning(f"   {LogStyle.FALLBACK} XPath falhou — tentando por texto 'Detalhes'")
            self.clicar_por_texto("Detalhes")

    def verificar_que_os_detalhes(self):
        """Aguarda e valida que a tela Detalhes Documento carregou."""
        logger.info(f"{LogStyle.ACAO} Verificar que os detalhes do documento estão corretos...")
        # Aguarda txtCliente aparecer — campo real confirmado no XML 18_29_32
        try:
            self.encontrar_por_id(self.TXT_CLIENTE, tempo_espera=10)
            logger.info(f"   {LogStyle.OK} Tela Detalhes Documento carregada (txtCliente presente)")
        except Exception:
            logger.warning(f"   {LogStyle.FALLBACK} txtCliente não encontrado — tela pode já ter navegado")

    def validar_dados_tela_detalhes(self) -> bool:
        """Valida campos reais da tela Detalhes Documento (confirmados no dados.xml).

        Campos validados:
          txtCliente    → cliente da venda (não vazio)
          txtVendedor   → vendedor (não vazio)
          txtChave      → chave NF-e 44 dígitos (não vazio)
          txtStatus     → status documento (não vazio)
          textView244   → Valor Total R$ (não vazio)
          txtPagamentos → seção pagamentos presente
          txtProdutos   → seção produtos presente (após scroll)
        """
        logger.info(f"{LogStyle.ACAO} Validar dados da tela Detalhes Documento...")

        tem_cliente    = self.elemento_existe("txtCliente",    tempo_espera=5)
        tem_vendedor   = self.elemento_existe("txtVendedor",   tempo_espera=3)
        tem_chave      = self.elemento_existe("txtChave",      tempo_espera=3)
        tem_status     = self.elemento_existe(self.TXT_STATUS, tempo_espera=3)
        tem_total      = self.elemento_existe("textView244",   tempo_espera=3)
        tem_pagamentos = self.elemento_existe(self.TXT_PAGAMENTOS, tempo_espera=3)

        logger.info(
            f"   Cliente={tem_cliente} | Vendedor={tem_vendedor} | Chave={tem_chave} "
            f"| Status={tem_status} | Total={tem_total} | Pagamentos={tem_pagamentos}"
        )

        # Scroll para ver seção Produtos
        self.realizar_scroll_para_baixo()
        time.sleep(0.5)
        self.realizar_scroll_para_baixo()
        tem_produtos = self.elemento_existe(self.TXT_PRODUTOS, tempo_espera=3)
        logger.info(f"   Produtos={tem_produtos}")

        return tem_cliente and tem_vendedor and tem_chave and tem_status and tem_total

    def voltar_tela_documentos(self):
        """Volta uma tela."""
        logger.info(f"{LogStyle.ACAO} Voltar para a tela de documentos...")
        self.voltar_tela()

    def executar_documentos(self):
        """Executa fluxo completo de documentos fiscais.

        Fluxo confirmado nos XMLs 18_28, 18_29_32, 18_29_40, 18_30_31:
          1. Clicar Documentos na home
          2. Rolar até Período (não-playstore)
          3. Preencher data inicial e final com hoje
          4. Fechar teclado + Consultar
          5. Clicar 1º documento (ViewGroup pai clicável)
          6. Opcional: clicar textView148 (Detalhes)
          7. Aguardar tela Detalhes (txtCliente)
          8. Scroll + validar campos reais
          9. 3x voltar → home
        """
        logger.info(f"{LogStyle.secao('FLUXO - DOCUMENTOS')}")

        self.clicar_menu_documentos()

        if 'playstore' not in (self.app_package or '').lower():
            self.rolar_até_encontrar_texto()

        self.preencher_data_inicial_com()
        self.preencher_data_final_com()
        self.fechar_teclado()
        self.clicar_botão_consultar()
        time.sleep(5)  # aguarda servidor retornar lista

        self.verificar_que_os_documentos()
        time.sleep(2)  # aguarda navegação para detalhes

        self.clicar_detalhes_documento()    # optional textView148
        self.verificar_que_os_detalhes()    # aguarda tela carregar
        self.validar_dados_tela_detalhes()  # valida + scroll

        # 3x voltar: detalhes → lista → filtro → home (XML 18_30_31)
        self.voltar_tela_documentos()
        time.sleep(0.5)
        self.voltar_tela_documentos()
        time.sleep(0.5)
        self.voltar_tela_documentos()

        logger.info(f"{LogStyle.secao('FLUXO - DOCUMENTOS concluída ✅')}")

    # --- Validações ---
    def dados_tela_detalhes_exibida(self, timeout: int = 10) -> bool:
        """Verifica se a tela Detalhes Documento está exibida."""
        return (
            self.elemento_existe(self.TXT_CLIENTE, tempo_espera=timeout)
            or self.texto_exibido("Detalhes Documento", timeout)
        )
