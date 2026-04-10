"""
Config Manager - Gerenciador de configuracoes externas.
Le e escreve settings.json para configuracao do QA Dashboard.
"""
import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


@dataclass
class Settings:
    """Estrutura de configuracoes do sistema."""
    # Conexao Appium
    appium_host: str = "127.0.0.1"
    appium_port: int = 4723

    # Conexao Servidor
    server_ip: str = "***SERVER_IP***"
    server_port: str = "***SERVER_PORT***"

    # Credenciais
    company: str = "382"
    user: str = "SERVER"
    password: str = "***PASSWORD***"

    # Dados de Teste
    customer_id: str = "1"
    customer_id_troca: str = "1"  # Cliente específico para trocas

    # Manter product_code para compatibilidade com test_bonus.py
    product_code: str = "123"

    # Produtos específicos por cenário
    product_code_sale: str = "123"           # Vendas normais
    product_code_future_sale: str = "1234"   # Vendas futuras
    product_size_future: str = "38"          # Tamanho para vendas futuras
    product_code_stock_1: str = "123"        # Produto 1 estoque
    product_code_stock_2: str = "1234"       # Produto 2 estoque

    # Timeouts
    timeout_default: int = 30
    timeout_short: int = 5

    # Modo de Exibicao
    modo_debug: bool = False

    # Caminhos (preenchidos automaticamente)
    qa_dev_path: str = ""
    last_report_path: str = ""


class ConfigManager:
    """Gerenciador de configuracoes com persistencia em JSON."""

    DEFAULT_FILENAME = "settings.json"

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Inicializa o gerenciador de configuracoes.

        Args:
            config_dir: Diretorio onde o settings.json sera salvo.
                       Se None, usa o diretorio do executavel/script.
        """
        if config_dir is None:
            # Tenta encontrar o diretorio mais apropriado
            if getattr(os.sys, 'frozen', False):
                # Rodando como EXE
                config_dir = Path(os.sys.executable).parent
            else:
                # Rodando como script
                config_dir = Path(__file__).parent.parent

        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / self.DEFAULT_FILENAME
        self._settings: Optional[Settings] = None

    @property
    def settings(self) -> Settings:
        """Retorna as configuracoes atuais, carregando se necessario."""
        if self._settings is None:
            self._settings = self.load()
        return self._settings

    def load(self) -> Settings:
        """
        Carrega configuracoes do arquivo JSON.
        Se o arquivo nao existir, cria com valores padrao.

        Returns:
            Settings: Objeto com as configuracoes.
        """
        if not self.config_file.exists():
            # Primeira execucao - cria arquivo com defaults
            default_settings = Settings()
            self.save(default_settings)
            return default_settings

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Cria Settings com os valores do arquivo
            # Campos ausentes usam o valor padrao do dataclass
            return Settings(**{k: v for k, v in data.items() if hasattr(Settings, k)})

        except (json.JSONDecodeError, TypeError) as e:
            print(f"[AVISO] Erro ao ler settings.json: {e}")
            print("[INFO] Usando configuracoes padrao.")
            return Settings()

    def save(self, settings: Optional[Settings] = None) -> bool:
        """
        Salva configuracoes no arquivo JSON.

        Args:
            settings: Objeto Settings a salvar. Se None, salva o atual.

        Returns:
            bool: True se salvou com sucesso, False caso contrario.
        """
        if settings is None:
            settings = self._settings or Settings()

        try:
            # Garante que o diretorio existe
            self.config_dir.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(settings), f, indent=2, ensure_ascii=False)

            self._settings = settings
            return True

        except Exception as e:
            print(f"[ERRO] Falha ao salvar settings.json: {e}")
            return False

    def update(self, **kwargs) -> bool:
        """
        Atualiza campos especificos das configuracoes.

        Args:
            **kwargs: Campos a atualizar (ex: server_ip="192.168.1.1")

        Returns:
            bool: True se atualizou com sucesso.
        """
        current = self.settings

        for key, value in kwargs.items():
            if hasattr(current, key):
                setattr(current, key, value)
            else:
                print(f"[AVISO] Campo desconhecido ignorado: {key}")

        return self.save(current)

    def reset_to_defaults(self) -> bool:
        """
        Reseta todas as configuracoes para os valores padrao.

        Returns:
            bool: True se resetou com sucesso.
        """
        default_settings = Settings()
        return self.save(default_settings)

    def get_display_dict(self) -> dict:
        """
        Retorna dicionario formatado para exibicao na UI.
        Oculta campos sensiveis como senha.

        Returns:
            dict: Configuracoes formatadas para exibicao.
        """
        data = asdict(self.settings)
        # Mascara a senha
        if 'password' in data:
            data['password'] = '*' * len(data['password'])
        return data


# Instancia global para uso conveniente
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Retorna instancia global do ConfigManager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_settings() -> Settings:
    """Atalho para obter as configuracoes atuais."""
    return get_config_manager().settings


if __name__ == "__main__":
    # Teste basico
    manager = ConfigManager(Path("."))
    print("Configuracoes carregadas:")
    for key, value in asdict(manager.settings).items():
        print(f"  {key}: {value}")
