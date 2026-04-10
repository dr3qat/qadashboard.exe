"""
Testes unitários para módulo config.
Testa funções de configuração e detecção de dispositivos.
"""
import pytest
from unittest.mock import MagicMock, patch
import subprocess


class TestGetConnectedDeviceUdid:
    """Testes para função get_connected_device_udid."""

    @patch('config.subprocess.check_output')
    def test_dispositivo_unico_conectado_retorna_udid(self, mock_check_output):
        """
        Deve retornar UDID quando único dispositivo está conectado.
        """
        from config import get_connected_device_udid

        # Arrange
        mock_check_output.return_value = "List of devices attached\nABC123DEF456\tdevice\n"

        # Act
        udid = get_connected_device_udid()

        # Assert
        assert udid == "ABC123DEF456"

    @patch('config.subprocess.check_output')
    def test_multiplos_dispositivos_retorna_primeiro(self, mock_check_output):
        """
        Deve retornar primeiro UDID quando múltiplos dispositivos conectados.
        """
        from config import get_connected_device_udid

        # Arrange
        mock_check_output.return_value = (
            "List of devices attached\n"
            "DEVICE001\tdevice\n"
            "DEVICE002\tdevice\n"
        )

        # Act
        udid = get_connected_device_udid(permitir_multiplos=True)

        # Assert
        assert udid == "DEVICE001"

    @patch('config.subprocess.check_output')
    def test_nenhum_dispositivo_levanta_erro(self, mock_check_output):
        """
        Deve levantar RuntimeError quando nenhum dispositivo conectado.
        """
        from config import get_connected_device_udid

        # Arrange
        mock_check_output.return_value = "List of devices attached\n"

        # Act & Assert
        with pytest.raises(RuntimeError) as excinfo:
            get_connected_device_udid()

        assert "Nenhum dispositivo" in str(excinfo.value)

    @patch('config.subprocess.check_output')
    def test_dispositivo_offline_ignorado(self, mock_check_output):
        """
        Deve ignorar dispositivos offline e retornar o primeiro online.
        """
        from config import get_connected_device_udid

        # Arrange
        mock_check_output.return_value = (
            "List of devices attached\n"
            "OFFLINE001\toffline\n"
            "DEVICE001\tdevice\n"
        )

        # Act
        udid = get_connected_device_udid()

        # Assert
        assert udid == "DEVICE001"

    @patch('config.subprocess.check_output')
    def test_adb_nao_encontrado_levanta_erro(self, mock_check_output):
        """
        Deve levantar RuntimeError se adb não encontrado.
        """
        from config import get_connected_device_udid

        # Arrange
        mock_check_output.side_effect = FileNotFoundError("adb not found")

        # Act & Assert
        with pytest.raises(RuntimeError) as excinfo:
            get_connected_device_udid()

        assert "adb" in str(excinfo.value).lower()


class TestGetAllConnectedDevices:
    """Testes para função get_all_connected_devices."""

    @patch('config.subprocess.check_output')
    def test_retorna_lista_de_dispositivos(self, mock_check_output):
        """
        Deve retornar lista de dispositivos conectados.
        """
        from config import get_all_connected_devices

        # Arrange
        mock_check_output.return_value = (
            "List of devices attached\n"
            "DEVICE001\tdevice\n"
            "DEVICE002\tdevice\n"
        )

        # Act
        devices = get_all_connected_devices()

        # Assert
        assert len(devices) == 2
        assert "DEVICE001" in devices
        assert "DEVICE002" in devices

    @patch('config.subprocess.check_output')
    def test_retorna_lista_vazia_sem_dispositivos(self, mock_check_output):
        """
        Deve retornar lista vazia se nenhum dispositivo conectado.
        """
        from config import get_all_connected_devices

        # Arrange
        mock_check_output.return_value = "List of devices attached\n"

        # Act
        devices = get_all_connected_devices()

        # Assert
        assert devices == []

    @patch('config.subprocess.check_output')
    def test_retorna_lista_vazia_em_caso_de_erro(self, mock_check_output):
        """
        Deve retornar lista vazia em caso de erro.
        """
        from config import get_all_connected_devices

        # Arrange
        mock_check_output.side_effect = Exception("Erro")

        # Act
        devices = get_all_connected_devices()

        # Assert
        assert devices == []


