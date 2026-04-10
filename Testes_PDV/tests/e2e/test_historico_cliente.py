"""
Test Historico Cliente - Testes E2E para consulta de histórico de cliente.
"""
import pytest
import allure
from pages.historico_cliente_page import HistoricoClientePage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Histórico Cliente")
@allure.story("Consulta de Histórico")
class TestHistoricoCliente:
    """Testes E2E para consulta de histórico de cliente."""

    @allure.title("Consultar Histórico de Cliente")
    @allure.description("""
    Cenário: Consultar histórico completo de um cliente

    Pré-condições:
    - Usuário logado no sistema
    - Cliente configurado no test_data.CUSTOMER_ID

    Passos:
    1. Navegar até "Histórico Cliente"
    2. Buscar cliente por código
    3. Selecionar cliente
    4. Validar dados do histórico carregados:
       - Valor Total de Compras
       - Top 5 Produtos (se disponível)
       - Tendências por Nível (se disponível)
    5. Voltar para tela anterior

    Resultado esperado:
    - Histórico do cliente exibido com sucesso
    - Todos os dados disponíveis listados no terminal
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("historico", "cliente", "consulta", "relatorio")
    def test_consultar_historico_cliente(self, driver_logado):
        """
        Cenário: Consultar histórico de cliente
        Dado que o usuário está logado
        Quando acessar "Histórico Cliente"
        E buscar pelo cliente configurado
        Então os dados do histórico devem ser exibidos
        E todas as informações devem ser listadas no terminal
        """
        # Arrange
        historico_page = HistoricoClientePage(driver_logado)
        codigo_cliente = test_data.CUSTOMER_ID

        # Act
        with allure.step("Navegar até Histórico Cliente"):
            historico_page.navegar_ate_historico_cliente()

        with allure.step(f"Buscar e selecionar cliente: {codigo_cliente}"):
            historico_page.selecionar_cliente(codigo_cliente)

        with allure.step("Validar dados do histórico"):
            dados_historico = historico_page.validar_resumo_historico()

        # Assert
        with allure.step("Verificar se histórico foi carregado com sucesso"):
            assert historico_page.historico_carregado_com_sucesso(), \
                "Histórico do cliente não foi carregado ou dados estão vazios"

            # Anexa dados coletados ao relatório Allure
            allure.attach(
                str(dados_historico),
                name=f"Histórico do Cliente {codigo_cliente}",
                attachment_type=allure.attachment_type.TEXT
            )

        # Cleanup
        with allure.step("Voltar para tela anterior"):
            historico_page.voltar_tela_anterior()
