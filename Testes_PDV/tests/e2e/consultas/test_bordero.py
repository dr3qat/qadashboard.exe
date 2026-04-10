"""
Test Bordero - Testes E2E para funcionalidade de Borderô.
"""
import pytest
import allure
from pages.bordero_page import BorderoPage
from datetime import datetime


@allure.epic("PDV Mobile")
@allure.feature("Borderô")
@allure.story("Geração de Borderô")
class TestBordero:
    """Testes E2E para funcionalidade de Borderô."""

    @allure.title("Gerar Borderô com Data Atual")
    @allure.description("""
    Cenário: Gerar borderô do dia atual e validar dados

    Pré-condições:
    - Usuário logado no sistema
    - Ter movimentações no caixa do dia

    Passos:
    1. Navegar até menu Borderô
    2. Inserir data atual no campo
    3. Clicar em "Gerar Borderô"
    4. Validar que os dados do borderô foram carregados

    Resultado esperado:
    - Borderô gerado com sucesso
    - Dados de faturamento, prestações, aportes e caixa exibidos
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("bordero", "relatorio", "caixa")
    def test_gerar_bordero_data_atual(self, driver_logado):
        """
        Cenário: Gerar borderô do dia atual
        Dado que o usuário está logado
        Quando acessar o menu Borderô
        E inserir a data atual
        E clicar em "Gerar Borderô"
        Então os dados do borderô devem ser exibidos corretamente
        """
        # Arrange
        bordero_page = BorderoPage(driver_logado)
        data_atual = datetime.now().strftime('%d/%m/%Y')

        # Act
        with allure.step("Navegar até menu Borderô"):
            bordero_page.navegar_ate_bordero()

        with allure.step(f"Inserir data atual ({data_atual})"):
            bordero_page.inserir_data_inicial()

        with allure.step("Gerar borderô"):
            bordero_page.gerar_bordero()

        with allure.step("Validar dados do borderô"):
            dados_bordero = bordero_page.validar_dados_bordero()

        # Assert
        with allure.step("Verificar se borderô foi gerado com sucesso"):
            assert bordero_page.bordero_gerado_com_sucesso(dados_bordero), \
                "Borderô não foi gerado ou dados não foram carregados"

            # Anexa dados coletados ao relatório Allure
            allure.attach(
                str(dados_bordero),
                name="Dados do Borderô",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Gerar Borderô com Data Específica")
    @allure.description("""
    Cenário: Gerar borderô de uma data específica

    Pré-condições:
    - Usuário logado no sistema
    - Ter movimentações no caixa na data especificada

    Passos:
    1. Navegar até menu Borderô
    2. Inserir data específica no campo
    3. Clicar em "Gerar Borderô"
    4. Validar que os dados do borderô foram carregados

    Resultado esperado:
    - Borderô gerado com sucesso para a data especificada
    - Dados de faturamento, prestações, aportes e caixa exibidos
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("bordero", "relatorio", "caixa")
    def test_gerar_bordero_data_especifica(self, driver_logado):
        """
        Cenário: Gerar borderô de uma data específica
        Dado que o usuário está logado
        Quando acessar o menu Borderô
        E inserir uma data específica
        E clicar em "Gerar Borderô"
        Então os dados do borderô devem ser exibidos para aquela data
        """
        # Arrange
        bordero_page = BorderoPage(driver_logado)
        data_teste = "01/03/2026"

        # Act
        with allure.step("Navegar até menu Borderô"):
            bordero_page.navegar_ate_bordero()

        with allure.step(f"Inserir data específica ({data_teste})"):
            bordero_page.inserir_data_inicial(data_teste)

        with allure.step("Gerar borderô"):
            bordero_page.gerar_bordero()

        with allure.step("Validar dados do borderô"):
            dados_bordero = bordero_page.validar_dados_bordero()

        # Assert
        with allure.step("Verificar se borderô foi gerado"):
            assert bordero_page.bordero_gerado_com_sucesso(dados_bordero), \
                f"Borderô não foi gerado para a data {data_teste}"

            # Anexa dados coletados ao relatório Allure
            allure.attach(
                str(dados_bordero),
                name=f"Dados do Borderô - {data_teste}",
                attachment_type=allure.attachment_type.TEXT
            )
