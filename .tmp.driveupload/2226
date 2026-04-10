"""
Smoke Tests E2E - Sanidade rapida (~8-10 min).

OBJETIVO:
    Verificar em poucos minutos se os fluxos criticos estao OK
    antes de rodar os testes E2E completos.

QUANDO USAR:
    - Antes de cada release
    - Apos corrigir bugs criticos
    - Para validar que o ambiente esta respondendo

TEMPO ESTIMADO: 8-10 minutos

COBERTURA (fluxos criticos derivados dos E2E):
    1. App abre e responde
    2. Login funciona
    3. Home com modulos visiveis
    4. Venda consumidor completa (produto + pagamento + sucesso)
    5. Venda cliente completa (busca cliente + produto + pagamento + sucesso)
    6. Consultar estoque de produto
    7. Cancelar venda sem itens (navegacao de saida)
"""
import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from pages.estoque_page import EstoquePage
from test_data import test_data
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@pytest.mark.smoke
class TestSmoke:
    """
    Smoke Tests - 7 verificacoes criticas.
    Se qualquer um falhar, nao adianta rodar os E2E.
    """

    # ──────────────────────────────────────────────
    # SMOKE 1: App abre
    # ──────────────────────────────────────────────
    @allure.title("SMOKE 1/7: App abre")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "ambiente")
    def test_01_app_abre(self, driver):
        """App inicializa sem crash e responde ao driver."""
        assert driver is not None, "Driver nao foi inicializado"
        page_source = driver.page_source
        assert page_source and len(page_source) > 100, \
            "App nao respondeu - page_source vazio ou muito pequeno"
        logger.info("[SMOKE 1/7] App abriu corretamente")

    # ──────────────────────────────────────────────
    # SMOKE 2: Login
    # ──────────────────────────────────────────────
    @allure.title("SMOKE 2/7: Login funciona")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "login")
    def test_02_login(self, driver):
        """Login com credenciais validas leva a tela inicial."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        login_page.garantir_login(
            ip=test_data.SERVER_IP,
            porta=test_data.SERVER_PORT,
            empresa=test_data.COMPANY,
            usuario=test_data.USER,
            senha=test_data.PASSWORD
        )

        assert home_page.tela_inicial_exibida(timeout=30), \
            "Tela inicial nao apareceu apos login"
        logger.info("[SMOKE 2/7] Login OK")

    # ──────────────────────────────────────────────
    # SMOKE 3: Home modulos visiveis
    # ──────────────────────────────────────────────
    @allure.title("SMOKE 3/7: Modulos principais visiveis na home")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "home")
    def test_03_home_modulos_visiveis(self, driver_logado):
        """Tela inicial exibe pelo menos o botao de Venda."""
        home_page = HomePage(driver_logado)

        venda_visivel = (
            home_page.texto_exibido("Venda", tempo_espera=5) or
            home_page.texto_exibido("Iniciar Venda", tempo_espera=3)
        )

        assert venda_visivel, \
            "Botao de Venda nao encontrado na home - app em estado invalido"
        logger.info("[SMOKE 3/7] Modulos visiveis na home")

    # ──────────────────────────────────────────────
    # SMOKE 4: Venda consumidor completa
    # ──────────────────────────────────────────────
    @allure.title("SMOKE 4/7: Venda consumidor - fluxo completo")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "venda", "consumidor")
    def test_04_venda_consumidor_completa(self, driver_logado):
        """
        Fluxo completo de venda para consumidor (sem cliente):
        Iniciar Venda → vendedor → sem cliente → produto → DINHEIRO → finalizar → home.
        """
        driver = driver_logado
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)

        with allure.step("1. Iniciar venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Executar fluxo consumidor (produto + dinheiro + finalizar)"):
            pagina_venda.executar_venda_consumidor(
                codigo_produto=test_data.PRODUCT_CODE_SALE
            )

        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial apos venda consumidor"

        logger.info("[SMOKE 4/7] Venda consumidor OK")

    # ──────────────────────────────────────────────
    # SMOKE 5: Venda cliente completa
    # ──────────────────────────────────────────────
    @allure.title("SMOKE 5/7: Venda cliente - fluxo completo")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "venda", "cliente")
    def test_05_venda_cliente_completa(self, driver_logado):
        """
        Fluxo completo de venda para cliente cadastrado:
        Iniciar Venda → vendedor → buscar cliente → produto → DINHEIRO → finalizar → home.
        """
        driver = driver_logado
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)

        with allure.step("1. Iniciar venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Executar fluxo cliente (busca + produto + dinheiro + finalizar)"):
            pagina_venda.executar_venda_cliente(
                id_cliente=test_data.CUSTOMER_ID,
                codigo_produto=test_data.PRODUCT_CODE_SALE
            )

        with allure.step("4. Validar sucesso e concluir"):
            pagina_venda.validar_sucesso_e_concluir()

        with allure.step("5. Verificar retorno a tela inicial"):
            assert pagina_inicial.tela_inicial_exibida(), \
                "Nao voltou para tela inicial apos venda cliente"

        logger.info("[SMOKE 5/7] Venda cliente OK")

    # ──────────────────────────────────────────────
    # SMOKE 6: Consultar estoque
    # ──────────────────────────────────────────────
    @allure.title("SMOKE 6/7: Consultar estoque de produto")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("smoke", "estoque")
    def test_06_consultar_estoque(self, driver_logado):
        """
        Navega ate Consultar Estoque, busca produto pelo codigo e
        valida que foi encontrado.
        """
        driver = driver_logado
        pagina_estoque = EstoquePage(driver)
        pagina_inicial = HomePage(driver)
        codigo = test_data.PRODUCT_CODE_SALE

        with allure.step("1. Acessar modulo de estoque"):
            pagina_estoque.acessar_estoque()

        with allure.step(f"2. Buscar produto codigo {codigo}"):
            pagina_estoque.buscar_produto_por_codigo(codigo)

        with allure.step("3. Validar produto encontrado"):
            assert pagina_estoque.produto_encontrado(), \
                f"Produto {codigo} nao foi encontrado no estoque"

        with allure.step("4. Voltar para home"):
            pagina_estoque.voltar_tela()
            # Confirma popup de saida se aparecer
            pagina_inicial.clicar_texto_se_existir("SIM", tempo_espera=2)

        logger.info("[SMOKE 6/7] Consultar estoque OK")

    # ──────────────────────────────────────────────
    # SMOKE 7: Cancelar venda (navegacao de saida)
    # ──────────────────────────────────────────────
    @allure.title("SMOKE 7/7: Cancelar venda vazia - navegacao funciona")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "cancelamento", "navegacao")
    def test_07_cancelar_venda_vazia(self, driver_logado):
        """
        Abre tela de venda sem adicionar produtos e volta para home.
        Valida que a navegacao de saida funciona.
        """
        driver = driver_logado
        pagina_inicial = HomePage(driver)
        pagina_venda = VendaPage(driver)

        with allure.step("1. Iniciar venda"):
            pagina_inicial.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            pagina_inicial.selecionar_vendedor()

        with allure.step("3. Entrar no carrinho sem cliente"):
            pagina_venda.iniciar_venda_sem_cliente()

        with allure.step("4. Voltar sem adicionar produtos"):
            pagina_venda.voltar_tela(confirmar=True)

        with allure.step("5. Verificar retorno a tela inicial"):
            # Pode precisar de um back extra dependendo do device
            if not pagina_inicial.tela_inicial_exibida(timeout=5):
                pagina_venda.voltar_tela(confirmar=True)
            assert pagina_inicial.tela_inicial_exibida(timeout=10), \
                "Nao voltou para tela inicial apos cancelar venda"

        logger.info("[SMOKE 7/7] Cancelar venda OK")
