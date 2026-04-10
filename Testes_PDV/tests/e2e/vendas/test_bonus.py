"""
Test Bonus - Testes de venda utilizando bonus/cashback.

PRE-REQUISITO:
O cliente precisa ter bonus disponivel para estes testes funcionarem.
O bonus e gerado atraves de uma TROCA:
  1. Realizar uma venda para o cliente
  2. Realizar uma troca sobre essa venda
  3. A troca gera o bonus no valor da venda

Se os testes falharem por falta de bonus, execute antes:
  pytest tests/test_venda_cliente.py -v
  pytest tests/test_troca_cliente.py -v
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.bonus_page import BonusPage
from pages.venda_page import VendaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Bonus")
@allure.story("Venda com Bonus")
class TestBonus:
    """Testes de venda utilizando bonus."""

    @allure.title("Verificar Bonus Disponivel na Tela")
    @allure.description("""
Cenario: Verificar se bonus aparece na tela de pagamento

Pre-condicoes:
- Usuario logado no sistema
- Cliente pode ou nao ter bonus disponivel

Dado que estou na tela inicial do PDV
Quando inicio uma venda para cliente
E adiciono um produto
E avanço para a tela de pagamento
Entao devo ver o card de bonus com switch (se disponivel)
E devo ver o valor do bonus disponivel

Nota: Nao finaliza a venda - apenas verifica a presenca do bonus.
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("bonus", "verificacao")
    def test_verificar_bonus_disponivel(self, driver_logado):
        """
        Cenario: Verificar se bonus aparece na tela de pagamento
        Dado que navego ate a tela de forma de pagamento
        Entao devo ver o card de bonus com switch
        E devo ver o valor do bonus disponivel
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_bonus = BonusPage(driver)

        # Act
        with allure.step("1. Iniciar venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Selecionar cliente"):
            pagina_bonus.buscar_cliente_por_cpf(test_data.CUSTOMER_ID)

        with allure.step("4. Adicionar produto"):
            pagina_bonus.adicionar_produto(test_data.PRODUCT_CODE)

        with allure.step("5. Avancar para pagamento"):
            pagina_bonus.clicar_avancar_carrinho()

        # Assert
        with allure.step("6. Verificar elementos de bonus"):
            assert pagina_bonus.tela_pagamento_exibida(timeout=10), \
                "Tela de pagamento nao carregou"

            bonus_existe = pagina_bonus.bonus_disponivel()

            if bonus_existe:
                valor = pagina_bonus.obter_valor_bonus()
                ativado = pagina_bonus.bonus_ativado()

                allure.attach(
                    f"Switch de bonus: ENCONTRADO\n"
                    f"Valor: {valor}\n"
                    f"Estado: {'Ativado' if ativado else 'Desativado'}",
                    name="Bonus Encontrado",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    "Switch de bonus: NAO ENCONTRADO\n"
                    "Cliente nao possui bonus disponivel.\n"
                    "Para gerar bonus, execute venda + troca primeiro.",
                    name="Bonus Nao Encontrado",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step("7. Cancelar venda (voltar)"):
            driver.back()
            driver.back()
            driver.back()

        # Resultado informativo (nao falha se nao tiver bonus)
        if not bonus_existe:
            pytest.skip(
                "Bonus nao disponivel. "
                "Execute test_venda_cliente + test_troca_cliente primeiro."
            )

    @allure.title("Venda com Bonus - Cobertura Total")
    @allure.description("""
Cenario: Realizar venda usando bonus que cobre o valor total

Pre-condicoes:
- Usuario logado no sistema
- Cliente com bonus disponivel (gerado por troca anterior)
- Bonus >= valor do produto

Dado que estou na tela inicial do PDV
E o cliente possui bonus disponivel
Quando inicio uma venda para esse cliente
E adiciono um produto de valor <= bonus
E avanço para a tela de pagamento
E ativo o switch de bonus
Entao o valor final e R$ 0,00
E a venda e concluida com sucesso
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("bonus", "venda", "e2e")
    def test_venda_com_bonus(self, driver_logado):
        """
        Cenario: Realizar venda usando bonus disponivel
        Dado que o cliente tem bonus (gerado por troca anterior)
        Quando inicio uma venda para esse cliente
        E adiciono um produto de valor <= bonus
        E ativo o switch de bonus na tela de pagamento
        Entao o valor final e R$ 0,00
        E a venda e concluida com sucesso
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_bonus = BonusPage(driver)
        pagina_venda = VendaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Iniciar Venda'"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Buscar e selecionar cliente"):
            pagina_bonus.buscar_cliente_por_cpf(test_data.CUSTOMER_ID)

        with allure.step("4. Adicionar produto ao carrinho"):
            pagina_bonus.adicionar_produto(test_data.PRODUCT_CODE)

        with allure.step("5. Avancar para forma de pagamento"):
            pagina_bonus.clicar_avancar_carrinho()

        with allure.step("6. Verificar disponibilidade do bonus"):
            assert pagina_bonus.tela_pagamento_exibida(timeout=10), \
                "Tela de forma de pagamento nao carregou"

            if not pagina_bonus.bonus_disponivel():
                pytest.fail(
                    "BONUS NAO DISPONIVEL!\n"
                    "O cliente nao possui bonus. Para gerar bonus:\n"
                    "1. Execute: pytest tests/test_venda_cliente.py -v\n"
                    "2. Execute: pytest tests/test_troca_cliente.py -v\n"
                    "3. Execute este teste novamente"
                )

        with allure.step("7. Capturar valor do bonus"):
            valor_bonus = pagina_bonus.obter_valor_bonus()
            allure.attach(
                f"Bonus disponivel: {valor_bonus}",
                name="Valor do Bonus",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("8. Ativar bonus"):
            pagina_bonus.ativar_bonus()

        with allure.step("9. Verificar valor final"):
            valor_final = pagina_bonus.obter_valor_final()
            desconto = pagina_bonus.obter_desconto_bonus()

            allure.attach(
                f"Desconto aplicado: {desconto}\nValor final: {valor_final}",
                name="Resumo Pagamento",
                attachment_type=allure.attachment_type.TEXT
            )

            assert pagina_bonus.bonus_foi_aplicado(), \
                f"Bonus nao cobriu o valor total. Valor final: {valor_final}"

        with allure.step("10. Avancar no pagamento"):
            pagina_bonus.clicar_avancar_pagamento()

        with allure.step("11. Finalizar venda"):
            pagina_venda.finalizar_venda()

        with allure.step("12. Responder impressao"):
            pagina_bonus.responder_impressao(imprimir=False)

        # Assert
        with allure.step("13. Validar venda concluida"):
            assert pagina_bonus.venda_sucesso_exibida(), \
                "Venda com bonus nao foi concluida com sucesso"
            pagina_bonus.concluir_venda()