"""
Log Filter - Filtro inteligente de logs para o QA Dashboard.
Modo Cliente: Filtra logs HTTP/Appium verbosos.
Modo Debug: Mostra todos os logs.
"""
import re
from typing import List, Tuple, Optional
from enum import Enum


class LogMode(Enum):
    """Modos de exibicao de logs."""
    CLIENT = "client"   # Filtra logs tecnicos
    DEBUG = "debug"     # Mostra tudo


class LogLevel(Enum):
    """Niveis de log."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    SYSTEM = "SYSTEM"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


# Padroes de logs a filtrar no modo cliente
FILTER_PATTERNS = [
    # Appium/Selenium HTTP logs
    r"^(GET|POST|DELETE|PUT|PATCH)\s+http",
    r"^Finished Request$",
    r"^Remote response$",
    r"^Started\s+(GET|POST|DELETE)",
    r"^Response data:",
    r"^\s*\{.*\}\s*$",  # JSON puro
    r"^127\.0\.0\.1",   # IPs locais

    # Selenium logs
    r"selenium\.webdriver",
    r"urllib3\.connectionpool",
    r"^DEBUG:",

    # Appium internal
    r"\[Appium\]",
    r"\[UiAutomator2\]",
    r"\[ADB\]",
    r"WebSocket",
    r"socket\.io",

    # Linhas vazias ou so espacos
    r"^\s*$",
]

# Padroes importantes que nunca devem ser filtrados
IMPORTANT_PATTERNS = [
    r"(PASSED|FAILED|ERROR|SKIPPED)",
    r"\[SYSTEM\]",
    r"\[(OK|ERRO|AVISO|AGUARDE)\]",
    r"^\s*[->]",  # Linhas de progresso
    r"test_\w+",  # Nomes de testes
    r"^={3,}",    # Separadores
    r"screenshot",
]


class LogFilter:
    """
    Filtro inteligente de logs.
    Analisa cada linha e decide se deve ser exibida baseado no modo.
    """

    def __init__(self, mode: LogMode = LogMode.CLIENT):
        self.mode = mode
        self._compiled_filters = [re.compile(p, re.IGNORECASE) for p in FILTER_PATTERNS]
        self._compiled_important = [re.compile(p, re.IGNORECASE) for p in IMPORTANT_PATTERNS]

    def set_mode(self, mode: LogMode):
        """Define o modo de filtragem."""
        self.mode = mode

    def should_display(self, line: str) -> bool:
        """
        Verifica se a linha deve ser exibida.

        Args:
            line: Linha de log a verificar.

        Returns:
            bool: True se a linha deve ser exibida.
        """
        # Modo debug mostra tudo
        if self.mode == LogMode.DEBUG:
            return True

        # Linhas vazias sao filtradas
        if not line.strip():
            return False

        # Verifica se eh importante (nunca filtrar)
        for pattern in self._compiled_important:
            if pattern.search(line):
                return True

        # Verifica se deve ser filtrado
        for pattern in self._compiled_filters:
            if pattern.search(line):
                return False

        # Por padrao, mostra
        return True

    def detect_level(self, line: str) -> LogLevel:
        """
        Detecta o nivel de log da linha.

        Args:
            line: Linha de log.

        Returns:
            LogLevel: Nivel detectado.
        """
        line_upper = line.upper()

        if "PASSED" in line_upper or "[OK]" in line_upper:
            return LogLevel.PASSED
        if "FAILED" in line_upper or "ERROR" in line_upper or "[ERRO]" in line_upper:
            return LogLevel.FAILED
        if "SKIPPED" in line_upper or "[SKIP]" in line_upper:
            return LogLevel.SKIPPED
        if "[SYSTEM]" in line_upper:
            return LogLevel.SYSTEM
        if "WARNING" in line_upper or "[AVISO]" in line_upper or "[AGUARDE]" in line_upper:
            return LogLevel.WARNING
        if "INFO" in line_upper:
            return LogLevel.INFO
        if "DEBUG" in line_upper:
            return LogLevel.DEBUG

        return LogLevel.INFO

    def process_line(self, line: str) -> Tuple[bool, str, LogLevel]:
        """
        Processa uma linha de log completa.

        Args:
            line: Linha de log.

        Returns:
            Tuple[bool, str, LogLevel]: (deve_exibir, linha_formatada, nivel)
        """
        should_show = self.should_display(line)
        level = self.detect_level(line)
        formatted = self._format_line(line, level)

        return should_show, formatted, level

    def _format_line(self, line: str, level: LogLevel) -> str:
        """Formata a linha para exibicao."""
        # Remove espacos extras no final
        line = line.rstrip()

        # Adiciona quebra de linha se necessario
        if not line.endswith('\n'):
            line += '\n'

        return line

    def filter_lines(self, lines: List[str]) -> List[Tuple[str, LogLevel]]:
        """
        Filtra multiplas linhas de uma vez.

        Args:
            lines: Lista de linhas.

        Returns:
            List[Tuple[str, LogLevel]]: Lista de (linha, nivel) para linhas aceitas.
        """
        result = []
        for line in lines:
            should_show, formatted, level = self.process_line(line)
            if should_show:
                result.append((formatted, level))
        return result


class TestResultDetector:
    """
    Detecta resultados de testes nas linhas de log.
    Usado pelo Scoreboard para atualizar contadores.
    """

    # Padroes pytest
    PASSED_PATTERN = re.compile(r"(PASSED|passed|\s1\s+passed)")
    FAILED_PATTERN = re.compile(r"(FAILED|failed|ERROR|\s1\s+failed)")
    SKIPPED_PATTERN = re.compile(r"(SKIPPED|skipped|SKIP|\s1\s+skipped)")

    # Padrao de resumo final: "1 passed, 2 failed, 1 skipped"
    SUMMARY_PATTERN = re.compile(
        r"(?:=+\s*)?(\d+)\s+passed(?:,?\s*(\d+)\s+failed)?(?:,?\s*(\d+)\s+skipped)?"
    )

    @classmethod
    def detect_result(cls, line: str) -> Optional[str]:
        """
        Detecta se a linha indica um resultado de teste.

        Returns:
            Optional[str]: 'passed', 'failed', 'skipped' ou None
        """
        if cls.PASSED_PATTERN.search(line) and "test_" in line.lower():
            return 'passed'
        if cls.FAILED_PATTERN.search(line) and "test_" in line.lower():
            return 'failed'
        if cls.SKIPPED_PATTERN.search(line) and "test_" in line.lower():
            return 'skipped'
        return None

    @classmethod
    def detect_summary(cls, line: str) -> Optional[dict]:
        """
        Detecta resumo final de execucao pytest.

        Returns:
            Optional[dict]: {'passed': N, 'failed': N, 'skipped': N} ou None
        """
        match = cls.SUMMARY_PATTERN.search(line)
        if match:
            return {
                'passed': int(match.group(1) or 0),
                'failed': int(match.group(2) or 0) if match.group(2) else 0,
                'skipped': int(match.group(3) or 0) if match.group(3) else 0
            }
        return None


# Instancia global para uso conveniente
_log_filter: Optional[LogFilter] = None


def get_log_filter() -> LogFilter:
    """Retorna instancia global do LogFilter."""
    global _log_filter
    if _log_filter is None:
        _log_filter = LogFilter()
    return _log_filter


def set_log_mode(mode: LogMode):
    """Define o modo de log global."""
    get_log_filter().set_mode(mode)


if __name__ == "__main__":
    # Teste do filtro
    test_lines = [
        "POST http://127.0.0.1:4723/session",
        "[SYSTEM] Iniciando testes...",
        "test_login_sucesso PASSED",
        "GET http://localhost:4723/status",
        "-> PASSO: Clicar no botao ENTRAR",
        "[OK] Elemento encontrado",
        "DEBUG: session_id=abc123",
        "test_venda_consumidor FAILED",
        "======== 2 passed, 1 failed ========",
    ]

    filter = LogFilter(LogMode.CLIENT)
    print("=== Modo Cliente ===")
    for line in test_lines:
        show, formatted, level = filter.process_line(line)
        if show:
            print(f"[{level.value}] {formatted}", end="")

    print("\n=== Modo Debug ===")
    filter.set_mode(LogMode.DEBUG)
    for line in test_lines:
        show, formatted, level = filter.process_line(line)
        if show:
            print(f"[{level.value}] {formatted}", end="")
