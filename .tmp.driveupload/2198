"""
Opcoes Item Page - Page Object para menu de ações do item no carrinho.
"""
import time
from pages.base_page import BasePage
from config import logger, LogStyle


class OpcoesItemPage(BasePage):
    """Page Object para menu de ações do item produto."""

    # --- Locators ---
    BTN_ACOES_ITEM = "acoes_item"
    TXT_REMOVER_ITEM = "Remover item"
    TXT_ALTERAR_QUANTIDADE = "Alterar quantidade"
    TXT_ALTERAR_PRECO = "Alterar preço"
    TXT_ALTERAR_TAMANHO = "Alterar tamanho"
    TXT_ALTERAR_VENDEDOR = "Alterar vendedor"
    TXT_VER_ESTOQUE = "Ver estoque"

    # Elementos do item no carrinho
    TXT_QUANTITY = "txt_quantity"
    TXT_PRICE_VALUE = "txt_price_value"
    TXT_SIZE_VALUE = "txt_size_value"
    TXT_VENDEDOR_ITEM = "txt_vendedor_item"

    # Diálogos
    MD_CONTENT = "md_content"
    MD_BTN_POSITIVE = "md_buttonDefaultPositive"
    EDT_XPATH = "//android.widget.EditText"
    TXT_CONFIRMAR = "CONFIRMAR"

    # Lista de seleção (tamanho, vendedor)
    LISTA_OPCAO = "android:id/text1"
    LISTA_VENDEDOR = "txt_dialog_seller_name"

    # Tela de estoque
    TXT_CONS_ESTOQUE = "Cons. Estoque"
    TXT_NOME_PRODUTO_ESTOQUE = "textView43"
    TXT_MARCA_PRODUTO_ESTOQUE = "textView46"

    # --- Ações do Menu ---
    def abrir_menu_acoes(self):
        """Abre o menu de ações do item."""
        logger.info(f"{LogStyle.ACAO} Abrindo menu de ações do item...")
        self.clicar_por_id(self.BTN_ACOES_ITEM)
        time.sleep(1)

    def remover_item(self):
        """Remove item do carrinho."""
        logger.info(f"{LogStyle.ACAO} Removendo item do carrinho...")

        self.abrir_menu_acoes()
        self.clicar_por_texto(self.TXT_REMOVER_ITEM)
        time.sleep(1)

        # Valida mensagem de confirmação
        logger.info(f"{LogStyle.VALIDAR} Validando mensagem de confirmação...")
        elemento = self.encontrar_por_id(self.MD_CONTENT, tempo_espera=5)
        if "Remover item do carrinho?" not in elemento.text:
            raise AssertionError(f"Mensagem esperada não encontrada. Texto: {elemento.text}")

        # Confirma exclusão
        logger.info(f"{LogStyle.CLICK} Confirmando exclusão...")
        self.clicar_por_id(self.MD_BTN_POSITIVE)
        time.sleep(2)
        logger.info(f"{LogStyle.OK} Item removido com sucesso!")

    def alterar_quantidade(self, nova_quantidade: str) -> str:
        """
        Altera quantidade do item.

        Args:
            nova_quantidade: Nova quantidade (string)

        Returns:
            str: Quantidade atualizada lida da tela
        """
        logger.info(f"{LogStyle.ACAO} Alterando quantidade para: {LogStyle.valor(nova_quantidade)}")

        self.abrir_menu_acoes()
        self.clicar_por_texto(self.TXT_ALTERAR_QUANTIDADE)
        time.sleep(1)

        # Digita nova quantidade
        self.digitar_por_xpath(self.EDT_XPATH, nova_quantidade)
        self.clicar_por_texto(self.TXT_CONFIRMAR)
        time.sleep(1.5)

        # Valida alteração
        quantidade_atualizada = self.encontrar_por_id(self.TXT_QUANTITY, tempo_espera=5).text
        if quantidade_atualizada != nova_quantidade:
            raise AssertionError(f"Quantidade esperada '{nova_quantidade}', mas encontrou '{quantidade_atualizada}'")

        logger.info(f"{LogStyle.OK} Quantidade alterada para: {LogStyle.valor(quantidade_atualizada)}")
        return quantidade_atualizada

    def obter_preco_atual(self) -> str:
        """Obtém preço atual do item."""
        preco = self.encontrar_por_id(self.TXT_PRICE_VALUE, tempo_espera=3).text
        logger.info(f"{LogStyle.INFO} Preço atual: {LogStyle.valor(preco)}")
        return preco

    def alterar_preco(self, novo_preco: str) -> str:
        """
        Altera preço do item.

        Args:
            novo_preco: Novo preço (string, ex: "15000")

        Returns:
            str: Preço atualizado lido da tela
        """
        preco_antigo = self.obter_preco_atual()
        logger.info(f"{LogStyle.ACAO} Alterando preço de {LogStyle.valor(preco_antigo)} para {LogStyle.valor(novo_preco)}")

        self.abrir_menu_acoes()
        self.clicar_por_texto(self.TXT_ALTERAR_PRECO)
        time.sleep(1)

        # Digita novo preço
        self.digitar_por_xpath(self.EDT_XPATH, novo_preco)
        self.clicar_por_texto(self.TXT_CONFIRMAR)
        time.sleep(1.5)

        # Valida alteração
        preco_novo = self.encontrar_por_id(self.TXT_PRICE_VALUE, tempo_espera=5).text
        if preco_novo == preco_antigo:
            raise AssertionError(f"Preço não foi alterado! Continua: {preco_antigo}")

        logger.info(f"{LogStyle.OK} Preço alterado de {LogStyle.valor(preco_antigo)} para {LogStyle.valor(preco_novo)}")
        return preco_novo

    def obter_tamanho_atual(self) -> str:
        """Obtém tamanho atual do item."""
        try:
            tamanho = self.encontrar_por_id(self.TXT_SIZE_VALUE, tempo_espera=3).text
            logger.info(f"{LogStyle.INFO} Tamanho atual: {LogStyle.valor(tamanho)}")
            return tamanho
        except:
            logger.warning(f"{LogStyle.AVISO} Tamanho não disponível")
            return "Desconhecido"

    def alterar_tamanho(self) -> tuple[str, str]:
        """
        Altera tamanho do item para uma opção diferente.

        Returns:
            tuple: (tamanho_antigo, tamanho_novo)
        """
        tamanho_antigo = self.obter_tamanho_atual()
        logger.info(f"{LogStyle.ACAO} Alterando tamanho de: {LogStyle.valor(tamanho_antigo)}")

        self.abrir_menu_acoes()
        self.clicar_por_texto(self.TXT_ALTERAR_TAMANHO)
        time.sleep(1)

        # Seleciona tamanho diferente
        opcoes = self.encontrar_todos_por_id(self.LISTA_OPCAO, tempo_espera=5)
        tamanho_escolhido = None

        for opcao in opcoes:
            texto_opcao = opcao.text
            if texto_opcao != tamanho_antigo and texto_opcao.strip() != "":
                opcao.click()
                tamanho_escolhido = texto_opcao
                break

        if not tamanho_escolhido:
            raise Exception("Não havia outras opções de tamanho disponíveis")

        time.sleep(1.5)

        # Valida alteração
        tamanho_novo = self.encontrar_por_id(self.TXT_SIZE_VALUE, tempo_espera=5).text
        if tamanho_novo != tamanho_escolhido:
            raise AssertionError(f"Esperava tamanho '{tamanho_escolhido}', mas encontrou '{tamanho_novo}'")

        logger.info(f"{LogStyle.OK} Tamanho alterado de {LogStyle.valor(tamanho_antigo)} para {LogStyle.valor(tamanho_novo)}")
        return tamanho_antigo, tamanho_novo

    def obter_vendedor_atual(self) -> str:
        """Obtém vendedor atual do item."""
        try:
            vendedor = self.encontrar_por_id(self.TXT_VENDEDOR_ITEM, tempo_espera=3).text
            logger.info(f"{LogStyle.INFO} Vendedor atual: {LogStyle.valor(vendedor)}")
            return vendedor
        except:
            logger.warning(f"{LogStyle.AVISO} Vendedor não disponível")
            return "Desconhecido"

    def alterar_vendedor(self) -> tuple[str, str]:
        """
        Altera vendedor do item para uma opção diferente.

        Returns:
            tuple: (vendedor_antigo, vendedor_novo)
        """
        vendedor_antigo = self.obter_vendedor_atual()
        logger.info(f"{LogStyle.ACAO} Alterando vendedor de: {LogStyle.valor(vendedor_antigo)}")

        self.abrir_menu_acoes()
        self.clicar_por_texto(self.TXT_ALTERAR_VENDEDOR)
        time.sleep(1)

        # Seleciona vendedor diferente
        opcoes = self.encontrar_todos_por_id(self.LISTA_VENDEDOR, tempo_espera=5)
        vendedor_escolhido = None

        for opcao in opcoes:
            texto_opcao = opcao.text
            if texto_opcao != vendedor_antigo and texto_opcao.strip() != "":
                opcao.click()
                vendedor_escolhido = texto_opcao
                break

        if not vendedor_escolhido:
            raise Exception("Não havia outros vendedores disponíveis")

        time.sleep(1.5)

        # Valida alteração
        vendedor_novo = self.encontrar_por_id(self.TXT_VENDEDOR_ITEM, tempo_espera=5).text
        if vendedor_novo != vendedor_escolhido:
            raise AssertionError(f"Esperava vendedor '{vendedor_escolhido}', mas encontrou '{vendedor_novo}'")

        logger.info(f"{LogStyle.OK} Vendedor alterado de {LogStyle.valor(vendedor_antigo)} para {LogStyle.valor(vendedor_novo)}")
        return vendedor_antigo, vendedor_novo

    def consultar_estoque(self) -> dict:
        """
        Consulta estoque do item.

        Returns:
            dict: Informações do produto (nome, marca)
        """
        logger.info(f"{LogStyle.ACAO} Consultando estoque do item...")

        self.abrir_menu_acoes()
        self.clicar_por_texto(self.TXT_VER_ESTOQUE)

        # Valida que tela de estoque carregou
        logger.info(f"{LogStyle.VALIDAR} Validando tela de estoque...")
        if not self.texto_exibido(self.TXT_CONS_ESTOQUE, tempo_espera=5):
            raise AssertionError("Tela 'Cons. Estoque' não foi exibida")

        # Lê dados do produto
        nome_produto = self.encontrar_por_id(self.TXT_NOME_PRODUTO_ESTOQUE, tempo_espera=3).text
        marca_produto = self.encontrar_por_id(self.TXT_MARCA_PRODUTO_ESTOQUE, tempo_espera=3).text

        if not nome_produto or not marca_produto:
            raise AssertionError("Detalhes do produto no estoque estão vazios!")

        logger.info(f"{LogStyle.OK} Produto: {LogStyle.valor(nome_produto)}")
        logger.info(f"{LogStyle.OK} Marca: {LogStyle.valor(marca_produto)}")

        # Volta para carrinho
        logger.info(f"{LogStyle.ACAO} Voltando para o carrinho...")
        self.voltar_tela()
        time.sleep(1)

        return {
            "nome": nome_produto,
            "marca": marca_produto
        }

    # --- Validações ---
    def item_existe_no_carrinho(self) -> bool:
        """Verifica se existe item no carrinho."""
        return self.elemento_existe(self.BTN_ACOES_ITEM, tempo_espera=3)
