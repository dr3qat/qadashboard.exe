"""
Test Consulta Pedido Consumidor - Testes de consulta e finalização de pedidos de consumidor.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.consulta_pedido_page import ConsultaPedidoPage


@allure.epic("PDV Mobile")
@allure.feature("Consulta de Pedidos")
@allure.story("Finalizar Pedido Consumidor")
class TestConsultaPedidoConsumidor:
    """Testes de consulta e finalização de pedidos de consumidor."""

    @allure.title("Consulta Pedido - Finalizar pedido consumidor")
    @allure.description("""
**Cenário:** Finalizar pedido de consumidor via consulta

**Pré-condições:**
- Usuário logado no sistema
- Pedido de consumidor pendente (gerado previamente)

**Dado** que estou na tela inicial do PDV
**Quando** configuro a flag "Buscar todos os pedidos"
**E** acesso "Cons. Pedido"
**E** seleciono o último pedido da lista (número maior)
**E** clico em "Finalizar Pedido"
**E** se aparecer popup de bônus, clico em "Mais tarde"
**E** clico em "Finalizar" na tela de pagamento
**E** clico em "CONCLUIR VENDA" na tela de impressões
**Então** a venda é realizada com sucesso
**E** retorno à tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("consulta", "pedido", "consumidor", "finalizar")
    def test_consulta_pedido_consumidor_sucesso(self, driver_logado):
        """
        Cenário: Finalizar pedido de consumidor via consulta
        Dado que estou logado no app
        E configurei a flag de buscar todos os pedidos
        Quando acesso a consulta de pedidos
        E seleciono o último pedido da lista (número maior)
        E finalizo o pedido
        Então a venda é realizada com sucesso
        E retorno à tela inicial
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_consulta = ConsultaPedidoPage(driver)

        # Act
        with allure.step("1. Configurar flag 'Buscar todos os pedidos'"):
            pagina_consulta.configurar_buscar_todos_pedidos()

        with allure.step("2. Executar consulta e finalização do pedido consumidor"):
            pagina_consulta.executar_consulta_e_finalizar_pedido()

        # Assert
        with allure.step("3. Validar sucesso e concluir"):
            pagina_consulta.validar_sucesso_e_concluir()

        with allure.step("4. Verificar retorno à tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
