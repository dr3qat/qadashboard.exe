"""
Testes de validacao de locators.
Garante que os IDs definidos nas Page Objects existem no app.

COMO ATUALIZAR A LISTA DE IDS VALIDOS:
1. Conecte o dispositivo com o app aberto
2. Execute: adb shell uiautomator dump /sdcard/ui.xml
3. Execute: adb pull /sdcard/ui.xml
4. Abra o arquivo e extraia os resource-id
5. Adicione os novos IDs em IDS_VALIDOS_DO_APP

NOTA: Este teste roda SEM precisar do Appium ou dispositivo.
"""
import pytest


# =============================================================================
# LISTA DE IDS VALIDOS EXTRAIDOS DO APP
# Atualize esta lista quando o app mudar
# =============================================================================
IDS_VALIDOS_DO_APP = {
    # --- Login ---
    "btn_next_intro",
    "btn_done_intro",
    "btn_config_connection",
    "edt_config_conn_ip_server",
    "edt_config_conn_gateway_server",
    "md_buttonDefaultPositive",
    "edt_company_login",
    "edt_user_login",
    "edt_password_login",
    "btn_enter_login",

    # --- Home / Vendedor ---
    "txt_dialog_seller_name",

    # --- Venda / Pedido (comuns) ---
    "btn_select_customer",
    "btn_adicionar_produtos",
    "editText",
    "imageView3",
    "btn_proximo",
    "btn_proceed",
    "btnFinalizar",
    "btn_confirmar_venda",
    "search_src_text",
    "button3",
    "button30",
    "btn_mais_tarde",

    # --- Pedido ---
    "button17",

    # --- Venda Futura ---
    "btn_venda_futura_loja",
    "btn_venda_futura_domicilio",
    "edtCpf",
    "txt_payment_title",
    "txt_option_title",
    "imageView19",
    "btn_pagar",

    # --- Troca ---
    "textInputLayout4",
    "button9",
    "textView100",
    "checkBox",
    "button12",
    "switch_bonus",

    # --- Consulta Pedido ---
    "textView230",

    # --- Documentos ---
    "textInputLayout4",
    "textInputLayout5",
    "lbl_nf",
    "textView148",
    "textView238",

    # --- Android padrao ---
    "android:id/button1",
    "android:id/button2",
}


# =============================================================================
# TESTES DE LOCATORS POR PAGE OBJECT
# =============================================================================

class TestLocatorsLoginPage:
    """Valida locators da LoginPage."""

    def test_todos_locators_existem_no_app(self):
        """Verifica se todos os locators da LoginPage estao na lista de IDs validos."""
        from pages.login_page import LoginPage

        locators = {
            "BTN_PROXIMO_INTRO": LoginPage.BTN_PROXIMO_INTRO,
            "BTN_CONCLUIR_INTRO": LoginPage.BTN_CONCLUIR_INTRO,
            "BTN_CONFIGURAR_CONEXAO": LoginPage.BTN_CONFIGURAR_CONEXAO,
            "EDT_IP_SERVIDOR": LoginPage.EDT_IP_SERVIDOR,
            "EDT_GATEWAY_SERVIDOR": LoginPage.EDT_GATEWAY_SERVIDOR,
            "BTN_SALVAR_DIALOGO": LoginPage.BTN_SALVAR_DIALOGO,
            "EDT_EMPRESA": LoginPage.EDT_EMPRESA,
            "EDT_USUARIO": LoginPage.EDT_USUARIO,
            "EDT_SENHA": LoginPage.EDT_SENHA,
            "BTN_ENTRAR": LoginPage.BTN_ENTRAR,
        }

        erros = []
        for nome, valor in locators.items():
            if valor not in IDS_VALIDOS_DO_APP:
                erros.append(f"  - {nome}: '{valor}'")

        if erros:
            pytest.fail(
                f"Locators da LoginPage NAO encontrados na lista de IDs validos:\n"
                + "\n".join(erros)
                + "\n\nAtualize IDS_VALIDOS_DO_APP ou corrija o locator no codigo."
            )

    def test_locators_nao_estao_vazios(self):
        """Verifica que nenhum locator esta vazio ou None."""
        from pages.login_page import LoginPage

        assert LoginPage.BTN_ENTRAR, "BTN_ENTRAR nao pode ser vazio"
        assert LoginPage.EDT_USUARIO, "EDT_USUARIO nao pode ser vazio"
        assert LoginPage.EDT_SENHA, "EDT_SENHA nao pode ser vazio"
        assert LoginPage.EDT_EMPRESA, "EDT_EMPRESA nao pode ser vazio"


