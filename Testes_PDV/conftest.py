"""
Conftest - Fixtures compartilhadas para pytest.
Suporta execucao em multiplos dispositivos.
Configuracao avancada do Allure para relatorios detalhados.
Compativel com CI/CD (GitHub Actions, Jenkins, etc).
"""
import subprocess
import pytest
import allure
import os
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from appium import webdriver

# Desabilitar logs DEBUG do Faker (limpa saída dos testes)
logging.getLogger('faker').setLevel(logging.WARNING)

# Filtrar logs de bibliotecas externas (só WARNING+)
for _lib in ('selenium.webdriver', 'urllib3', 'appium', 'asyncio'):
    logging.getLogger(_lib).setLevel(logging.WARNING)

# _NO_WINDOW definido em config.py — importado de lá


# ============================================================================
# 🧹 LIMPEZA AUTOMÁTICA DE CACHE
# ============================================================================
def _limpar_cache_pytest():
    """Limpa cache do pytest e arquivos .pyc/__pycache__ antes de iniciar testes."""
    diretorios_cache = [
        '.pytest_cache',
        '__pycache__',
        'tests/__pycache__',
        'tests/e2e/__pycache__',
        'tests/unit/__pycache__',
        'tests/smoke/__pycache__',
        'tests/regression/__pycache__',
        'pages/__pycache__',
    ]

    for diretorio in diretorios_cache:
        caminho = Path(diretorio)
        if caminho.exists():
            try:
                shutil.rmtree(caminho)
            except Exception:
                pass


def pytest_sessionstart(session):
    """Hook chamado no início da sessão de testes - limpa cache automaticamente."""
    _limpar_cache_pytest()


# ============================================================================
# 🔧 MODO DE LOGGING
# ============================================================================
# Modo de logging: False = Normal (limpo), True = Debug (técnico)
DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"


def _executar_adb_getprop(adb_prefix: list, propriedade: str) -> str:
    """Executa adb shell getprop e retorna valor ou 'N/A'."""
    try:
        cmd = adb_prefix + ['shell', 'getprop', propriedade]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, **_NO_WINDOW)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return "N/A"


def _obter_resolucao_tela(adb_prefix: list) -> str:
    """Obtem resolução de tela via 'wm size'."""
    try:
        cmd = adb_prefix + ['shell', 'wm', 'size']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, **_NO_WINDOW)
        if result.returncode == 0 and result.stdout.strip():
            for linha in result.stdout.strip().split('\n'):
                if 'Physical size:' in linha:
                    return linha.split(':')[-1].strip()
            return result.stdout.strip().split(':')[-1].strip()
    except Exception:
        pass
    return "N/A"


def _obter_densidade_tela(adb_prefix: list) -> str:
    """Obtem densidade de tela (DPI) via 'wm density'."""
    try:
        cmd = adb_prefix + ['shell', 'wm', 'density']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, **_NO_WINDOW)
        if result.returncode == 0 and result.stdout.strip():
            for linha in result.stdout.strip().split('\n'):
                if 'Physical density:' in linha:
                    return linha.split(':')[-1].strip() + " dpi"
            return result.stdout.strip().split(':')[-1].strip() + " dpi"
    except Exception:
        pass
    return "N/A"


def _obter_ram_total(adb_prefix: list) -> str:
    """Obtem RAM total do dispositivo."""
    try:
        cmd = adb_prefix + ['shell', 'cat', '/proc/meminfo']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, **_NO_WINDOW)
        if result.returncode == 0:
            for linha in result.stdout.split('\n'):
                if 'MemTotal:' in linha:
                    partes = linha.split()
                    if len(partes) >= 2:
                        kb = int(partes[1])
                        gb = kb / 1024 / 1024
                        return f"{gb:.1f} GB"
    except Exception:
        pass
    return "N/A"


