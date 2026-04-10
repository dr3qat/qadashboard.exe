"""
Test Validar Cashback - Teste de validação de cashback no carrinho.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from pages.bonus_page import BonusPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Cashback")
@allure.story("Validação de Cashback")
class TestValidarCashback:
    """Teste de validação de cashback durante a venda."""

    @allure.title("Validar visualização de cashback disponível")
    @allure.description("""
    Teste de validação de cashback (EXATAMENTE como ValidarCashback.py):
    1. Iniciar venda
    2. Selecionar vendedor
    3. Buscar e selecionar cliente com cashback
    4. Adicionar produto ao carrinho
    5. Ler saldo disponível de cashback

    IMPORTANTE: Este teste NÃO avança para pagamento (conforme arquivo legado)
    Apenas valida que o cashback está visível no CARRINHO, não na tela de pagamento.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("cashback", "venda", "validacao", "critico")
    def test_validar_cashback(self, driver_logado):
        """
        Cenário: Validar visualização de cashback disponível
        Dado que o usuário está logado
        E possui um cliente com cashback disponível
        Quando adiciona um produto ao carrinho
        Então o valor do cashback deve ser exibido corretamente
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

        # Assert - Linha 38 do legado: Ler saldo de cashback
        with allure.step("Ler saldo disponível de cashback"):
            valor_cashback = bonus_page.obter_valor_cashback()

            # Anexa o valor ao relatório Allure
            allure.attach(valor_cashback, name="Valor do Cashback Disponível", attachment_type=allure.attachment_type.TEXT)

            # Valida que o valor foi carregado (não está vazio)
            assert valor_cashback, "Valor do cashback está vazio"
            assert "R$" in valor_cashback or "," in valor_cashback, \
                f"Formato do valor de cashback inválido: {valor_cashback}"