class TestLocatorsHomePage:
    """Valida locators da HomePage."""

    def test_todos_locators_existem_no_app(self):
        """Verifica se todos os locators da HomePage estao na lista de IDs validos."""
        from pages.home_page import HomePage

        locators = {
            "DIALOGO_VENDEDOR": HomePage.DIALOGO_VENDEDOR,
        }

        erros = []
        for nome, valor in locators.items():
            if valor not in IDS_VALIDOS_DO_APP:
                erros.append(f"  - {nome}: '{valor}'")

        if erros:
            pytest.fail(
                f"Locators da HomePage NAO encontrados:\n" + "\n".join(erros)
            )


class TestLocatorsVendaPage:
    """Valida locators da VendaPage."""

    def test_todos_locators_existem_no_app(self):
        """Verifica se todos os locators da VendaPage estao na lista de IDs validos."""
        from pages.venda_page import VendaPage

        locators = {
            "BTN_BUSCAR_CLIENTE": VendaPage.BTN_BUSCAR_CLIENTE,
            "BTN_INICIAR_VENDA_SEM_CLIENTE": VendaPage.BTN_INICIAR_VENDA_SEM_CLIENTE,
            "BTN_ADICIONAR_PRODUTOS": VendaPage.BTN_ADICIONAR_PRODUTOS,
            "EDT_BUSCA_PRODUTO": VendaPage.EDT_BUSCA_PRODUTO,
            "IMG_PRODUTO": VendaPage.IMG_PRODUTO,
            "BTN_PROXIMO": VendaPage.BTN_PROXIMO,
            "BTN_AVANCAR": VendaPage.BTN_AVANCAR,
            "BTN_FINALIZAR": VendaPage.BTN_FINALIZAR,
            "BTN_CONFIRMAR_VENDA": VendaPage.BTN_CONFIRMAR_VENDA,
            "BTN_IMPRIMIR_SIM": VendaPage.BTN_IMPRIMIR_SIM,
            "BTN_IMPRIMIR_NAO": VendaPage.BTN_IMPRIMIR_NAO,
            "EDT_BUSCA_CLIENTE": VendaPage.EDT_BUSCA_CLIENTE,
            "BTN_CONFIRMAR_CLIENTE": VendaPage.BTN_CONFIRMAR_CLIENTE,
            "BTN_MAIS_TARDE": VendaPage.BTN_MAIS_TARDE,
        }

        erros = []
        for nome, valor in locators.items():
            if valor not in IDS_VALIDOS_DO_APP:
                erros.append(f"  - {nome}: '{valor}'")

        if erros:
            pytest.fail(
                f"Locators da VendaPage NAO encontrados:\n" + "\n".join(erros)
            )


class TestLocatorsPedidoPage:
    """Valida locators da PedidoPage."""

    def test_todos_locators_existem_no_app(self):
        """Verifica se todos os locators da PedidoPage estao na lista de IDs validos."""
        from pages.pedido_page import PedidoPage

        locators = {
            "BTN_BUSCAR_CLIENTE": PedidoPage.BTN_BUSCAR_CLIENTE,
            "BTN_ADICIONAR_PRODUTOS": PedidoPage.BTN_ADICIONAR_PRODUTOS,
            "EDT_BUSCA_PRODUTO": PedidoPage.EDT_BUSCA_PRODUTO,
            "IMG_PRODUTO": PedidoPage.IMG_PRODUTO,
            "BTN_PROXIMO": PedidoPage.BTN_PROXIMO,
            "BTN_AVANCAR": PedidoPage.BTN_AVANCAR,
            "BTN_FINALIZAR": PedidoPage.BTN_FINALIZAR,
            "BTN_PEDIDO_GERADO": PedidoPage.BTN_PEDIDO_GERADO,
            "EDT_BUSCA_CLIENTE": PedidoPage.EDT_BUSCA_CLIENTE,
            "BTN_CONFIRMAR_CLIENTE": PedidoPage.BTN_CONFIRMAR_CLIENTE,
            "BTN_INICIAR_VENDA": PedidoPage.BTN_INICIAR_VENDA,
            "TXT_VENDEDOR": PedidoPage.TXT_VENDEDOR,
            "BTN_MAIS_TARDE": PedidoPage.BTN_MAIS_TARDE,
        }

        erros = []
        for nome, valor in locators.items():
            if valor not in IDS_VALIDOS_DO_APP:
                erros.append(f"  - {nome}: '{valor}'")

        if erros:
            pytest.fail(
                f"Locators da PedidoPage NAO encontrados:\n" + "\n".join(erros)
            )


