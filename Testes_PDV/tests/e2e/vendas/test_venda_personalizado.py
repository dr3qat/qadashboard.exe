"""Test Venda Personalizado - Venda consumidor usando Pagamento Personalizado.
Parametrizado dinamicamente a partir de formas_pagamento.json.
Cada tipo_venda habilitado gera um caso de teste independente."""
import json
import pytest
import allure
from pages.home_page import HomePage
from pages.venda_page import VendaPage
from test_data import test_data
from config import logger


def _params_personalizado():
    """Lê tipos_venda habilitados do Personalizado em formas_pagamento.json.
    Retorna lista de pytest.param(tipo_venda, parcela, id=...) para parametrize."""
    formas = test_data.FORMAS_PAGAMENTO
    if not formas:
        # Sem JSON: cai em skip
        return [pytest.param("__skip__", None, id="sem_discovery")]

    personalizado = next(
        (f for f in formas
         if f.get("tipo_auto") == "personalizado" and f.get("habilitado", True)),
        None,
    )
    if not personalizado:
        return [pytest.param("__skip__", None, id="sem_personalizado")]

    parcelas = personalizado.get("parcelas", [])
    params = []
    for tv in personalizado.get("tipos_venda", []):
        if not tv.get("habilitado", True):
            continue
        nome = tv["nome"]
        parcela = parcelas[0] if ("credito" in nome.lower() and parcelas) else None
        params.append(pytest.param(nome, parcela, id=nome.lower().replace(" ", "_")))

    return params if params else [pytest.param("__skip__", None, id="sem_tipos_habilitados")]


_PARAMS = _params_personalizado()


@allure.epic("PDV Mobile")
@allure.feature("Vendas")
@allure.story("Formas de Pagamento — Personalizado")
class TestVendaPersonalizado:

    @allure.title("Venda Consumidor — Personalizado ({tipo_venda})")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("venda", "consumidor", "personalizado", "dinamico")
    @pytest.mark.parametrize("tipo_venda,parcela", _PARAMS)
    def test_venda_consumidor_personalizado(self, driver_logado, tipo_venda, parcela):
        """Venda consumidor usando Pagamento Personalizado com tipo_venda dinâmico.
        Skip se formas_pagamento.json não foi gerado ou tipo não está habilitado."""
        if tipo_venda == "__skip__":
            pytest.skip("formas_pagamento.json não encontrado ou sem tipos_venda habilitados. "
                        "Execute o teste de discovery primeiro.")

        home  = HomePage(driver_logado)
        venda = VendaPage(driver_logado)

        with allure.step("1. Iniciar venda"):
            home.iniciar_venda()

        with allure.step("2. Selecionar vendedor"):
            home.selecionar_vendedor()

        with allure.step("3. Iniciar sem cliente (consumidor)"):
            venda.iniciar_venda_sem_cliente()

        with allure.step("4. Adicionar produto"):
            venda.adicionar_produto(test_data.PRODUCT_CODE_SALE)

        with allure.step("5. Avançar para pagamento"):
            venda.clicar_avancar()

        with allure.step(f"6. Selecionar Personalizado → {tipo_venda}"
                         + (f" → {parcela}" if parcela else "")):
            allure.dynamic.parameter("tipo_venda", tipo_venda)
            if parcela:
                allure.dynamic.parameter("parcela", parcela)
            venda.selecionar_personalizado(tipo_venda, parcela)

        with allure.step("7. Finalizar venda"):
            venda.finalizar_venda()

        with allure.step("8. Validar sucesso e concluir"):
            venda.validar_sucesso_e_concluir()

        with allure.step("9. Verificar retorno à tela inicial"):
            assert home.tela_inicial_exibida(), \
                f"Não voltou para home após venda Personalizado {tipo_venda}"

        logger.info(f"[PERSONALIZADO] {tipo_venda}"
                    + (f" / {parcela}" if parcela else "") + " OK")
