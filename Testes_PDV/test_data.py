"""
Test Data - Dados de teste externalizados.
Prioridade de configuracao:
1. Variaveis de ambiente (TEST_*)
2. settings.json (se existir)
3. Valores padrao hardcoded
"""
import os
import json
from pathlib import Path
from typing import Optional, Any


# Caminho real do settings.json que foi carregado (para escrita posterior)
_settings_path: Optional[Path] = None


def _load_settings() -> dict:
    """
    Carrega configuracoes do settings.json se existir.
    Procura em locais comuns: diretorio atual, pai, ou ao lado do executavel.
    """
    global _settings_path
    possible_paths = [
        Path("settings.json"),
        Path("../settings.json"),
        Path(__file__).parent / "settings.json",
        Path(__file__).parent.parent / "settings.json",
    ]

    # Se estiver rodando como EXE, adiciona o diretorio do executavel
    if getattr(os.sys, 'frozen', False):
        exe_dir = Path(os.sys.executable).parent
        possible_paths.insert(0, exe_dir / "settings.json")

    for path in possible_paths:
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                _settings_path = path
                return data
            except (json.JSONDecodeError, IOError):
                pass

    return {}


def _get_config(key: str, env_var: str, default: Any, settings: dict) -> Any:
    """
    Obtem valor de configuracao com prioridade:
    1. Variavel de ambiente
    2. settings.json
    3. Valor padrao

    Args:
        key: Chave no settings.json
        env_var: Nome da variavel de ambiente
        default: Valor padrao
        settings: Dicionario carregado do settings.json
    """
    # Prioridade 1: Variavel de ambiente
    env_value = os.getenv(env_var)
    if env_value is not None:
        if env_value.lower() == "true":
            return True
        if env_value.lower() == "false":
            return False
        return env_value

    # Prioridade 2: settings.json
    if key in settings:
        return settings[key]

    # Prioridade 3: Valor padrao
    return default


def _load_formas_pagamento() -> list:
    """Carrega formas_pagamento.json do mesmo diretório do settings.json."""
    if not _settings_path:
        return []
    path = _settings_path.parent / "formas_pagamento.json"
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("formas", [])
    except Exception:
        return []


# Carrega settings uma vez
_settings = _load_settings()


