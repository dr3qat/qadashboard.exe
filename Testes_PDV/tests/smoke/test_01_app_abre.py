"""Smoke 01 - App abre e responde ao driver."""
import pytest
import allure
from config import logger


@allure.epic("PDV Mobile")
@allure.feature("Smoke Tests")
@allure.story("Ambiente")
@pytest.mark.smoke
class TestSmoke01AppAbre:

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
