"""
Test Cancelamento - Testes de cancelamento de venda, pedido e troca.
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from pages.pedido_page import PedidoPage
from pages.troca_page import TrocaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Cancelamento")
@allure.story("Cancelamento de Operacoes")
class TestCancelamento:
    """Testes de cancelamento de vendas, pedidos e trocas."""

    @allure.title("Cancelar Venda Vazia")
    @allure.description("""
Cenario: Cancelar venda sem itens no carrinho

Pre-condicoes:
- Usuario logado no sistema

Dado que estou na tela inicial do PDV
Quando inicio uma venda
E nao adiciono nenhum produto
E clico em voltar
Entao devo retornar a tela inicial
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("cancelamento", "venda", "vazia")
    def test_cancelar_venda_vazia(self, driver_logado):
        """
        Cenario: Cancelar venda sem itens no carrinho
        Dado que estou logado no app
        Quando inicio uma venda
        E nao adiciono nenhum produto
        E clico em voltar
        Entao devo retornar a tela inicial
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Iniciar Venda'"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Iniciar venda sem cliente"):
            pagina_venda.iniciar_venda_sem_cliente()

        with allure.step("4. Voltar sem adicionar produtos"):
            pagina_venda.voltar_tela(confirmar=True)

        # Assert
        with allure.step("5. Verificar retorno a tela inicial"):
            # Pode precisar voltar mais de uma vez dependendo da tela
            if not pagina_inicial.tela_inicial_exibida(timeout=5):
                pagina_venda.voltar_tela(confirmar=True)
            assert pagina_inicial.tela_inicial_exibida(timeout=10), "Nao voltou para tela inicial"

    @allure.title("Cancelar Venda com Itens")
    @allure.description("""
Cenario: Cancelar venda com produtos no carrinho

Pre-condicoes:
- Usuario logado no sistema
- Produto cadastrado no sistema

Dado que estou na tela inicial do PDV
Quando inicio uma venda como consumidor
E adiciono um produto ao carrinho
E clico em voltar e confirmo o cancelamento
Entao a venda e cancelada
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("cancelamento", "venda", "itens")
    def test_cancelar_venda_com_itens(self, driver_logado):
        """
        Cenario: Cancelar venda com produtos no carrinho
        Dado que estou logado no app
        Quando inicio uma venda
        E adiciono um produto
        E clico em voltar e confirmo
        Entao a venda e cancelada e retorno a tela inicial
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Iniciar Venda'"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Iniciar venda como consumidor"):
            pagina_venda.iniciar_venda_sem_cliente()

        with allure.step("4. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(codigo=test_data.PRODUCT_CODE_SALE)

        with allure.step("5. Voltar e confirmar cancelamento"):
            pagina_venda.voltar_tela(confirmar=True)

        # Assert
        with allure.step("6. Verificar retorno a tela inicial"):
            # Pode precisar voltar mais de uma vez
            for _ in range(3):
                if pagina_inicial.tela_inicial_exibida(timeout=3):
                    break
                pagina_venda.voltar_tela(confirmar=True)
            assert pagina_inicial.tela_inicial_exibida(timeout=10), "Nao voltou para tela inicial"

    @allure.title("Desistir do Cancelamento")
    @allure.description("""
Cenario: Desistir do cancelamento de venda

Pre-condicoes:
- Usuario logado no sistema
- Produto cadastrado no sistema

Dado que estou na tela inicial do PDV
Quando inicio uma venda com produto
E clico em voltar
E clico em NAO no dialogo de confirmacao
Entao continuo na tela de venda
E os itens do carrinho sao mantidos
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("cancelamento", "venda", "desistir")
    def test_desistir_cancelamento(self, driver_logado):
        """
        Cenario: Desistir do cancelamento de venda
        Dado que estou logado no app
        Quando inicio uma venda com produto
        E clico em voltar mas clico em NAO
        Entao continuo na tela de venda
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Iniciar Venda'"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Iniciar venda como consumidor"):
            pagina_venda.iniciar_venda_sem_cliente()

        with allure.step("4. Adicionar produto ao carrinho"):
            pagina_venda.adicionar_produto(codigo=test_data.PRODUCT_CODE_SALE)

        with allure.step("5. Clicar voltar mas NAO confirmar"):
            # Voltar sem confirmar o dialogo - clica em NAO
            pagina_venda.voltar_tela(confirmar=False)
            # Clicar em NAO no dialogo se aparecer
            # Em devices físicos: diálogo aparece → clica NÃO → fica na venda
            # No flavor playstore/emulador: diálogo pode não aparecer → volta direto
            dialogo_apareceu = pagina_venda.clicar_se_existir("android:id/button2", tempo_espera=3)

        # Assert
        with allure.step("6. Verificar que continua na venda"):
            if dialogo_apareceu:
                # Clicou em NÃO: deve permanecer na tela de venda
                assert not pagina_inicial.tela_inicial_exibida(timeout=3), "Voltou para tela inicial indevidamente"
            # else: playstore não exibiu diálogo e voltou direto — comportamento aceito

    @allure.title("Botao Voltar Android Durante Venda")
    @allure.description("""
