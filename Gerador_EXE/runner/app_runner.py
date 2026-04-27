import sys
import os
import io
import re
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DE ENCODING UTF-8 (DEVE SER PRIMEIRO)
# ==============================================================================
# Força UTF-8 em todo o sistema para evitar problemas com acentos e emojis
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# ==============================================================================
# LÓGICA DO WORKER (EXECUTOR DE TESTES)
# ==============================================================================
if len(sys.argv) > 1 and sys.argv[1] == "worker_pytest_runner":
    # Força UTF-8 globalmente para evitar problemas com acentos e emojis
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    if sys.stdout is None:
        sys.stdout = io.TextIOWrapper(open(os.devnull, "w", encoding='utf-8'))
    if sys.stderr is None:
        sys.stderr = io.TextIOWrapper(open(os.devnull, "w", encoding='utf-8'))

    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except: pass

    import pytest
    import errno

    try:
        pytest_args = sys.argv[2:]
        sys.exit(pytest.main(pytest_args))
    except (BrokenPipeError, IOError) as e:
        if e.errno == errno.EPIPE or e.errno == 32:
            try: sys.stderr.close()
            except: pass
            sys.exit(0)
        else:
            raise
    except Exception:
        sys.exit(1)

# ==============================================================================
# LÓGICA DA APLICAÇÃO (GUI)
# ==============================================================================

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import glob
import webbrowser
import json
import socket
import time
import shutil

# ==============================================================================
# CLASSE AUXILIAR: TOOLTIP HOVER
# ==============================================================================

