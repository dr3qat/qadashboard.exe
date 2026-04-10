"""
Test Validar Bonus - Teste de validação de bônus no pagamento.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from pages.bonus_page import BonusPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Pagamento")
@allure.story("Validação de Bônus")
class TestValidarBonus:
    """Teste de validação de bônus durante o pagamento."""

    @allure.title("Validar aplicação de bônus no pagamento")
    @allure.description("""
    Teste de validação de bônus (EXATAMENTE como ValidarBonus.py):
    1. Iniciar venda
    2. Selecionar vendedor
    3. Buscar e selecionar cliente com bônus
    4. Adicionar produto ao carrinho
    5. Avançar para pagamento
    6. Ler saldo disponível de bônus ANTES de ativar
    7. Ativar pagamento com bônus (switch)
    8. Validar se o bônus foi aplicado no resumo (txt_bonus_compact)

    IMPORTANTE: Este teste NÃO finaliza a venda (conforme arquivo legado)
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("bonus", "pagamento", "validacao", "critico")
    def test_validar_bonus(self, driver_logado):
        """
        Cenário: Validar aplicação de bônus no pagamento
        Dado que o usuário está logado
        E possui um cliente com bônus disponível
        Quando adiciona um produto e vai para pagamento
        E ativa o bônus
        Então o valor do bônus deve ser aplicado corretamente
        """
        # Arrange
        home_page = HomePage(driver_logado)
        venda_page = VendaPage(driver_logado)
        bonus_page = BonusPage(driver_logado)

        # Act - Iniciar Venda (linha 28 do legado)
        with allure.step("Clicar no botão 'Iniciar Venda'"):
            home_page.iniciar_venda()

        # Linha 29 do legado
        with allure.step("Selecionar Vendedor"):
            home_page.selecionar_vendedor()

        # Linhas 31-33 do legado
        with allure.step(f"Clicar no botão 'Buscar Cliente' e selecionar cliente {test_data.CUSTOMER_ID_BONUS}"):
            venda_page.clicar_buscar_cliente()
            venda_page.selecionar_cliente(test_data.CUSTOMER_ID_BONUS)

        # Linhas 35-37 do legado
        with allure.step(f"Adicionar produto (código: {test_data.PRODUCT_CODE})"):
            venda_page.adicionar_produto(test_data.PRODUCT_CODE)

        # Linha 38 do legado
        with allure.step("Clicar no botão AVANÇAR"):
            venda_page.clicar_avancar()

        # Act - Validação do Bônus (EXATAMENTE como linhas 40-50 do legado)

        # Linha 43: Ler saldo ANTES de ativar
        with allure.step("1. Ler saldo disponível de bônus"):
            valor_bonus = bonus_page.obter_valor_bonus()
            assert valor_bonus != "N/A", "Saldo de bônus não foi encontrado"
            allure.attach(valor_bonus, name="Valor do Bônus Disponível", attachment_type=allure.attachment_type.TEXT)

        # Linha 46: Clicar no switch para ativar
        with allure.step("2. Ativar pagamento com bônus (switch_bonus)"):
            bonus_page.ativar_bonus()

        # Assert - Linha 49-50: Validar se o bônus foi aplicado no resumo
        with allure.step(f"3. Validar se o bônus de {valor_bonus} foi aplicado (txt_bonus_compact)"):
            desconto_aplicado = bonus_page.obter_desconto_bonus()
            assert valor_bonus in desconto_aplicado, \
                f"Bônus de {valor_bonus} não foi aplicado. Valor no resumo: {desconto_aplicado}"
            allure.attach(desconto_aplicado, name="Desconto Aplicado no Resumo", attachment_type=allure.attachment_type.TEXT)
