"""
Testes unitários para BasePage.
Testa métodos utilitários sem necessidade de driver real.
"""
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


class TestBasePageIdCompleto:
    """Testes para o método _id_completo."""

    @patch('pages.base_page.logger')
    def test_id_completo_com_package_existente_retorna_sem_modificacao(self, mock_logger):
        """
        Quando ID já contém ':id/', deve retornar sem modificação.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.capabilities = {"appPackage": "com.bsoft.app"}

        page = BasePage(mock_driver)
        page._app_package = "com.bsoft.app"

        # Act
        resultado = page._id_completo("com.outro.app:id/btn_teste")

        # Assert
        assert resultado == "com.outro.app:id/btn_teste"

    @patch('pages.base_page.logger')
    def test_id_completo_adiciona_package_quando_parcial(self, mock_logger):
        """
        Quando ID é parcial, deve adicionar package do app.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.capabilities = {"appPackage": "com.serverinfo.bshoppdv"}

        page = BasePage(mock_driver)
        page._app_package = "com.serverinfo.bshoppdv"

        # Act
        resultado = page._id_completo("btn_entrar")

        # Assert
        assert resultado == "com.serverinfo.bshoppdv:id/btn_entrar"

    @patch('pages.base_page.logger')
    def test_id_completo_sem_package_retorna_id_original(self, mock_logger):
        """
        Sem package definido, deve retornar ID original com warning.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.capabilities = {}

        page = BasePage(mock_driver)
        page._app_package = None

        # Act
        resultado = page._id_completo("btn_entrar")

        # Assert
        assert resultado == "btn_entrar"


class TestBasePageElementoRealmenteVisivel:
    """Testes para o método _elemento_realmente_visivel."""

    @patch('pages.base_page.logger')
    def test_elemento_none_retorna_false(self, mock_logger):
        """
        Elemento None deve retornar False.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        page = BasePage(mock_driver)

        # Act & Assert
        assert page._elemento_realmente_visivel(None) is False

    @patch('pages.base_page.logger')
    def test_elemento_nao_displayed_retorna_false(self, mock_logger):
        """
        Elemento não displayed deve retornar False.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = False
        mock_elemento.is_enabled.return_value = True

        page = BasePage(mock_driver)

        # Act & Assert
        assert page._elemento_realmente_visivel(mock_elemento) is False

    @patch('pages.base_page.logger')
    def test_elemento_nao_enabled_retorna_false(self, mock_logger):
        """
        Elemento não enabled deve retornar False.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = True
        mock_elemento.is_enabled.return_value = False

        page = BasePage(mock_driver)

        # Act & Assert
        assert page._elemento_realmente_visivel(mock_elemento) is False

    @patch('pages.base_page.logger')
    def test_elemento_tamanho_zero_retorna_false(self, mock_logger):
        """
        Elemento com tamanho zero deve retornar False.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = True
        mock_elemento.is_enabled.return_value = True
        mock_elemento.size = {"width": 0, "height": 100}

        page = BasePage(mock_driver)

        # Act & Assert
        assert page._elemento_realmente_visivel(mock_elemento) is False

    @patch('pages.base_page.logger')
    def test_elemento_fora_tela_y_negativo_retorna_false(self, mock_logger):
        """
        Elemento fora da tela (Y negativo) deve retornar False.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = True
        mock_elemento.is_enabled.return_value = True
        mock_elemento.size = {"width": 100, "height": 50}
        mock_elemento.location = {"x": 100, "y": -50}

        page = BasePage(mock_driver)

        # Act & Assert
        assert page._elemento_realmente_visivel(mock_elemento) is False

    @patch('pages.base_page.logger')
    def test_elemento_fora_tela_y_maior_altura_retorna_false(self, mock_logger):
        """
        Elemento fora da tela (Y maior que altura) deve retornar False.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = True
        mock_elemento.is_enabled.return_value = True
        mock_elemento.size = {"width": 100, "height": 50}
        mock_elemento.location = {"x": 100, "y": 2000}

        page = BasePage(mock_driver)

        # Act & Assert
        assert page._elemento_realmente_visivel(mock_elemento) is False

    @patch('pages.base_page.logger')
    def test_elemento_visivel_retorna_true(self, mock_logger):
        """
        Elemento totalmente visível deve retornar True.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = True
        mock_elemento.is_enabled.return_value = True
        mock_elemento.size = {"width": 200, "height": 50}
        mock_elemento.location = {"x": 100, "y": 500}

        page = BasePage(mock_driver)

        # Act & Assert
        assert page._elemento_realmente_visivel(mock_elemento) is True

    @patch('pages.base_page.logger')
    def test_elemento_stale_exception_retorna_false(self, mock_logger):
        """
        StaleElementReferenceException deve retornar False.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.side_effect = StaleElementReferenceException("Stale")

        page = BasePage(mock_driver)

        # Act & Assert
        assert page._elemento_realmente_visivel(mock_elemento) is False


class TestBasePageAppPackage:
    """Testes para a property app_package."""

    @patch('pages.base_page.logger')
    def test_app_package_retorna_de_capabilities(self, mock_logger):
        """
        Deve retornar appPackage das capabilities.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.capabilities = {"appPackage": "com.bsoft.app"}

        page = BasePage(mock_driver)

        # Act
        resultado = page.app_package

        # Assert
        assert resultado == "com.bsoft.app"

    @patch('pages.base_page.logger')
    def test_app_package_usa_cache(self, mock_logger):
        """
        Deve cachear o package após primeira chamada.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.capabilities = {"appPackage": "com.bsoft.app"}

        page = BasePage(mock_driver)
        page._app_package = "com.cached.app"

        # Act
        resultado = page.app_package

        # Assert
        assert resultado == "com.cached.app"


class TestBasePageClicarSeExistir:
    """Testes para método clicar_se_existir."""

    @patch('pages.base_page.WebDriverWait')
    @patch('pages.base_page.logger')
    def test_clicar_se_existir_elemento_nao_encontrado_retorna_false(self, mock_logger, mock_wait):
        """
        Deve retornar False se elemento não encontrado.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.capabilities = {"appPackage": "com.bsoft.app"}

        mock_wait.return_value.until.side_effect = TimeoutException("Timeout")

        page = BasePage(mock_driver)

        # Act
        resultado = page.clicar_se_existir("btn_inexistente", tempo_espera=1)

        # Assert
        assert resultado is False

    @patch('pages.base_page.WebDriverWait')
    @patch('pages.base_page.logger')
    def test_clicar_se_existir_elemento_nao_visivel_retorna_false(self, mock_logger, mock_wait):
        """
        Deve retornar False se elemento existe mas não está visível.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.capabilities = {"appPackage": "com.bsoft.app"}
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = False

        mock_wait.return_value.until.return_value = mock_elemento

        page = BasePage(mock_driver)

        # Act
        resultado = page.clicar_se_existir("btn_invisivel", tempo_espera=1)

        # Assert
        assert resultado is False


class TestBasePageTextoExibido:
    """Testes para método texto_exibido."""

    @patch('pages.base_page.logger')
    def test_texto_exibido_retorna_true_quando_visivel(self, mock_logger):
        """
        Deve retornar True quando texto está visível.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = True
        mock_elemento.is_enabled.return_value = True
        mock_elemento.size = {"width": 100, "height": 50}
        mock_elemento.location = {"x": 100, "y": 500}

        page = BasePage(mock_driver)
        page.encontrar_por_texto = MagicMock(return_value=mock_elemento)

        # Act
        resultado = page.texto_exibido("Teste", tempo_espera=5)

        # Assert
        assert resultado is True

    @patch('pages.base_page.logger')
    def test_texto_exibido_retorna_false_quando_excecao(self, mock_logger):
        """
        Deve retornar False quando ocorre exceção.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()

        page = BasePage(mock_driver)
        page.encontrar_por_texto = MagicMock(side_effect=TimeoutException("Timeout"))

        # Act
        resultado = page.texto_exibido("Texto inexistente", tempo_espera=1)

        # Assert
        assert resultado is False


class TestBasePageElementoExiste:
    """Testes para método elemento_existe."""

    @patch('pages.base_page.logger')
    def test_elemento_existe_retorna_true_quando_visivel(self, mock_logger):
        """
        Deve retornar True quando elemento existe e está visível.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.capabilities = {"appPackage": "com.bsoft.app"}
        mock_driver.get_window_size.return_value = {"width": 1080, "height": 1920}

        mock_elemento = MagicMock()
        mock_elemento.is_displayed.return_value = True
        mock_elemento.is_enabled.return_value = True
        mock_elemento.size = {"width": 100, "height": 50}
        mock_elemento.location = {"x": 100, "y": 500}

        page = BasePage(mock_driver)
        page.encontrar_por_id = MagicMock(return_value=mock_elemento)

        # Act
        resultado = page.elemento_existe("btn_teste", tempo_espera=3)

        # Assert
        assert resultado is True

    @patch('pages.base_page.logger')
    def test_elemento_existe_retorna_false_quando_excecao(self, mock_logger):
        """
        Deve retornar False quando elemento não é encontrado.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()

        page = BasePage(mock_driver)
        page.encontrar_por_id = MagicMock(side_effect=TimeoutException("Timeout"))

        # Act
        resultado = page.elemento_existe("btn_inexistente", tempo_espera=1)

        # Assert
        assert resultado is False


class TestBasePageVoltarTela:
    """Testes para método voltar_tela."""

    @patch('pages.base_page.time')
    @patch('pages.base_page.logger')
    def test_voltar_tela_chama_driver_back(self, mock_logger, mock_time):
        """
        Deve chamar driver.back() e retornar True.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()

        page = BasePage(mock_driver)

        # Act
        resultado = page.voltar_tela()

        # Assert
        assert resultado is True
        mock_driver.back.assert_called_once()

    @patch('pages.base_page.time')
    @patch('pages.base_page.logger')
    def test_voltar_tela_com_erro_retorna_false(self, mock_logger, mock_time):
        """
        Deve retornar False quando ocorre erro.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.back.side_effect = Exception("Erro")

        page = BasePage(mock_driver)

        # Act
        resultado = page.voltar_tela()

        # Assert
        assert resultado is False


class TestBasePageFecharTeclado:
    """Testes para método fechar_teclado."""

    @patch('pages.base_page.subprocess')
    @patch('pages.base_page.time')
    @patch('pages.base_page.logger')
    def test_fechar_teclado_quando_nao_visivel_retorna_true(self, mock_logger, mock_time, mock_subprocess):
        """
        Deve retornar True se teclado não está visível.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        mock_driver.execute_script.return_value = False  # Teclado não visível

        page = BasePage(mock_driver)

        # Act
        resultado = page.fechar_teclado()

        # Assert
        assert resultado is True

    @patch('pages.base_page.subprocess')
    @patch('pages.base_page.time')
    @patch('pages.base_page.logger')
    def test_fechar_teclado_usando_hide_keyboard(self, mock_logger, mock_time, mock_subprocess):
        """
        Deve tentar usar hide_keyboard primeiro.
        """
        from pages.base_page import BasePage

        # Arrange
        mock_driver = MagicMock()
        # Primeira chamada: teclado visível, depois fecha
        mock_driver.execute_script.side_effect = [True, False]
        mock_driver.hide_keyboard.return_value = None

        page = BasePage(mock_driver)

        # Act
        resultado = page.fechar_teclado()

        # Assert
        assert resultado is True
        mock_driver.hide_keyboard.assert_called()