class TestLocatorsVendaFuturaPage:
    """Valida locators da VendaFuturaPage."""

    def test_todos_locators_existem_no_app(self):
        """Verifica se todos os locators da VendaFuturaPage estao na lista de IDs validos."""
        from pages.venda_futura_page import VendaFuturaPage

        locators = {
            "BTN_VENDA_FUTURA_LOJA": VendaFuturaPage.BTN_VENDA_FUTURA_LOJA,
            "BTN_VENDA_FUTURA_DOMICILIO": VendaFuturaPage.BTN_VENDA_FUTURA_DOMICILIO,
            "TXT_VENDEDOR": VendaFuturaPage.TXT_VENDEDOR,
            "EDT_CPF": VendaFuturaPage.EDT_CPF,
            "BTN_CONFIRMAR_CPF": VendaFuturaPage.BTN_CONFIRMAR_CPF,
            "BTN_ADICIONAR_PRODUTOS": VendaFuturaPage.BTN_ADICIONAR_PRODUTOS,
            "EDT_BUSCA_PRODUTO": VendaFuturaPage.EDT_BUSCA_PRODUTO,
            "IMG_PRODUTO": VendaFuturaPage.IMG_PRODUTO,
            "BTN_PROXIMO": VendaFuturaPage.BTN_PROXIMO,
            "BTN_AVANCAR": VendaFuturaPage.BTN_AVANCAR,
            "TXT_PAGAMENTO_TITULO": VendaFuturaPage.TXT_PAGAMENTO_TITULO,
            "TXT_OPCAO_TITULO": VendaFuturaPage.TXT_OPCAO_TITULO,
            "IMG_PAGAMENTOS": VendaFuturaPage.IMG_PAGAMENTOS,
            "BTN_PAGAR": VendaFuturaPage.BTN_PAGAR,
            "BTN_FINALIZAR": VendaFuturaPage.BTN_FINALIZAR,
            "BTN_CONFIRMAR_VENDA": VendaFuturaPage.BTN_CONFIRMAR_VENDA,
            "BTN_IMPRIMIR_NAO": VendaFuturaPage.BTN_IMPRIMIR_NAO,
            "BTN_MAIS_TARDE": VendaFuturaPage.BTN_MAIS_TARDE,
        }

        erros = []
        for nome, valor in locators.items():
            if valor not in IDS_VALIDOS_DO_APP:
                erros.append(f"  - {nome}: '{valor}'")

        if erros:
            pytest.fail(
                f"Locators da VendaFuturaPage NAO encontrados:\n" + "\n".join(erros)
            )


class TestLocatorsTrocaPage:
    """Valida locators da TrocaPage."""

    def test_todos_locators_existem_no_app(self):
        """Verifica se todos os locators da TrocaPage estao na lista de IDs validos."""
        from pages.troca_page import TrocaPage

        locators = {
            "INPUT_DATA_INICIAL": TrocaPage.INPUT_DATA_INICIAL,
            "BTN_CONSULTAR": TrocaPage.BTN_CONSULTAR,
            "ITEM_LISTA_NOTAS": TrocaPage.ITEM_LISTA_NOTAS,
            "CHECKBOX_ITEM": TrocaPage.CHECKBOX_ITEM,
            "BTN_DEVOLVER": TrocaPage.BTN_DEVOLVER,
            "BTN_DIALOGO_OK": TrocaPage.BTN_DIALOGO_OK,
            "BTN_ADICIONAR_PRODUTOS": TrocaPage.BTN_ADICIONAR_PRODUTOS,
            "EDT_BUSCA_PRODUTO": TrocaPage.EDT_BUSCA_PRODUTO,
            "IMG_PRODUTO": TrocaPage.IMG_PRODUTO,
            "BTN_PROXIMO": TrocaPage.BTN_PROXIMO,
            "BTN_AVANCAR": TrocaPage.BTN_AVANCAR,
            "SWITCH_BONUS": TrocaPage.SWITCH_BONUS,
            "BTN_FINALIZAR": TrocaPage.BTN_FINALIZAR,
            "BTN_CONFIRMAR_VENDA": TrocaPage.BTN_CONFIRMAR_VENDA,
            "BTN_IMPRIMIR_NAO": TrocaPage.BTN_IMPRIMIR_NAO,
            "EDT_BUSCA_CLIENTE": TrocaPage.EDT_BUSCA_CLIENTE,
            "BTN_CONFIRMAR_CLIENTE": TrocaPage.BTN_CONFIRMAR_CLIENTE,
            "BTN_MAIS_TARDE": TrocaPage.BTN_MAIS_TARDE,
        }

        erros = []
        for nome, valor in locators.items():
            if valor not in IDS_VALIDOS_DO_APP:
                erros.append(f"  - {nome}: '{valor}'")

        if erros:
            pytest.fail(
                f"Locators da TrocaPage NAO encontrados:\n" + "\n".join(erros)
            )