def _obter_info_device_adb(device_id: str = None) -> dict:
    """Obtem informações detalhadas do device via ADB."""
    info = {}
    adb_prefix = ['adb', '-s', device_id] if device_id else ['adb']

    # Propriedades via getprop
    propriedades = [
        ("model", "ro.product.model"),
        ("manufacturer", "ro.product.manufacturer"),
        ("brand", "ro.product.brand"),
        ("android_version", "ro.build.version.release"),
        ("api_level", "ro.build.version.sdk"),
        ("security_patch", "ro.build.version.security_patch"),
        ("build_id", "ro.build.display.id"),
        ("cpu_abi", "ro.product.cpu.abi"),
        ("serial", "ro.serialno"),
    ]

    for chave, prop in propriedades:
        info[chave] = _executar_adb_getprop(adb_prefix, prop)

    # Comandos especiais
    info["screen_size"] = _obter_resolucao_tela(adb_prefix)
    info["screen_density"] = _obter_densidade_tela(adb_prefix)
    info["ram_total"] = _obter_ram_total(adb_prefix)

    return info


from config import (
    APPIUM_SERVER_URL,
    get_appium_options,
    SCREENSHOTS_DIR,
    APP_PACKAGE,
    logger,
    configurar_logger_modo,
    _NO_WINDOW,
)
from pages.login_page import LoginPage
from pages.home_page import HomePage
from test_data import test_data


# Diretorio para resultados Allure
ALLURE_RESULTS_DIR = Path(__file__).parent / "allure-results"

# --- Opcoes de linha de comando para multiplos dispositivos ---
def pytest_addoption(parser):
    """Adiciona opcoes de linha de comando."""
    parser.addoption(
        "--device-id",
        action="store",
        default=None,
        help="ID do dispositivo (UDID) para rodar os testes"
    )
    parser.addoption(
        "--appium-port",
        action="store",
        default=4723,
        type=int,
        help="Porta do servidor Appium (default: 4723)"
    )


# --- Ordem dos testes (dependencias de dados) ---
# Troca precisa de venda IMEDIATAMENTE antes para pegar a nota certa
# A primeira nota da lista eh sempre a mais recente
# Pedido precisa ser consultado/finalizado logo apos criacao
ORDEM_TESTES = [
    # 1. Login primeiro
    "test_login_sucesso",
    "test_login_falha_senha_invalida",       # test_login_invalido.py
    "test_login_empresa_invalida_nao_entra", # test_login_invalido.py
    # 2. Venda Consumidor -> Troca Consumidor (em sequencia)
    "test_venda_consumidor_sucesso",
    "test_troca_consumidor_sucesso",
    # 3. Venda Cliente -> Troca Cliente (em sequencia)
    "test_venda_cliente_sucesso",
    "test_troca_cliente_sucesso",
    # 4. Pedido Consumidor -> Consulta/Finaliza (em sequencia)
    "test_pedido_venda_consumidor_sucesso",
    "test_consulta_pedido_consumidor_sucesso",
    # 5. Pedido Cliente -> Consulta/Finaliza (em sequencia)
    "test_pedido_venda_cliente_sucesso",
    "test_consulta_pedido_cliente_sucesso",
    # 6. Venda Futura Retirada Loja
    "test_venda_futura_sucesso",
    # 7. Venda Futura Domicilio
    "test_venda_futura_domicilio_sucesso",
    # 8. Consulta de Documentos Fiscais
    "test_consulta_documentos_sucesso",
]


def pytest_collection_modifyitems(session, config, items):
    """
    Hook para ordenar os testes baseado na lista ORDEM_TESTES.
    Testes nao listados rodam por ultimo na ordem original.

    IMPORTANTE: Se E2E_ORDER_MODE=true (modo E2E Full do dashboard),
    mantém a ordem original dos arquivos passados via linha de comando.
    """
    # Verifica se está em modo E2E Full (ordem via JSON)
    e2e_order_mode = os.getenv("E2E_ORDER_MODE", "false").lower() == "true"

    if not e2e_order_mode:
        # Modo normal: ordena pela ORDEM_TESTES; itens fora da lista vão pro final
        def obter_ordem(item):
            nome = item.name
            try:
                return ORDEM_TESTES.index(nome)
            except ValueError:
                return len(ORDEM_TESTES) + 1

        items.sort(key=obter_ordem)
    else:
        # Modo E2E Full: avisa se algum teste esperado não foi coletado
        nomes_coletados = {item.name for item in items}
        for nome in ORDEM_TESTES:
            if nome not in nomes_coletados:
                logger.warning(f"[AVISO] '{nome}' em ORDEM_TESTES mas não coletado!")

    # Log da ordem final (lista apenas o que vai rodar)
    logger.info("=" * 50)
    if e2e_order_mode:
        logger.info("ORDEM DE EXECUCAO DOS TESTES (Modo E2E Full - via JSON):")
    else:
        logger.info("ORDEM DE EXECUCAO DOS TESTES:")
    for i, item in enumerate(items, 1):
        logger.info(f"  {i}. {item.name}")
    logger.info("=" * 50)