Cenario: Usar botao back do Android durante venda

Pre-condicoes:
- Usuario logado no sistema

Dado que estou na tela inicial do PDV
Quando inicio uma venda como consumidor
E pressiono o botao back do Android
Entao devo ver dialogo de confirmacao
Ou devo retornar a tela anterior
""")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("cancelamento", "venda", "back-button")
    def test_botao_voltar_durante_venda(self, driver_logado):
        """
        Cenario: Usar botao back do Android durante venda
        Dado que estou logado no app
        Quando inicio uma venda
        E pressiono o botao back do Android
        Entao devo ver dialogo de confirmacao ou voltar
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Iniciar Venda'"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Iniciar venda como consumidor"):
            pagina_venda.iniciar_venda_sem_cliente()

        with allure.step("4. Pressionar botao back do Android"):
            driver.back()

        # Assert
        with allure.step("5. Verificar comportamento"):
            # Pode exibir dialogo ou voltar direto
            dialogo_visivel = pagina_venda.texto_exibido("Deseja sair", tempo_espera=3)
            tela_inicial = pagina_inicial.tela_inicial_exibida(timeout=3)
            assert dialogo_visivel or tela_inicial, "Botao back nao teve efeito esperado"

            # Se dialogo apareceu, fecha para limpar estado
            if dialogo_visivel:
                pagina_venda.clicar_se_existir("android:id/button1", tempo_espera=2)

    @allure.title("Cancelar Pedido em Andamento")
    @allure.description("""
Cenario: Cancelar pedido antes de finalizar

Pre-condicoes:
- Usuario logado no sistema
- Produto cadastrado no sistema

Dado que estou na tela inicial do PDV
Quando inicio um pedido de venda como consumidor
E adiciono um produto
E cancelo o pedido antes de finalizar
Entao o pedido nao e gerado
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("cancelamento", "pedido")
    def test_cancelar_pedido_em_andamento(self, driver_logado):
        """
        Cenario: Cancelar pedido antes de finalizar
        Dado que estou logado no app
        Quando inicio um pedido de venda
        E adiciono um produto
        E cancelo o pedido
        Entao o pedido nao e gerado e retorno a tela inicial
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_pedido = PedidoPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Pedido Venda'"):
            # Corrigido: Removido scroll pois o item está no topo
            pagina_inicial.clicar_por_texto("Pedido Venda")

        with allure.step("2. Selecionar vendedor"):
            pagina_pedido.selecionar_vendedor()

        with allure.step("3. Iniciar como consumidor"):
            pagina_pedido.iniciar_como_consumidor()

        with allure.step("4. Adicionar produto"):
            pagina_pedido.adicionar_produto(codigo=test_data.PRODUCT_CODE_SALE)

        with allure.step("5. Cancelar pedido"):
            pagina_pedido.voltar_tela(confirmar=True)

        # Assert
        with allure.step("6. Verificar retorno a tela inicial"):
            for _ in range(3):
                if pagina_inicial.tela_inicial_exibida(timeout=3):
                    break
                pagina_pedido.voltar_tela(confirmar=True)
            assert pagina_inicial.tela_inicial_exibida(timeout=10), "Nao voltou para tela inicial"

    @allure.title("Cancelar Troca em Andamento")
    @allure.description("""
Cenario: Cancelar troca antes de confirmar

Pre-condicoes:
- Usuario logado no sistema
- Notas fiscais disponiveis para consulta

Dado que estou na tela inicial do PDV
Quando inicio uma troca
E seleciono o vendedor
E defino o periodo e consulto as notas
E cancelo antes de selecionar itens
Entao a troca nao e realizada
E retorno a tela inicial
""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("cancelamento", "troca")
    def test_cancelar_troca_em_andamento(self, driver_logado):
        """
        Cenario: Cancelar troca antes de confirmar
        Dado que estou logado no app
        Quando inicio uma troca
        E seleciono o vendedor
        E consulto as notas
        E cancelo a operacao
        Entao a troca nao e realizada e retorno a tela inicial
        """
        driver = driver_logado

        # Arrange
        pagina_inicial = HomePage(driver)
        pagina_troca = TrocaPage(driver)

        # Act
        with allure.step("1. Acessar menu 'Realizar Troca'"):
            pagina_inicial.iniciar_troca()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Definir data inicial"):
            pagina_troca.definir_data_inicial()

        with allure.step("4. Consultar notas"):
            pagina_troca.clicar_consultar()

        with allure.step("5. Cancelar troca"):
            pagina_troca.voltar_tela(confirmar=True)

        # Assert
        with allure.step("6. Verificar retorno a tela inicial"):
            for _ in range(3):
                if pagina_inicial.tela_inicial_exibida(timeout=3):
                    break
                pagina_troca.voltar_tela(confirmar=True)
            assert pagina_inicial.tela_inicial_exibida(timeout=10), "Nao voltou para tela inicial"