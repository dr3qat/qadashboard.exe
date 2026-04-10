"""
Test Venda Vale Presente - Teste de venda de vale presente.
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.vale_presente_page import ValePresentePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Venda")
@allure.story("Vale Presente")
class TestVendaValePresente:
    """Teste de venda de vale presente."""

    @allure.title("Venda de Vale Presente - Fluxo Completo")
    @allure.description("""
    Teste de venda de vale presente:
    - Navega para a tela de Vale Presente
    - Seleciona o vendedor
    - Valida os dados do resumo do vale presente (cliente, nome, número, valor)
    - Finaliza a venda com pagamento em dinheiro
    - Responde ao diálogo de impressão de comprovante
    - Valida mensagem de sucesso
    - Conclui a venda
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("vale-presente", "venda", "pagamento", "critico")
    def test_venda_vale_presente(self, driver_logado):
        """
        Cenário: Realizar venda de vale presente
        Dado que o usuário está logado
        Quando navega para Vale Presente
        E seleciona o vendedor
        E valida os dados do resumo
        E finaliza a venda com pagamento em dinheiro
        Então a venda deve ser realizada com sucesso
        """
        # Arrange
        home_page = HomePage(driver_logado)
        vale_presente_page = ValePresentePage(driver_logado)

        # Act
        with allure.step("Navegar para a tela de Vale Presente"):
            vale_presente_page.navegar_para_vale_presente()

        with allure.step("Selecionar Vendedor"):
            vale_presente_page.selecionar_vendedor()

        with allure.step("Validar dados do Vale Presente na tela"):
            dados = vale_presente_page.obter_dados_resumo_vale_presente()

            # Anexa os dados ao relatório Allure
            allure.attach(f"Cliente: {dados['cliente']}", name="Cliente", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"Produto: {dados['nome_vale']}", name="Nome do Vale", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"Número: {dados['numero_vale']}", name="Número do Vale", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"Valor: {dados['valor']}", name="Valor", attachment_type=allure.attachment_type.TEXT)

            # Valida que os dados não estão vazios (nome_vale pode ser vazio para vale novo)
            assert dados['cliente'], "Campo Cliente está vazio"
            assert dados['numero_vale'], "Campo Número do Vale está vazio"
            assert dados['valor'], "Campo Valor está vazio"

        with allure.step("Inserir valor do vale presente"):
            vale_presente_page.inserir_valor_vale()

        with allure.step("Clicar em FINALIZAR"):
            vale_presente_page.clicar_finalizar()

        with allure.step("Selecionar atalho de pagamento DINHEIRO"):
            vale_presente_page.selecionar_pagamento_dinheiro()

        with allure.step("Clicar em Avançar com a forma selecionada"):
            vale_presente_page.clicar_avancar_pagamento()

        with allure.step("Finalizar pagamento (botão Finalizar)"):
            vale_presente_page.finalizar_pagamento()

        with allure.step("Responder diálogo de impressão de comprovante (aguardando até 20s)"):
            vale_presente_page.responder_impressao()

        # Assert
        with allure.step("Validar mensagem de sucesso"):
            assert vale_presente_page.venda_sucesso_exibida(), \
                "Mensagem 'Venda realizada com sucesso!' não foi exibida"

        with allure.step("Clicar no botão CONCLUIR VENDA"):
            vale_presente_page.concluir_venda()
