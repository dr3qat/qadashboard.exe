"""Test Bonus Cashback - Regressão: validação de bônus e cashback."""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from pages.bonus_page import BonusPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Bonus e Cashback")
@allure.story("Validação de Bônus")
class TestValidarBonus:

    @allure.title("REG: Bônus - Aplicação no Pagamento")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "bonus", "validacao")
    @pytest.mark.regression
    def test_validar_bonus(self, driver_logado):
        """Bônus ativado e desconto refletido no resumo de pagamento."""
        home_page = HomePage(driver_logado)
        venda_page = VendaPage(driver_logado)
        bonus_page = BonusPage(driver_logado)

        home_page.iniciar_venda()
        home_page.selecionar_vendedor()
        venda_page.clicar_buscar_cliente()
        venda_page.selecionar_cliente(test_data.CUSTOMER_ID_BONUS)
        venda_page.adicionar_produto(test_data.PRODUCT_CODE_SALE)
        venda_page.clicar_avancar()

        with allure.step("Ler saldo e ativar bonus"):
            valor_bonus = bonus_page.obter_valor_bonus()
            assert valor_bonus != "N/A", "Saldo de bonus nao encontrado"
            allure.attach(valor_bonus, name="Valor Bonus", attachment_type=allure.attachment_type.TEXT)
            bonus_page.ativar_bonus()

        with allure.step("Validar desconto aplicado"):
            desconto = bonus_page.obter_desconto_bonus()
            assert valor_bonus in desconto, \
                f"Bonus {valor_bonus} nao aplicado. Resumo: {desconto}"


@allure.epic("PDV Mobile")
@allure.feature("Bonus e Cashback")
@allure.story("Validação de Cashback")
class TestValidarCashback:

    @allure.title("REG: Cashback - Visível no Carrinho")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("regression", "cashback", "validacao")
    @pytest.mark.regression
    def test_validar_cashback(self, driver_logado):
        """Cashback disponível exibido no carrinho após adicionar produto."""
        home_page = HomePage(driver_logado)
        venda_page = VendaPage(driver_logado)
        bonus_page = BonusPage(driver_logado)

        home_page.iniciar_venda()
        home_page.selecionar_vendedor()
        venda_page.clicar_buscar_cliente()
        venda_page.selecionar_cliente(test_data.CUSTOMER_ID_BONUS)
        venda_page.adicionar_produto(test_data.PRODUCT_CODE_SALE)

        with allure.step("Validar cashback visivel"):
            valor_cashback = bonus_page.obter_valor_cashback()
            allure.attach(valor_cashback, name="Cashback Disponivel", attachment_type=allure.attachment_type.TEXT)
            assert valor_cashback, "Cashback vazio"
            assert "R$" in valor_cashback or "," in valor_cashback, \
                f"Formato invalido: {valor_cashback}"
