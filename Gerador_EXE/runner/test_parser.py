"""
Test Parser - Parser de saida do pytest para o QA Dashboard.
Extrai informacoes de testes em tempo real para atualizar Scoreboard.
"""
import re
from typing import Optional, Callable, Dict, List
from dataclasses import dataclass, field
from enum import Enum


class TestStatus(Enum):
    """Status possiveis de um teste."""
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class TestResult:
    """Resultado de um teste individual."""
    name: str
    status: TestStatus
    duration: Optional[float] = None
    error_message: Optional[str] = None
    file_path: Optional[str] = None


@dataclass
class TestSession:
    """Sessao de execucao de testes."""
    tests: Dict[str, TestResult] = field(default_factory=dict)
    current_test: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    total_passed: int = 0
    total_failed: int = 0
    total_skipped: int = 0
    total_errors: int = 0

    @property
    def total_tests(self) -> int:
        return self.total_passed + self.total_failed + self.total_skipped + self.total_errors

    @property
    def success_rate(self) -> float:
        total = self.total_passed + self.total_failed + self.total_errors
        if total == 0:
            return 0.0
        return (self.total_passed / total) * 100


class PytestOutputParser:
    """
    Parser para saida do pytest.
    Extrai resultados em tempo real e notifica callbacks.
    """

    # Padroes regex para pytest output
    PATTERNS = {
        # Teste individual: "test_login.py::test_login_sucesso PASSED"
        'test_result': re.compile(
            r"(?P<file>[\w/\\]+\.py)::(?P<name>test_\w+)\s+(?P<status>PASSED|FAILED|SKIPPED|ERROR)",
            re.IGNORECASE
        ),

        # Inicio de teste: "tests/test_login.py::test_login_sucesso"
        'test_start': re.compile(
            r"(?P<file>[\w/\\]+\.py)::(?P<name>test_\w+)\s*$"
        ),

        # Coleta: "collected 5 items"
        'collected': re.compile(r"collected\s+(?P<count>\d+)\s+items?"),

        # Resumo final: "= 5 passed, 2 failed, 1 skipped in 45.23s ="
        'summary': re.compile(
            r"(?:=+\s*)?(?P<passed>\d+)\s+passed"
            r"(?:,?\s*(?P<failed>\d+)\s+failed)?"
            r"(?:,?\s*(?P<skipped>\d+)\s+skipped)?"
            r"(?:,?\s*(?P<errors>\d+)\s+error)?"
            r"(?:\s+in\s+(?P<duration>[\d.]+)s?)?"
        ),

        # Erro com stack trace
        'error_line': re.compile(r"^E\s+(?P<message>.+)$", re.MULTILINE),

        # Linha de falha com assert
        'assertion': re.compile(r"AssertionError:\s*(?P<message>.+)?"),

        # Separadores de secao
        'section_start': re.compile(r"^=+\s*(.+?)\s*=+$"),
        'section_failures': re.compile(r"FAILURES|ERRORS", re.IGNORECASE),
    }

    def __init__(self):
        self.session = TestSession()
        self._callbacks: Dict[str, List[Callable]] = {
            'on_test_start': [],
            'on_test_end': [],
            'on_session_start': [],
            'on_session_end': [],
            'on_progress': [],
        }
        self._collected_count = 0
        self._in_error_section = False
        self._current_error_lines: List[str] = []

    def register_callback(self, event: str, callback: Callable):
        """
        Registra callback para eventos.

        Events:
            - on_test_start: (test_name: str)
            - on_test_end: (result: TestResult)
            - on_session_start: (total_tests: int)
            - on_session_end: (session: TestSession)
            - on_progress: (current: int, total: int)
        """
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    def _notify(self, event: str, *args):
        """Notifica todos os callbacks registrados."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(*args)
            except Exception as e:
                print(f"[PARSER] Erro em callback {event}: {e}")

    def parse_line(self, line: str) -> Optional[TestResult]:
        """
        Processa uma linha de saida do pytest.

        Args:
            line: Linha de texto do stdout.

        Returns:
            Optional[TestResult]: Resultado se um teste foi detectado.
        """
        line = line.strip()

        # Verifica coleta de testes
        match = self.PATTERNS['collected'].search(line)
        if match:
            self._collected_count = int(match.group('count'))
            self._notify('on_session_start', self._collected_count)
            return None

        # Verifica inicio de teste
        match = self.PATTERNS['test_start'].match(line)
        if match:
            test_name = match.group('name')
            self.session.current_test = test_name
            self._notify('on_test_start', test_name)
            return None

        # Verifica resultado de teste
        match = self.PATTERNS['test_result'].search(line)
        if match:
            return self._process_test_result(match)

        # Verifica resumo final
        match = self.PATTERNS['summary'].search(line)
        if match:
            self._process_summary(match)
            return None

        # Detecta secao de erros
        if self.PATTERNS['section_failures'].search(line):
            self._in_error_section = True

        # Coleta mensagens de erro
        if self._in_error_section:
            error_match = self.PATTERNS['error_line'].match(line)
            if error_match:
                self._current_error_lines.append(error_match.group('message'))

        return None

    def _process_test_result(self, match) -> TestResult:
        """Processa resultado de um teste individual."""
        file_path = match.group('file')
        test_name = match.group('name')
        status_str = match.group('status').upper()

        # Mapeia status
        status_map = {
            'PASSED': TestStatus.PASSED,
            'FAILED': TestStatus.FAILED,
            'SKIPPED': TestStatus.SKIPPED,
            'ERROR': TestStatus.ERROR,
        }
        status = status_map.get(status_str, TestStatus.ERROR)

        # Cria resultado
        result = TestResult(
            name=test_name,
            status=status,
            file_path=file_path,
            error_message='\n'.join(self._current_error_lines) if self._current_error_lines else None
        )

        # Atualiza sessao
        self.session.tests[test_name] = result
        self.session.current_test = None

        if status == TestStatus.PASSED:
            self.session.total_passed += 1
        elif status == TestStatus.FAILED:
            self.session.total_failed += 1
        elif status == TestStatus.SKIPPED:
            self.session.total_skipped += 1
        elif status == TestStatus.ERROR:
            self.session.total_errors += 1

        # Notifica
        self._notify('on_test_end', result)
        self._notify('on_progress', self.session.total_tests, self._collected_count)

        # Limpa erros acumulados
        self._current_error_lines = []
        self._in_error_section = False

        return result

    def _process_summary(self, match):
        """Processa linha de resumo final."""
        passed = int(match.group('passed') or 0)
        failed = int(match.group('failed') or 0) if match.group('failed') else 0
        skipped = int(match.group('skipped') or 0) if match.group('skipped') else 0
        errors = int(match.group('errors') or 0) if match.group('errors') else 0

        # Atualiza sessao com valores finais (pode ter perdido algum durante streaming)
        self.session.total_passed = max(self.session.total_passed, passed)
        self.session.total_failed = max(self.session.total_failed, failed)
        self.session.total_skipped = max(self.session.total_skipped, skipped)
        self.session.total_errors = max(self.session.total_errors, errors)

        # Notifica fim de sessao
        self._notify('on_session_end', self.session)

    def reset(self):
        """Reseta o parser para nova execucao."""
        self.session = TestSession()
        self._collected_count = 0
        self._in_error_section = False
        self._current_error_lines = []

    def get_session(self) -> TestSession:
        """Retorna a sessao atual."""
        return self.session


def create_scoreboard_updater(scoreboard) -> PytestOutputParser:
    """
    Cria parser configurado para atualizar um Scoreboard.

    Args:
        scoreboard: Instancia de Scoreboard (ui_components.py)

    Returns:
        PytestOutputParser: Parser configurado.
    """
    parser = PytestOutputParser()

    def on_test_end(result: TestResult):
        if result.status == TestStatus.PASSED:
            scoreboard.add_passed()
        elif result.status in (TestStatus.FAILED, TestStatus.ERROR):
            scoreboard.add_failed()
        elif result.status == TestStatus.SKIPPED:
            scoreboard.add_skipped()

    def on_session_start(total: int):
        scoreboard.reset()

    parser.register_callback('on_test_end', on_test_end)
    parser.register_callback('on_session_start', on_session_start)

    return parser


if __name__ == "__main__":
    # Teste do parser
    test_output = """
============================= test session starts ==============================
collected 5 items

tests/test_login.py::test_login_sucesso PASSED
tests/test_login.py::test_login_falha FAILED
tests/test_venda.py::test_venda_consumidor PASSED
tests/test_venda.py::test_venda_cliente SKIPPED
tests/test_troca.py::test_troca_sucesso PASSED

=========================== short test summary info ============================
FAILED tests/test_login.py::test_login_falha - AssertionError: Login failed
========================= 3 passed, 1 failed, 1 skipped in 45.23s =========================
"""

    parser = PytestOutputParser()

    # Registra callbacks de debug
    parser.register_callback('on_test_start', lambda n: print(f"[START] {n}"))
    parser.register_callback('on_test_end', lambda r: print(f"[END] {r.name}: {r.status.value}"))
    parser.register_callback('on_session_start', lambda t: print(f"[SESSION] {t} testes"))
    parser.register_callback('on_session_end', lambda s: print(f"[FIM] {s.total_passed}P {s.total_failed}F"))

    for line in test_output.split('\n'):
        parser.parse_line(line)

    session = parser.get_session()
    print(f"\nResumo: {session.total_passed} passed, {session.total_failed} failed, "
          f"{session.total_skipped} skipped ({session.success_rate:.1f}%)")