class TestData:
    """Dados de configuracao para os testes."""

    # --- Conexao ---
    SERVER_IP = _get_config("server_ip", "TEST_SERVER_IP", "***SERVER_IP***", _settings)
    SERVER_PORT = _get_config("server_port", "TEST_SERVER_PORT", "***SERVER_PORT***", _settings)

    # --- Credenciais ---
    COMPANY = _get_config("company", "TEST_COMPANY", "382", _settings)
    USER = _get_config("user", "TEST_USER", "SERVER", _settings)
    PASSWORD = _get_config("password", "TEST_PASSWORD", "***PASSWORD***", _settings)

    # --- Dados de Venda ---
    _default_customer = "1"
    CUSTOMER_ID = _get_config("customer_id", "TEST_CUSTOMER_ID", _default_customer, _settings)

    # Cliente para Trocas
    CUSTOMER_ID_TROCA = _get_config("customer_id_troca", "TEST_CUSTOMER_ID_TROCA", _default_customer, _settings)

    # Cliente com Bônus/Cashback
    CUSTOMER_ID_BONUS = _get_config("customer_id_bonus", "TEST_CUSTOMER_ID_BONUS", _default_customer, _settings)

    # --- Produtos ---
    PRODUCT_CODE = _get_config("product_code", "TEST_PRODUCT_CODE", "123", _settings)  # Mantido para bonus

    # Produtos específicos por cenário
    PRODUCT_CODE_SALE = _get_config("product_code_sale", "TEST_PRODUCT_CODE_SALE", "123", _settings)
    PRODUCT_CODE_FUTURE_SALE = _get_config("product_code_future_sale", "TEST_PRODUCT_CODE_FUTURE_SALE", "1234", _settings)
    PRODUCT_SIZE_FUTURE = _get_config("product_size_future", "TEST_PRODUCT_SIZE_FUTURE", "38", _settings)
    PRODUCT_CODE_STOCK_1 = _get_config("product_code_stock_1", "TEST_PRODUCT_CODE_STOCK_1", "123", _settings)
    PRODUCT_CODE_STOCK_2 = _get_config("product_code_stock_2", "TEST_PRODUCT_CODE_STOCK_2", "1234", _settings)

    # Override manual de formas de pagamento (opcional)
    # Se None → auto-descoberta por tipo semântico ao rodar o teste
    # Se configurado → usa o nome exato sem descoberta (zero overhead)
    FORMA_DINHEIRO = _get_config("forma_dinheiro", "TEST_FORMA_DINHEIRO", None, _settings)
    FORMA_DEBITO   = _get_config("forma_debito",   "TEST_FORMA_DEBITO",   None, _settings)
    FORMA_CREDITO  = _get_config("forma_credito",  "TEST_FORMA_CREDITO",  None, _settings)

    # Parcelas de crédito POS descobertas dinamicamente (ex: ["A Prazo 0 + 1", "A Prazo 0 + 2"])
    PARCELAS_CREDITO = _get_config("parcelas_credito", "TEST_PARCELAS_CREDITO", [], _settings)

    # Mapa completo de formas descobertas (carregado de formas_pagamento.json)
    # Cada item: {"titulo", "subtitulo", "detalhes", "tipo_auto", "habilitado", "parcelas", "tipos_venda"}
    FORMAS_PAGAMENTO: list = _load_formas_pagamento()

    # Vale Presente
    VALE_VALUE = _get_config("vale_value", "TEST_VALE_VALUE", "1000", _settings)  # 1000 = R$ 10,00 (máscara monetária)

    # --- Timeouts ---
    DEFAULT_TIMEOUT = int(_get_config("timeout_default", "TEST_TIMEOUT", 30, _settings))
    SHORT_TIMEOUT = int(_get_config("timeout_short", "TEST_SHORT_TIMEOUT", 5, _settings))

    # --- Configurações de Impressão ---
    PRINT_CUPOM_VENDA = _get_config("print_cupom_venda", "TEST_PRINT_CUPOM_VENDA", False, _settings)
    PRINT_NFCE = _get_config("print_nfce", "TEST_PRINT_NFCE", False, _settings)
    PRINT_DANFE = _get_config("print_danfe", "TEST_PRINT_DANFE", False, _settings)
    PRINT_CUPOM_TROCA = _get_config("print_cupom_troca", "TEST_PRINT_CUPOM_TROCA", False, _settings)
    PRINT_GIFTBACK = _get_config("print_giftback", "TEST_PRINT_GIFTBACK", False, _settings)
    PRINT_DIALOG_TIMEOUT = int(_get_config("print_dialog_timeout", "TEST_PRINT_DIALOG_TIMEOUT", 20, _settings))

    @classmethod
    def reload(cls) -> None:
        """Recarrega configuracoes do settings.json."""
        global _settings
        _settings = _load_settings()

        # Conexão
        cls.SERVER_IP = _get_config("server_ip", "TEST_SERVER_IP", "***SERVER_IP***", _settings)
        cls.SERVER_PORT = _get_config("server_port", "TEST_SERVER_PORT", "***SERVER_PORT***", _settings)

        # Credenciais
        cls.COMPANY = _get_config("company", "TEST_COMPANY", "382", _settings)
        cls.USER = _get_config("user", "TEST_USER", "SERVER", _settings)
        cls.PASSWORD = _get_config("password", "TEST_PASSWORD", "***PASSWORD***", _settings)

        # Clientes
        cls.CUSTOMER_ID = _get_config("customer_id", "TEST_CUSTOMER_ID", cls._default_customer, _settings)
        cls.CUSTOMER_ID_TROCA = _get_config("customer_id_troca", "TEST_CUSTOMER_ID_TROCA", cls._default_customer, _settings)
        cls.CUSTOMER_ID_BONUS = _get_config("customer_id_bonus", "TEST_CUSTOMER_ID_BONUS", cls._default_customer, _settings)
        

        # Produtos
        cls.PRODUCT_CODE = _get_config("product_code", "TEST_PRODUCT_CODE", "123", _settings)
        cls.PRODUCT_CODE_SALE = _get_config("product_code_sale", "TEST_PRODUCT_CODE_SALE", "123", _settings)
        cls.PRODUCT_CODE_FUTURE_SALE = _get_config("product_code_future_sale", "TEST_PRODUCT_CODE_FUTURE_SALE", "1234", _settings)
        cls.PRODUCT_SIZE_FUTURE = _get_config("product_size_future", "TEST_PRODUCT_SIZE_FUTURE", "38", _settings)
        cls.PRODUCT_CODE_STOCK_1 = _get_config("product_code_stock_1", "TEST_PRODUCT_CODE_STOCK_1", "123", _settings)
        cls.PRODUCT_CODE_STOCK_2 = _get_config("product_code_stock_2", "TEST_PRODUCT_CODE_STOCK_2", "1234", _settings)
        cls.VALE_VALUE = _get_config("vale_value", "TEST_VALE_VALUE", "1000", _settings)  # 1000 = R$ 10,00

        # Formas de pagamento (override manual)
        cls.FORMA_DINHEIRO = _get_config("forma_dinheiro", "TEST_FORMA_DINHEIRO", None, _settings)
        cls.FORMA_DEBITO   = _get_config("forma_debito",   "TEST_FORMA_DEBITO",   None, _settings)
        cls.FORMA_CREDITO  = _get_config("forma_credito",  "TEST_FORMA_CREDITO",  None, _settings)
        cls.PARCELAS_CREDITO = _get_config("parcelas_credito", "TEST_PARCELAS_CREDITO", [], _settings)

        # Timeouts
        cls.DEFAULT_TIMEOUT = int(_get_config("timeout_default", "TEST_TIMEOUT", 30, _settings))
        cls.SHORT_TIMEOUT = int(_get_config("timeout_short", "TEST_SHORT_TIMEOUT", 5, _settings))

        # Impressão
        cls.PRINT_CUPOM_VENDA = _get_config("print_cupom_venda", "TEST_PRINT_CUPOM_VENDA", False, _settings)
        cls.PRINT_NFCE = _get_config("print_nfce", "TEST_PRINT_NFCE", False, _settings)
        cls.PRINT_DANFE = _get_config("print_danfe", "TEST_PRINT_DANFE", False, _settings)
        cls.PRINT_CUPOM_TROCA = _get_config("print_cupom_troca", "TEST_PRINT_CUPOM_TROCA", False, _settings)
        cls.PRINT_GIFTBACK = _get_config("print_giftback", "TEST_PRINT_GIFTBACK", False, _settings)
        cls.PRINT_DIALOG_TIMEOUT = int(_get_config("print_dialog_timeout", "TEST_PRINT_DIALOG_TIMEOUT", 20, _settings))

    @classmethod
    def atualizar_formas_descobertas(
        cls,
        forma_dinheiro: Optional[str] = None,
        forma_debito: Optional[str] = None,
        forma_credito: Optional[str] = None,
        parcelas_credito: Optional[list] = None,
    ) -> None:
        """Persiste formas descobertas em settings.json sem sobrescrever campos existentes.
        Chamado automaticamente por venda_page após discovery Appium."""
        global _settings_path
        path = _settings_path
        if not path:
            return
        try:
            data: dict = {}
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            changed = False
            if forma_dinheiro and not data.get("forma_dinheiro"):
                data["forma_dinheiro"] = forma_dinheiro
                cls.FORMA_DINHEIRO = forma_dinheiro
                changed = True
            if forma_debito and not data.get("forma_debito"):
                data["forma_debito"] = forma_debito
                cls.FORMA_DEBITO = forma_debito
                changed = True
            if forma_credito and not data.get("forma_credito"):
                data["forma_credito"] = forma_credito
                cls.FORMA_CREDITO = forma_credito
                changed = True
            if parcelas_credito and not data.get("parcelas_credito"):
                data["parcelas_credito"] = parcelas_credito
                cls.PARCELAS_CREDITO = parcelas_credito
                changed = True

            if changed:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
        except Exception:
            pass  # discovery é best-effort — não quebra o teste


# Instancia global para uso nos testes
test_data = TestData()
