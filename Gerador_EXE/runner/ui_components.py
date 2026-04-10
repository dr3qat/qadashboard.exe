"""
UI Components - Componentes visuais reutilizaveis para o QA Dashboard.
Inclui: Cronometro, Scoreboard, ProgressoIndeterminado
"""
import tkinter as tk
from tkinter import ttk
import time
from typing import Callable, Optional


class Cronometro(ttk.Frame):
    """
    Widget de cronometro em tempo real.
    Exibe tempo decorrido no formato MM:SS ou HH:MM:SS.
    """

    def __init__(self, parent, font_size: int = 14, **kwargs):
        super().__init__(parent, **kwargs)

        self.start_time: Optional[float] = None
        self.running = False
        self._after_id: Optional[str] = None

        # Label principal
        self.lbl_tempo = tk.Label(
            self,
            text="00:00",
            font=('Consolas', font_size, 'bold'),
            fg="#569cd6",
            bg="#1e1e1e"
        )
        self.lbl_tempo.pack(pady=5)

        # Label de status
        self.lbl_status = tk.Label(
            self,
            text="Parado",
            font=('Segoe UI', 9),
            fg="#808080",
            bg="#1e1e1e"
        )
        self.lbl_status.pack()

    def start(self):
        """Inicia o cronometro."""
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.lbl_status.config(text="Em execucao...", fg="#6a9955")
            self._update()

    def stop(self) -> str:
        """
        Para o cronometro.

        Returns:
            str: Tempo total formatado.
        """
        self.running = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        self.lbl_status.config(text="Finalizado", fg="#dcdcaa")
        return self.lbl_tempo.cget("text")

    def reset(self):
        """Reseta o cronometro para 00:00."""
        self.stop()
        self.start_time = None
        self.lbl_tempo.config(text="00:00")
        self.lbl_status.config(text="Parado", fg="#808080")

    def _update(self):
        """Atualiza o display do cronometro."""
        if self.running and self.start_time:
            elapsed = time.time() - self.start_time
            self.lbl_tempo.config(text=self._format_time(elapsed))
            self._after_id = self.after(1000, self._update)

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Formata segundos para MM:SS ou HH:MM:SS."""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, secs = divmod(remainder, 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"


class Scoreboard(ttk.Frame):
    """
    Widget de placar para contagem de testes.
    Exibe: Aprovados, Falhas, Total, Taxa de Sucesso.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.passed = 0
        self.failed = 0
        self.skipped = 0

        # Container principal
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.X, padx=5, pady=5)

        # Aprovados
        self.frame_passed = ttk.Frame(self.container)
        self.frame_passed.pack(side=tk.LEFT, padx=10)
        tk.Label(self.frame_passed, text="Aprovados", font=('Segoe UI', 9), fg="#6a9955").pack()
        self.lbl_passed = tk.Label(
            self.frame_passed,
            text="0",
            font=('Consolas', 20, 'bold'),
            fg="#6a9955"
        )
        self.lbl_passed.pack()

        # Falhas
        self.frame_failed = ttk.Frame(self.container)
        self.frame_failed.pack(side=tk.LEFT, padx=10)
        tk.Label(self.frame_failed, text="Falhas", font=('Segoe UI', 9), fg="#f44747").pack()
        self.lbl_failed = tk.Label(
            self.frame_failed,
            text="0",
            font=('Consolas', 20, 'bold'),
            fg="#f44747"
        )
        self.lbl_failed.pack()

        # Skipped
        self.frame_skipped = ttk.Frame(self.container)
        self.frame_skipped.pack(side=tk.LEFT, padx=10)
        tk.Label(self.frame_skipped, text="Pulados", font=('Segoe UI', 9), fg="#dcdcaa").pack()
        self.lbl_skipped = tk.Label(
            self.frame_skipped,
            text="0",
            font=('Consolas', 20, 'bold'),
            fg="#dcdcaa"
        )
        self.lbl_skipped.pack()

        # Taxa de sucesso
        self.frame_rate = ttk.Frame(self.container)
        self.frame_rate.pack(side=tk.RIGHT, padx=10)
        tk.Label(self.frame_rate, text="Taxa", font=('Segoe UI', 9), fg="#569cd6").pack()
        self.lbl_rate = tk.Label(
            self.frame_rate,
            text="--",
            font=('Consolas', 16, 'bold'),
            fg="#569cd6"
        )
        self.lbl_rate.pack()

    def add_passed(self, count: int = 1):
        """Adiciona testes aprovados."""
        self.passed += count
        self.lbl_passed.config(text=str(self.passed))
        self._update_rate()

    def add_failed(self, count: int = 1):
        """Adiciona testes com falha."""
        self.failed += count
        self.lbl_failed.config(text=str(self.failed))
        self._update_rate()

    def add_skipped(self, count: int = 1):
        """Adiciona testes pulados."""
        self.skipped += count
        self.lbl_skipped.config(text=str(self.skipped))
        self._update_rate()

    def reset(self):
        """Reseta todos os contadores."""
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.lbl_passed.config(text="0")
        self.lbl_failed.config(text="0")
        self.lbl_skipped.config(text="0")
        self.lbl_rate.config(text="--", fg="#569cd6")

    def _update_rate(self):
        """Atualiza a taxa de sucesso."""
        total = self.passed + self.failed
        if total > 0:
            rate = (self.passed / total) * 100
            color = "#6a9955" if rate >= 80 else "#dcdcaa" if rate >= 50 else "#f44747"
            self.lbl_rate.config(text=f"{rate:.0f}%", fg=color)

    def get_summary(self) -> dict:
        """Retorna resumo dos resultados."""
        total = self.passed + self.failed + self.skipped
        return {
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "total": total,
            "rate": (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0
        }


class ProgressoIndeterminado(ttk.Frame):
    """
    Barra de progresso indeterminada (animada).
    Usada quando nao sabemos o tempo total de execucao.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.running = False

        # Barra de progresso
        self.progressbar = ttk.Progressbar(
            self,
            mode='indeterminate',
            length=300
        )
        self.progressbar.pack(fill=tk.X, pady=5)

        # Label de status
        self.lbl_status = tk.Label(
            self,
            text="",
            font=('Segoe UI', 9),
            fg="#808080"
        )
        self.lbl_status.pack()

    def start(self, status_text: str = "Executando testes..."):
        """Inicia a animacao da barra."""
        self.running = True
        self.lbl_status.config(text=status_text, fg="#569cd6")
        self.progressbar.start(10)

    def stop(self, success: bool = True):
        """Para a animacao da barra."""
        self.running = False
        self.progressbar.stop()
        if success:
            self.lbl_status.config(text="Concluido!", fg="#6a9955")
        else:
            self.lbl_status.config(text="Finalizado com erros", fg="#f44747")

    def set_status(self, text: str, color: str = "#569cd6"):
        """Define texto de status personalizado."""
        self.lbl_status.config(text=text, fg=color)


class StatusBar(ttk.Frame):
    """
    Barra de status na parte inferior do aplicativo.
    Exibe informacoes contextuais e status da conexao.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Container com borda
        self.configure(relief=tk.SUNKEN, borderwidth=1)

        # Status principal
        self.lbl_status = tk.Label(
            self,
            text="Pronto",
            font=('Segoe UI', 9),
            anchor=tk.W
        )
        self.lbl_status.pack(side=tk.LEFT, padx=5)

        # Indicador Appium
        self.lbl_appium = tk.Label(
            self,
            text="Appium: --",
            font=('Segoe UI', 9),
            fg="#808080"
        )
        self.lbl_appium.pack(side=tk.RIGHT, padx=10)

        # Versao
        self.lbl_version = tk.Label(
            self,
            text="v1.0.0",
            font=('Segoe UI', 8),
            fg="#808080"
        )
        self.lbl_version.pack(side=tk.RIGHT, padx=5)

    def set_status(self, text: str, color: str = "#000000"):
        """Define o texto de status."""
        self.lbl_status.config(text=text, fg=color)

    def set_appium_status(self, connected: bool, port: int = 4723):
        """Define o status do Appium."""
        if connected:
            self.lbl_appium.config(text=f"Appium: {port}", fg="#6a9955")
        else:
            self.lbl_appium.config(text="Appium: Offline", fg="#f44747")

    def set_version(self, version: str):
        """Define a versao exibida."""
        self.lbl_version.config(text=version)


if __name__ == "__main__":
    # Teste dos componentes
    root = tk.Tk()
    root.title("Teste UI Components")
    root.geometry("600x400")
    root.configure(bg="#1e1e1e")

    # Cronometro
    ttk.Label(root, text="Cronometro:").pack(pady=5)
    cron = Cronometro(root)
    cron.pack(pady=10)

    # Scoreboard
    ttk.Label(root, text="Scoreboard:").pack(pady=5)
    score = Scoreboard(root)
    score.pack(pady=10)

    # Progresso
    ttk.Label(root, text="Progresso:").pack(pady=5)
    prog = ProgressoIndeterminado(root)
    prog.pack(pady=10)

    # Botoes de teste
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=20)

    def start_test():
        cron.start()
        prog.start()
        score.reset()

    def add_pass():
        score.add_passed()

    def add_fail():
        score.add_failed()

    def stop_test():
        cron.stop()
        prog.stop()

    ttk.Button(btn_frame, text="Start", command=start_test).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="+Pass", command=add_pass).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="+Fail", command=add_fail).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Stop", command=stop_test).pack(side=tk.LEFT, padx=5)

    # StatusBar
    status = StatusBar(root)
    status.pack(side=tk.BOTTOM, fill=tk.X)
    status.set_appium_status(True)

    root.mainloop()
