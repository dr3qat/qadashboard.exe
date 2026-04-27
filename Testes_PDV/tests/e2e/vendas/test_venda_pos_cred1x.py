"""Test POS Crédito 1x - Venda consumidor com POS crédito 1x (nome descoberto dinamicamente)."""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage, TipoForma
from test_data import test_data
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Formas de Pagamento POS")
class TestVendaPosCred1x:

    @allure.title("Venda Consumidor - POS Crédito 1x (descoberta dinâmica)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("venda", "consumidor", "pos", "credito", "1x")
    def test_venda_consumidor_pos_credito_1x(self, driver_logado):
        """Venda consumidor com POS crédito parcela 0+1 — forma descoberta dinamicamente.
        Skip automático se POS Crédito não estiver configurado nesta base."""
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

        with allure.step("6. Selecionar POS Crédito 1x (qualquer base)"):
            parcela = test_data.PARCELAS_CREDITO[0] if len(test_data.PARCELAS_CREDITO) > 0 else "A Prazo 0 + 1"
            nome = venda.selecionar_pagamento_por_tipo(
                TipoForma.POS_CREDITO, com_cliente=False, parcela=parcela
            )
            allure.dynamic.parameter("forma_pagamento", nome)
            allure.dynamic.parameter("parcela", parcela)

        with allure.step("7. Finalizar venda"):
            venda.finalizar_venda()

        with allure.step("8. Validar sucesso e concluir"):
            venda.validar_sucesso_e_concluir()

        with allure.step("9. Verificar retorno à tela inicial"):
            assert home.tela_inicial_exibida(), "Não voltou para tela inicial após venda POS crédito 1x"

        logger.info(f"[POS CRÉDITO 1x] Venda consumidor {nome} 0+1 OK")