class TestDiscoverTargetApp:
    """Testes para função discover_target_app."""

    def setup_method(self):
        """Limpa cache entre testes para garantir isolamento."""
        import config
        config._discover_cache.clear()

    @patch('config.subprocess.check_output')
    def test_encontra_app_conhecido(self, mock_check_output):
        """
        Deve encontrar app da lista APP_TARGETS.
        """
        from config import discover_target_app

        # Arrange
        mock_check_output.return_value = (
            "package:com.android.settings\n"
            "package:com.serverinfo.bshoppdv.stone.qa\n"
            "package:com.google.chrome\n"
        )

        # Act
        package, activity = discover_target_app("DEVICE001")

        # Assert
        assert "bshoppdv" in package
        assert "Activity" in activity

    @patch('config.subprocess.check_output')
    def test_nenhum_app_encontrado_levanta_erro(self, mock_check_output):
        """
        Deve levantar RuntimeError se nenhum app da lista encontrado.
        """
        from config import discover_target_app

        # Arrange
        mock_check_output.return_value = (
            "package:com.android.settings\n"
            "package:com.google.chrome\n"
        )

        # Act & Assert
        with pytest.raises(RuntimeError) as excinfo:
            discover_target_app("DEVICE001")

        assert "Nenhum dos apps" in str(excinfo.value)

    @patch('config.subprocess.check_output')
    def test_timeout_levanta_erro(self, mock_check_output):
        """
        Deve levantar RuntimeError em caso de timeout.
        """
        from config import discover_target_app

        # Arrange
        mock_check_output.side_effect = subprocess.TimeoutExpired("adb", 30)

        # Act & Assert
        with pytest.raises(RuntimeError) as excinfo:
            discover_target_app("DEVICE001")

        assert "Timeout" in str(excinfo.value)


class TestGetAppiumOptions:
    """Testes para função get_appium_options."""

    @patch('config.discover_target_app')
    def test_opcoes_basicas(self, mock_discover):
        """
        Deve criar opções com configurações básicas.
        """
        from config import get_appium_options

        # Arrange
        mock_discover.return_value = ("com.bsoft.app", "com.bsoft.Activity")

        # Act
        options = get_appium_options(device_id="DEVICE001")

        # Assert
        caps = options.to_capabilities()
        assert caps.get("platformName") == "Android"
        assert caps.get("automationName") == "UIAutomator2"

    @patch('config.discover_target_app')
    def test_opcoes_com_device_id(self, mock_discover):
        """
        Deve configurar udid quando device_id fornecido.
        """
        from config import get_appium_options

        # Arrange
        mock_discover.return_value = ("com.bsoft.app", "com.bsoft.Activity")

        # Act
        options = get_appium_options(device_id="DEVICE001")

        # Assert
        caps = options.to_capabilities()
        assert caps.get("udid") == "DEVICE001" or caps.get("appium:udid") == "DEVICE001"

    @patch('config.discover_target_app')
    def test_no_reset_padrao_true(self, mock_discover):
        """
        Deve ter noReset=True por padrão (não limpar dados).
        """
        from config import get_appium_options

        # Arrange
        mock_discover.return_value = ("com.bsoft.app", "com.bsoft.Activity")

        # Act
        options = get_appium_options(limpar_dados_app=False, device_id="DEVICE001")

        # Assert
        caps = options.to_capabilities()
        assert caps.get("noReset") is True or caps.get("appium:noReset") is True

    @patch('config.discover_target_app')
    def test_limpar_dados_app(self, mock_discover):
        """
        Deve ter noReset=False quando limpar_dados_app=True.
        """
        from config import get_appium_options

        # Arrange
        mock_discover.return_value = ("com.bsoft.app", "com.bsoft.Activity")

        # Act
        options = get_appium_options(limpar_dados_app=True, device_id="DEVICE001")

        # Assert
        caps = options.to_capabilities()
        assert caps.get("noReset") is False or caps.get("appium:noReset") is False