class TestLocatorsConsultaPedidoPage:
    """Valida locators da ConsultaPedidoPage."""

    def test_todos_locators_existem_no_app(self):
        """Verifica se todos os locators da ConsultaPedidoPage estao na lista de IDs validos."""
        from pages.consulta_pedido_page import ConsultaPedidoPage

        locators = {
            "TXT_ITEM_PEDIDO": ConsultaPedidoPage.TXT_ITEM_PEDIDO,
            "BTN_FINALIZAR": ConsultaPedidoPage.BTN_FINALIZAR,
            "BTN_MAIS_TARDE": ConsultaPedidoPage.BTN_MAIS_TARDE,
            "BTN_DIALOG_SIM": ConsultaPedidoPage.BTN_DIALOG_SIM,
            "BTN_DIALOG_NAO": ConsultaPedidoPage.BTN_DIALOG_NAO,
        }

        erros = []
        for nome, valor in locators.items():
            if valor not in IDS_VALIDOS_DO_APP:
                erros.append(f"  - {nome}: '{valor}'")

        if erros:
            pytest.fail(
                f"Locators da ConsultaPedidoPage NAO encontrados:\n" + "\n".join(erros)
            )


class TestLocatorsDocumentosPage:
    """Valida locators da DocumentosPage."""

    def test_todos_locators_existem_no_app(self):
        """Verifica se todos os locators da DocumentosPage estao na lista de IDs validos."""
        from pages.documentos_page import DocumentosPage

        locators = {
            "EDT_PREENCHER_DATA_INICIAL": DocumentosPage.EDT_PREENCHER_DATA_INICIAL,
            "EDT_PREENCHER_DATA_FINAL": DocumentosPage.EDT_PREENCHER_DATA_FINAL,
            "LBL_VERIFICAR_QUE_DOCUMENTOS": DocumentosPage.LBL_VERIFICAR_QUE_DOCUMENTOS,
            "TXT_DETALHES_DOCUMENTO": DocumentosPage.TXT_DETALHES_DOCUMENTO,
            "TXT_VERIFICAR_QUE_DETALHES": DocumentosPage.TXT_VERIFICAR_QUE_DETALHES,
        }

        erros = []
        for nome, valor in locators.items():
            if valor not in IDS_VALIDOS_DO_APP:
                erros.append(f"  - {nome}: '{valor}'")

        if erros:
            pytest.fail(
                f"Locators da DocumentosPage NAO encontrados:\n" + "\n".join(erros)
            )


# =============================================================================
# TESTES DE CONSISTENCIA GERAL
# =============================================================================

class TestLocatorsConsistencia:
    """Testes de consistencia entre Page Objects."""

    def test_ids_compartilhados_sao_iguais(self):
        """
        Verifica que IDs usados em multiplas pages tem o mesmo valor.
        Ex: BTN_FINALIZAR deve ser igual em VendaPage e PedidoPage.
        """
        from pages.venda_page import VendaPage
        from pages.pedido_page import PedidoPage
        from pages.venda_futura_page import VendaFuturaPage
        from pages.troca_page import TrocaPage

        # BTN_FINALIZAR
        assert VendaPage.BTN_FINALIZAR == PedidoPage.BTN_FINALIZAR == VendaFuturaPage.BTN_FINALIZAR == TrocaPage.BTN_FINALIZAR, \
            "BTN_FINALIZAR tem valores diferentes entre pages!"

        # BTN_ADICIONAR_PRODUTOS
        assert VendaPage.BTN_ADICIONAR_PRODUTOS == PedidoPage.BTN_ADICIONAR_PRODUTOS == VendaFuturaPage.BTN_ADICIONAR_PRODUTOS, \
            "BTN_ADICIONAR_PRODUTOS tem valores diferentes entre pages!"

        # EDT_BUSCA_PRODUTO
        assert VendaPage.EDT_BUSCA_PRODUTO == PedidoPage.EDT_BUSCA_PRODUTO == VendaFuturaPage.EDT_BUSCA_PRODUTO, \
            "EDT_BUSCA_PRODUTO tem valores diferentes entre pages!"

    def test_nenhum_locator_id_tem_espacos(self):
        """
        Verifica que nenhum locator de ID tem espacos (erro comum).
        Ignora locators que sao textos (TXT_, TELA_, etc).
        """
        from pages.login_page import LoginPage
        from pages.home_page import HomePage
        from pages.venda_page import VendaPage

        todas_pages = [LoginPage, HomePage, VendaPage]

        # Prefixos que indicam IDs (nao podem ter espacos)
        prefixos_id = ('BTN_', 'EDT_', 'IMG_', 'CHECKBOX_', 'SWITCH_', 'INPUT_')

        for page in todas_pages:
            for attr_name in dir(page):
                if attr_name.isupper() and not attr_name.startswith('_'):
                    # Verifica apenas locators que sao IDs (nao textos)
                    if attr_name.startswith(prefixos_id):
                        valor = getattr(page, attr_name)
                        if isinstance(valor, str):
                            assert ' ' not in valor, \
                                f"{page.__name__}.{attr_name} contem espacos: '{valor}'"