# --- Hooks pytest ---
def pytest_configure(config):
    """Configurações iniciais do pytest."""
    # Cria diretórios necessários
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Cria arquivo de ambiente para o Allure
    _criar_ambiente_allure(config)


def _criar_ambiente_allure(config):
    """Cria arquivo environment.properties para o Allure com dados completos do device."""
    try:
        import platform

        # Obtém diretório do Allure (usa --alluredir se especificado, senão padrão)
        allure_dir = config.getoption("--alluredir", default=None)
        if allure_dir:
            allure_results_path = Path(allure_dir)
        else:
            allure_results_path = ALLURE_RESULTS_DIR

        # Garante que o diretório existe
        allure_results_path.mkdir(parents=True, exist_ok=True)

        # Obtém informações do dispositivo
        device_id = config.getoption("--device-id", default=None)
        appium_port = config.getoption("--appium-port", default=4723)

        # Obtém informações detalhadas do device via ADB
        device_info = _obter_info_device_adb(device_id)

        # Monta conteúdo do environment.properties com seções organizadas
        linhas = []

        # === SISTEMA ===
        linhas.append("Sistema_Operacional=" + platform.system())
        linhas.append("Python=" + platform.python_version())
        linhas.append("Servidor_Appium=http://127.0.0.1:" + str(appium_port))

        # === EXECUCAO ===
        linhas.append("Data_Execucao=" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        linhas.append("Ambiente=Local")

        # === APLICATIVO ===
        linhas.append("App_Package=" + (APP_PACKAGE or "N/A"))

        # === DISPOSITIVO ===
        linhas.append("Device_ID=" + (device_id or 'auto-detectar'))
        linhas.append("Modelo=" + device_info.get('model', 'N/A'))
        linhas.append("Fabricante=" + device_info.get('manufacturer', 'N/A'))
        linhas.append("Brand=" + device_info.get('brand', 'N/A'))
        linhas.append("Android=" + device_info.get('android_version', 'N/A'))
        linhas.append("API_Level=" + device_info.get('api_level', 'N/A'))
        linhas.append("Security_Patch=" + device_info.get('security_patch', 'N/A'))
        linhas.append("Build_ID=" + device_info.get('build_id', 'N/A'))

        # === HARDWARE ===
        linhas.append("Arquitetura_CPU=" + device_info.get('cpu_abi', 'N/A'))
        linhas.append("Resolucao_Tela=" + device_info.get('screen_size', 'N/A'))
        linhas.append("Densidade_Tela=" + device_info.get('screen_density', 'N/A'))
        linhas.append("RAM_Total=" + device_info.get('ram_total', 'N/A'))
        linhas.append("Serial=" + device_info.get('serial', 'N/A'))

        # Escreve arquivo environment.properties (sem comentários - Allure não suporta)
        env_file = allure_results_path / "environment.properties"
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))

        logger.info(f"Environment Allure criado em: {env_file}")

        # Escreve arquivo categories.json para categorizar falhas
        categories = [
            {
                "name": "Falhas de Elemento",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*nao encontrado.*|.*TimeoutException.*|.*NoSuchElementException.*"
            },
            {
                "name": "Falhas de Assertiva",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*AssertionError.*|.*assert.*"
            },
            {
                "name": "Falhas de Conexao",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*Connection.*|.*WebDriverException.*"
            },
            {
                "name": "Testes Ignorados",
                "matchedStatuses": ["skipped"]
            }
        ]
        categories_file = allure_results_path / "categories.json"
        with open(categories_file, "w", encoding="utf-8") as f:
            json.dump(categories, f, indent=2)

    except Exception as e:
        logger.warning(f"Erro ao criar ambiente Allure: {e}")
        import traceback
        logger.warning(traceback.format_exc())


def _obter_nome_device(driver) -> str:
    """Obtém nome do device a partir do driver."""
    try:
        caps = driver.capabilities
        # Tenta obter modelo do dispositivo
        device_name = caps.get('deviceModel') or caps.get('deviceName') or caps.get('udid') or 'device'
        # Remove caracteres especiais
        return device_name.replace(' ', '_').replace(':', '_').replace('/', '_')
    except:
        return 'device'