class ToolTip:
    """
    Cria tooltips hover para widgets tkinter.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("Segoe UI", 9))
        label.pack(ipadx=5, ipady=3)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# --- FORÇAR IMPORTS ---
try:
    import pytest_html
    import pytest_metadata
    import appium
    import urllib3
    # Tenta importar para garantir que existe
    import allure_combine
except ImportError:
    pass

# --- CONFIGURAÇÃO DE AMBIENTE ---
if getattr(sys, 'frozen', False):
    # Modo EXE compilado - PyInstaller extrai arquivos para _MEIPASS
    BASE_DIR = os.path.dirname(sys.executable)
    # Para arquivos empacotados, usa o diretório temporário do PyInstaller
    MEIPASS_DIR = getattr(sys, '_MEIPASS', BASE_DIR)
else:
    # Modo desenvolvimento - usa staging se existir (simulação do EXE)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    staging_dir = os.path.join(os.path.dirname(current_dir), "output", "staging")

    if os.path.isdir(staging_dir) and os.path.exists(os.path.join(staging_dir, "config.py")):
        BASE_DIR = staging_dir
        MEIPASS_DIR = staging_dir
        print(f"[DEV MODE] Usando staging: {staging_dir}")
    else:
        BASE_DIR = current_dir
        MEIPASS_DIR = current_dir
        print(f"[DEV MODE] Usando diretório atual: {current_dir}")

SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
FORMAS_FILE   = os.path.join(BASE_DIR, "formas_pagamento.json")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
# VERSION fica no _MEIPASS quando compilado, ou no BASE_DIR em dev
VERSION_FILE = os.path.join(MEIPASS_DIR, "VERSION") if getattr(sys, 'frozen', False) else os.path.join(BASE_DIR, "VERSION")
FIRST_RUN_MARKER = os.path.join(BASE_DIR, ".first_run")

# Auto-sync: detecta dev mode (True quando staging/ existe e é usado como BASE_DIR)
try:
    _DEV_MODE = (BASE_DIR == staging_dir)
    _TESTES_PDV_DIR = os.path.normpath(os.path.join(
        os.path.dirname(os.path.dirname(current_dir)), "Testes_PDV"
    )) if _DEV_MODE else None
except NameError:
    _DEV_MODE = False
    _TESTES_PDV_DIR = None


# ==============================================================================
# FUNÇÃO PARA LER VERSÃO
# ==============================================================================

def get_app_version():
    """Lê a versão do arquivo VERSION."""
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
    except Exception:
        pass
    return "2.0.0"  # Versão padrão caso não encontre


def is_first_run():
    """Detecta se é a primeira execução (logo após instalação)."""
    return os.path.exists(FIRST_RUN_MARKER)


def mark_first_run_complete():
    """Remove o marcador de primeira execução."""
    try:
        if os.path.exists(FIRST_RUN_MARKER):
            os.remove(FIRST_RUN_MARKER)
    except Exception:
        pass


# ==============================================================================
# FUNÇÕES AUXILIARES DE DETECÇÃO DE AMBIENTE (Busca robusta)
# ==============================================================================

from dependency_scanner import (
    _buscar_node_instalado,
    _buscar_allure_instalado,
    _buscar_appium_instalado,
    _buscar_adb_instalado,
)


class TestRunnerApp:
    def __init__(self, root):
        self.root = root
        app_version = get_app_version()
        self.root.title(f"QA Dashboard v{app_version} - Automacao PDV Mobile")
        self.root.geometry("1100x750")
        
        # Inicialização paralela
        self.root.after(100, self.verificar_dependencias_startup)
        self.root.after(500, self.iniciar_appium_background)
        self.root.after(200, self._recarregar_painel_formas)   # checar JSON instantâneo, sem subprocess
        self._discovery_running = False
        self._discovery_last_error = ""
        self._formas_habilitado_vars: dict = {}   # titulo → BooleanVar
        self._tipos_venda_vars: dict = {}          # titulo:tipo_venda → BooleanVar

        self.appium_proc = None 
        self.pytest_proc = None
        self.allure_proc = None 
        self.fila_de_execucao = [] 
        self.start_time = None
        self.is_running = False
        self.pass_count = 0
        self.fail_count = 0
        self.exit_code = 0
        self.fail_lines = []  # Linhas de erro para fail.log.txt
        self.mostrar_logs_tecnicos = tk.BooleanVar(value=False)
        self.simultaneo_var = tk.BooleanVar(value=False)
        self.devices_para_rodar = []  # [(udid, model), ...]
        self.parar_simultaneo = False
        self.log_widgets = {}  # udid -> ScrolledText
        self.modo_simultaneo_ativo = False

        # Configurações
        self.config_vars = {
            "server_ip": tk.StringVar(),
            "server_port": tk.StringVar(),
            "company": tk.StringVar(),
            "user": tk.StringVar(),
            "password": tk.StringVar(),
            "customer_id": tk.StringVar(),
            "customer_id_troca": tk.StringVar(),
            "customer_id_bonus": tk.StringVar(),
            "appium_port": tk.StringVar(value="4723"),
            "appium_path": tk.StringVar(),
            "qa_dev_path": tk.StringVar(),
            "timeout_default": tk.StringVar(value="30"),
            "product_code_sale": tk.StringVar(),
            "product_code": tk.StringVar(),
            "product_code_future_sale": tk.StringVar(),
            "product_size_future": tk.StringVar(),
            "product_code_stock_1": tk.StringVar(),
            "product_code_stock_2": tk.StringVar(),
            "clean_logs": tk.BooleanVar(value=False),
            "auto_open": tk.BooleanVar(value=False),
            "use_allure": tk.BooleanVar(value=False),
            # Se marcado, gera o HTML unico (tipo PDF funcional)
            "generate_single_file": tk.BooleanVar(value=False),
            # Se marcado, abre o servidor ou o arquivo unico ao final
            "open_allure_end": tk.BooleanVar(value=False),
            # Configurações de Impressão
            "print_cupom_venda": tk.BooleanVar(value=False),
            "print_nfce": tk.BooleanVar(value=False),
            "print_danfe": tk.BooleanVar(value=False),
            "print_cupom_troca": tk.BooleanVar(value=False),
            "print_giftback": tk.BooleanVar(value=False),
            "print_dialog_timeout": tk.StringVar(value="20"),
            # Configurações de Ordem E2E
            "run_e2e_full": tk.BooleanVar(value=False),
            "e2e_order_file": tk.StringVar(value=""),
            # Formas de pagamento POS (preenchidas por auto-descoberta ou manual)
            "forma_dinheiro": tk.StringVar(value=""),
            "forma_debito":   tk.StringVar(value=""),
            "forma_credito":  tk.StringVar(value=""),
        }

        # Arquivo settings ativo (não salvo dentro do JSON — é o próprio arquivo)
        self.settings_file_var = tk.StringVar(value=SETTINGS_FILE)

        self.carregar_inicializacao()
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_programa)

        try:
            icon_path = os.path.join(BASE_DIR, "assets", "icon.ico")
            if os.path.exists(icon_path): self.root.iconbitmap(icon_path)
        except: pass
        
        self.tab_control = ttk.Notebook(root)
        self.tab_testes = ttk.Frame(self.tab_control)
        self.tab_config = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_testes, text='   Testes   ')
        self.tab_control.add(self.tab_config, text=' Configurações ')
        self.tab_control.pack(expand=1, fill="both")

        # Rodapé com versão
        footer_frame = tk.Frame(root, bg="#2d2d30", height=25)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        footer_frame.pack_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text=f"QA Dashboard v{app_version} - Desenvolvido para Automação PDV Mobile",
            bg="#2d2d30",
            fg="#a0a0a0",
            font=('Segoe UI', 8),
            anchor=tk.W,
            padx=10
        )
        footer_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_formas_status = tk.Label(
            footer_frame,
            text="",
            bg="#2d2d30",
            fg="#a0a0a0",
            font=('Segoe UI', 8),
            anchor=tk.E,
            padx=10
        )
        self.lbl_formas_status.pack(side=tk.RIGHT)

        self.setup_tab_testes()
        self.setup_tab_config()

    def carregar_inicializacao(self):
        carregou_arquivo = False
        campos_faltando = []

        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Carrega valores do arquivo
                    for key, var in self.config_vars.items():
                        if key in data and data[key] is not None:
                            var.set(data[key])
                        else:
                            # Registra campos faltando para adicionar
                            campos_faltando.append(key)

                    carregou_arquivo = True

                    # Se houver campos faltando, adiciona e salva
                    if campos_faltando:
                        print(f"[INFO] Adicionando {len(campos_faltando)} campos faltando ao settings.json")
                        self.salvar_settings(mostrar_msg=False)

            except Exception as e:
                print(f"Erro ao ler settings: {e}")

        # Garante que qa_dev_path tenha valor
        if not self.config_vars["qa_dev_path"].get():
            self.config_vars["qa_dev_path"].set(BASE_DIR)
            if not carregou_arquivo:
                self.salvar_settings(mostrar_msg=False)

    def verificar_dependencias_startup(self, silent=True):
        # Se é primeira execução (logo após instalação), força modo silencioso
        # porque PATH pode não estar atualizado ainda
        primeira_exec = is_first_run()
        if primeira_exec:
            silent = True  # Força silencioso na primeira execução

        log_report = [f"=== VERIFICACAO DE AMBIENTE: {datetime.now()} ==="]
        self.faltantes_map = {}

        # 1. JAVA (busca robusta)
        java_path = shutil.which("java")
        if not java_path:
            # Busca em locais típicos
            for jpath in [
                os.path.expandvars(r"%JAVA_HOME%\bin\java.exe"),
                r"C:\Program Files\Java\jdk-17\bin\java.exe",
                r"C:\Program Files\Java\jdk-11\bin\java.exe",
                r"C:\Program Files\Eclipse Adoptium\jdk-17\bin\java.exe",
                r"C:\Program Files\Eclipse Adoptium\jdk-11\bin\java.exe",
            ]:
                if jpath and os.path.isfile(jpath):
                    java_path = jpath
                    break

        if java_path:
            log_report.append(f"✅ JAVA:   {java_path}")
        else:
            log_report.append(f"❌ JAVA:   NAO ENCONTRADO")
            self.faltantes_map["Java JDK"] = "script:instalar_dependencias.bat"

        # 2. NODE (busca robusta usando função auxiliar)
        node_path = _buscar_node_instalado()
        if node_path:
            log_report.append(f"✅ NODE:   {node_path}")
        else:
            log_report.append(f"❌ NODE:   NAO ENCONTRADO")
            self.faltantes_map["Node.js"] = "winget:OpenJS.NodeJS"

        # 3. ALLURE CLI (busca robusta usando função auxiliar)
        allure_cmd = _buscar_allure_instalado()
        if allure_cmd:
            log_report.append(f"✅ ALLURE CLI: {allure_cmd}")
        else:
            log_report.append(f"⚠️ ALLURE CLI: NAO ENCONTRADO (opcional)")
            # Allure é OPCIONAL - não adiciona ao faltantes_map para não bloquear
            # self.faltantes_map["Allure Completo"] = "script:instalar_allure.bat"

        # 4. ALLURE COMBINE (biblioteca Python)
        try:
            import allure_combine
            log_report.append(f"✅ ALLURE COMBINE: Instalado")
        except ImportError:
            log_report.append(f"⚠️ ALLURE COMBINE: NAO ENCONTRADO (opcional)")
            # Allure Combine é OPCIONAL - não adiciona ao faltantes_map
            # self.faltantes_map["Lib allure-combine"] = "cmd:python -m pip install allure-combine"

        # 5. APPIUM (busca robusta usando função auxiliar)
        appium_path = self.config_vars["appium_path"].get()
        if not appium_path or not os.path.exists(appium_path):
            appium_path = _buscar_appium_instalado()

        if appium_path:
            log_report.append(f"✅ APPIUM: {appium_path}")
            if not self.config_vars["appium_path"].get():
                self.config_vars["appium_path"].set(appium_path)
                self.salvar_settings(mostrar_msg=False)
        else:
            log_report.append(f"❌ APPIUM: NAO ENCONTRADO")
            self.faltantes_map["Appium Server"] = "script:instalar_dependencias.bat"

        # 6. ADB (busca robusta usando função auxiliar)
        adb_path = _buscar_adb_instalado()
        if adb_path:
            log_report.append(f"✅ ADB:    {adb_path}")
        else:
            log_report.append(f"❌ ADB:    NAO ENCONTRADO")
            self.faltantes_map["Android SDK (adb)"] = "script:instalar_android_sdk.bat"

        try:
            verif_dir = os.path.join(BASE_DIR, "logs", "verificacoes")
            if not os.path.exists(verif_dir): os.makedirs(verif_dir)
            log_file = os.path.join(verif_dir, "ambiente_check.txt")
            with open(log_file, 'w', encoding='utf-8') as f: f.write("\n".join(log_report))
        except: pass

        if self.faltantes_map:
            # Se é primeira execução, não mostra popup (PATH pode não estar atualizado)
            if not primeira_exec and not silent:
                itens_str = "\n- ".join(self.faltantes_map.keys())
                msg = f"ATENÇÃO: Ambiente incompleto.\n\nItens faltando:\n- {itens_str}\n\nDeseja realizar a INSTALAÇÃO AUTOMÁTICA desses itens agora?"
                if messagebox.askyesno("Ambiente Incompleto", msg):
                    self.executar_instalacao_automatica()
            elif primeira_exec:
                # Log silencioso na primeira execução
                print("[INFO] Primeira execução detectada. Verificação de ambiente será feita posteriormente.")
                print("[INFO] Use o botão 'Verificar Ambiente' nas Configurações após reiniciar o Windows.")
        elif not silent:
            msg = "Ambiente verificado com sucesso!\n\n" + "\n".join(log_report)
            messagebox.showinfo("Ambiente OK", msg)

        # Marca primeira execução como completa
        if primeira_exec:
            mark_first_run_complete()

    def executar_instalacao_automatica(self):
        if not hasattr(self, 'faltantes_map') or not self.faltantes_map: return
        comandos_executados = []
        for item, action in self.faltantes_map.items():
            tipo, valor = action.split(":", 1)
            
            if tipo == "script":
                script_path = os.path.join(SCRIPTS_DIR, valor)
                if os.path.exists(script_path) and script_path not in comandos_executados:
                    subprocess.Popen(["start", "cmd", "/c", script_path], shell=True)
                    comandos_executados.append(script_path)
            elif tipo == "winget":
                cmd_winget = f'winget install -e --id {valor} --accept-source-agreements --accept-package-agreements'
                full_cmd = f'start cmd /c "echo Instalando {item}... && {cmd_winget} && echo. && echo Fechando em 5s... && timeout /t 5"'
                subprocess.Popen(full_cmd, shell=True)
            elif tipo == "cmd":
                # Executa com python -m pip
                full_cmd = f'start cmd /c "echo Instalando {item}... && {valor} && echo. && echo Fechando em 5s... && timeout /t 5"'
                subprocess.Popen(full_cmd, shell=True)
        
        messagebox.showinfo("Instalando", "As janelas de instalação foram abertas.\n\nIMPORTANTE: Após o término, REINICIE o computador ou o programa.")
        sys.exit(0)

    # ==========================================================================
    # AUTO-DESCOBERTA DE FORMAS DE PAGAMENTO POS
    # ==========================================================================

    def _atualizar_status_formas(self, texto: str, cor: str = "#a0a0a0"):
        """Atualiza label de status de formas no footer (thread-safe via root.after)."""
        if hasattr(self, 'lbl_formas_status'):
            self.lbl_formas_status.config(text=texto, fg=cor)


    def _autodescobrir_formas_bg(self):
        """Roda pytest de discovery completo em thread daemon — sem janela visível."""
        self._discovery_running = True
        self._discovery_last_error = ""
        try:
            # Usa BASE_DIR (staging em dev, dir do EXE em prod) — não qa_dev_path que pode
            # estar apontando para o diretório instalado enquanto se edita em staging.
            projeto_path = BASE_DIR
            appium_port  = self.config_vars["appium_port"].get() or "4723"
            device_id    = self.config_vars.get("device_id", tk.StringVar()).get()
            test_node = (
                "tests/e2e/vendas/test_discovery_completo.py"
                "::TestDiscoveryCompleto::test_mapear_todas_formas"
            )
            base_args = [
                test_node,
                "--no-header", "-q", "--tb=short",
                f"--rootdir={projeto_path}",
                f"--appium-port={appium_port}",
            ]
            if device_id:
                base_args.append(f"--device-id={device_id}")

            if getattr(sys, 'frozen', False):
                cmd = [sys.executable, "worker_pytest_runner"] + base_args
            else:
                cmd = [sys.executable, "-m", "pytest"] + base_args

            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONPATH"] = projeto_path + os.pathsep + env.get("PYTHONPATH", "")
            env["TEST_SERVER_IP"]   = self.config_vars["server_ip"].get()
            env["TEST_SERVER_PORT"] = self.config_vars["server_port"].get()
            env["TEST_COMPANY"]     = self.config_vars["company"].get()
            env["TEST_USER"]        = self.config_vars["user"].get()
            env["TEST_PASSWORD"]    = self.config_vars["password"].get()
            env["TEST_PRINT_CUPOM_VENDA"]  = "false"
            env["TEST_PRINT_NFCE"]         = "false"
            env["TEST_PRINT_DANFE"]        = "false"
            env["TEST_PRINT_CUPOM_TROCA"]  = "false"
            env["TEST_PRINT_GIFTBACK"]     = "false"

            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE

            result = subprocess.run(
                cmd,
                cwd=projeto_path,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                startupinfo=si,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=180,
            )
            # Salva output para diagnóstico se falhar
            if result.returncode != 0:
                output = (result.stdout or "") + (result.stderr or "")
                self._discovery_last_error = output[-500:] if len(output) > 500 else output
                # Log no arquivo para debug
                try:
                    log_path = os.path.join(BASE_DIR, "logs", "discovery_error.log")
                    os.makedirs(os.path.dirname(log_path), exist_ok=True)
                    with open(log_path, "w", encoding="utf-8") as f:
                        f.write(f"CMD: {' '.join(cmd)}\nCWD: {projeto_path}\n\n{output}")
                except Exception:
                    pass
        except subprocess.TimeoutExpired:
            self._discovery_last_error = "Timeout (180s) — teste demorou demais"
        except Exception as e:
            self._discovery_last_error = str(e)
        finally:
            self._discovery_running = False
            self.root.after(0, self._pos_autodescoberta)

    def _pos_autodescoberta(self):
        """Chamado após pytest de discovery terminar (botão manual)."""
        err = getattr(self, "_discovery_last_error", "")
        if err:
            linhas = [l.strip() for l in err.splitlines() if l.strip()]
            msg = f"⚠️ {linhas[-1][:80]}" if linhas else "⚠️ Discovery falhou"
            self._atualizar_status_formas(msg, "#e74c3c")
        self.root.after(200, self._recarregar_painel_formas)

    # ------------------------------------------------------------------
    # PAINEL DE ATALHOS DE PAGAMENTO (formas_pagamento.json)
    # ------------------------------------------------------------------

    def _formas_json_path(self) -> str:
        """Retorna o caminho correto do formas_pagamento.json."""
        settings = self.settings_file_var.get() if hasattr(self, "settings_file_var") else ""
        if settings:
            candidate = os.path.join(os.path.dirname(settings), "formas_pagamento.json")
            if os.path.exists(candidate):
                return candidate
            # Usa mesmo diretório mesmo que ainda não exista
            return candidate
        return FORMAS_FILE

    def _ler_formas_json(self) -> list:
        """Lê formas_pagamento.json. Retorna [] se não existe ou inválido."""
        path = self._formas_json_path()
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f).get("formas", [])
        except Exception:
            return []

    def _recarregar_painel_formas(self):
        """Popula os 8 slots de atalhos a partir do formas_pagamento.json."""
        if not hasattr(self, "_atalhos_nome_vars"):
            return
        formas = self._ler_formas_json()
        if formas:
            n_hab = sum(1 for f in formas if f.get("habilitado", True))
            self._atualizar_status_formas(f"✅ {len(formas)} atalhos mapeados ({n_hab} habilitados)", "#2ecc71")
        else:
            self._atualizar_status_formas("⚠️ Atalhos não mapeados — clique 🔄 para mapear", "#e67e22")
        COR_TIPO = {
            "pos_debito":   "#1565c0",
            "pos_credito":  "#6a1b9a",
            "dinheiro":     "#2e7d32",
            "personalizado":"#e65100",
            "tef":          "#888888",
            "pix":          "#00838f",
            "outro":        "#888888",
        }
        for i in range(8):
            if i < len(formas):
                f = formas[i]
                titulo    = f.get("titulo", "")
                tipo_auto = f.get("tipo_auto", "outro")
                habilitado = f.get("habilitado", True)
                parcelas  = f.get("parcelas", [])
                tipos_v   = f.get("tipos_venda", [])
                self._atalhos_nome_vars[i].set(titulo)
                self._atalhos_hab_vars[i].set(habilitado)
                # Label de tipo com info extra
                info = tipo_auto
                if parcelas:
                    info += f" · {len(parcelas)}parc"
                if tipos_v:
                    n_hab = sum(1 for t in tipos_v if t.get("habilitado", True))
                    info += f" · {n_hab}tv"
                if hasattr(self, "_atalhos_tipo_labels") and i < len(self._atalhos_tipo_labels):
                    self._atalhos_tipo_labels[i].config(
                        text=info, foreground=COR_TIPO.get(tipo_auto, "#555"))
            else:
                self._atalhos_nome_vars[i].set("")
                self._atalhos_hab_vars[i].set(False)
                if hasattr(self, "_atalhos_tipo_labels") and i < len(self._atalhos_tipo_labels):
                    self._atalhos_tipo_labels[i].config(text="—", foreground="#ccc")

    def _salvar_formas_json(self):
        """Salva os valores dos 8 slots de volta no formas_pagamento.json."""
        path = self._formas_json_path()
        try:
            # Lê existente para preservar parcelas/tipos_venda
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {"formas": []}
            formas = data.get("formas", [])
            # Atualiza nome + habilitado de cada slot
            for i in range(8):
                nome = self._atalhos_nome_vars[i].get().strip()
                hab  = self._atalhos_hab_vars[i].get()
                if i < len(formas):
                    formas[i]["titulo"]    = nome
                    formas[i]["habilitado"] = hab
                elif nome:
                    formas.append({"titulo": nome, "subtitulo": "", "detalhes": "",
                                   "tipo_auto": "outro", "habilitado": hab,
                                   "parcelas": [], "tipos_venda": []})
            # Remove slots vazios no final
            while formas and not formas[-1].get("titulo"):
                formas.pop()
            data["formas"] = formas
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar formas_pagamento.json:\n{e}")

    def _abrir_formas_json(self):
        """Abre formas_pagamento.json no editor padrão. Cria vazio se não existir."""
        path = self._formas_json_path()
        if not os.path.exists(path):
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({"_discovery_timestamp": "", "formas": []}, f, indent=2)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível criar {path}:\n{e}")
                return
        try:
            os.startfile(path)
        except Exception:
            try:
                subprocess.Popen(["notepad.exe", path])
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir:\n{path}\n\n{e}")

    def _appium_esta_rodando(self) -> bool:
        """Verifica se o Appium está ouvindo na porta configurada."""
        import socket
        try:
            port = int(self.config_vars.get(
                "appium_port", tk.StringVar(value="4723")).get() or 4723)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(("127.0.0.1", port))
            s.close()
            return result == 0
        except Exception:
            return False

    def _forcar_redescoberta_formas(self):
        """Limpa formas mapeadas e inicia redescoberta (chamado pelo botão)."""
        if self._discovery_running:
            messagebox.showinfo("Aguarde", "Já existe uma descoberta em andamento.")
            return
        if not self._appium_esta_rodando():
            messagebox.showwarning("Appium offline", "O Appium não está rodando.\nInicie o Appium e tente novamente.")
            return
        # Apaga formas_pagamento.json para forçar re-mapeamento completo
        path = self._formas_json_path()
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        # Limpa campos legados no settings.json
        try:
            settings_path = self.settings_file_var.get() or SETTINGS_FILE
            with open(settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for campo in ("forma_debito", "forma_credito", "forma_dinheiro", "parcelas_credito"):
                data.pop(campo, None)
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
        # Limpa slots visuais
        for i in range(8):
            self._atalhos_nome_vars[i].set("")
            self._atalhos_hab_vars[i].set(False)
            if i < len(self._atalhos_tipo_labels):
                self._atalhos_tipo_labels[i].config(text="—", foreground="#ccc")
        self._atualizar_status_formas("🔄 Iniciando descoberta...", "#f39c12")
        t = threading.Thread(target=self._autodescobrir_formas_bg, daemon=True)
        t.start()

    # ==========================================================================
    # SETUP DA TAB DE TESTES
    # ==========================================================================
    def setup_tab_testes(self):
        left_frame = ttk.Frame(self.tab_testes, padding="10", width=430)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        left_frame.pack_propagate(False) 
        
        right_frame = ttk.Frame(self.tab_testes, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_frame, text="Cenários de Teste:", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0,5))
        
        tree_container = ttk.Frame(left_frame)
        tree_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_container, show="tree", selectmode="none", height=20)
        self.tree.column("#0", stretch=False, minwidth=300, width=520)
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.bind("<Button-1>", self.on_tree_click)

        # --- Estilo visual da árvore ---
        _ts = ttk.Style()
        _ts.configure("Treeview", rowheight=24)
        self.tree.tag_configure("cat_e2e",       foreground="#1a6b3c", font=('Segoe UI', 9))
        self.tree.tag_configure("cat_smoke",      foreground="#007a6c", font=('Segoe UI', 9))
        self.tree.tag_configure("cat_unit",       foreground="#5c2d91", font=('Segoe UI', 9))
        self.tree.tag_configure("cat_negativos",  foreground="#8b0000", font=('Segoe UI', 9))
        self.tree.tag_configure("cat_descontos",  foreground="#8b4513", font=('Segoe UI', 9))
        self.tree.tag_configure("cat_default",    foreground="#2d2d30", font=('Segoe UI', 9))
        self.tree.tag_configure("folder_root",    font=('Segoe UI', 9, 'bold'))
        self.tree.tag_configure("subfolder",      font=('Segoe UI', 9, 'italic'))

        self.lbl_status_fila = tk.Label(left_frame, text="Fila: (Vazia)", fg="gray", wraplength=250, justify="left", font=('Segoe UI', 8))
        self.lbl_status_fila.pack(side=tk.TOP, fill=tk.X, pady=(10, 2))

        # --- MODO SIMULTÂNEO ---
        self.chk_simultaneo = ttk.Checkbutton(
            left_frame,
            text="Simultâneo (múltiplos devices)",
            variable=self.simultaneo_var,
            command=self._toggle_simultaneo
        )
        self.chk_simultaneo.pack(anchor=tk.W, pady=(0, 2))

        self.frame_devices = ttk.LabelFrame(left_frame, text="Devices Conectados", padding=4)
        # NÃO faz pack aqui - _toggle_simultaneo faz isso

        dev_list_frame = ttk.Frame(self.frame_devices)
        dev_list_frame.pack(fill=tk.BOTH, expand=True)
        self.devices_listbox = tk.Listbox(dev_list_frame, height=4, font=('Consolas', 8), selectmode=tk.SINGLE)
        self.devices_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        dev_btn_row = ttk.Frame(self.frame_devices)
        dev_btn_row.pack(fill=tk.X, pady=(3, 0))
        ttk.Button(dev_btn_row, text="↑", width=3, command=self._mover_device_up).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(dev_btn_row, text="↓", width=3, command=self._mover_device_down).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(dev_btn_row, text="Atualizar", command=self._atualizar_painel_devices).pack(side=tk.LEFT)

        self.atualizar_lista_testes()

        # Banner de aviso: E2E Full ativo sobrescreve seleção manual
        self.lbl_e2e_full_aviso = tk.Label(
            left_frame,
            text="⚠️ MODO E2E FULL ATIVO — seleção manual ignorada",
            bg="#c0392b", fg="white",
            font=('Segoe UI', 8, 'bold'),
            wraplength=280, justify="center", pady=3
        )
        # Não faz pack aqui — _atualizar_aviso_e2e_full controla visibilidade
        self.config_vars["run_e2e_full"].trace_add("write", lambda *_: self._atualizar_aviso_e2e_full())
        self._atualizar_aviso_e2e_full()

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.btn_run = tk.Button(btn_frame, text="▶ RODAR NA ORDEM", command=self.iniciar_testes, bg="#007acc", fg="white", font=('Segoe UI', 10, 'bold'), height=2, relief=tk.FLAT)
        self.btn_run.pack(fill=tk.X, pady=5)

        # --- Botões de categoria rápida ---
        cat_label = ttk.Label(btn_frame, text="Rodar categoria:", font=('Segoe UI', 8))
        cat_label.pack(anchor=tk.W, pady=(2, 1))
        cat_frame = ttk.Frame(btn_frame)
        cat_frame.pack(fill=tk.X, pady=(0, 2))
        tk.Button(cat_frame, text="⚡ Unitários", command=lambda: self._rodar_categoria("unit"), bg="#5c2d91", fg="white", font=('Segoe UI', 8, 'bold'), relief=tk.FLAT, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 1))
        tk.Button(cat_frame, text="💨 Smoke", command=lambda: self._rodar_categoria("smoke"), bg="#007a6c", fg="white", font=('Segoe UI', 8, 'bold'), relief=tk.FLAT, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(cat_frame, text="🔁 Regressão", command=lambda: self._rodar_categoria("regression"), bg="#8b4513", fg="white", font=('Segoe UI', 8, 'bold'), relief=tk.FLAT, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(1, 0))
        cat_frame2 = ttk.Frame(btn_frame)
        cat_frame2.pack(fill=tk.X, pady=(0, 4))
        tk.Button(cat_frame2, text="🔄 E2E", command=lambda: self._rodar_categoria("e2e"), bg="#1a6b3c", fg="white", font=('Segoe UI', 8, 'bold'), relief=tk.FLAT, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 1))
        tk.Button(cat_frame2, text="🚫 Negativos", command=lambda: self._rodar_categoria("negativos"), bg="#8b0000", fg="white", font=('Segoe UI', 8, 'bold'), relief=tk.FLAT, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(1, 0))

        report_frame = ttk.Frame(btn_frame)
        report_frame.pack(fill=tk.X, pady=5)

        self.btn_report = tk.Button(report_frame, text="📄 Relatório Simples", command=self.abrir_relatorio, bg="#2d2d30", fg="white", height=1, relief=tk.FLAT)
        self.btn_report.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.btn_allure = tk.Button(report_frame, text="📊 Relatório Funcional (Allure)", command=self.gerar_e_abrir_allure_unico, bg="#d35400", fg="white", height=1, relief=tk.FLAT)
        self.btn_allure.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

        dash_frame = tk.Frame(right_frame, bg="#f0f0f0", height=80)
        dash_frame.pack(fill=tk.X, pady=(0, 10))
        self.lbl_timer = tk.Label(dash_frame, text="00:00:00", bg="#f0f0f0", fg="#333", font=('Segoe UI', 20, 'bold'))
        self.lbl_timer.place(x=10, y=20)
        self.lbl_pass = tk.Label(dash_frame, text="✔ APROVADOS: 0", bg="#f0f0f0", fg="#2ecc71", font=('Segoe UI', 12, 'bold'))
        self.lbl_pass.place(x=200, y=25)
        self.lbl_fail = tk.Label(dash_frame, text="❌ FALHAS: 0", bg="#f0f0f0", fg="#e74c3c", font=('Segoe UI', 12, 'bold'))
        self.lbl_fail.place(x=380, y=25)

        self.progress = ttk.Progressbar(right_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 5))

        self.chk_logs = ttk.Checkbutton(right_frame, text="Exibir Logs Técnicos (Debug)", variable=self.mostrar_logs_tecnicos)
        self.chk_logs.pack(anchor=tk.E)

        self.log_notebook = ttk.Notebook(right_frame)
        self.log_notebook.pack(fill=tk.BOTH, expand=True)
        self.log_area = self._criar_aba_log("", "Log")

    def atualizar_lista_testes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.fila_de_execucao = []
        self.atualizar_label_fila()
        projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR
        
        IGNORED_FILES = ["test_data.py", "conftest.py", "__init__.py", "config.py", "framework.py"]

        test_files = []
        for pattern in [os.path.join(projeto_path, "tests", "**", "test_*.py"), os.path.join(projeto_path, "test_*.py")]:
             test_files.extend(glob.glob(pattern, recursive=True))
        test_files = sorted(list(set(test_files)))

        if not test_files:
            self.escrever_log(f"[AVISO] Nenhum teste encontrado em: {projeto_path}", 'WARNING')
            return

        # Pré-computa contagem de testes por categoria (1º nível abaixo de 'tests')
        category_counts = {}
        for fp in test_files:
            fn = os.path.basename(fp)
            if fn in IGNORED_FILES: continue
            rp = os.path.relpath(fp, projeto_path)
            pts = rp.split(os.sep)
            if len(pts) >= 2 and pts[0] == "tests":
                cat_key = os.path.join(pts[0], pts[1])
            elif len(pts) >= 1:
                cat_key = pts[0]
            else:
                continue
            category_counts[cat_key] = category_counts.get(cat_key, 0) + 1

        total_tests = len([fp for fp in test_files if os.path.basename(fp) not in IGNORED_FILES])

        CAT_ICONS = {
            "e2e": "🔄", "smoke": "💨", "unit": "⚡", "negativos": "🚫",
            "vendas": "💰", "descontos": "🏷️", "trocas": "🔁", "pedidos": "📋",
            "login": "🔑", "cliente": "👤", "validar": "✔️", "venda_futura": "🗓️",
            "consultas": "🔍",
        }
        CAT_LABELS = {
            "e2e": "E2E", "smoke": "Smoke", "unit": "Unitários", "negativos": "Negativos",
            "vendas": "Vendas", "descontos": "Descontos", "trocas": "Trocas",
            "pedidos": "Pedidos", "login": "Login", "cliente": "Cliente",
            "validar": "Validar", "venda_futura": "Venda Futura", "consultas": "Consultas",
        }
        CAT_TAGS = {
            "e2e": "cat_e2e", "smoke": "cat_smoke", "unit": "cat_unit",
            "negativos": "cat_negativos", "descontos": "cat_descontos",
        }

        def _get_cat(pts):
            if len(pts) >= 2 and pts[0] == "tests":
                return pts[1]
            return pts[0] if pts else ""

        def _fmt_file(name):
            return name.replace("test_", "").replace(".py", "").replace("_", " ").title()

        folder_ids = {}

        for full_path in test_files:
            file_name = os.path.basename(full_path)
            if file_name in IGNORED_FILES: continue

            rel_path = os.path.relpath(full_path, projeto_path)
            parts = rel_path.split(os.sep)
            file_cat = _get_cat(parts)

            parent_id = ""

            for i, part in enumerate(parts[:-1]):
                current_path_str = os.path.join(*parts[:i+1])
                if current_path_str not in folder_ids:
                    is_category = (parts[0] == "tests" and i == 1) or (parts[0] != "tests" and i == 0)
                    folder_cat = _get_cat(parts[:i+1])
                    tag = CAT_TAGS.get(folder_cat, "cat_default")
                    is_root = (parts[0] == "tests" and i == 0)
                    if is_category and current_path_str in category_counts:
                        icon = CAT_ICONS.get(folder_cat, "📂")
                        display = CAT_LABELS.get(folder_cat, part.capitalize())
                        label = f"⬜ {icon} {display}  ({category_counts[current_path_str]})"
                        tags = (tag, "folder_root")
                    elif is_root:
                        label = f"⬜ 📁 {part.replace('_', ' ').capitalize()}  ({total_tests})"
                        tags = (tag, "folder_root")
                    else:
                        label = f"⬜ 📁 {part.replace('_', ' ').capitalize()}"
                        tags = (tag, "subfolder")
                    # só tests raiz abre; categorias e subpastas: recolhidas
                    should_open = is_root
                    folder_id = self.tree.insert(parent_id, "end", text=label, open=should_open, values=("folder", current_path_str), tags=tags)
                    folder_ids[current_path_str] = folder_id
                parent_id = folder_ids[current_path_str]

            tag = CAT_TAGS.get(file_cat, "cat_default")
            display = _fmt_file(file_name)
            self.tree.insert(parent_id, "end", text=f"⬜ 🐍 {display}", values=("file", full_path), tags=(tag,))

    def on_tree_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id: return

        element = self.tree.identify_element(event.x, event.y)
        if "text" not in element: return 

        values = self.tree.item(item_id, "values") 
        item_type = values[0] if values else None
        current_text = self.tree.item(item_id, "text")
        
        new_state = False
        if "⬜" in current_text:
            new_text = current_text.replace("⬜", "✅")
            new_state = True
        elif "✅" in current_text:
            new_text = current_text.replace("✅", "⬜")
            new_state = False
        else: return 

        self.tree.item(item_id, text=new_text)
        
        if item_type == "folder": self._propagar_selecao(item_id, new_state)
        
        self._recalcular_fila()

    def _propagar_selecao(self, parent_id, check):
        icon = "✅" if check else "⬜"
        children = self.tree.get_children(parent_id)
        for child in children:
            text = self.tree.item(child, "text")
            if "⬜" in text: new_text = text.replace("⬜", icon)
            elif "✅" in text: new_text = text.replace("✅", icon)
            else: new_text = text
            
            self.tree.item(child, text=new_text)
            self._propagar_selecao(child, check)

    def _recalcular_fila(self):
        self.fila_de_execucao = []
        
        def varrer(item_id):
            text = self.tree.item(item_id, "text")
            values = self.tree.item(item_id, "values")
            
            if "✅" in text and values and values[0] == "file":
                self.fila_de_execucao.append(values[1])
            
            for child in self.tree.get_children(item_id):
                varrer(child)
        
        for child in self.tree.get_children(""):
            varrer(child)
            
        self.atualizar_label_fila()

    def _atualizar_aviso_e2e_full(self):
        """Mostra/oculta banner de aviso quando Modo E2E Full está ativo."""
        if self.config_vars["run_e2e_full"].get():
            self.lbl_e2e_full_aviso.pack(fill=tk.X, pady=(0, 4))
        else:
            self.lbl_e2e_full_aviso.pack_forget()

    def atualizar_label_fila(self):
        if not self.fila_de_execucao:
            self.lbl_status_fila.config(text="Fila: (Vazia)", fg="gray")
            return
        nomes = [os.path.basename(f).replace('test_', '').replace('.py', '') for f in self.fila_de_execucao]
        texto_fila = ' ➔ '.join(nomes)
        if len(texto_fila) > 60: texto_fila = texto_fila[:60] + "..."
        self.lbl_status_fila.config(text=f"Fluxo: {texto_fila}", fg="#007acc")

    # ==========================================================================
    # MODO SIMULTÂNEO - MÚLTIPLOS DEVICES
    # ==========================================================================

    def _criar_aba_log(self, udid, titulo):
        """Cria aba no log_notebook e retorna o ScrolledText configurado."""
        frame = ttk.Frame(self.log_notebook)
        self.log_notebook.add(frame, text=titulo)
        widget = scrolledtext.ScrolledText(frame, bg="#1e1e1e", fg="#d4d4d4", font=('Consolas', 10), state='disabled')
        widget.pack(fill=tk.BOTH, expand=True)
        widget.tag_config('INFO', foreground='#6a9955')
        widget.tag_config('ERROR', foreground='#f44747', font=('Consolas', 10, 'bold'))
        widget.tag_config('SYSTEM', foreground='#569cd6', font=('Consolas', 10, 'bold'))
        widget.tag_config('SUCCESS', foreground='#4ec9b0', font=('Consolas', 12, 'bold'))
        widget.tag_config('WARNING', foreground='#dcdcaa')
        if udid:
            self.log_widgets[udid] = widget
        return widget

    def _toggle_simultaneo(self):
        if self.simultaneo_var.get():
            self.frame_devices.pack(side=tk.TOP, fill=tk.X, pady=(0, 4))
            self._atualizar_painel_devices()
        else:
            self.frame_devices.pack_forget()
            self.devices_para_rodar = []

    def _detectar_devices_adb(self):
        """Detecta devices Android via ADB. Retorna [(udid, model), ...]."""
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        flags = {"creationflags": subprocess.CREATE_NO_WINDOW, "startupinfo": si}

        devices = []
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True, text=True, timeout=5, **flags
            )
            for linha in result.stdout.strip().split('\n')[1:]:
                linha = linha.strip()
                if '\tdevice' in linha:
                    udid = linha.split('\t')[0].strip()
                    if not udid:
                        continue
                    try:
                        r = subprocess.run(
                            ["adb", "-s", udid, "shell", "getprop", "ro.product.model"],
                            capture_output=True, text=True, timeout=3, **flags
                        )
                        model = r.stdout.strip() or udid
                    except Exception:
                        model = udid
                    devices.append((udid, model))
        except Exception:
            pass
        return devices

    def _atualizar_painel_devices(self):
        self.devices_para_rodar = self._detectar_devices_adb()
        self._sincronizar_listbox_devices()
        if not self.devices_para_rodar:
            self.devices_listbox.insert(tk.END, "(nenhum device detectado)")

    def _sincronizar_listbox_devices(self):
        self.devices_listbox.delete(0, tk.END)
        for i, (udid, model) in enumerate(self.devices_para_rodar, 1):
            self.devices_listbox.insert(tk.END, f"[{i}] {model}  ({udid})")

    def _mover_device_up(self):
        sel = self.devices_listbox.curselection()
        if not sel or sel[0] == 0:
            return
        idx = sel[0]
        self.devices_para_rodar[idx], self.devices_para_rodar[idx - 1] = \
            self.devices_para_rodar[idx - 1], self.devices_para_rodar[idx]
        self._sincronizar_listbox_devices()
        self.devices_listbox.selection_set(idx - 1)

    def _mover_device_down(self):
        sel = self.devices_listbox.curselection()
        if not sel or sel[0] >= len(self.devices_para_rodar) - 1:
            return
        idx = sel[0]
        self.devices_para_rodar[idx], self.devices_para_rodar[idx + 1] = \
            self.devices_para_rodar[idx + 1], self.devices_para_rodar[idx]
        self._sincronizar_listbox_devices()
        self.devices_listbox.selection_set(idx + 1)

    def _preparar_log_notebook_para_devices(self, devices):
        """Apaga abas existentes e cria uma aba por device."""
        for tab_id in self.log_notebook.tabs():
            self.log_notebook.forget(tab_id)
        self.log_widgets = {}
        for udid, model in devices:
            nome_curto = model[:14] if len(model) > 14 else model
            self._criar_aba_log(udid, f"⏳ {nome_curto}")

    def _parar_simultaneo(self):
        self.parar_simultaneo = True
        if self.pytest_proc:
            try: self.pytest_proc.terminate()
            except: pass
        self.btn_run.config(state=tk.DISABLED, text="PARANDO...", bg="#7f8c8d")

    def _rodar_todos_devices(self, devices, test_files):
        """Thread: roda todos os testes em cada device sequencialmente."""
        # Verifica Appium uma única vez antes de iniciar
        if not self.aguardar_appium():
            self.root.after(0, self.escrever_log, "ABORTADO: Appium não detectado.", 'ERROR')
            self.root.after(0, self.finalizar_execucao)
            return

        total_pass = 0
        total_fail = 0

        for i, (udid, model) in enumerate(devices):
            if self.parar_simultaneo:
                break

            # Ativa aba deste device e aponta log_area para ela
            self.log_area = self.log_widgets[udid]
            self.pass_count = 0
            self.fail_count = 0
            self.root.after(0, lambda idx=i: self.log_notebook.select(idx))
            self.root.after(0, lambda idx=i, m=model: self.log_notebook.tab(idx, text=f"▶ {m[:14]}"))
            self.root.after(0, lambda: self.lbl_pass.config(text="✔ APROVADOS: 0"))
            self.root.after(0, lambda: self.lbl_fail.config(text="❌ FALHAS: 0"))

            self.root.after(0, self.escrever_log,
                            f"[SYSTEM] ═══ Device {i+1}/{len(devices)}: {model} ({udid}) ═══", 'SYSTEM')

            self.rodar_processo(test_files, device_id=udid, modelo=model, skip_finalize=True)

            total_pass += self.pass_count
            total_fail += self.fail_count

            # Atualiza título da aba com resultado
            if self.parar_simultaneo:
                self.root.after(0, lambda idx=i, m=model: self.log_notebook.tab(idx, text=f"⏹ {m[:14]}"))
            elif self.fail_count > 0 or (self.exit_code != 0 and self.exit_code != 1):
                self.root.after(0, lambda idx=i, m=model: self.log_notebook.tab(idx, text=f"✗ {m[:14]}"))
            else:
                self.root.after(0, lambda idx=i, m=model: self.log_notebook.tab(idx, text=f"✓ {m[:14]}"))

        # Restaura contadores totais para finalizar_execucao
        self.pass_count = total_pass
        self.fail_count = total_fail
        self.root.after(0, lambda: self.lbl_pass.config(text=f"✔ APROVADOS: {total_pass}"))
        self.root.after(0, lambda: self.lbl_fail.config(text=f"❌ FALHAS: {total_fail}"))
        self.root.after(0, self.finalizar_execucao)

    def setup_tab_config(self):
        # Canvas com scrollbar para comportar todos os campos
        canvas = tk.Canvas(self.tab_config, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_config, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding="20")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind scroll do mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Usar scrollable_frame ao invés de frame daqui em diante
        frame = scrollable_frame
        r = 0

        # === DADOS DO SISTEMA ===
        ttk.Label(frame, text="Dados do Sistema", font=('Segoe UI', 12, 'bold')).grid(row=r, column=0, columnspan=3, pady=(0, 10), sticky="w")
        r += 1

        campos_sistema = [
            ("IP do Servidor:", "server_ip", "Endereço IP do servidor backend (ex: ***SERVER_IP***)"),
            ("Porta API:", "server_port", "Porta da API REST do servidor (ex: ***SERVER_PORT***)"),
            ("Empresa:", "company", "Código da empresa no sistema (ex: 382)"),
            ("Usuario:", "user", "Usuário para login no PDV (ex: SERVER)"),
            ("Senha:", "password", "Senha do usuário para autenticação"),
            ("ID Cliente (Vendas):", "customer_id", "ID do cliente usado em vendas normais"),
            ("ID Cliente (Trocas):", "customer_id_troca", "ID do cliente específico para testes de troca"),
            ("ID Cliente (Bonus):", "customer_id_bonus", "ID do cliente com saldo de bônus/cashback para testes de bônus"),
            ("Timeout (seg):", "timeout_default", "Tempo máximo de espera para ações (segundos)")
        ]

        for label, var, tooltip in campos_sistema:
            ttk.Label(frame, text=label).grid(row=r, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(frame, textvariable=self.config_vars[var], width=40)
            entry.grid(row=r, column=1, sticky="w", padx=5, pady=5)
            ToolTip(entry, tooltip)
            r += 1

        ttk.Separator(frame, orient='horizontal').grid(row=r, column=0, columnspan=3, sticky="ew", pady=15)
        r += 1

        # Nova categoria: Produtos
        ttk.Label(frame, text="Produtos para Testes", font=('Segoe UI', 12, 'bold')).grid(
            row=r, column=0, columnspan=3, pady=(0, 10), sticky="w"
        )
        r += 1

        campos_produtos = [
            ("Produto Vendas Normais:", "product_code_sale", "Usado em: venda consumidor, venda cliente, pedido venda"),
            ("Produto Bonus/Cashback:", "product_code", "Usado em: testes de bonus, validar cashback e opções de item"),
            ("Produto Venda Futura:", "product_code_future_sale", "Usado em: venda futura retirada e domicílio"),
            ("Tamanho (Venda Futura):", "product_size_future", "Tamanho do produto para vendas futuras"),
            ("Produto Estoque 1:", "product_code_stock_1", "Primeiro produto para testes de estoque"),
            ("Produto Estoque 2:", "product_code_stock_2", "Segundo produto para testes de estoque")
        ]

        for label, var, tooltip in campos_produtos:
            ttk.Label(frame, text=label).grid(row=r, column=0, sticky="e", padx=5, pady=3)
            entry = ttk.Entry(frame, textvariable=self.config_vars[var], width=40)
            entry.grid(row=r, column=1, sticky="w", padx=5, pady=3)
            # Adicionar tooltip hover ao campo (sem label cinza)
            ToolTip(entry, tooltip)
            r += 1

        ttk.Separator(frame, orient='horizontal').grid(row=r, column=0, columnspan=3, sticky="ew", pady=15)
        r += 1

        # === ATALHOS DE PAGAMENTO (8 slots fixos) ===
        ttk.Label(frame, text="Atalhos de Pagamento", font=('Segoe UI', 12, 'bold')).grid(
            row=r, column=0, columnspan=3, pady=(0, 5), sticky="w")
        r += 1
        ttk.Label(frame,
                  text="8 slots fixos da tela de pagamento do app. "
                       "Mapeados automaticamente no startup (quando Appium estiver pronto). "
                       "Edite o JSON para ajustar tipos_venda e parcelas do Personalizado.",
                  font=('Segoe UI', 8), foreground="gray", wraplength=480).grid(
            row=r, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 8))
        r += 1

        # Grade com os 8 atalhos
        atalhos_frame = ttk.LabelFrame(frame, text="Atalhos descobertos", padding=6)
        atalhos_frame.grid(row=r, column=0, columnspan=3, sticky="ew", padx=5, pady=(0, 6))
        self._painel_formas_frame = atalhos_frame

        # Inicializa as variáveis dos 8 slots (se ainda não criadas no __init__)
        if not hasattr(self, "_atalhos_nome_vars"):
            self._atalhos_nome_vars  = [tk.StringVar() for _ in range(8)]
            self._atalhos_hab_vars   = [tk.BooleanVar(value=True) for _ in range(8)]
            self._atalhos_tipo_labels = []

        # Cabeçalho
        ttk.Label(atalhos_frame, text="Slot",   font=('Segoe UI', 8, 'bold'), width=6 ).grid(row=0, column=0, padx=4)
        ttk.Label(atalhos_frame, text="Nome da Forma", font=('Segoe UI', 8, 'bold'), width=30).grid(row=0, column=1, padx=4)
        ttk.Label(atalhos_frame, text="Tipo",   font=('Segoe UI', 8, 'bold'), width=14).grid(row=0, column=2, padx=4)
        ttk.Label(atalhos_frame, text="Testar", font=('Segoe UI', 8, 'bold'), width=6 ).grid(row=0, column=3, padx=4)
        ttk.Separator(atalhos_frame, orient='horizontal').grid(row=1, column=0, columnspan=4, sticky="ew", pady=2)

        self._atalhos_tipo_labels = []
        for i in range(8):
            slot_r = i + 2
            ttk.Label(atalhos_frame, text=f"Atalho {i+1}", font=('Segoe UI', 8), foreground="#555").grid(
                row=slot_r, column=0, sticky="e", padx=4, pady=2)
            entry = ttk.Entry(atalhos_frame, textvariable=self._atalhos_nome_vars[i], width=30)
            entry.grid(row=slot_r, column=1, sticky="w", padx=4, pady=2)
            ToolTip(entry, f"Nome do atalho {i+1} na tela de pagamento do app. Preenchido pelo discovery.")
            lbl_tipo = ttk.Label(atalhos_frame, text="—", width=14,
                                  font=('Segoe UI', 7), foreground="#888")
            lbl_tipo.grid(row=slot_r, column=2, sticky="w", padx=4)
            self._atalhos_tipo_labels.append(lbl_tipo)
            chk = ttk.Checkbutton(atalhos_frame, variable=self._atalhos_hab_vars[i],
                                   command=self._salvar_formas_json)
            chk.grid(row=slot_r, column=3, padx=4)
        r += 1

        # Botões
        atalhos_btn_frame = ttk.Frame(frame)
        atalhos_btn_frame.grid(row=r, column=0, columnspan=3, sticky="w", padx=5, pady=(4, 2))
        ttk.Button(atalhos_btn_frame, text="🔄 Descobrir Atalhos",
                   command=self._forcar_redescoberta_formas).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(atalhos_btn_frame, text="🔃 Recarregar",
                   command=self._recarregar_painel_formas).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(atalhos_btn_frame, text="📝 Abrir JSON",
                   command=self._abrir_formas_json).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(atalhos_btn_frame, text="💾 Salvar",
                   command=self._salvar_formas_json).pack(side=tk.LEFT)
        r += 1

        # Carrega painel após a UI estar pronta
        self.root.after(500, self._recarregar_painel_formas)

        ttk.Separator(frame, orient='horizontal').grid(row=r, column=0, columnspan=3, sticky="ew", pady=15)
        r += 1

        ttk.Label(frame, text="Infraestrutura e Pastas", font=('Segoe UI', 12, 'bold')).grid(row=r, column=0, columnspan=3, pady=(0, 10), sticky="w")
        r += 1

        ttk.Label(frame, text="Projeto QA Dev (Raiz):").grid(row=r, column=0, sticky="e", padx=5)
        entry_qa = ttk.Entry(frame, textvariable=self.config_vars["qa_dev_path"], width=40)
        entry_qa.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(entry_qa, "Caminho raiz do projeto de testes (onde ficam os testes E2E)")
        ttk.Button(frame, text="Selecionar", command=self.selecionar_pasta_projeto).grid(row=r, column=2, padx=5)
        r += 1

        ttk.Label(frame, text="Arquivo Settings:", font=('Segoe UI', 9)).grid(row=r, column=0, sticky="e", padx=5)
        entry_settings_path = ttk.Entry(frame, textvariable=self.settings_file_var, width=40, state='readonly')
        entry_settings_path.grid(row=r, column=1, sticky="w", padx=5)
        ttk.Button(frame, text="📂", width=3, command=self.selecionar_settings_arquivo).grid(row=r, column=2, padx=5)
        ToolTip(entry_settings_path, "Arquivo settings.json ativo. Salvamentos usam este arquivo.\nClique em 📂 para trocar o arquivo ativo.")
        r += 1

        ttk.Label(frame, text="Porta Appium:").grid(row=r, column=0, sticky="e", padx=5)
        entry_port = ttk.Entry(frame, textvariable=self.config_vars["appium_port"], width=10)
        entry_port.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(entry_port, "Porta onde o servidor Appium está rodando (padrão: 4723)")
        r += 1

        ttk.Label(frame, text="Caminho Appium (Opcional):").grid(row=r, column=0, sticky="e", padx=5)
        entry_appium = ttk.Entry(frame, textvariable=self.config_vars["appium_path"], width=40)
        entry_appium.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(entry_appium, "Caminho do executável do Appium (deixe vazio para usar PATH do sistema)")
        ttk.Button(frame, text="Buscar", command=self.selecionar_appium_manual).grid(row=r, column=2, padx=5)
        r += 1

        ttk.Separator(frame, orient='horizontal').grid(row=r, column=0, columnspan=3, sticky="ew", pady=20)
        r += 1
        
        ttk.Label(frame, text="Preferências de Execução", font=('Segoe UI', 12, 'bold')).grid(row=r, column=0, columnspan=3, pady=(0, 10), sticky="w")
        r += 1

        chk_clean = ttk.Checkbutton(frame, text="Limpar logs/prints antigos antes de rodar", variable=self.config_vars["clean_logs"])
        chk_clean.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_clean, "Remove arquivos de log anteriores antes de iniciar os testes")
        r += 1

        chk_open = ttk.Checkbutton(frame, text="Abrir relatório padrão automaticamente ao finalizar", variable=self.config_vars["auto_open"])
        chk_open.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_open, "Abre o relatório HTML automaticamente quando os testes terminarem")
        r += 1

        # Flags do Allure
        chk_allure = ttk.Checkbutton(frame, text="Gerar Relatório Allure (Base)", variable=self.config_vars["use_allure"])
        chk_allure.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_allure, "Gera relatório Allure em formato multi-página (requer servidor)")
        r += 1

        chk_single = ttk.Checkbutton(frame, text="Gerar Arquivo Único (allure-combine)", variable=self.config_vars["generate_single_file"])
        chk_single.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_single, "Combina o relatório Allure em um único arquivo HTML portável")
        r += 1

        chk_allure_open = ttk.Checkbutton(frame, text="Abrir Relatório Allure ao final", variable=self.config_vars["open_allure_end"])
        chk_allure_open.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_allure_open, "Abre o relatório Allure automaticamente (servidor ou arquivo único)")
        r += 1

        # --- SEÇÃO: Configurações de Impressão ---
        ttk.Separator(frame, orient='horizontal').grid(row=r, column=0, columnspan=3, sticky="ew", pady=20)
        r += 1

        ttk.Label(frame, text="Configurações de Impressão", font=('Segoe UI', 12, 'bold')).grid(row=r, column=0, columnspan=3, pady=(0, 10), sticky="w")
        r += 1

        # Checkbox 1: Cupom de Venda
        chk_cupom_venda = ttk.Checkbutton(frame, text="Cupom de Venda (padrão após finalizar)", variable=self.config_vars["print_cupom_venda"])
        chk_cupom_venda.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_cupom_venda, "Desmarcado = Clica NÃO no diálogo | Marcado = Clica SIM no diálogo")
        r += 1

        # Checkbox 2: NFC-E
        chk_nfce = ttk.Checkbutton(frame, text="NFC-E (Nota Fiscal Consumidor)", variable=self.config_vars["print_nfce"])
        chk_nfce.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_nfce, "Desmarcado = Não clica no botão | Marcado = Clica no botão + SIM no diálogo")
        r += 1

        # Checkbox 3: DANFE
        chk_danfe = ttk.Checkbutton(frame, text="DANFE via Servidor (NF-e)", variable=self.config_vars["print_danfe"])
        chk_danfe.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_danfe, "Desmarcado = Não clica no botão | Marcado = Clica no botão + OK na mensagem")
        r += 1

        # Checkbox 4: Cupom de Troca
        chk_cupom_troca = ttk.Checkbutton(frame, text="Cupom de Troca", variable=self.config_vars["print_cupom_troca"])
        chk_cupom_troca.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_cupom_troca, "Desmarcado = Não clica no botão | Marcado = Clica no botão + SIM no diálogo")
        r += 1

        # Checkbox 5: Giftback Receipt
        chk_giftback = ttk.Checkbutton(frame, text="Giftback Receipt (cashback utilizado)", variable=self.config_vars["print_giftback"])
        chk_giftback.grid(row=r, column=1, sticky="w", padx=5)
        ToolTip(chk_giftback, "Ativo somente em testes que usam cashback (switch_cashback marcado)\nDesmarcado = descarta botão automaticamente | Marcado = clica btn_share_giftback_receipt")
        r += 1

        # Campo: Timeout do Diálogo
        ttk.Label(frame, text="Timeout Diálogo (seg):").grid(row=r, column=0, sticky="e", padx=5, pady=3)
        entry_timeout = ttk.Entry(frame, textvariable=self.config_vars["print_dialog_timeout"], width=10)
        entry_timeout.grid(row=r, column=1, sticky="w", padx=5, pady=3)
        ToolTip(entry_timeout, "Tempo máximo em segundos para aguardar diálogo de impressão aparecer (padrão: 20)")
        r += 1

        ttk.Separator(frame, orient='horizontal').grid(row=r, column=0, columnspan=3, sticky="ew", pady=20)
        r += 1

        # === SEÇÃO: ORDEM E2E ===
        ttk.Label(frame, text="Execução E2E Automática", font=('Segoe UI', 12, 'bold')).grid(row=r, column=0, columnspan=3, pady=(0, 10), sticky="w")
        r += 1

        chk_run_e2e = ttk.Checkbutton(frame, text="🚀 Rodar E2E Full (ordem automática)", variable=self.config_vars["run_e2e_full"])
        chk_run_e2e.grid(row=r, column=0, columnspan=3, sticky="w", pady=5)
        ToolTip(chk_run_e2e,
            "Quando ativado, ignora a seleção manual e executa TODOS os testes E2E\n"
            "na ordem definida no arquivo JSON (respeitando dependências).\n\n"
            "Se desativado, funciona normalmente (seleção manual na árvore).")
        r += 1

        ttk.Label(frame, text="Arquivo de Ordem E2E:", font=('Segoe UI', 9)).grid(row=r, column=0, sticky="w", pady=5)
        entry_order = ttk.Entry(frame, textvariable=self.config_vars["e2e_order_file"], width=40)
        entry_order.grid(row=r, column=1, sticky="w", padx=5)

        btn_sel_order = ttk.Button(frame, text="📂", width=3, command=self.selecionar_ordem_e2e)
        btn_sel_order.grid(row=r, column=2, sticky="w")
        ToolTip(btn_sel_order, "Selecionar arquivo JSON com a ordem dos testes E2E")

        ToolTip(entry_order,
            "Caminho do arquivo JSON que define a ordem de execução.\n"
            "Exemplo: test_order_e2e.json\n\n"
            "Deixe vazio para usar o padrão (templates/test_order_e2e.json)")
        r += 1

        ttk.Separator(frame, orient='horizontal').grid(row=r, column=0, columnspan=3, sticky="ew", pady=20)
        r += 1

        frame_btn = ttk.Frame(frame)
        frame_btn.grid(row=r, column=0, columnspan=3, pady=10)

        btn_salvar = ttk.Button(frame_btn, text="💾 Salvar Configurações", command=lambda: self.salvar_settings(mostrar_msg=True))
        btn_salvar.pack(side=tk.LEFT, padx=5)
        ToolTip(btn_salvar, "Salva todas as configurações no arquivo settings.json")

        btn_exportar = ttk.Button(frame_btn, text="📤 Exportar Settings", command=self.exportar_settings)
        btn_exportar.pack(side=tk.LEFT, padx=5)
        ToolTip(btn_exportar, "Salva configurações com nome diferente (ex: settings_prod.json)")

        btn_importar = ttk.Button(frame_btn, text="📥 Importar Settings", command=self.importar_settings)
        btn_importar.pack(side=tk.LEFT, padx=5)
        ToolTip(btn_importar, "Carrega configurações de outro arquivo settings.json")

        btn_verificar = ttk.Button(frame_btn, text="🔍 Verificar Ambiente", command=lambda: self.verificar_dependencias_startup(silent=False))
        btn_verificar.pack(side=tk.LEFT, padx=5)
        ToolTip(btn_verificar, "Verifica se Appium, ADB e outras dependências estão instaladas")

        btn_reload = ttk.Button(frame_btn, text="🔄 Recarregar Testes", command=self.atualizar_lista_testes)
        btn_reload.pack(side=tk.LEFT, padx=5)
        ToolTip(btn_reload, "Recarrega a lista de testes disponíveis do projeto")

    def salvar_settings(self, mostrar_msg=True):
        data = {k: v.get() for k, v in self.config_vars.items()}
        target = getattr(self, 'settings_file_var', None)
        target = target.get() if target else SETTINGS_FILE
        if not target:
            target = SETTINGS_FILE
        try:
            with open(target, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)
            if mostrar_msg:
                messagebox.showinfo("Sucesso", f"Configurações salvas em:\n{target}")
            self.atualizar_lista_testes()
        except Exception as e:
            if mostrar_msg: messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def exportar_settings(self):
        """Exporta configurações atuais para um arquivo com nome personalizado."""
        data = {k: v.get() for k, v in self.config_vars.items()}

        # Sugere nome padrão baseado na configuração atual
        sugestao_nome = f"settings_{data.get('company', 'default')}_{data.get('server_ip', '').replace('.', '_')}.json"

        arquivo = filedialog.asksaveasfilename(
            title="Exportar Configurações",
            defaultextension=".json",
            initialfile=sugestao_nome,
            filetypes=[
                ("JSON Settings", "*.json"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                messagebox.showinfo("Sucesso", f"Configurações exportadas para:\n{arquivo}\n\nUse 'Importar Settings' para carregar depois.")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar: {e}")

    def importar_settings(self):
        """Importa configurações de um arquivo settings.json."""
        arquivo = filedialog.askopenfilename(
            title="Importar Configurações",
            filetypes=[
                ("JSON Settings", "*.json"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if arquivo:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Atualiza todas as variáveis de configuração
                for key, var in self.config_vars.items():
                    if key in data and data[key] is not None:
                        var.set(data[key])

                # Salva no settings.json padrão
                self.salvar_settings(mostrar_msg=False)

                messagebox.showinfo(
                    "Sucesso",
                    f"Configurações importadas de:\n{arquivo}\n\n"
                    f"Empresa: {data.get('company', 'N/A')}\n"
                    f"Servidor: {data.get('server_ip', 'N/A')}:{data.get('server_port', 'N/A')}\n"
                    f"Usuário: {data.get('user', 'N/A')}\n\n"
                    f"Todos os campos foram preenchidos!"
                )

                # Recarrega lista de testes com novo projeto
                self.atualizar_lista_testes()

            except json.JSONDecodeError:
                messagebox.showerror("Erro", "Arquivo JSON inválido!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao importar: {e}")

    def selecionar_pasta_projeto(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.config_vars["qa_dev_path"].set(caminho)
            self.salvar_settings(mostrar_msg=False)

    def selecionar_appium_manual(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Appium Executable", "*.cmd;*.exe;*.js")])
        if arquivo:
            self.config_vars["appium_path"].set(arquivo)

    def selecionar_settings_arquivo(self):
        """Seleciona outro settings.json, carrega os dados e o torna o arquivo ativo."""
        arquivo = filedialog.askopenfilename(
            title="Carregar arquivo Settings",
            initialdir=os.path.dirname(self.settings_file_var.get() or BASE_DIR),
            defaultextension=".json",
            filetypes=[("JSON Settings", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if not arquivo:
            return
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for key, var in self.config_vars.items():
                if key in data and data[key] is not None:
                    var.set(data[key])
            self.settings_file_var.set(arquivo)
            messagebox.showinfo(
                "Settings Carregado",
                f"Arquivo ativo:\n{arquivo}\n\n"
                f"Empresa: {data.get('company', 'N/A')}\n"
                f"Servidor: {data.get('server_ip', 'N/A')}:{data.get('server_port', 'N/A')}\n"
                f"Usuário: {data.get('user', 'N/A')}\n\n"
                f"Salvamentos futuros irão para este arquivo."
            )
            self.atualizar_lista_testes()
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Arquivo JSON inválido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar settings: {e}")

    def selecionar_ordem_e2e(self):
        """Seleciona arquivo JSON com a ordem dos testes E2E."""
        # Define diretório inicial (instalação ou dev)
        initial_dir = BASE_DIR
        templates_dir = os.path.join(BASE_DIR, "templates")
        if os.path.exists(templates_dir):
            initial_dir = templates_dir

        arquivo = filedialog.askopenfilename(
            title="Selecionar Ordem E2E",
            filetypes=[
                ("JSON Order File", "*.json"),
                ("Todos os arquivos", "*.*")
            ],
            initialdir=initial_dir
        )
        if arquivo:
            self.config_vars["e2e_order_file"].set(arquivo)
            self.salvar_settings(mostrar_msg=False)

            # Valida o arquivo
            try:
                ordem = self.carregar_ordem_e2e()
                messagebox.showinfo(
                    "Ordem E2E Carregada",
                    f"Arquivo de ordem carregado com sucesso!\n\n"
                    f"Total de testes: {len(ordem)}\n"
                    f"Testes obrigatórios: {sum(1 for t in ordem if t.get('required', False))}\n\n"
                    f"Marque 'Rodar E2E Full' para usar esta ordem."
                )
            except Exception as e:
                messagebox.showerror(
                    "Erro",
                    f"Erro ao validar arquivo de ordem:\n{e}\n\n"
                    f"Verifique se o JSON está correto."
                )

    def carregar_ordem_e2e(self):
        """Carrega a ordem dos testes E2E do arquivo JSON."""
        ordem_file = self.config_vars["e2e_order_file"].get()

        # Se não especificou, busca no padrão (instalação ou dev)
        if not ordem_file or not os.path.exists(ordem_file):
            # 1. Tenta na raiz (pós-instalação)
            ordem_file = os.path.join(BASE_DIR, "test_order_e2e.json")

            # 2. Se não encontrar, tenta em templates/ (modo dev)
            if not os.path.exists(ordem_file):
                ordem_file = os.path.join(BASE_DIR, "templates", "test_order_e2e.json")

        if not os.path.exists(ordem_file):
            raise FileNotFoundError(
                f"Arquivo de ordem não encontrado:\n{ordem_file}\n\n"
                f"Crie o arquivo ou selecione um existente."
            )

        with open(ordem_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if "test_order" not in data:
            raise ValueError("JSON inválido: campo 'test_order' não encontrado")

        return data["test_order"]

    def _encontrar_appium_path(self):
        """Busca Appium usando a função auxiliar robusta."""
        # 1. Primeiro verifica se há caminho manual configurado
        manual_path = self.config_vars["appium_path"].get()
        if manual_path and os.path.exists(manual_path):
            return manual_path

        # 2. Usa função auxiliar de busca robusta
        return _buscar_appium_instalado()

    def iniciar_appium_background(self):
        self.escrever_log("[SYSTEM] Verificando Appium...", 'SYSTEM')
        threading.Thread(target=self._iniciar_appium_thread, daemon=True).start()

    def _iniciar_appium_thread(self):
        port = self.config_vars["appium_port"].get()
        
        if self._aguardar_appium_interno(timeout=2):
            self.root.after(0, self.escrever_log, f"✅ Servidor Appium já estava rodando na porta {port}.", 'SUCCESS')
            return

        if self.appium_proc:
            self.root.after(0, self.escrever_log, "[SYSTEM] Reiniciando Appium na nova porta...", 'SYSTEM')
            self._matar_appium()

        appium_path = self._encontrar_appium_path()
        if not appium_path:
            self.root.after(0, self.escrever_log, "[ERRO] Appium não encontrado. Configure o caminho manualmente.", 'ERROR')
            return

        self.root.after(0, self.escrever_log, f"[SYSTEM] Iniciando Appium: {appium_path}", 'SYSTEM')

        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            cmd = ["cmd.exe", "/c", appium_path, "-p", port, "--log-level", "error:error"]
            
            self.appium_proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            def ler_erros():
                try:
                    out, err = self.appium_proc.communicate(timeout=5)
                    if self.appium_proc.returncode != 0:
                        msg = err.decode('utf-8', errors='ignore') if err else "Erro desconhecido"
                        self.root.after(0, self.escrever_log, f"[ERRO APPIUM] {msg}", 'ERROR')
                except: pass

            threading.Thread(target=ler_erros, daemon=True).start()

            if self._aguardar_appium_interno(timeout=15):
                self.root.after(0, self.escrever_log, f"✅ Appium iniciado com sucesso na porta {port}.", 'SUCCESS')
            else:
                self.root.after(0, self.escrever_log, "[AVISO] Appium demorou para responder.", 'WARNING')

        except Exception as e:
            self.root.after(0, self.escrever_log, f"[ERRO] Falha ao iniciar processo Appium: {e}", 'ERROR')

    def _matar_appium(self):
        if self.appium_proc:
            try:
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(self.appium_proc.pid)],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except: pass
            self.appium_proc = None

    def _aguardar_appium_interno(self, timeout=30):
        port = int(self.config_vars["appium_port"].get() or 4723)
        inicio = time.time()
        while time.time() - inicio < timeout:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                if sock.connect_ex(('127.0.0.1', port)) == 0:
                    sock.close(); return True
            except: pass
            time.sleep(1)
        return False

    def aguardar_appium(self, timeout=45):
        if self._aguardar_appium_interno(timeout=timeout):
            self.escrever_log("✅ Appium Confirmado.", 'SUCCESS')
            return True
        self.escrever_log("⚠️ Appium não respondeu.", 'WARNING')
        return False

    def iniciar_testes(self):
        if self._discovery_running:
            messagebox.showinfo(
                "Aguarde",
                "🔄 Mapeamento de formas POS em andamento.\n\nAguarde alguns segundos e tente novamente."
            )
            return

        # Flag para indicar se está em modo E2E Full
        self.e2e_full_mode = False

        # Aviso: E2E Full ativo vai ignorar seleção manual
        if self.config_vars["run_e2e_full"].get() and self.fila_de_execucao:
            continuar = messagebox.askyesno(
                "Modo E2E Full Ativo",
                "⚠️ 'Rodar E2E Full' está ativo na aba Configurações.\n\n"
                f"Sua seleção manual ({len(self.fila_de_execucao)} arquivo(s)) será IGNORADA "
                "e todos os testes E2E do JSON serão executados.\n\n"
                "Deseja continuar com E2E Full?\n"
                "(Clique NÃO para desativar E2E Full e rodar só a seleção manual)"
            )
            if not continuar:
                self.config_vars["run_e2e_full"].set(False)
                # Usa a seleção manual normalmente
            # Se sim: segue fluxo E2E Full abaixo

        # Modo E2E Full: carrega ordem do JSON
        if self.config_vars["run_e2e_full"].get():
            self.e2e_full_mode = True
            try:
                ordem_e2e = self.carregar_ordem_e2e()
                projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR

                # Monta lista de testes na ordem do JSON
                test_files = []
                testes_nao_encontrados = []

                for item in ordem_e2e:
                    test_name = item["name"]
                    # Busca o arquivo no projeto
                    test_path = None

                    # Caminho relativo (ex: "e2e/login/test_login.py") → resolve direto
                    if "/" in test_name or "\\" in test_name:
                        candidate = os.path.join(projeto_path, "tests", os.path.normpath(test_name))
                        if os.path.exists(candidate):
                            test_path = candidate
                    else:
                        # Legado: nome de arquivo plano (ex: "test_login.py")
                        # Busca em tests/e2e/ primeiro
                        e2e_path = os.path.join(projeto_path, "tests", "e2e", test_name)
                        if os.path.exists(e2e_path):
                            test_path = e2e_path
                        else:
                            # Busca recursivamente (fallback)
                            for root, dirs, files in os.walk(os.path.join(projeto_path, "tests")):
                                if test_name in files:
                                    test_path = os.path.join(root, test_name)
                                    break

                    if test_path:
                        test_files.append(test_path)
                    else:
                        testes_nao_encontrados.append(test_name)

                if testes_nao_encontrados:
                    aviso = f"⚠️ {len(testes_nao_encontrados)} teste(s) do JSON não encontrado(s):\n"
                    for t in testes_nao_encontrados[:5]:
                        aviso += f"  - {t}\n"
                    if len(testes_nao_encontrados) > 5:
                        aviso += f"  ... e mais {len(testes_nao_encontrados)-5}"

                    messagebox.showwarning("Testes Não Encontrados", aviso)

                if not test_files:
                    messagebox.showerror("Erro", "Nenhum teste E2E encontrado!\nVerifique o arquivo de ordem e o caminho do projeto.")
                    return

                # Substitui a fila de execução pela ordem E2E
                self.fila_de_execucao = test_files
                self.escrever_log(f"🚀 MODO E2E FULL ATIVADO", 'SYSTEM')
                self.escrever_log(f"Executando {len(test_files)} testes na ordem do JSON", 'INFO')

            except Exception as e:
                messagebox.showerror(
                    "Erro ao Carregar Ordem E2E",
                    f"Erro ao carregar arquivo de ordem:\n{e}\n\n"
                    f"Desative 'Rodar E2E Full' ou selecione um arquivo válido."
                )
                return

        # Modo normal: verifica se há testes selecionados
        if not self.fila_de_execucao:
            return messagebox.showwarning("Aviso", "Selecione um teste!")

        self.btn_run.config(state=tk.DISABLED, text="EXECUTANDO...", bg="#ca5100")
        self.resetar_dashboard()

        # --- MODO SIMULTÂNEO ---
        if self.simultaneo_var.get():
            devices = list(self.devices_para_rodar)
            if not devices:
                messagebox.showwarning("Aviso", "Nenhum device detectado! Clique em Atualizar.")
                self.btn_run.config(state=tk.NORMAL, text="▶ RODAR NA ORDEM", bg="#007acc")
                return
            self.modo_simultaneo_ativo = True
            self.parar_simultaneo = False
            self._preparar_log_notebook_para_devices(devices)
            self.btn_run.config(
                state=tk.NORMAL, text="⏹ PARAR", bg="#c0392b",
                command=self._parar_simultaneo
            )
            threading.Thread(
                target=self._rodar_todos_devices,
                args=(devices, list(self.fila_de_execucao)),
                daemon=True
            ).start()
            return

        # --- MODO NORMAL (1 device) ---
        self.modo_simultaneo_ativo = False
        # Limpa a aba de log existente
        for tab_id in self.log_notebook.tabs():
            self.log_notebook.forget(tab_id)
        self.log_area = self._criar_aba_log("", "Log")
        threading.Thread(target=self.rodar_processo, args=(list(self.fila_de_execucao),), daemon=True).start()

    def _limpar_logs_antigos(self):
        """Limpa TODO o conteúdo da pasta logs no processo da thread."""
        projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR
        logs_dir = os.path.join(projeto_path, "logs")
        
        if not os.path.exists(logs_dir): return

        self.root.after(0, self.escrever_log, "[SYSTEM] Esvaziando pasta de logs...", 'SYSTEM')
        
        try:
            for item in os.listdir(logs_dir):
                item_path = os.path.join(logs_dir, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    pass
            
            self.root.after(0, self.escrever_log, "[SYSTEM] Pasta logs limpa com sucesso.", 'SUCCESS')
        except Exception as e:
            self.root.after(0, self.escrever_log, f"[AVISO] Erro na limpeza: {e}", 'WARNING')

    def _sincronizar_staging(self):
        """Sincroniza Testes_PDV/ → staging/ antes de cada run (dev mode only)."""
        if not _DEV_MODE or not _TESTES_PDV_DIR:
            return
        if not os.path.isdir(_TESTES_PDV_DIR):
            self.escrever_log(f"[SYNC] Testes_PDV não encontrado: {_TESTES_PDV_DIR}", 'WARNING')
            return

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE

        cmd = [
            "robocopy", _TESTES_PDV_DIR, BASE_DIR,
            "/MIR",
            "/XD", "__pycache__", ".git",
            "/XF", "*.pyc", "settings.json",
            "/NFL", "/NDL", "/NJH", "/NJS", "/NC", "/NS"
        ]
        result = subprocess.run(
            cmd, startupinfo=si,
            creationflags=subprocess.CREATE_NO_WINDOW,
            capture_output=True
        )
        # robocopy: 0-7 = sucesso, 8+ = erro real
        if result.returncode >= 8:
            self.escrever_log(f"[SYNC] Erro robocopy (code={result.returncode})", 'WARNING')
        else:
            self.escrever_log("[SYNC] staging atualizado com Testes_PDV/", 'INFO')

    def rodar_processo(self, test_files, device_id=None, modelo=None, skip_finalize=False):
        self._sincronizar_staging()
        # 1. Limpeza (só no modo normal, evita limpar entre devices no simultâneo)
        if self.config_vars["clean_logs"].get() and not skip_finalize:
            self._limpar_logs_antigos()

        # 2. Appium Check (skip se chamado por _rodar_todos_devices, que já verificou)
        if not skip_finalize:
            if not self.aguardar_appium():
                self.root.after(0, self.escrever_log, "ABORTADO: Appium não detectado.", 'ERROR')
                self.root.after(0, self.finalizar_execucao)
                return

        projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR

        logs_dir = os.path.join(projeto_path, "logs")
        reports_dir = os.path.join(logs_dir, "reports")
        allure_dir = os.path.join(logs_dir, "allure-results")

        for p in [logs_dir, reports_dir, allure_dir]:
            if not os.path.exists(p):
                try: os.makedirs(p)
                except: pass

        # Nome do relatório inclui device quando em modo simultâneo
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        if device_id and modelo:
            nome_seguro = re.sub(r'[^\w\-]', '_', modelo)[:20]
            html_report_path = os.path.join(reports_dir, f"relatorio_{nome_seguro}_{ts}.html")
            txt_log = os.path.join(logs_dir, f"execucao_{nome_seguro}_{ts}.log")
        else:
            html_report_path = os.path.join(reports_dir, "relatorio_gui.html")
            txt_log = os.path.join(logs_dir, "execucao_tecnica.log")

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"  # Garante UTF-8 no processo filho
        env["PYTHONPATH"] = projeto_path + os.pathsep + env.get("PYTHONPATH", "")
        env["TEST_SERVER_IP"] = self.config_vars["server_ip"].get()
        env["TEST_SERVER_PORT"] = self.config_vars["server_port"].get()
        env["TEST_COMPANY"] = self.config_vars["company"].get()
        env["TEST_USER"] = self.config_vars["user"].get()
        env["TEST_PASSWORD"] = self.config_vars["password"].get()
        # Versão sem credenciais para uso em logs (nunca logar env diretamente)
        _CHAVES_SENSIVEIS = {"TEST_PASSWORD", "TEST_USER", "TEST_COMPANY", "TEST_SERVER_IP"}
        env_para_log = {k: v for k, v in env.items() if k not in _CHAVES_SENSIVEIS}  # noqa: F841
        # Flags de impressão: passados como env vars para garantir valores da UI
        env["TEST_PRINT_CUPOM_VENDA"] = "true" if self.config_vars["print_cupom_venda"].get() else "false"
        env["TEST_PRINT_NFCE"] = "true" if self.config_vars["print_nfce"].get() else "false"
        env["TEST_PRINT_DANFE"] = "true" if self.config_vars["print_danfe"].get() else "false"
        env["TEST_PRINT_CUPOM_TROCA"] = "true" if self.config_vars["print_cupom_troca"].get() else "false"
        env["TEST_PRINT_GIFTBACK"] = "true" if self.config_vars["print_giftback"].get() else "false"

        # MODO E2E FULL: Desabilita reordenamento do conftest.py
        if hasattr(self, 'e2e_full_mode') and self.e2e_full_mode:
            env["E2E_ORDER_MODE"] = "true"
            self.escrever_log("[SYSTEM] Modo E2E Full: mantendo ordem do JSON", 'SYSTEM')
        else:
            env["E2E_ORDER_MODE"] = "false"

        # MODO DEBUG: Passa DEBUG_MODE=true para ativar logs técnicos completos
        if self.mostrar_logs_tecnicos.get():
            env["DEBUG_MODE"] = "true"
            self.escrever_log("[SYSTEM] MODO DEBUG ATIVADO - Logs técnicos completos", 'SYSTEM')
        else:
            env["DEBUG_MODE"] = "false"

        worker_arg = "worker_pytest_runner"
        
        if getattr(sys, 'frozen', False):
            base_cmd = [sys.executable, worker_arg]
        else:
            base_cmd = [sys.executable, os.path.abspath(__file__), worker_arg]

        # Configuração base do pytest
        cmd = base_cmd + test_files + [
            "-v",  # Verbose
            "-s",  # Não captura stdout (permite prints)
            "-o", "log_cli=true",  # Exibe logs no console
            "-o", "log_cli_level=INFO",  # Nível de log no console
            f"-o", f"log_file={txt_log}",  # Arquivo de log técnico
            f"-o", f"log_file_level=DEBUG",  # Nível DEBUG no arquivo
            f"--html={html_report_path}",  # Relatório HTML
            "--self-contained-html",  # HTML com tudo embutido
            "--capture=no",  # Não captura output (mostra tudo)
        ]

        # Se modo debug ativado, aumenta verbosidade
        if self.mostrar_logs_tecnicos.get():
            cmd.extend([
                "-vv",  # Ainda mais verbose
                "-o", "log_cli_level=DEBUG",  # Nível DEBUG no console também
            ])
        
        # Device específico (modo simultâneo)
        if device_id:
            cmd.extend([f"--device-id={device_id}"])
            appium_port = int(self.config_vars["appium_port"].get() or 4723)
            cmd.extend([f"--appium-port={appium_port}"])

        if self.config_vars["use_allure"].get():
            cmd.append(f"--alluredir={allure_dir}")

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        try:
            self.pytest_proc = subprocess.Popen(cmd, cwd=projeto_path, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     universal_newlines=True, startupinfo=startupinfo, encoding='utf-8', errors='replace', bufsize=1)

            # Processa cada linha em tempo real via root.after (thread-safe)
            for line in self.pytest_proc.stdout:
                self.root.after(0, self.processar_linha_log, line)

            self.pytest_proc.wait()
            self.exit_code = self.pytest_proc.returncode
            if not skip_finalize:
                self.root.after(0, self.finalizar_execucao)
        except Exception as e:
            self.root.after(0, self.escrever_log, f"ERRO: {e}", 'ERROR')
            if not skip_finalize:
                self.root.after(0, self.finalizar_execucao)

    def processar_linha_log(self, linha):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        linha_limpa = ansi_escape.sub('', linha).strip()
        if not linha_limpa: return

        # FILTRO GLOBAL: Aplica tanto em modo normal quanto debug
        # Ignora logs de bibliotecas externas (Selenium, urllib3, etc.)
        if any(lib in linha_limpa for lib in [
            'selenium.webdriver', 'urllib3', 'DEBUG    selenium',
            'DEBUG    urllib3', 'DEBUG    appium', 'remote_connection',
            'connectionpool', 'Captured log setup', 'Captured log teardown',
            'Captured Log', 'Captured stdout setup', 'Captured stdout teardown',
            'Captured stderr', 'DEBUG    urllib3.connectionpool'
        ]):
            return

        # Ignora linhas muito longas (stack traces internos, JSONs gigantes, etc.)
        if len(linha_limpa) > 500:
            return

        # Ignora linhas vazias ou só com espaços
        if not linha_limpa.strip():
            return

        # ======================================================================
        # CONTADOR DE TESTES - Captura marcadores incluídos nas mensagens
        # ======================================================================
        if "[PASSED]" in linha_limpa:
            self.pass_count += 1
            self.lbl_pass.config(text=f"✔ APROVADOS: {self.pass_count}")
            # Exibe a mensagem completa (já vem formatada do conftest)
            self.escrever_log(linha_limpa, 'SUCCESS')
            return
        elif "[FAILED]" in linha_limpa:
            self.fail_count += 1
            self.lbl_fail.config(text=f"❌ FALHAS: {self.fail_count}")
            # Exibe a mensagem completa
            self.escrever_log(linha_limpa, 'ERROR')
            self.fail_lines.append(linha_limpa)
            return
        elif "[SKIPPED]" in linha_limpa:
            # Testes pulados não contam como falha
            self.escrever_log(linha_limpa, 'WARNING')
            return

        # Captura resumo final do pytest (backup)
        if "===" in linha_limpa and ("passed" in linha_limpa or "failed" in linha_limpa):
            try:
                passed = re.search(r'(\d+) passed', linha_limpa)
                failed = re.search(r'(\d+) failed', linha_limpa)
                if passed:
                    self.pass_count = int(passed.group(1))
                    self.lbl_pass.config(text=f"✔ APROVADOS: {self.pass_count}")
                if failed:
                    self.fail_count = int(failed.group(1))
                    self.lbl_fail.config(text=f"❌ FALHAS: {self.fail_count}")
            except: pass

        mostrar, tag, texto = False, 'NORMAL', linha_limpa

        # ======================================================================
        # FILTRO DE EXIBIÇÃO - UNIFICADO (Normal e Debug usam a mesma lógica)
        # ======================================================================

        # DIFERENÇA: Modo debug mostra TUDO quando há erro, normal ignora detalhes técnicos
        modo_debug_ativo = self.mostrar_logs_tecnicos.get()

        # 1. ERROS E FALHAS - SEMPRE mostra (ambos os modos)
        if any(palavra in linha_limpa for palavra in ["ERROR", "FAILED", "ERRO", "Traceback", "Exception", "AssertionError"]):
            mostrar, tag = True, 'ERROR'

        # 2. WARNINGS - SEMPRE mostra (ambos os modos)
        elif any(palavra in linha_limpa for palavra in ["WARNING", "WARN", "AVISO", "⚠️"]):
            mostrar, tag = True, 'WARNING'

        # === RESTO: Apenas visual limpo (ações do teste) ===

        # 3. Ações importantes (setas e símbolos de ação)
        elif any(linha_limpa.startswith(x) for x in ['→', '==>', '->', '> ', ': ', 'v ', '? ']):
            mostrar, tag = True, 'INFO'

        # 4. Marcadores de log
        elif any(x in linha_limpa for x in ['[CLICK]', '[DIGITAR]', '[SCROLL]', '[BUSCA]', '[VALIDAR]', '[FLUXO]', '[TYPE]']):
            mostrar, tag = True, 'INFO'

        # 5. Emojis e símbolos importantes
        elif any(icon in linha_limpa for icon in ["🖱️", "⌨️", "✅", "⏭️", "❌", "🔍", "📋", "✔️", "⏳"]):
            mostrar, tag = True, 'INFO'

        # 6. Mensagens de sistema
        elif any(x in linha_limpa for x in ["[SYSTEM]", "[AGUARDE]", "[OK]", "[AVISO]", "[WORKER]", "[ERRO]", "[INFO]"]):
            mostrar, tag = True, 'SYSTEM'
            if "[OK]" in linha_limpa or "✅" in linha_limpa:
                tag = 'SUCCESS'
            elif "[ERRO]" in linha_limpa or "[AVISO]" in linha_limpa:
                tag = 'WARNING'

        # 7. Separadores visuais - Encurtar
        elif linha_limpa.startswith("===") or linha_limpa.startswith("---"):
            texto = linha_limpa[0] * 7
            mostrar, tag = True, 'SYSTEM'

        # 8. Nomes de testes
        elif "::" in linha_limpa and "test_" in linha_limpa:
            mostrar = True
            try:
                nome = linha_limpa.split("::")[-1].replace("test_", "").replace(".py", "").title()
                texto = f"🧪 Executando: {nome}"
                tag = 'SYSTEM'
            except:
                tag = 'INFO'

        # 9. Palavras-chave de ações
        elif any(palavra in linha_limpa for palavra in [
            "Executando:", "Adicionando:", "Selecionando:", "Iniciando:", "Finalizando:",
            "Clicando:", "Digitando:", "Respondendo:", "Aguardando:", "Verificando:",
            "Buscando:", "Configurando:", "Avançando:", "Preenchendo:", "Usuario logado",
            "logado com sucesso", "Garantir", "garantir"
        ]):
            mostrar, tag = True, 'INFO'

        # 10. Resultados de assertivas
        elif any(palavra in linha_limpa for palavra in ["assert", "validando", "confirmando", "verificado"]):
            mostrar, tag = True, 'INFO'

        # === MODO DEBUG EXTRA: Mostra detalhes técnicos APENAS em contexto de erro ===
        if modo_debug_ativo and not mostrar:
            # Se a linha contém stack trace, detalhes de falha, ou INFO crítico
            if any(x in linha_limpa for x in ["File \"", "line ", "  at ", "AssertionError:", "raise ", "during "]):
                mostrar, tag = True, 'ERROR'
            # Logs INFO do pytest sobre erros
            elif "INFO" in linha_limpa and any(x in linha_limpa for x in ["failed", "error", "exception"]):
                mostrar, tag = True, 'WARNING'

        if mostrar:
            self.escrever_log(texto, tag)
            if tag == 'ERROR':
                self.fail_lines.append(texto)

    def escrever_log(self, texto, tag='NORMAL'):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, texto + "\n", tag)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def resetar_dashboard(self):
        self.start_time = time.time()
        self.is_running = True
        self.pass_count = 0; self.fail_count = 0; self.exit_code = 0
        self.fail_lines = []
        self.lbl_pass.config(text="✔ APROVADOS: 0")
        self.lbl_fail.config(text="❌ FALHAS: 0")
        self.progress.start(10)
        self.atualizar_cronometro()

    def atualizar_cronometro(self):
        if self.is_running:
            diff = int(time.time() - self.start_time)
            m, s = divmod(diff, 60); h, m = divmod(m, 60)
            self.lbl_timer.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            self.root.after(1000, self.atualizar_cronometro)

    def _rodar_categoria(self, pasta: str):
        """Coleta todos os testes de uma categoria (pasta) e executa."""
        if self.is_running:
            messagebox.showwarning("Aviso", "Já há uma execução em andamento.")
            return

        projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR
        categoria_path = os.path.join(projeto_path, "tests", pasta)

        if not os.path.exists(categoria_path):
            messagebox.showerror("Erro", f"Pasta não encontrada:\n{categoria_path}")
            return

        test_files = sorted(glob.glob(os.path.join(categoria_path, "**", "test_*.py"), recursive=True))
        if not test_files:
            messagebox.showwarning("Aviso", f"Nenhum teste encontrado em tests/{pasta}/")
            return

        self.e2e_full_mode = False
        self.fila_de_execucao = test_files
        self.btn_run.config(state=tk.DISABLED, text="EXECUTANDO...", bg="#ca5100")
        self.resetar_dashboard()
        self.escrever_log(f"{'=' * 50}", 'SYSTEM')
        self.escrever_log(f"🧪 Executando: {pasta.capitalize()} ({len(test_files)} arquivo(s))", 'SYSTEM')
        self.escrever_log(f"{'=' * 50}", 'SYSTEM')
        threading.Thread(target=self.rodar_processo, args=(test_files,), daemon=True).start()

    def finalizar_execucao(self):
        self.is_running = False
        self.progress.stop()
        self.modo_simultaneo_ativo = False
        self.btn_run.config(state=tk.NORMAL, text="▶ RODAR NA ORDEM", bg="#007acc", command=self.iniciar_testes)
        # Recarrega painel: se algum teste gerou/atualizou formas_pagamento.json, reflete aqui
        self.root.after(500, self._recarregar_painel_formas)
        self.escrever_log("-" * 50, 'SYSTEM')

        # 1. Abre Relatório Simples (não abre em modo simultâneo — múltiplos relatórios)
        if self.config_vars["auto_open"].get() and not self.modo_simultaneo_ativo:
            self.abrir_relatorio()

        # 2. Gerar e Abrir Allure (Thread para não travar)
        if self.config_vars["use_allure"].get():
            threading.Thread(target=self.gerar_e_abrir_allure_unico, daemon=True).start()

        if self.exit_code != 0 and self.exit_code != 1:
            self.escrever_log(f"ERRO CRÍTICO: Processo terminou com código {self.exit_code}", 'ERROR')
            messagebox.showerror("Erro Fatal", f"O executor de testes falhou.\nCódigo de erro: {self.exit_code}")
        elif self.fail_count > 0:
            self.escrever_log("FIM: TESTES FALHARAM.", 'ERROR')
            self._salvar_fail_log()
            messagebox.showwarning("Atenção", f"{self.fail_count} testes falharam.")
        elif self.pass_count > 0:
            self.escrever_log("FIM: SUCESSO TOTAL.", 'SUCCESS')
            messagebox.showinfo("Sucesso", "Todos os testes passaram!")
        else:
            self.escrever_log("ALERTA: Nenhum teste foi registrado.", 'WARNING')
            messagebox.showwarning("Aviso", "Nenhum teste rodou. Verifique sua seleção.")

    def _salvar_fail_log(self):
        """Grava fail.log.txt com apenas as linhas de erro da última execução."""
        try:
            projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR
            logs_dir = os.path.join(projeto_path, "logs")
            fail_log_path = os.path.join(logs_dir, "fail.log.txt")
            with open(fail_log_path, 'w', encoding='utf-8') as f:
                f.write(f"=== FALHAS — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                f.write(f"Total de falhas: {self.fail_count}\n")
                f.write("=" * 50 + "\n\n")
                for linha in self.fail_lines:
                    f.write(linha + "\n")
            self.escrever_log(f"[SYSTEM] fail.log.txt salvo em: {fail_log_path}", 'SYSTEM')
        except Exception as e:
            self.escrever_log(f"[AVISO] Não foi possível salvar fail.log.txt: {e}", 'WARNING')

    def fechar_programa(self):
        self._matar_appium()
        if self.pytest_proc:
            try: self.pytest_proc.terminate()
            except: pass
        if self.allure_proc:
            try: subprocess.run(f"taskkill /F /T /PID {self.allure_proc.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except: pass
        self.root.destroy()

    def abrir_relatorio(self):
        projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR
        caminhos = [
            os.path.join(projeto_path, "logs", "reports", "relatorio_gui.html"),
            os.path.join(projeto_path, "logs", "relatorio_gui.html"),
            os.path.join(projeto_path, "relatorio_gui.html")
        ]
        for p in caminhos:
            if os.path.exists(p): webbrowser.open(p); return
        self.escrever_log("[SYSTEM] Relatório não encontrado para abrir.", 'WARNING')

    def _get_free_port(self, exclude_ports=None):
        if exclude_ports is None: exclude_ports = []
        port = 5000
        while port < 6000:
            if port in exclude_ports:
                port += 1
                continue
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0: return port
            port += 1
        return 0

    def gerar_e_abrir_allure_unico(self):
        """
        1. Gera o relatório estático base (allure generate).
        2. Se 'generate_single_file' estiver marcado, converte em arquivo único (combine).
        3. Decide o que abrir com base em 'open_allure_end' e o que foi gerado.
        """
        projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR
        allure_results = os.path.join(projeto_path, "logs", "allure-results")
        allure_report_dir = os.path.join(projeto_path, "logs", "allure-report")
        
        if not os.path.exists(allure_results) or not os.listdir(allure_results):
            self.escrever_log("[AVISO] Nenhum resultado Allure para exibir.", 'WARNING')
            return

        allure_cmd = shutil.which("allure") or shutil.which("allure.bat")
        if not allure_cmd:
            self.escrever_log("[ERRO] Allure CLI não encontrado. Instale via botão de Ambiente.", 'ERROR')
            return

        # -----------------------------------------------------
        # PASSO 1: GERAR ESTATICO BASE
        # -----------------------------------------------------
        self.escrever_log("[SYSTEM] Gerando relatório Allure base...", 'SYSTEM')
        try:
            subprocess.run([allure_cmd, "generate", allure_results, "-o", allure_report_dir, "--clean"], 
                           cwd=projeto_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            self.escrever_log(f"[ERRO] Falha ao gerar Allure base: {e}", 'ERROR')
            return

        # -----------------------------------------------------
        # PASSO 2: GERAR ARQUIVO ÚNICO (COMBINE) - SE MARCADO
        # -----------------------------------------------------
        final_file_path = None
        
        if self.config_vars["generate_single_file"].get():
            self.escrever_log("[SYSTEM] Criando arquivo funcional único (allure-combine)...", 'SYSTEM')
            
            try:
                from allure_combine import combine_allure
                combine_allure(allure_report_dir)
                
                generated_file = os.path.join(allure_report_dir, "complete.html")
                
                if os.path.exists(generated_file):
                    # Move para reports com timestamp
                    reports_dir = os.path.join(projeto_path, "logs", "reports")
                    if not os.path.exists(reports_dir): os.makedirs(reports_dir)
                    
                    final_file_path = os.path.join(reports_dir, f"Allure_Completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
                    shutil.copy2(generated_file, final_file_path)
                    
                    self.escrever_log(f"[SUCESSO] Relatório Único salvo: {final_file_path}", 'SUCCESS')
                else:
                    self.escrever_log("[ERRO] Falha ao criar complete.html. Verifique a instalação.", 'ERROR')

            except Exception as e:
                self.escrever_log(f"[ERRO] Exceção no Combine: {e}", 'ERROR')

        # -----------------------------------------------------
        # PASSO 3: ABRIR RELATÓRIO (SE MARCADO)
        # -----------------------------------------------------
        if self.config_vars["open_allure_end"].get():
            # Prioridade: Arquivo Único (mais rápido) > Servidor
            if final_file_path and os.path.exists(final_file_path):
                self.escrever_log("[SYSTEM] Abrindo arquivo único no navegador...", 'SYSTEM')
                webbrowser.open(final_file_path)
            else:
                # Fallback: Servidor Allure
                self.abrir_servidor_allure()

    def abrir_servidor_allure(self):
        """Sobe o servidor Allure em porta segura."""
        projeto_path = self.config_vars["qa_dev_path"].get() or BASE_DIR
        allure_results = os.path.join(projeto_path, "logs", "allure-results")
        
        allure_cmd = shutil.which("allure") or shutil.which("allure.bat")
        
        # Mata processo anterior
        if self.allure_proc:
            try: 
                subprocess.run(f"taskkill /F /T /PID {self.allure_proc.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.allure_proc = None
            except: pass

        # Porta Segura
        try:
            appium_port = int(self.config_vars["appium_port"].get() or 4723)
        except: appium_port = 4723
            
        allure_port = self._get_free_port(exclude_ports=[appium_port])
        
        self.escrever_log(f"[SYSTEM] Iniciando Servidor Allure na porta {allure_port}...", 'SYSTEM')
        
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            self.allure_proc = subprocess.Popen(
                [allure_cmd, "serve", allure_results, "-p", str(allure_port)],
                cwd=projeto_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            self.escrever_log(f"[ERRO] Falha ao iniciar Allure Server: {e}", 'ERROR')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "worker_pytest_runner":
        args = sys.argv[2:]
        sys.exit(pytest.main(args))
    else:
        root = tk.Tk()
        app = TestRunnerApp(root)
        root.mainloop()