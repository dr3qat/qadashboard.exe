"""
Bordero Page - Page Object para tela de Borderô.
"""
import time
from datetime import datetime
from pages.base_page import BasePage
from config import logger, LogStyle, SimbolosASCII, log_acao, log_tecnico
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BorderoPage(BasePage):
    """Page Object para funcionalidade de Borderô."""

    # ========== LOCATORS ==========
    TXT_BORDERO = "Borderô"
    TIL_DATA_INICIAL = "textInputLayout4"
    BTN_GERAR_BORDERO = "bt_gerar_bordero"

    # Locators para validação de dados
    TXT_FUNDO_CAIXA_LABEL = "Fundo de Caixa"
    TXT_TOTAL_LIQUIDO_LABEL = "Total Líquido Faturado"
    TXT_TOTAL_PRESTACOES_LABEL = "Total de prestações"
    TXT_QTD_PRESTACOES_LABEL = "Quantidade de prestações"
    TXT_TOTAL_APORTE_LABEL = "Total Aporte"
    TXT_TOTAL_REMESSAS_LABEL = "Total Remessas"
    TXT_TOTAL_PAGAMENTOS_LABEL = "Total Pagamentos"
    TXT_DINHEIRO_INFORMADO = "textView275"
    TXT_DINHEIRO_REALIZADO = "textView278"
    TXT_DIFERENCA_CAIXA = "textView279"
    TXT_TOTAL_SESSAO_CAIXA = "txtCaixaRealizado"
    TXT_TOTAL_REALIZADO_GERAL = "txtCaixaTotalRealizado"

    # ========== ACOES ==========

    def navegar_ate_bordero(self):
        """Navega até a tela de Borderô."""
        log_acao(f"{SimbolosASCII.SCROLL} Navegando até Borderô")
        self.ver_e_clicar_texto(self.TXT_BORDERO)
        logger.info("   [✅] Tela de Borderô acessada")

    def inserir_data_inicial(self, data: str = None):
        """
        Insere data inicial no campo. Se não informada, usa data atual.

        Args:
            data: Data no formato DD/MM/YYYY. Se None, usa data atual.
        """
        if data is None:
            data = datetime.now().strftime('%d/%m/%Y')

        log_acao(f"{SimbolosASCII.DIGITAR} Inserindo data inicial: {data}")
        logger.info(f"   Data selecionada: {data}")

        # Clica no campo para dar foco
        logger.info(f"   Clicando no campo de data (ID: {self.TIL_DATA_INICIAL})")
        self.clicar_por_id(self.TIL_DATA_INICIAL)

        # Monta XPath para EditText dentro do layout
        xpath_campo_data = f"//*[@resource-id='{self.app_package}:id/{self.TIL_DATA_INICIAL}']//android.widget.EditText"

        # Digita a data
        logger.info(f"   Digitando data: {data}")
        self.digitar_por_xpath(xpath_campo_data, data)
        logger.info(f"   [✅] Data {data} inserida com sucesso")

    def gerar_bordero(self):
        """Clica no botão para gerar o borderô."""
        log_acao(f"{SimbolosASCII.CLICK} Gerando borderô")
        # Garante que o teclado esteja fechado antes de clicar no botão
        # (emuladores/flavor playstore mantém o teclado aberto após digitar a data)
        self.fechar_teclado()
        logger.info(f"   Clicando no botão 'Gerar Borderô' (ID: {self.BTN_GERAR_BORDERO})")
        self.clicar_por_id(self.BTN_GERAR_BORDERO)
        logger.info("   Aguardando carregamento dos dados do borderô...")
        time.sleep(2)  # Aguarda carregamento dos dados
        logger.info("   [✅] Borderô sendo processado")

    def ler_campo_bordero(self, nome_campo: str, identificador: str, eh_id: bool = False) -> str:
        """
        Lê o valor de um campo do borderô.

        Args:
            nome_campo: Nome amigável do campo para log
            identificador: ID do elemento ou texto do label
            eh_id: True se identificador for ID, False se for texto do label

        Returns:
            Valor do campo ou "sem dados" se não encontrado/vazio
        """
        try:
            if eh_id:
                locator = (AppiumBy.ID, f"{self.app_package}:id/{identificador}")
            else:
                # XPath para pegar o valor ao lado do label
                locator = (AppiumBy.XPATH,
                          f"//*[@text='{identificador}']/following-sibling::android.widget.TextView")

            elemento = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(locator)
            )
            texto_extraido = elemento.text

            if not texto_extraido or texto_extraido.strip() == "":
                logger.warning(f"   [⚠️] {nome_campo}: sem dados")
                return "sem dados"

            logger.info(f"   [✅] {nome_campo}: {texto_extraido}")
            return texto_extraido

        except Exception:
            logger.warning(f"   [⚠️] {nome_campo}: sem dados")
            return "sem dados"

    # ========== VALIDACOES ==========

    def validar_dados_bordero(self) -> dict:
        """
        Valida e coleta todos os dados do borderô.

        Returns:
            Dicionário com todos os dados coletados do borderô
        """
        log_acao(f"{SimbolosASCII.VALIDAR} Validando dados do borderô")
        logger.info("")
        logger.info("=" * 70)
        logger.info("LENDO TODOS OS DADOS DA TELA DE BORDERÔ")
        logger.info("=" * 70)

        dados = {}

        # Bloco 1: Faturamento e Prestações (topo)
        logger.info("")
        logger.info("--- BLOCO TOPO (Faturamento e Prestações) ---")
        dados['fundo_caixa'] = self.ler_campo_bordero("Fundo de Caixa", self.TXT_FUNDO_CAIXA_LABEL)
        dados['total_liquido'] = self.ler_campo_bordero("Total Líquido Faturado", self.TXT_TOTAL_LIQUIDO_LABEL)
        dados['total_prestacoes'] = self.ler_campo_bordero("Total de Prestações", self.TXT_TOTAL_PRESTACOES_LABEL)
        dados['qtd_prestacoes'] = self.ler_campo_bordero("Quantidade de Prestações", self.TXT_QTD_PRESTACOES_LABEL)

        # Bloco 2: Aportes e Remessas (meio)
        logger.info("")
        logger.info("   [ℹ️] Rolando a tela para a seção de Aportes...")
        self.realizar_scroll_para_baixo()
        time.sleep(1)

        logger.info("")
        logger.info("--- BLOCO MEIO (Aportes e Remessas) ---")
        dados['total_aporte'] = self.ler_campo_bordero("Total Aporte", self.TXT_TOTAL_APORTE_LABEL)
        dados['total_remessas'] = self.ler_campo_bordero("Total Remessas", self.TXT_TOTAL_REMESSAS_LABEL)

        # Bloco 3: Resumo Geral do Caixa (final)
        logger.info("")
        logger.info("   [ℹ️] Rolando para o final do Borderô...")
        self.realizar_scroll_para_baixo()
        time.sleep(1)
        self.realizar_scroll_para_baixo()  # Segundo scroll para garantir
        time.sleep(1)

        logger.info("")
        logger.info("--- BLOCO FINAL (Resumo Geral do Caixa) ---")
        dados['total_pagamentos'] = self.ler_campo_bordero("Total Pagamentos", self.TXT_TOTAL_PAGAMENTOS_LABEL)
        dados['dinheiro_informado'] = self.ler_campo_bordero("Dinheiro Informado", self.TXT_DINHEIRO_INFORMADO, eh_id=True)
        dados['dinheiro_realizado'] = self.ler_campo_bordero("Dinheiro Realizado", self.TXT_DINHEIRO_REALIZADO, eh_id=True)
        dados['diferenca_caixa'] = self.ler_campo_bordero("Diferença de Caixa", self.TXT_DIFERENCA_CAIXA, eh_id=True)
        dados['total_sessao'] = self.ler_campo_bordero("Total da Sessão (Caixa)", self.TXT_TOTAL_SESSAO_CAIXA, eh_id=True)
        dados['total_realizado_geral'] = self.ler_campo_bordero("Total Realizado Geral", self.TXT_TOTAL_REALIZADO_GERAL, eh_id=True)

        # Resumo final
        logger.info("")
        logger.info("=" * 70)
        logger.info("RESUMO DOS DADOS COLETADOS DO BORDERÔ")
        logger.info("=" * 70)
        logger.info(f"   Fundo de Caixa: {dados.get('fundo_caixa', 'sem dados')}")
        logger.info(f"   Total Líquido Faturado: {dados.get('total_liquido', 'sem dados')}")
        logger.info(f"   Total de Prestações: {dados.get('total_prestacoes', 'sem dados')}")
        logger.info(f"   Quantidade de Prestações: {dados.get('qtd_prestacoes', 'sem dados')}")
        logger.info(f"   Total Aporte: {dados.get('total_aporte', 'sem dados')}")
        logger.info(f"   Total Remessas: {dados.get('total_remessas', 'sem dados')}")
        logger.info(f"   Total Pagamentos: {dados.get('total_pagamentos', 'sem dados')}")
        logger.info(f"   Dinheiro Informado: {dados.get('dinheiro_informado', 'sem dados')}")
        logger.info(f"   Dinheiro Realizado: {dados.get('dinheiro_realizado', 'sem dados')}")
        logger.info(f"   Diferença de Caixa: {dados.get('diferenca_caixa', 'sem dados')}")
        logger.info(f"   Total da Sessão: {dados.get('total_sessao', 'sem dados')}")
        logger.info(f"   Total Realizado Geral: {dados.get('total_realizado_geral', 'sem dados')}")
        logger.info("=" * 70)
        logger.info("")

        log_acao(f"{SimbolosASCII.OK} Validação do borderô concluída")
        return dados

    def bordero_gerado_com_sucesso(self, dados_bordero: dict = None) -> bool:
        """
        Verifica se o borderô foi gerado com sucesso.
        Considera sucesso se pelo menos um campo obrigatório estiver preenchido.

        Args:
            dados_bordero: Dicionário com dados já coletados (opcional)

        Returns:
            True se borderô foi gerado, False caso contrário
        """
        # Se já temos os dados coletados, usa eles
        if dados_bordero:
            total_liquido = dados_bordero.get('total_liquido', 'sem dados')
            if total_liquido != "sem dados":
                logger.info("   [✅] Borderô gerado com sucesso - Total Líquido Faturado encontrado")
                return True
            else:
                logger.warning("   [⚠️] Borderô sem dados - Total Líquido Faturado vazio")
                return False

        # Se não tem dados, busca na tela (fallback)
        try:
            # Verifica se campo obrigatório está presente (Total Líquido Faturado)
            total_liquido = self.ler_campo_bordero("Total Líquido Faturado",
                                                    self.TXT_TOTAL_LIQUIDO_LABEL)
            if total_liquido != "sem dados":
                logger.info("   [✅] Borderô gerado com sucesso")
                return True
            else:
                logger.warning("   [⚠️] Borderô sem dados")
                return False
        except Exception as e:
            logger.error(f"   [❌] Erro ao verificar borderô: {e}")
            return False