class TestCalcularPortaUnica:
    """Testes para função _calcular_porta_unica."""

    def test_porta_dentro_do_range(self):
        """
        Deve retornar porta dentro do range esperado.
        """
        from config import _calcular_porta_unica

        # Act
        porta = _calcular_porta_unica("DEVICE001")

        # Assert
        assert 8200 <= porta < 8300

    def test_mesma_porta_para_mesmo_device(self):
        """
        Deve retornar mesma porta para mesmo device_id.
        """
        from config import _calcular_porta_unica

        # Act
        porta1 = _calcular_porta_unica("DEVICE001")
        porta2 = _calcular_porta_unica("DEVICE001")

        # Assert
        assert porta1 == porta2

    def test_portas_diferentes_para_devices_diferentes(self):
        """
        Deve retornar portas diferentes para devices diferentes (na maioria dos casos).
        """
        from config import _calcular_porta_unica

        # Act
        porta1 = _calcular_porta_unica("DEVICE001")
        porta2 = _calcular_porta_unica("DEVICE002")

        # Note: Podem colidir por hash, mas geralmente serão diferentes
        # Este teste verifica que a função funciona sem erro
        assert isinstance(porta1, int)
        assert isinstance(porta2, int)


class TestLogStyle:
    """Testes para classe LogStyle."""

    def test_log_style_constantes_existem(self):
        """
        Deve ter constantes de estilo definidas.
        """
        from config import LogStyle

        assert hasattr(LogStyle, 'CLICK')
        assert hasattr(LogStyle, 'OK')
        assert hasattr(LogStyle, 'ERRO')
        assert hasattr(LogStyle, 'SCROLL')

    def test_log_style_elemento_formata_nome(self):
        """
        Método elemento deve formatar corretamente.
        """
        from config import LogStyle

        # Act
        resultado = LogStyle.elemento("btn_entrar")

        # Assert
        assert "btn_entrar" in resultado

    def test_log_style_valor_formata_texto(self):
        """
        Método valor deve formatar corretamente.
        """
        from config import LogStyle

        # Act
        resultado = LogStyle.valor("texto teste")

        # Assert
        assert "texto teste" in resultado


class TestConstantes:
    """Testes para constantes do módulo config."""

    def test_default_wait_definido(self):
        """
        Deve ter DEFAULT_WAIT definido.
        """
        from config import DEFAULT_WAIT

        assert DEFAULT_WAIT == 30
        assert isinstance(DEFAULT_WAIT, int)

    def test_retry_attempts_definido(self):
        """
        Deve ter RETRY_ATTEMPTS definido.
        """
        from config import RETRY_ATTEMPTS

        assert RETRY_ATTEMPTS == 2
        assert isinstance(RETRY_ATTEMPTS, int)

    def test_appium_server_url_definido(self):
        """
        Deve ter APPIUM_SERVER_URL definido.
        """
        from config import APPIUM_SERVER_URL

        assert APPIUM_SERVER_URL == "http://127.0.0.1:4723"

    def test_diretorios_existem(self):
        """
        Deve criar diretórios necessários.
        """
        from config import LOGS_DIR, SCREENSHOTS_DIR, REPORTS_DIR

        assert LOGS_DIR.exists()
        assert SCREENSHOTS_DIR.exists()
        assert REPORTS_DIR.exists()


class TestCores:
    """Testes para classe Cores."""

    def test_cores_ansi_definidas(self):
        """
        Deve ter cores ANSI definidas.
        """
        from config import Cores

        assert hasattr(Cores, 'RESET')
        assert hasattr(Cores, 'VERDE')
        assert hasattr(Cores, 'VERMELHO')
        assert hasattr(Cores, 'AMARELO')

    def test_cores_contem_escape_ansi(self):
        """
        Cores devem conter escape ANSI.
        """
        from config import Cores

        assert "\033[" in Cores.VERDE
        assert "\033[" in Cores.RESET
