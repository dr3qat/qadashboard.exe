"""Test POS Crédito Parcelas - Descobre e testa todas as parcelas disponíveis na base."""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage, TipoForma
from test_data import test_data
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Formas de Pagamento POS")
class TestVendaPosCreditoParcelas:

    @allure.title("POS Crédito - Mapear parcelas disponíveis nesta base")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("venda", "pos", "credito", "dinamico", "parcelas", "mapeamento")
    def test_mapear_parcelas_disponiveis(self, driver_logado):
        """Navega até o sheet de parcelamento e documenta todas as parcelas disponíveis.
        Não finaliza a venda — apenas mapeia e volta. Útil para diagnóstico de nova base."""
        home = HomePage(driver_logado)
        venda = VendaPage(driver_logado)

        with allure.step("1. Iniciar venda até tela de pagamento"):
            home.iniciar_venda()
            home.selecionar_vendedor()
            venda.iniciar_venda_sem_cliente()
            venda.adicionar_produto(test_data.PRODUCT_CODE_SALE)
            venda.clicar_avancar()

        with allure.step("2. Descobrir formas tipadas disponíveis"):
            formas = venda.descobrir_formas_tipadas()
            allure.attach(
                "\n".join(f"{tipo}: {info.titulo}" for tipo, info in formas.items()),
                name="Formas de pagamento desta base",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.info(f"[MAPEAMENTO] Formas: {formas}")

        info_credito = formas.get(TipoForma.POS_CREDITO)
        if not info_credito:
            pytest.skip("POS Crédito não disponível nesta base — não há parcelas para mapear")

        with allure.step(f"3. Clicar em '{info_credito.titulo}' para abrir sheet de parcelas"):
            venda.ver_e_clicar_texto(info_credito.titulo)
            venda.clicar_por_id(venda.BTN_AVANCAR)

        with allure.step("4. Capturar parcelas disponíveis no sheet"):
            parcelas = venda.obter_parcelas_disponiveis()
            allure.attach(
                "\n".join(parcelas) if parcelas else "(nenhuma parcela encontrada)",
                name="Parcelas disponíveis",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.info(f"[MAPEAMENTO] Parcelas: {parcelas}")

        # Volta sem finalizar — apenas mapeou
        with allure.step("5. Voltar sem finalizar"):
            venda.voltar_tela()  # fecha sheet
            venda.voltar_tela()  # volta da tela de pagamento
            venda.voltar_tela()  # volta do carrinho
            venda.voltar_tela()  # volta para home

        assert formas, "Nenhuma forma de pagamento encontrada — verifique conexão com a base"

    @allure.title("POS Crédito - Testar primeira parcela disponível (dinâmico)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("venda", "pos", "credito", "dinamico", "parcelas")
    def test_venda_pos_credito_primeira_parcela(self, driver_logado):
        """Descobre a forma POS Crédito e testa com a primeira parcela disponível.
        Funciona em qualquer base — independente do nome configurado no caixa.exe.
        Skip automático se POS Crédito não estiver disponível."""
        home = HomePage(driver_logado)
        venda = VendaPage(driver_logado)

        with allure.step("1. Iniciar venda"):
            home.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            home.selecionar_vendedor()

        with allure.step("3. Iniciar sem cliente (consumidor)"):
            venda.iniciar_venda_sem_cliente()

        with allure.step("4. Adicionar produto"):
            venda.adicionar_produto(test_data.PRODUCT_CODE_SALE)

        with allure.step("5. Avançar para pagamento"):
            venda.clicar_avancar()

        # Descobre formas (usa cache se já foi preenchido nesta sessão)
        formas = venda.descobrir_formas_tipadas()
        info = formas.get(TipoForma.POS_CREDITO)
        if not info:
            pytest.skip("POS Crédito não disponível nesta base")

        with allure.step(f"6. Selecionar '{info.titulo}' e abrir sheet de parcelas"):
            allure.attach(
                str(formas),
                name="Formas descobertas",
                attachment_type=allure.attachment_type.TEXT
            )
            venda.ver_e_clicar_texto(info.titulo)
            venda.clicar_por_id(venda.BTN_AVANCAR)

        with allure.step("7. Capturar e selecionar primeira parcela disponível"):
            parcelas = venda.obter_parcelas_disponiveis()
            allure.attach(
                "\n".join(parcelas) if parcelas else "(vazio)",
                name="Parcelas disponíveis",
                attachment_type=allure.attachment_type.TEXT
            )
            if not parcelas:
                pytest.skip("Sheet de parcelas não encontrado — verifique se é forma de crédito")
            primeira = parcelas[0]
            allure.dynamic.parameter("forma_pagamento", info.titulo)
            allure.dynamic.parameter("parcela", primeira)
            logger.info(f"[POS CRÉDITO DINÂMICO] Usando: {info.titulo} / {primeira}")
            venda._selecionar_parcela(primeira)

        with allure.step("8. Finalizar venda"):
            venda.finalizar_venda()

        with allure.step("9. Validar sucesso e concluir"):
            venda.validar_sucesso_e_concluir()

        with allure.step("10. Verificar retorno à tela inicial"):
            assert home.tela_inicial_exibida(), "Não voltou para home após venda POS crédito dinâmico"

        logger.info(f"[POS CRÉDITO DINÂMICO] {info.titulo} / {primeira} OK")
