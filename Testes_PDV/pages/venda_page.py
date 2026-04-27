"""
Venda Page - Page Object para tela de venda.
"""
import time
from collections import namedtuple
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from config import logger, LogStyle, Cores
from test_data import test_data


# ---------------------------------------------------------------------------
# Tipos semânticos de forma de pagamento (agnósticos ao nome da loja)
# ---------------------------------------------------------------------------
class TipoForma:
    """Categorias fixas independentes do nome configurado no caixa.exe."""
    DINHEIRO      = "dinheiro"
    POS_DEBITO    = "pos_debito"
    POS_CREDITO   = "pos_credito"
    PIX           = "pix"
    PERSONALIZADO = "personalizado"   # Pagamento Personalizado (sheet c/ tipo_venda + parcelas)
    TEF           = "tef"             # TEF — requer hardware externo, excluído por padrão
    OUTRO         = "outro"           # Forma desconhecida / não classificada


# Dados de uma forma descoberta na tela
FormaInfo = namedtuple("FormaInfo", ["titulo", "tipo", "tem_parcelamento"])

# Cache de processo — preenchido na primeira chamada, reutilizado no resto da sessão
_formas_cache: dict | None = None


def _salvar_formas_pagamento(formas: list) -> None:
    """Salva lista completa de formas em formas_pagamento.json (best-effort).
    Formato: {"_discovery_timestamp": ..., "formas": [...]}"""
    try:
        from test_data import _settings_path
        import json
        from datetime import datetime
        if not _settings_path:
            return
        path = _settings_path.parent / "formas_pagamento.json"
        data = {
            "_discovery_timestamp": datetime.now().isoformat(timespec="seconds"),
            "formas": formas,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"{LogStyle.OK} formas_pagamento.json salvo: {len(formas)} formas")
    except Exception:
        pass


def _persistir_formas_descobertas(mapa: dict) -> None:
    """Salva formas descobertas no settings.json (best-effort, não quebra testes)."""
    try:
        from test_data import TestData
        kwargs = {}
        for tipo, info in mapa.items():
            if tipo == TipoForma.DINHEIRO:
                kwargs["forma_dinheiro"] = info.titulo
            elif tipo == TipoForma.POS_DEBITO:
                kwargs["forma_debito"] = info.titulo
            elif tipo == TipoForma.POS_CREDITO:
                kwargs["forma_credito"] = info.titulo
        if kwargs:
            TestData.atualizar_formas_descobertas(**kwargs)
    except Exception:
        pass


