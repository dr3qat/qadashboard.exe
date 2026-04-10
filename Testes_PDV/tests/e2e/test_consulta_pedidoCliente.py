"""
Test Consulta Pedido Cliente - Testes de consulta e finalização de pedidos de cliente.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.consulta_pedido_page import ConsultaPedidoPage


@allure.epic("PDV Mobile")
@allure.feature("Consulta de Pedidos")
@allure.story("Finalizar Pedido Cliente")
class TestConsultaPedidoCliente:
    """Testes de consulta e finalização de pedidos de cliente."""

    @allure.title("Consulta Pedido - Finalizar pedido cliente")
    @allure.description("""
**Cenário:** Finalizar pedido de cliente via consulta

**Pré-condições:**
- Usuário logado no sistema
- Pedido de cliente pendente (gerado previamente)
- Flag "Buscar todos os pedidos" já configurada

**Dado** que estou na tela inicial do PDV
**E** a flag "Buscar todos os pedidos" está ativa
**Quando** acesso "Cons. Pedido"
**E** seleciono o último pedido da lista (número maior)
**E** clico em "Finalizar Pedido"
**E** se aparecer popup de bônus, clico em "Mais tarde"
**E** clico em "Finalizar" na tela de pagamento
**E** clico em "CONCLUIR VENDA" na tela de impressões
**Então** a venda é realizada com sucesso
**E** retorno à tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("consulta", "pedido", "cliente", "finalizar")
    def test_consulta_pedido_cliente_sucesso(self, driver_logado):
        """
        Cenário: Finalizar pedido de cliente via consulta
        Dado que estou logado no app
        E a flag de buscar todos os pedidos já está configurada
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

        # Act - Flag já deve estar ativa do teste anterior
        with allure.step("1. Executar consulta e finalização do pedido cliente"):
            pagina_consulta.executar_consulta_e_finalizar_pedido()

        # Assert
        with allure.step("2. Validar sucesso e concluir"):
            pagina_consulta.validar_sucesso_e_concluir()

        with allure.step("3. Verificar retorno à tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), "Nao voltou para tela inicial"
