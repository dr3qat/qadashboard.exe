"""Test Discovery Completo - Mapeia TODAS as formas + Personalizado e salva em formas_pagamento.json."""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Discovery")
@allure.story("Mapeamento de Formas de Pagamento")
class TestDiscoveryCompleto:

    @allure.title("Discovery - Mapear TODAS as formas de pagamento desta base")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("discovery", "formas", "pagamento", "mapeamento")
    def test_mapear_todas_formas(self, driver_logado):
        """Navega até a tela de pagamento, mapeia TODOS os atalhos (incluindo
        Pagamento Personalizado com tipos_venda e parcelas) e salva em
        formas_pagamento.json ao lado do settings.json.
        Não finaliza a venda — apenas mapeia e volta."""
        home  = HomePage(driver_logado)
        venda = VendaPage(driver_logado)

        with allure.step("1. Iniciar venda consumidor até tela de pagamento"):
            home.iniciar_venda()
            home.selecionar_vendedor()
            venda.iniciar_venda_sem_cliente()
            venda.adicionar_produto(test_data.PRODUCT_CODE_SALE)
            venda.clicar_avancar()

        with allure.step("2. Descobrir e mapear todas as formas"):
            formas = venda.descobrir_formas_completo()
            allure.attach(
                "\n".join(
                    f"[{'✅' if f['habilitado'] else '❌'}] {f['titulo']!r} → {f['tipo_auto']}"
                    + (f"\n    parcelas: {f['parcelas']}" if f["parcelas"] else "")
                    + (f"\n    tipos_venda: {[t['nome'] for t in f['tipos_venda']]}"
                       if f["tipos_venda"] else "")
                    for f in formas
                ),
                name="Formas descobertas",
                attachment_type=allure.attachment_type.TEXT,
            )
            logger.info(f"[DISCOVERY] {len(formas)} formas mapeadas")

        with allure.step("3. Voltar sem finalizar"):
            venda.voltar_tela()  # fecha tela de pagamento
            venda.voltar_tela()  # volta do carrinho
            venda.voltar_tela()  # volta para home

        assert formas, "Nenhuma forma de pagamento encontrada — verifique conexão com a base"
