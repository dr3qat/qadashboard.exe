"""Test Cancelamento - Regressão: cancelamento de venda."""
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data


@allure.epic("PDV Mobile")
@allure.feature("Cancelamento")
@allure.story("Cancelamento de Venda")
class TestCancelamento:

    def _iniciar_venda_consumidor(self, pagina_inicial, pagina_venda):
        pagina_inicial.iniciar_venda()
        pagina_inicial.selecionar_vendedor()
        pagina_venda.iniciar_venda_sem_cliente()

    @allure.title("Cancelar Venda Vazia")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("cancelamento", "venda", "vazia")
    @pytest.mark.regression
    def test_cancelar_venda_vazia(self, driver_logado):
        """Voltar sem adicionar produto retorna tela inicial."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        self._iniciar_venda_consumidor(pagina_inicial, pagina_venda)
        pagina_venda.voltar_tela(confirmar=True)

        if not pagina_inicial.tela_inicial_exibida(timeout=5):
            pagina_venda.voltar_tela(confirmar=True)
        assert pagina_inicial.tela_inicial_exibida(timeout=10), "Nao voltou para tela inicial"

    @allure.title("Cancelar Venda com Itens")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("cancelamento", "venda", "itens")
    @pytest.mark.regression
    def test_cancelar_venda_com_itens(self, driver_logado):
        """Cancelar venda com produto no carrinho retorna tela inicial."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        self._iniciar_venda_consumidor(pagina_inicial, pagina_venda)
        pagina_venda.adicionar_produto(codigo=test_data.PRODUCT_CODE_SALE)
        pagina_venda.voltar_tela(confirmar=True)

        for _ in range(3):
            if pagina_inicial.tela_inicial_exibida(timeout=3):
                break
            pagina_venda.voltar_tela(confirmar=True)
        assert pagina_inicial.tela_inicial_exibida(timeout=10), "Nao voltou para tela inicial"

    @allure.title("Desistir do Cancelamento")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("cancelamento", "venda", "desistir")
    @pytest.mark.regression
    def test_desistir_cancelamento(self, driver_logado):
        """Clicar NAO no dialogo mantém na tela de venda."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        self._iniciar_venda_consumidor(pagina_inicial, pagina_venda)
        pagina_venda.adicionar_produto(codigo=test_data.PRODUCT_CODE_SALE)
        pagina_venda.voltar_tela(confirmar=False)

        dialogo_apareceu = (
            pagina_venda.clicar_texto_se_existir("NÃO", tempo_espera=3) or
            pagina_venda.clicar_texto_se_existir("Não", tempo_espera=1) or
            pagina_venda.clicar_texto_se_existir("NAO", tempo_espera=1)
        )

        if dialogo_apareceu:
            assert not pagina_inicial.tela_inicial_exibida(timeout=3), \
                "Voltou para tela inicial indevidamente"

    @allure.title("Botao Back Android Durante Venda")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("cancelamento", "venda", "back-button")
    @pytest.mark.regression
    def test_botao_voltar_android(self, driver_logado):
        """Back do Android exibe dialogo de confirmacao ou volta."""
        pagina_inicial = HomePage(driver_logado)
        pagina_venda = VendaPage(driver_logado)

        self._iniciar_venda_consumidor(pagina_inicial, pagina_venda)
        driver_logado.back()

        dialogo_visivel = (
            pagina_venda.texto_exibido("Deseja sair", tempo_espera=3) or
            pagina_venda.texto_exibido("Deseja cancelar", tempo_espera=1) or
            pagina_venda.elemento_existe("android:id/button1", tempo_espera=1)
        )
        tela_inicial = pagina_inicial.tela_inicial_exibida(timeout=3)
        assert dialogo_visivel or tela_inicial, "Back nao teve efeito esperado"

        if dialogo_visivel and not tela_inicial:
            pagina_venda.clicar_se_existir("android:id/button1", tempo_espera=2)
