"""
Estoque Page - Page Object para tela de consulta de estoque.
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle

class EstoquePage(BasePage):
    """Page Object para tela de consulta de estoque."""

    # --- Locators ---
    # Menu/Navegacao
    TXT_CONSULTAR_ESTOQUE = "Consultar Estoque"
    TXT_ESTOQUE = "Estoque"

    # Busca
    EDT_BUSCA_PRODUTO = "search_src_text"
    EDT_CODIGO_PRODUTO = "search_src_text"
    BTN_PESQUISAR = "action_searchable_activity_pdv"

    # Filtro
    BTN_FILTRO = "action_filtro_produto_pdv"
    TXT_FILTRO_SELECIONADO = "android:id/text1"
    OPCAO_CODIGO = "Código"
    OPCAO_DESCRICAO = "Descrição"

    # Resultados (Locators)
    # Correção baseada no seu feedback:
    TXT_NOME_PRODUTO = "textView43" # Nome do produto
    TXT_MARCA_PRODUTO = "textView46" # Você confirmou que este ID traz a Marca (ex: USAFLEX)

    # XPaths para Labels (Baseado na imagem da tela de detalhes)
    XPATH_LABEL_COR = "//android.widget.TextView[contains(@text, 'Cor')]/following-sibling::android.widget.TextView"
    XPATH_LABEL_MATERIAL = "//android.widget.TextView[contains(@text, 'Material')]/following-sibling::android.widget.TextView"
    XPATH_LABEL_OBS = "//android.widget.TextView[contains(@text, 'Observações')]/following-sibling::android.widget.TextView"

    # Tabela Inferior (Preço Real)
    # Busca texto que contem 'R$' e tem tamanho maior que 3 (evita pegar só o cabeçalho 'R$')
    XPATH_PRECO_VALOR = "//android.widget.TextView[contains(@text, 'R$') and string-length(@text) > 3]"

    # Lista (Cores)
    LISTA_PRODUTOS = "rcv_products_stock"
    ITEM_PRODUTO = "txt_color_stock"

    # Erros
    TXT_PRODUTO_NAO_ENCONTRADO = "md_content"
    TXT_NENHUM_RESULTADO = "md_content"
    TXT_SEM_ESTOQUE = "Sem estoque"
    BTN_OK_ERRO = "md_buttonDefaultPositive"

    # --- Navegacao (REVERTIDO PARA VERSÃO ORIGINAL) ---
    def _fechar_popup_voce_sabia(self):
        """Fecha popup 'Você sabia?' se aparecer na tela de estoque."""
        if not self.texto_exibido("Você sabia?", tempo_espera=2):
            return
        logger.info(f"{LogStyle.ACAO} Fechando popup 'Voce sabia?'...")
        fechou = False
        for locator in ("×", "✕", "X"):
            try:
                el = self.driver.find_element("xpath", f"//*[@text='{locator}']")
                el.click()
                fechou = True
                break
            except Exception:
                pass
        if not fechou:
            # Fallback: tenta clicar fora do popup (NUNCA pressionar BACK — dispara "Sair do Estoque")
            self.clicar_texto_se_existir("FECHAR", tempo_espera=1)
        time.sleep(0.5)

    def _fechar_popup_sair_estoque(self):
        """Dispensa dialog 'Sair do Estoque' clicando CANCELAR (mantém na tela)."""
        if self.texto_exibido("Sair do Estoque", tempo_espera=2):
            logger.info(f"{LogStyle.FALLBACK} Dialog 'Sair do Estoque' detectado — clicando CANCELAR")
            self.clicar_texto_se_existir("CANCELAR", tempo_espera=3)
            time.sleep(0.5)

    def acessar_estoque(self):
        """Navega ate a tela de consulta de estoque."""
        logger.info(f"{LogStyle.ACAO} Acessando consulta de estoque...")
        self.ver_e_clicar_texto(self.TXT_ESTOQUE)
        self._fechar_popup_voce_sabia()
        self._fechar_popup_sair_estoque()

    # --- Filtro ---
    def garantir_filtro(self, opcao_desejada: str):
        try:
            el = self.encontrar_por_id(self.TXT_FILTRO_SELECIONADO, tempo_espera=3)
            if el:
                if el.text == opcao_desejada:
                    # logger.info(f"   [FILTRO] Já está em: {opcao_desejada}")
                    return

                logger.info(f"   {LogStyle.ACAO} Mudando filtro para: {opcao_desejada}")
                self.clicar_por_id(self.BTN_FILTRO)
                self.clicar_por_texto(opcao_desejada)  # clicar_por_texto aguarda elemento aparecer
            else:
                # Fallback cego se não conseguir ler o texto
                self.clicar_por_id(self.BTN_FILTRO)
                self.clicar_por_texto(opcao_desejada)
        except:
            pass

    # --- Busca ---
    def buscar_produto_por_codigo(self, codigo: str):
        logger.info(f"{LogStyle.ACAO} Buscando CODIGO: {codigo}")

        # 1. Clica lupa
        self.clicar_pesquisar()

        # 2. Garante filtro
        self.garantir_filtro(self.OPCAO_CODIGO)

        # 3. Digita
        try: self.digitar_por_id(self.EDT_BUSCA_PRODUTO, codigo)
        except: self.digitar_por_id(self.EDT_CODIGO_PRODUTO, codigo)

        # 4. Pesquisa — resultado aguardado por obter_detalhes_completos/produto_encontrado
        self.pressionar_pesquisar()

    def buscar_produto_por_nome(self, nome: str):
        logger.info(f"{LogStyle.ACAO} Buscando NOME: {nome}")

        self.clicar_pesquisar()

        self.garantir_filtro(self.OPCAO_DESCRICAO)

        try: self.digitar_por_id(self.EDT_BUSCA_PRODUTO, nome)
        except: self.digitar_por_id(self.EDT_CODIGO_PRODUTO, nome)

        self.pressionar_pesquisar()

    def clicar_pesquisar(self):
        try: self.clicar_por_id(self.BTN_PESQUISAR)
        except: self.pressionar_pesquisar()

    # --- Extração de Detalhes (Corrigido Preço/Marca) ---
    def obter_detalhes_completos(self) -> dict:
        """Extrai e LOGA todas as informações da tela."""
        logger.info(f"{LogStyle.secao('EXTRAINDO DETALHES DO PRODUTO')}")

        dados = {
            "nome": "N/A", "marca": "N/A", "cor": "N/A",
            "material": "N/A", "obs": "N/A", "preco": "N/A"
        }

        # 1. Dados via ID
        try: dados["nome"] = self.encontrar_por_id(self.TXT_NOME_PRODUTO).text
        except: pass

        try: dados["marca"] = self.encontrar_por_id(self.TXT_MARCA_PRODUTO).text
        except: pass

        # 2. Dados via XPath (Labels)
        dados["cor"] = self._get_text(self.XPATH_LABEL_COR)
        dados["material"] = self._get_text(self.XPATH_LABEL_MATERIAL)
        dados["obs"] = self._get_text(self.XPATH_LABEL_OBS)

        # 3. Preço Real (Busca por R$ na parte inferior)
        try:
            el_preco = self.driver.find_element("xpath", self.XPATH_PRECO_VALOR)
            dados["preco"] = el_preco.text
        except:
            pass

        # LOGAR TUDO NO CONSOLE
        logger.info(f"   🔹 NOME:      {dados['nome']}")
        logger.info(f"   🔹 MARCA:     {dados['marca']}")
        logger.info(f"   🔹 COR:       {dados['cor']}")
        logger.info(f"   🔹 MATERIAL:  {dados['material']}")
        logger.info(f"   🔹 OBS:       {dados['obs']}")
        logger.info(f"   🔹 PREÇO:     {dados['preco']}")

        return dados

    def _get_text(self, xpath):
        try: return self.driver.find_element("xpath", xpath).text
        except: return "N/A"

    # --- Compatibilidade com Testes Antigos ---
    def obter_quantidade_estoque(self) -> str:
        # Produto na tela = detalhes exibidos = tabela presente
        try:
            if self.elemento_existe(self.TXT_NOME_PRODUTO, 5):
                return "Disponível"
        except: pass
        return ""

    def obter_nome_produto(self) -> str:
        return self._get_text(f"//*[@resource-id='{self.TXT_NOME_PRODUTO}']")

    def obter_preco_produto(self) -> str:
        return self._get_text(self.XPATH_PRECO_VALOR)

    def obter_lista_produtos(self) -> list:
        try: return self.encontrar_todos_por_id(self.ITEM_PRODUTO, tempo_espera=5)
        except: return []

    def produto_encontrado(self, timeout: int = 5) -> bool:
        if self.elemento_existe(self.TXT_PRODUTO_NAO_ENCONTRADO, 2):
            try: self.clicar_por_id(self.BTN_OK_ERRO)
            except: pass
            return False
        return self.elemento_existe(self.TXT_NOME_PRODUTO, timeout) or self.elemento_existe(self.LISTA_PRODUTOS, timeout)

    def mensagem_nao_encontrado_exibida(self, timeout: int = 5) -> bool:
        return self.elemento_existe(self.TXT_PRODUTO_NAO_ENCONTRADO, timeout)

    def executar_consulta_estoque(self, codigo: str) -> dict:
        self.buscar_produto_por_codigo(codigo)
        dados = self.obter_detalhes_completos()

        return {
            'encontrado': self.produto_encontrado(),
            'nome': dados['nome'],
            'quantidade': "Sim" if dados['preco'] != "N/A" else "Não",
            'preco': dados['preco'],
            'marca': dados['marca'],
            'cor': dados['cor'],
            'material': dados['material'],
            'obs': dados['obs']
        }
