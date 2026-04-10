"""
Historico Cliente Page - Page Object para tela de Histórico do Cliente.
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle, SimbolosASCII, log_acao, log_tecnico
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HistoricoClientePage(BasePage):
    """Page Object para funcionalidade de Histórico do Cliente."""

    # ========== LOCATORS ==========
    TXT_HISTORICO_CLIENTE = "Histórico Cliente"

    # Campo de busca
    SEARCH_SRC_TEXT = "search_src_text"
    BTN_CONFIRMAR_SELECAO = "button3"

    # Locators da aba Resumo/Tendências
    TXT_VALOR_TOTAL_COMPRAS = "Valor Total de Compras"
    TXT_TOTAL_COMPRAS_ID = "textView206"

    # Top 5 Produtos
    TXT_NOME_PRODUTO = "textView4"
    TXT_VALOR_PRODUTO = "textView236"

    # Tendências por Nível
    TXT_POR_NIVEL = "Por nível"
    TXT_CATEGORIA_TENDENCIA = "textView209"
    TXT_QTD_CATEGORIA = "textView207"

    # ========== ACOES ==========

    def navegar_ate_historico_cliente(self):
        """Navega até a tela de Histórico do Cliente."""
        log_acao(f"{SimbolosASCII.SCROLL} Navegando até Histórico Cliente")
        self.ver_e_clicar_texto(self.TXT_HISTORICO_CLIENTE)
        logger.info("   [OK] Tela de Histórico Cliente acessada")

    def selecionar_cliente(self, identificador: str):
        """
        Seleciona um cliente através da busca.

        Args:
            identificador: CPF, CNPJ, código ou nome do cliente
        """
        log_acao(f"{SimbolosASCII.BUSCA} Selecionando cliente: {identificador}")
        logger.info(f"   Cliente ID: {identificador}")

        # Digita o identificador no campo de busca
        logger.info(f"   Digitando '{identificador}' no campo de busca")
        self.digitar_por_id(self.SEARCH_SRC_TEXT, identificador)

        # Aciona pesquisa pelo teclado
        logger.info("   Acionando pesquisa pelo teclado")
        self.pressionar_pesquisar()

        # Confirma seleção
        logger.info("   Confirmando seleção do cliente")
        self.clicar_por_id(self.BTN_CONFIRMAR_SELECAO)

        time.sleep(1)  # Aguarda carregamento dos dados
        logger.info("   [OK] Cliente selecionado com sucesso")

    def _elemento_visivel_silencioso(self, element_id: str) -> bool:
        """
        Verifica silenciosamente se elemento está visível (sem logs de erro).

        Args:
            element_id: ID do elemento

        Returns:
            True se elemento está visível, False caso contrário
        """
        try:
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((AppiumBy.ID, f"{self.app_package}:id/{element_id}"))
            )
            return True
        except:
            return False

    def _ler_campo_historico(self, nome_campo: str, element_id: str) -> str:
        """
        Lê o valor de um campo do histórico.

        Args:
            nome_campo: Nome amigável do campo para log
            element_id: ID do elemento

        Returns:
            Valor do campo ou "sem dados" se vazio/não encontrado
        """
        try:
            elemento = self.encontrar_clicavel_por_id(element_id, tempo_espera=3)
            texto_extraido = elemento.text

            if not texto_extraido or texto_extraido.strip() == "":
                logger.warning(f"   [AVISO] {nome_campo}: sem dados")
                return "sem dados"

            logger.info(f"   [OK] {nome_campo}: {texto_extraido}")
            return texto_extraido
        except:
            logger.warning(f"   [AVISO] {nome_campo}: sem dados")
            return "sem dados"

    # ========== VALIDACOES ==========

    def validar_resumo_historico(self) -> dict:
        """
        Valida e coleta dados da aba Resumo/Tendências de Compra.

        Returns:
            Dicionário com todos os dados coletados do histórico
        """
        log_acao(f"{SimbolosASCII.VALIDAR} Validando dados do histórico do cliente")
        logger.info("")
        logger.info("=" * 60)
        logger.info("DADOS DO HISTÓRICO DO CLIENTE")
        logger.info("=" * 60)

        dados = {}

        # Rola até a seção de Valor Total de Compras
        logger.info("   Rolando até 'Valor Total de Compras'...")
        self.rolar_ate_texto(self.TXT_VALOR_TOTAL_COMPRAS)

        # Valida Valor Total de Compras
        logger.info("")
        logger.info("--- VALOR TOTAL DE COMPRAS ---")
        dados['valor_total'] = self._ler_campo_historico("Valor Total de Compras",
                                                          self.TXT_TOTAL_COMPRAS_ID)

        # Valida seção Top 5 Produtos (se disponível)
        logger.info("")
        logger.info("--- TOP 5 PRODUTOS ---")
        if not self._elemento_visivel_silencioso(self.TXT_NOME_PRODUTO):
            logger.info("   Produtos escondidos. Fazendo scroll...")
            self.realizar_scroll_para_baixo()
            time.sleep(1)

        try:
            dados['top_produto_nome'] = self._ler_campo_historico("Nome do Produto Mais Comprado",
                                                                   self.TXT_NOME_PRODUTO)
            dados['top_produto_valor'] = self._ler_campo_historico("Valor do Produto Mais Comprado",
                                                                    self.TXT_VALOR_PRODUTO)
        except Exception:
            logger.warning("   [AVISO] Lista de Top 5 Produtos vazia para este cliente")
            dados['top_produto_nome'] = "sem dados"
            dados['top_produto_valor'] = "sem dados"

        # Valida seção Por Nível (Tendências)
        logger.info("")
        logger.info("--- TENDÊNCIAS DE COMPRA POR NÍVEL ---")
        if not self._elemento_visivel_silencioso(self.TXT_CATEGORIA_TENDENCIA):
            logger.info("   Tendências escondidas. Fazendo scroll...")
            self.realizar_scroll_para_baixo()
            time.sleep(1)

        try:
            self.rolar_ate_texto(self.TXT_POR_NIVEL)
            dados['categoria_tendencia'] = self._ler_campo_historico("Categoria (ex: CALÇADOS)",
                                                                      self.TXT_CATEGORIA_TENDENCIA)
            dados['qtd_categoria'] = self._ler_campo_historico("Quantidade da Categoria",
                                                                self.TXT_QTD_CATEGORIA)
        except Exception:
            logger.warning("   [AVISO] Lista de Tendências vazia para este cliente")
            dados['categoria_tendencia'] = "sem dados"
            dados['qtd_categoria'] = "sem dados"

        # Resumo final
        logger.info("")
        logger.info("=" * 60)
        logger.info("RESUMO DOS DADOS COLETADOS")
        logger.info("=" * 60)
        logger.info(f"   Valor Total de Compras: {dados.get('valor_total', 'sem dados')}")
        logger.info(f"   Top Produto (Nome): {dados.get('top_produto_nome', 'sem dados')}")
        logger.info(f"   Top Produto (Valor): {dados.get('top_produto_valor', 'sem dados')}")
        logger.info(f"   Categoria Tendência: {dados.get('categoria_tendencia', 'sem dados')}")
        logger.info(f"   Qtd da Categoria: {dados.get('qtd_categoria', 'sem dados')}")
        logger.info("=" * 60)
        logger.info("")

        log_acao(f"{SimbolosASCII.OK} Validação do histórico concluída")
        return dados

    def historico_carregado_com_sucesso(self) -> bool:
        """
        Verifica se o histórico foi carregado com sucesso.
        Considera sucesso se pelo menos o valor total estiver preenchido.

        Returns:
            True se histórico foi carregado, False caso contrário
        """
        try:
            # Rola até valor total
            self.rolar_ate_texto(self.TXT_VALOR_TOTAL_COMPRAS)

            # Verifica se campo obrigatório está presente
            valor_total = self._ler_campo_historico("Valor Total de Compras",
                                                     self.TXT_TOTAL_COMPRAS_ID)

            if valor_total != "sem dados":
                logger.info("   [OK] Histórico carregado com sucesso - Valor Total encontrado")
                return True
            else:
                logger.warning("   [AVISO] Histórico sem dados - Valor Total vazio")
                return False
        except Exception as e:
            logger.error(f"   [ERRO] Falha ao verificar histórico: {e}")
            return False

    def voltar_tela_anterior(self):
        """Volta para a tela anterior."""
        log_acao("Voltando para tela anterior")
        logger.info("   Pressionando botão voltar")
        self.voltar_tela()
        time.sleep(0.5)
        logger.info("   [OK] Voltou para tela anterior")