# ============================================================================
# CAPTURA DE LOGS PARA HTML REPORT
# ============================================================================
# Lista global para armazenar logs de cada teste
_current_test_logs = []


class HTMLLogHandler(logging.Handler):
    """Handler que captura logs para o relatório HTML."""
    def emit(self, record):
        try:
            msg = self.format(record)
            _current_test_logs.append(msg)
        except:
            pass


# Handler global para HTML
_html_handler = HTMLLogHandler()
_html_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S'))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """Antes do teste, limpa logs e adiciona handler."""
    global _current_test_logs
    _current_test_logs = []
    logger.addHandler(_html_handler)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Durante o teste, captura todos os logs."""
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """Após o teste, remove handler e salva logs."""
    yield
    logger.removeHandler(_html_handler)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para:
    1. Adicionar logs capturados ao relatório HTML
    2. Capturar screenshots e page source em falhas
    """
    outcome = yield
    report = outcome.get_result()

    # ===== ADICIONA LOGS AO HTML E ALLURE =====
    if report.when == "call" and _current_test_logs:
        # Adiciona logs capturados como seção no report
        logs_text = "\n".join(_current_test_logs)
        if hasattr(report, 'sections'):
            report.sections.append(("Captured Logs", logs_text))
        else:
            report.sections = [("Captured Logs", logs_text)]

        # Adiciona logs ao Allure como anexo de texto
        allure.attach(
            logs_text,
            name="Log Completo do Teste",
            attachment_type=allure.attachment_type.TEXT
        )

    # ===== CAPTURA DE SCREENSHOTS E PAGE SOURCE EM FALHAS =====
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("driver_logado")
        if driver:
            try:
                # Obtém nome do device
                device_name = _obter_nome_device(driver)

                # Screenshot com nome do device
                screenshot_name = f"FALHA_{device_name}_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = SCREENSHOTS_DIR / screenshot_name
                driver.get_screenshot_as_file(str(screenshot_path))

                allure.attach.file(
                    str(screenshot_path),
                    name=f"Screenshot da Falha ({device_name})",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.error(f"Screenshot salvo: {screenshot_path}")

                # Page Source (XML da tela)
                try:
                    page_source = driver.page_source
                    allure.attach(
                        page_source,
                        name="Page Source (XML)",
                        attachment_type=allure.attachment_type.XML
                    )
                except:
                    pass

            except Exception as e:
                logger.warning(f"Falha ao capturar screenshot: {e}")


def pytest_runtest_logreport(report):
    """
    Hook para exibir resultado claro de cada teste ao final.
    Mostra PASSOU ✅ ou FALHOU ❌ com contador.
    """
    # Só processa o resultado final (call phase)
    if report.when == "call":
        nome_teste = report.nodeid.split("::")[-1] if "::" in report.nodeid else report.nodeid

        if report.passed:
            logger.info("")
            logger.info("=" * 50)
            # Marcador PASSED incluído na mensagem para evitar contagem dupla
            logger.info(f"✅ TESTE APROVADO: {nome_teste} [PASSED]")
            logger.info("=" * 50)
            logger.info("")
        elif report.failed:
            logger.error("")
            logger.error("=" * 50)
            # Marcador FAILED incluído na mensagem
            logger.error(f"❌ TESTE FALHOU: {nome_teste} [FAILED]")
            if report.longrepr:
                # Mostra resumo do erro
                erro_resumo = str(report.longrepr).split('\n')[-1] if '\n' in str(report.longrepr) else str(report.longrepr)
                logger.error(f"Erro: {erro_resumo}")
            logger.error("=" * 50)
            logger.error("")
        elif report.skipped:
            logger.warning("")
            logger.warning("=" * 50)
            logger.warning(f"⏭️  TESTE PULADO: {nome_teste} [SKIPPED]")
            logger.warning("=" * 50)
            logger.warning("")


# --- Fixtures ---
@pytest.fixture(scope="session", autouse=True)
def configurar_modo_log():
    """
    Configura o modo de logging baseado em DEBUG_MODE.
    Também filtra logs de bibliotecas externas no modo normal.
    """
    configurar_logger_modo(DEBUG_MODE)

    # Se NÃO estiver em modo DEBUG, suprime logs de bibliotecas externas
    if not DEBUG_MODE:
        # Lista de bibliotecas para suprimir (só mostra WARNING ou superior)
        bibliotecas_externas = [
            'selenium.webdriver',
            'urllib3',
            'selenium',
            'appium',
            'asyncio',
            'urllib3.connectionpool',
            'selenium.webdriver.remote.remote_connection',
        ]

        for lib in bibliotecas_externas:
            lib_logger = logging.getLogger(lib)
            lib_logger.setLevel(logging.WARNING)  # Só mostra WARNING e ERROR

    yield


def _criar_driver_appium(request, limpar_dados: bool):
    """Cria driver Appium com logging e tags Allure. Usado por driver e driver_limpo."""
    device_id = request.config.getoption("--device-id")
    appium_port = request.config.getoption("--appium-port")

    logger.info("=" * 50)
    logger.info(f"INICIANDO TESTE: {request.node.name}")
    logger.info(f"Dispositivo SOLICITADO: {device_id or 'auto-detectar'}")
    logger.info(f"Porta Appium: {appium_port}")
    logger.info(f"Limpar dados do app: {limpar_dados}")
    logger.info("=" * 50)

    appium_url = f"http://127.0.0.1:{appium_port}"
    options = get_appium_options(limpar_dados_app=limpar_dados, device_id=device_id)

    logger.info(f"[DEBUG] UDID nas capabilities: {options.get_capability('udid')}")
    logger.info(f"[DEBUG] App package: {options.app_package}")

    drv = webdriver.Remote(command_executor=appium_url, options=options)

    try:
        session_caps = drv.capabilities
        device_real = session_caps.get('udid') or session_caps.get('deviceUDID') or session_caps.get('deviceName')
        device_model = session_caps.get('deviceModel') or device_real or 'Desconhecido'
        logger.info(f"[DEBUG] Device REAL conectado: {device_real}")
        logger.info(f"[DEBUG] Modelo: {device_model}")
        allure.dynamic.parameter("device_id", device_real)
        allure.dynamic.parameter("device_model", device_model)
        allure.dynamic.tag(f"device:{device_model}")
        if limpar_dados:
            allure.dynamic.tag("app-limpo")
    except Exception as e:
        logger.warning(f"Erro ao obter info do device: {e}")

    return drv


@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture principal - Cria e gerencia o driver Appium.
    Suporta multiplos dispositivos via parametros de linha de comando.

    Uso:
        def test_exemplo(driver):
            driver.find_element(...)

    Linha de comando:
        pytest --device-id=XXXXX --appium-port=4723
    """
    param = getattr(request, "param", None)
    limpar_dados = param.get("limpar_dados", False) if isinstance(param, dict) else False

    drv = _criar_driver_appium(request, limpar_dados)
    yield drv
    logger.info("Encerrando driver...")
    drv.quit()


@pytest.fixture(scope="function")
def driver_logado(driver):
    """
    Fixture que garante que o usuario esta logado.

    Uso:
        def test_venda(driver_logado):
            # Ja esta logado, pode comecar o teste
    """
    login_page = LoginPage(driver)
    home_page = HomePage(driver)

    login_page.garantir_login(
        ip=test_data.SERVER_IP,
        porta=test_data.SERVER_PORT,
        empresa=test_data.COMPANY,
        usuario=test_data.USER,
        senha=test_data.PASSWORD
    )

    assert home_page.tela_inicial_exibida(timeout=30), "Falha ao fazer login"
    logger.info("Usuario logado com sucesso.")
    return driver


@pytest.fixture(scope="function")
def driver_limpo(request):
    """
    Fixture para testes negativos de login.
    Limpa dados do app (no_reset=False) para garantir tela de login limpa,
    eliminando sessoes salvas pelo botao 'Manter Conectado'.
    """
    drv = _criar_driver_appium(request, limpar_dados=True)
    yield drv
    logger.info("Encerrando driver (app limpo)...")
    drv.quit()


@pytest.fixture
def pagina_login(driver):
    """Fixture para LoginPage."""
    return LoginPage(driver)


@pytest.fixture
def pagina_inicial(driver):
    """Fixture para HomePage."""
    return HomePage(driver)