def _persistir_parcelas_descobertas(parcelas: list) -> None:
    """Salva lista de parcelas de crédito no settings.json (best-effort)."""
    try:
        from test_data import TestData
        TestData.atualizar_formas_descobertas(parcelas_credito=parcelas)
    except Exception:
        pass


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

    # Tela de atalhos de formas de pagamento
    RECYCLER_FORMAS      = "recycler_payment_methods"
    TXT_TITULO_FORMA     = "txt_payment_title"
    TXT_SUBTITULO_FORMA  = "txt_payment_subtitle"   # tipo fixo: "Dinheiro", "Cartão de Crédito/Débito"
    TXT_DETALHES_FORMA   = "txt_payment_details"    # movimentos: "CREDITO", "DEBITO", "TEF", "A VISTA"
    # Bottom sheet de parcelamento (aparece ao clicar forma de crédito)
    RECYCLER_PARCELAS    = "recycler_plano_venda"
    # Bottom sheet "Pagamento Personalizado"
    RECYCLER_TIPO_VENDA  = "recycler_tipo_venda"     # lista de tipos (A VISTA, BANRICOMPRAS DEBITO, ...)
    BTN_FECHAR_SHEET     = "btn_close"               # fecha qualquer bottom sheet de pagamento

    # Formas excluídas da seleção automática (requerem hardware externo)
    _EXCLUIR_FORMAS = ["tef", "bshoppix", "bshop pix", "pagamento personalizado"]

    # Tipos de tipo_venda do Personalizado que requerem hardware externo → habilitado=False por padrão
    _EXCLUIR_TIPOS_VENDA = ["tef", "pix", "whatsapp", " app"]

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

    def obter_formas_pagamento_disponiveis(self) -> list:
        """Lê atalhos exibidos na tela e filtra TEF/BShopPIX/Personalizado.
        Chamar quando já estiver na tela de seleção de forma de pagamento."""
        elementos = self.encontrar_todos_por_id(self.TXT_TITULO_FORMA)
        formas = []
        for el in elementos:
            texto = el.text.strip()
            if not any(exc in texto.lower() for exc in self._EXCLUIR_FORMAS):
                formas.append(texto)
        logger.info(f"{LogStyle.INFO} Formas disponíveis: {LogStyle.valor(str(formas))}")
        return formas

    def descobrir_formas_tipadas(self) -> dict:
        """Classifica formas de pagamento por tipo semântico lendo subtitle + details.
        Chamar quando já estiver na tela de seleção de forma de pagamento.
        Resultado cacheado por processo — não redescobre em testes subsequentes.
        Retorna {TipoForma: FormaInfo}."""
        global _formas_cache
        if _formas_cache is not None:
            return _formas_cache

        titulos    = self.encontrar_todos_por_id(self.TXT_TITULO_FORMA)
        subtitulos = self.encontrar_todos_por_id(self.TXT_SUBTITULO_FORMA)
        # NOTA: nem todos os cards têm txt_payment_details (ex: Pagamento Personalizado)
        # Por isso NÃO indexamos detalhes por posição — buscamos por XPath ancorado no título

        mapa = {}
        for i, titulo_el in enumerate(titulos):
            titulo    = titulo_el.text.strip()
            subtitulo = subtitulos[i].text.strip().lower() if i < len(subtitulos) else ""

            # Busca details como irmão do título — evita desalinhamento de índices
            detalhe = ""
            try:
                xpath_det = (
                    f'//android.widget.TextView[contains(@resource-id,"txt_payment_title")'
                    f' and @text="{titulo}"]'
                    f'/following-sibling::android.widget.TextView'
                    f'[contains(@resource-id,"txt_payment_details")]'
                )
                det_els = self.driver.find_elements(AppiumBy.XPATH, xpath_det)
                if det_els:
                    detalhe = det_els[0].text.strip().lower()
            except Exception:
                pass

            tipo = self._classificar_tipo(titulo, subtitulo, detalhe)
            if tipo and tipo not in mapa:
                mapa[tipo] = FormaInfo(
                    titulo=titulo,
                    tipo=tipo,
                    tem_parcelamento=(tipo == TipoForma.POS_CREDITO)
                )

        _formas_cache = mapa
        _persistir_formas_descobertas(mapa)
        logger.info(f"{LogStyle.INFO} Formas tipadas: {LogStyle.valor(str(mapa))}")
        return mapa

    def _classificar_tipo(self, titulo: str, subtitulo: str, detalhe: str):
        """Classifica uma forma pelo subtítulo (campo fixo do app) e detalhes."""
        if "selecione manualmente" in subtitulo:
            return None
        if "dinheiro" in subtitulo:
            return TipoForma.DINHEIRO
        if "bshoppix" in subtitulo or ("pix" in subtitulo and "cartão" not in subtitulo):
            return None  # PIX excluído — requer integração BshopPix
        if "cartão" in subtitulo or "cartao" in subtitulo or \
           "credito" in subtitulo or "debito" in subtitulo:
            if "tef" in detalhe or "tef" in titulo.lower():
                return None  # TEF excluído — requer hardware externo
            if "debito" in detalhe:
                return TipoForma.POS_DEBITO
            if "credito" in detalhe:
                return TipoForma.POS_CREDITO
        return None

    def _classificar_tipo_completo(self, subtitulo: str, detalhe: str) -> str:
        """Como _classificar_tipo mas SEM exclusões — inclui TEF, PIX, Personalizado.
        Usado em descobrir_formas_completo()."""
        sub = subtitulo.lower()
        det = detalhe.lower()
        if "dinheiro" in sub:
            return TipoForma.DINHEIRO
        if "selecione manualmente" in sub:
            return TipoForma.PERSONALIZADO
        if "bshoppix" in sub or ("pix" in sub and "cartão" not in sub):
            return TipoForma.PIX
        if "cartão" in sub or "cartao" in sub or "credito" in sub or "debito" in sub:
            if "tef" in det or "tef" in sub:
                return TipoForma.TEF
            if "debito" in det:
                return TipoForma.POS_DEBITO
            if "credito" in det:
                return TipoForma.POS_CREDITO
        return TipoForma.OUTRO

    # ------------------------------------------------------------------
    # DESCOBERTA COMPLETA (todos os atalhos + Personalizado)
    # ------------------------------------------------------------------

    def descobrir_formas_completo(self) -> list:
        """Descobre TODAS as formas + subopções do Personalizado.
        Chamar quando na tela de seleção de formas de pagamento.
        Salva em formas_pagamento.json E atualiza settings.json.
        Retorna lista de dicts prontos para JSON.

        FASE 1: lê info básica de todos os cards SEM navegar (evita stale elements).
        FASE 2: para cada forma que precisa de sub-discovery, navega e volta.
        """
        # --- FASE 1: leitura básica (sem navegação) ---
        formas = []
        titulos    = self.encontrar_todos_por_id(self.TXT_TITULO_FORMA)
        subtitulos = self.encontrar_todos_por_id(self.TXT_SUBTITULO_FORMA)

        for i, titulo_el in enumerate(titulos):
            try:
                titulo    = titulo_el.text.strip()
                subtitulo = subtitulos[i].text.strip() if i < len(subtitulos) else ""
                detalhe   = ""
                try:
                    xpath_det = (
                        f'//android.widget.TextView[contains(@resource-id,"txt_payment_title")'
                        f' and @text="{titulo}"]'
                        f'/following-sibling::android.widget.TextView'
                        f'[contains(@resource-id,"txt_payment_details")]'
                    )
                    det_els = self.driver.find_elements(AppiumBy.XPATH, xpath_det)
                    if det_els:
                        detalhe = det_els[0].text.strip()
                except Exception:
                    pass

                tipo_auto  = self._classificar_tipo_completo(subtitulo, detalhe)
                habilitado = tipo_auto not in (TipoForma.TEF, TipoForma.PIX, TipoForma.OUTRO)
                formas.append({
                    "titulo":      titulo,
                    "subtitulo":   subtitulo,
                    "detalhes":    detalhe,
                    "tipo_auto":   tipo_auto,
                    "habilitado":  habilitado,
                    "parcelas":    [],
                    "tipos_venda": [],
                })
                logger.info(f"{LogStyle.INFO} Forma: {titulo!r} → {tipo_auto}")
            except Exception as exc:
                logger.info(f"{LogStyle.DEBUG} Fase1 erro item {i}: {exc}")

        # --- FASE 2: sub-discoveries (navegam e voltam) ---
        # Elementos da fase 1 já foram consumidos; agora podemos navegar sem stale.
        for forma in formas:
            try:
                if forma["tipo_auto"] == TipoForma.PERSONALIZADO:
                    forma["tipos_venda"], forma["parcelas"] = self._descobrir_personalizado()
                elif forma["tipo_auto"] == TipoForma.POS_CREDITO:
                    forma["parcelas"] = self._descobrir_parcelas_pos_credito(forma["titulo"])
            except Exception as exc:
                logger.info(f"{LogStyle.DEBUG} Fase2 erro {forma['titulo']!r}: {exc}")

        if formas:
            _salvar_formas_pagamento(formas)
            self._sincronizar_settings_de_formas(formas)

        return formas

    def _fechar_sheet_ativo(self) -> None:
        """Fecha o bottom sheet no topo (btn_close ou voltar_tela como fallback)."""
        try:
            if not self.clicar_se_existir(self.BTN_FECHAR_SHEET, tempo_espera=2):
                self.voltar_tela()
            time.sleep(0.5)
        except Exception:
            pass

    def _descobrir_personalizado(self) -> tuple:
        """Abre sheet do Personalizado, lê tipos_venda + parcelas, fecha AMBOS os sheets.
        Retorna (tipos_venda: list[dict], parcelas: list[str])."""
        tipos_venda   = []
        parcelas      = []
        abriu_parcelas = False
        entrou_sheet  = False
        try:
            self.ver_e_clicar_texto("Pagamento Personalizado")
            # Clicar AVANÇAR abre o recycler_tipo_venda (igual _descobrir_parcelas_pos_credito)
            self.clicar_por_id(self.BTN_AVANCAR)
            time.sleep(1.0)
            entrou_sheet = True

            # Ler tipos_venda de recycler_tipo_venda
            els = self.driver.find_elements(
                AppiumBy.XPATH,
                '//android.widget.RecyclerView[contains(@resource-id,"recycler_tipo_venda")]'
                '//android.widget.TextView[contains(@resource-id,"txt_option_title")]',
            )
            for el in els:
                nome = el.text.strip()
                if nome:
                    hab = not any(x in nome.lower() for x in self._EXCLUIR_TIPOS_VENDA)
                    tipos_venda.append({"nome": nome, "habilitado": hab})

            # Tentar ler parcelas: clicar no primeiro tipo_venda com "credito" no nome
            for tv in tipos_venda:
                if "credito" in tv["nome"].lower():
                    xpath_tv = (
                        '//android.widget.RecyclerView[contains(@resource-id,"recycler_tipo_venda")]'
                        f'//android.widget.TextView[contains(@resource-id,"txt_option_title")'
                        f' and @text="{tv["nome"]}"]'
                    )
                    tv_els = self.driver.find_elements(AppiumBy.XPATH, xpath_tv)
                    if tv_els:
                        tv_els[0].click()
                        time.sleep(0.5)
                        parc_els = self.driver.find_elements(
                            AppiumBy.XPATH,
                            '//android.widget.RecyclerView[contains(@resource-id,"recycler_plano_venda")]'
                            '//android.widget.TextView[contains(@resource-id,"txt_option_title")]',
                        )
                        parcelas = [p.text.strip() for p in parc_els if p.text.strip()]
                        if parcelas:
                            abriu_parcelas = True
                            break
        except Exception as exc:
            logger.info(f"{LogStyle.DEBUG} _descobrir_personalizado falhou: {exc}")
        finally:
            # Fecha sheet de parcelas (se abriu) e depois sheet de tipo_venda
            if abriu_parcelas:
                self._fechar_sheet_ativo()   # fecha recycler_plano_venda
            if entrou_sheet:
                self._fechar_sheet_ativo()   # fecha recycler_tipo_venda
        return tipos_venda, parcelas

    def _descobrir_parcelas_pos_credito(self, titulo: str) -> list:
        """Abre sheet de crédito POS, lê parcelas disponíveis, fecha sem avançar."""
        try:
            self.ver_e_clicar_texto(titulo)
            self.clicar_por_id(self.BTN_AVANCAR)
            time.sleep(1)
            if self._parcelamento_visivel():
                els = self.driver.find_elements(
                    AppiumBy.XPATH,
                    '//android.widget.TextView[contains(@resource-id,"txt_option_title")]',
                )
                parcelas = [el.text.strip() for el in els if el.text.strip()]
                self.voltar_tela()
                return parcelas
            self.voltar_tela()
        except Exception:
            pass
        return []

    def _sincronizar_settings_de_formas(self, formas: list) -> None:
        """Atualiza settings.json com forma_debito/credito/dinheiro/parcelas (backward compat)."""
        try:
            from test_data import TestData
            kwargs: dict = {}
            for f in formas:
                if f["tipo_auto"] == TipoForma.DINHEIRO and "forma_dinheiro" not in kwargs:
                    kwargs["forma_dinheiro"] = f["titulo"]
                elif f["tipo_auto"] == TipoForma.POS_DEBITO and "forma_debito" not in kwargs:
                    kwargs["forma_debito"] = f["titulo"]
                elif f["tipo_auto"] == TipoForma.POS_CREDITO and "forma_credito" not in kwargs:
                    kwargs["forma_credito"] = f["titulo"]
                    if f["parcelas"] and "parcelas_credito" not in kwargs:
                        kwargs["parcelas_credito"] = f["parcelas"]
            if kwargs:
                TestData.atualizar_formas_descobertas(**kwargs)
        except Exception:
            pass

    def selecionar_personalizado(self, tipo_venda: str, parcela: str = None) -> None:
        """Seleciona Pagamento Personalizado → tipo_venda → parcela (se houver).
        Chamar na tela de seleção de formas de pagamento."""
        logger.info(f"{LogStyle.ACAO} Personalizado: tipo={LogStyle.valor(tipo_venda)}"
                    + (f" parcela={LogStyle.valor(parcela)}" if parcela else ""))
        self.ver_e_clicar_texto("Pagamento Personalizado")
        xpath_tv = (
            '//android.widget.RecyclerView[contains(@resource-id,"recycler_tipo_venda")]'
            f'//android.widget.TextView[contains(@resource-id,"txt_option_title")'
            f' and @text="{tipo_venda}"]'
        )
        self.encontrar_por_xpath(xpath_tv, tempo_espera=5).click()
        time.sleep(0.3)
        if parcela:
            xpath_parc = (
                '//android.widget.RecyclerView[contains(@resource-id,"recycler_plano_venda")]'
                f'//android.widget.TextView[contains(@resource-id,"txt_option_title")'
                f' and @text="{parcela}"]'
            )
            self.encontrar_por_xpath(xpath_parc, tempo_espera=5).click()
            time.sleep(0.3)
        self.ver_e_clicar(self.BTN_AVANCAR)

    def selecionar_pagamento_por_tipo(
        self,
        tipo: str,
        com_cliente: bool = True,
        parcela: str = "A Prazo 0 + 1"
    ) -> str:
        """Seleciona forma de pagamento pelo tipo semântico (não pelo nome).
        Override manual em settings.json tem prioridade.
        Chama pytest.skip() se o tipo não estiver disponível na base.
        Retorna o título real usado."""
        override = self._override_forma(tipo)
        if override:
            nome = override
            logger.info(f"{LogStyle.INFO} Override settings: {LogStyle.valor(nome)}")
        else:
            formas = self.descobrir_formas_tipadas()
            info = formas.get(tipo)
            if not info:
                import pytest
                pytest.skip(f"Tipo de pagamento '{tipo}' não configurado nesta base")
            nome = info.titulo

        parcela_arg = parcela if tipo == TipoForma.POS_CREDITO else None
        self.selecionar_pagamento(nome, com_cliente=com_cliente, parcela=parcela_arg)
        return nome

    def _override_forma(self, tipo: str):
        """Retorna override manual de settings.json, ou None para auto-descoberta."""
        mapa = {
            TipoForma.DINHEIRO:    getattr(test_data, "FORMA_DINHEIRO", None),
            TipoForma.POS_DEBITO:  getattr(test_data, "FORMA_DEBITO",   None),
            TipoForma.POS_CREDITO: getattr(test_data, "FORMA_CREDITO",  None),
        }
        return mapa.get(tipo)

    def obter_parcelas_disponiveis(self) -> list:
        """Lista todas as parcelas visíveis no bottom sheet de parcelamento.
        Chamar após btn_proceed em forma de crédito.
        Retorna ex: ['A Prazo 0 + 1', 'A Prazo 0 + 2', 'A Prazo 0 + 3'].
        Auto-persiste no settings.json na primeira descoberta."""
        try:
            els = self.driver.find_elements(
                AppiumBy.XPATH,
                '//android.widget.TextView[contains(@resource-id,"txt_option_title")]'
            )
            parcelas = [el.text.strip() for el in els if el.text.strip()]
            if parcelas:
                _persistir_parcelas_descobertas(parcelas)
            return parcelas
        except Exception:
            return []

    # XPath para detectar e clicar opções de parcelamento
    XPATH_PARCELA = '//android.widget.TextView[contains(@resource-id,"txt_option_title") and @text="{parcela}"]'
    XPATH_QUALQUER_PARCELA = '//android.widget.TextView[contains(@resource-id,"txt_option_title") and contains(@text,"A Prazo")]'

    def _parcelamento_visivel(self) -> bool:
        """Detecta se bottom sheet de parcelamento (crédito) abriu via XPath."""
        try:
            self.encontrar_por_xpath(self.XPATH_QUALQUER_PARCELA, tempo_espera=8)
            return True
        except Exception:
            return False

    def _selecionar_parcela(self, parcela: str = "A Prazo 0 + 1"):
        """Seleciona parcela no bottom sheet via XPath e avança."""
        logger.info(f"{LogStyle.ACAO} Parcela: {LogStyle.valor(parcela)}")
        xpath = self.XPATH_PARCELA.format(parcela=parcela)
        elemento = self.encontrar_por_xpath(xpath, tempo_espera=5)
        elemento.click()
        self.ver_e_clicar(self.BTN_AVANCAR)

    def selecionar_pagamento(self, nome_forma: str, com_cliente: bool = True, parcela: str = None):
        """Seleciona forma de pagamento pelo nome do atalho.

        Fluxo:
        - Clica no card → clica btn_proceed (igual DINHEIRO)
        - Para crédito: btn_proceed abre sheet de parcelas → seleciona parcela → btn_proceed no sheet
        - Para débito/dinheiro: btn_proceed avança direto (sem sheet)

        Args:
            nome_forma: Texto exibido no card (ex: 'BANRI POS', 'BANRI DEB POS', 'DINHEIRO').
            com_cliente: Se True, trata alerta de cashback após avançar.
            parcela: Texto da parcela para formas de crédito (ex: 'A Prazo 0 + 1').
                     Se None, assume débito/dinheiro — sem sheet de parcelas.
        """
        logger.info(f"{LogStyle.ACAO} Selecionando pagamento: {LogStyle.valor(nome_forma)}")
        self.ver_e_clicar_texto(nome_forma)
        self.clicar_por_id(self.BTN_AVANCAR)  # Igual DINHEIRO — para crédito abre sheet de parcelas

        if parcela and self._parcelamento_visivel():
            logger.info(f"{LogStyle.INFO} Sheet de parcelas detectado → {LogStyle.valor(parcela)}")
            self._selecionar_parcela(parcela)

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

        # Quando vai imprimir: usa timeout cheio (impressão pode demorar)
        # Quando descarta: timeout menor — dialog sempre aparece rápido, sleep curto
        timeout = test_data.PRINT_DIALOG_TIMEOUT if imprimir else 12
        sleep_pos = 2.0 if imprimir else 0.5
        logger.info(f"{LogStyle.ACAO} Respondendo impressão cupom venda: {LogStyle.valor('SIM' if imprimir else 'NÃO')} (config: {test_data.PRINT_CUPOM_VENDA})")
        btn = self.BTN_IMPRIMIR_SIM if imprimir else self.BTN_IMPRIMIR_NAO
        self.clicar_se_existir(btn, tempo_espera=timeout)
        time.sleep(sleep_pos)  # Aguarda fechamento do diálogo

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
            time.sleep(2.0 if imprimir else 0.5)
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

        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente concluída ✅')}")

    def executar_venda_consumidor(self, codigo_produto: str = "123"):
        """Executa fluxo completo de venda para consumidor (sem cliente)."""
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda consumidor')}")

        self.iniciar_venda_sem_cliente()
        self.adicionar_produto(codigo_produto)
        self.clicar_avancar()
        self.selecionar_pagamento_dinheiro(com_cliente=False)  # Consumidor não tem cashback
        self.finalizar_venda()

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
        elemento = self.encontrar_por_xpath(xpath_cb)
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
        logger.info(f"{LogStyle.secao('📋 FLUXO - Venda cliente com acréscimo concluída ✅')}")

    # --- Validações ---
    def venda_sucesso_exibida(self, timeout: int = 10) -> bool:
        """Verifica se mensagem de sucesso apareceu."""
        return self.texto_exibido("Venda realizada com sucesso!", timeout)

    def validar_sucesso_e_concluir(self):
        """
        Event-driven: trata dialogs de impressão ao aparecer, aguarda tela de sucesso,
        processa impressões da tela e conclui venda.

        Budget único 45s — sem timeouts fixos por dialog.
        Substitui: responder_impressao(12s) + responder_dialogo_cupom_troca(3s) + aguardar_texto(30s).
        """
        from pages.venda_sucesso_page import VendaSucessoPage

        # Event-driven: dialogs respondidos ao aparecer, sucesso aguardado no mesmo budget
        self._aguardar_sucesso_event_driven(timeout=45)

        # Processa impressões da tela de sucesso (NFC-E, DANFE, Cupom Troca botão)
        sucesso_page = VendaSucessoPage(self.driver)
        sucesso_page.processar_todas_impressoes()

        # Concluir venda
        self.concluir_venda()
