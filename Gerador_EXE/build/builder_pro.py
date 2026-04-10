r"""
Builder Pro - Pipeline de Build para QA Dashboard.
Compila o QA Dashboard com os artefatos do Testes_PDV.

Uso via bat:
    Duplo-clique em D:\PDV_AUTOMACAO\COMPILAR.bat
"""
import os
import sys
import json
import stat
import time
import shutil
import argparse
import importlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Optional


class Colors:
    """Cores ANSI para terminal."""
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"


def log(msg: str, level: str = "INFO"):
    """Log formatado."""
    colors = {
        "INFO": Colors.GREEN,
        "WARN": Colors.YELLOW,
        "ERROR": Colors.RED,
        "STEP": Colors.BLUE + Colors.BOLD,
    }
    color = colors.get(level, Colors.RESET)
    print(f"{color}[{level}]{Colors.RESET} {msg}")


def handle_remove_readonly(func, path, exc_info):
    """
    Handler para erros de permissão no Windows.
    Remove o atributo read-only e tenta novamente.
    """
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR | stat.S_IREAD)
        func(path)
    else:
        raise


def safe_rmtree(path, max_retries=3, retry_delay=1.0):
    """
    Remove diretório com retry para lidar com erros de permissão no Windows.

    Args:
        path: Caminho do diretório a ser removido
        max_retries: Número máximo de tentativas
        retry_delay: Tempo de espera entre tentativas (segundos)
    """
    path = Path(path)
    if not path.exists():
        return

    for attempt in range(max_retries):
        try:
            shutil.rmtree(path, onerror=handle_remove_readonly)
            return
        except PermissionError as e:
            if attempt < max_retries - 1:
                log(f"Tentativa {attempt + 1}/{max_retries} falhou ao remover {path.name}. "
                    f"Aguardando {retry_delay}s...", "WARN")
                time.sleep(retry_delay)
            else:
                log(f"Falha ao remover {path.name} após {max_retries} tentativas.", "ERROR")
                log(f"Feche qualquer programa que esteja usando arquivos em: {path}", "ERROR")
                raise


def safe_copy_tree(src, dst):
    """
    Copia árvore de diretórios de forma segura, sobrescrevendo arquivos existentes.
    Não tenta remover o diretório de destino, apenas atualiza os arquivos.

    Args:
        src: Diretório de origem
        dst: Diretório de destino
    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        return

    # Cria o diretório de destino se não existir
    dst.mkdir(parents=True, exist_ok=True)

    # Copia todos os arquivos e subdiretórios
    for item in src.rglob('*'):
        # Calcula o caminho relativo e o destino
        rel_path = item.relative_to(src)
        dst_item = dst / rel_path

        if item.is_dir():
            # Cria diretório se não existir
            dst_item.mkdir(parents=True, exist_ok=True)
        else:
            # Copia arquivo, sobrescrevendo se existir
            try:
                dst_item.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_item)
            except PermissionError:
                log(f"Aviso: Não foi possível copiar {rel_path} (arquivo em uso)", "WARN")


class BuilderPro:
    """Pipeline de build para o QA Dashboard."""

    def __init__(self, builder_dir: Path, qa_dev_dir: Path):
        self.builder_dir = Path(builder_dir).resolve()
        self.qa_dev_dir = Path(qa_dev_dir).resolve()

        # Diretorios de saida
        self.output_dir = self.builder_dir / "output"
        self.staging_dir = self.output_dir / "staging"
        self.dist_dir = self.output_dir / "dist"
        self.installer_dir = self.output_dir / "installer"

        # Arquivos de configuracao
        self.whitelist_file = self.builder_dir / "build" / "whitelist.json"
        self.whitelist = self._load_whitelist()

        # Versionamento
        self.version_file = self.qa_dev_dir / "VERSION"
        self.root_version_file = self.qa_dev_dir.parent / "VERSION"  # Arquivo VERSION na raiz do projeto
        self.version = self._load_and_increment_version()

        # Timestamp para nomes de arquivos
        self.timestamp = datetime.now().strftime("%Y_%m_%d")

    def _load_whitelist(self) -> dict:
        """Carrega configuracao de whitelist."""
        if self.whitelist_file.exists():
            with open(self.whitelist_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"core_files": [], "directories": {}, "exclude_patterns": []}

    def _load_and_increment_version(self) -> str:
        """Carrega a versao do arquivo VERSION e incrementa automaticamente."""
        if not self.version_file.exists():
            log("Arquivo VERSION não encontrado. Criando versão inicial 2.0.0", "WARN")
            initial_version = "2.0.0"
            with open(self.version_file, 'w', encoding='utf-8') as f:
                f.write(initial_version)
            return initial_version

        # Lê versão atual
        with open(self.version_file, 'r', encoding='utf-8') as f:
            current_version = f.read().strip()

        log(f"Versão atual: {current_version}", "INFO")

        # Incrementa patch version (último número)
        try:
            parts = current_version.split('.')
            if len(parts) == 3:
                major, minor, patch = parts
                new_patch = int(patch) + 1
                new_version = f"{major}.{minor}.{new_patch}"
            else:
                log("Formato de versão inválido. Mantendo versão atual.", "WARN")
                return current_version
        except Exception as e:
            log(f"Erro ao incrementar versão: {e}. Mantendo versão atual.", "WARN")
            return current_version

        # Salva nova versão em AMBOS os arquivos (Testes_PDV e raiz do projeto)
        with open(self.version_file, 'w', encoding='utf-8') as f:
            f.write(new_version)

        # Sincroniza com VERSION na raiz do projeto
        if self.root_version_file.exists() or self.root_version_file.parent.exists():
            try:
                with open(self.root_version_file, 'w', encoding='utf-8') as f:
                    f.write(new_version)
                log(f"VERSION na raiz do projeto também atualizado: {self.root_version_file}", "INFO")
            except Exception as e:
                log(f"Aviso: Não foi possível atualizar VERSION na raiz: {e}", "WARN")

        log(f"Nova versão: {new_version}", "STEP")
        return new_version

    def clean_python_cache(self):
        """Limpa TODO o cache Python (.pyc, __pycache__, .pytest_cache) antes do build."""
        log("Limpando cache Python completo...", "STEP")

        total_pycache = 0
        total_pyc = 0

        # Limpa __pycache__ recursivamente
        for pycache_dir in self.qa_dev_dir.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir, ignore_errors=True)
                total_pycache += 1
            except Exception as e:
                log(f"Aviso ao remover {pycache_dir}: {e}", "WARN")

        # Limpa .pyc recursivamente
        for pyc_file in self.qa_dev_dir.rglob("*.pyc"):
            try:
                pyc_file.unlink()
                total_pyc += 1
            except Exception as e:
                log(f"Aviso ao remover {pyc_file}: {e}", "WARN")

        # Limpa .pytest_cache
        pytest_cache = self.qa_dev_dir / ".pytest_cache"
        if pytest_cache.exists():
            shutil.rmtree(pytest_cache, ignore_errors=True)

        log(f"Cache limpo: {total_pycache} __pycache__, {total_pyc} .pyc removidos")

    def clean(self):
        """Limpa diretorios de build anteriores."""
        log("Limpando builds anteriores...", "STEP")

        for dir_path in [self.staging_dir, self.dist_dir]:
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                except PermissionError as e:
                    log(f"Arquivos em uso em {dir_path.name}. Build continuará com atualização incremental.", "WARN")
                except Exception as e:
                    log(f"Nao foi possivel limpar {dir_path}: {e}", "WARN")
            dir_path.mkdir(parents=True, exist_ok=True)

        self.installer_dir.mkdir(parents=True, exist_ok=True)
        log("Diretorios de build limpos")

    def stage_runner(self):
        """Copia arquivos do Runner para staging."""
        log("Copiando arquivos do Runner...", "STEP")

        runner_src = self.builder_dir / "runner"
        runner_dst = self.staging_dir

        if runner_src.exists():
            for file in runner_src.glob("*.py"):
                shutil.copy2(file, runner_dst)
                log(f"  + {file.name}")

        # Copia arquivo VERSION
        if self.version_file.exists():
            shutil.copy2(self.version_file, self.staging_dir / "VERSION")
            log("  + VERSION")

        # Assets
        assets_src = self.builder_dir / "assets"
        assets_dst = self.staging_dir / "assets"
        if assets_src.exists():
            safe_copy_tree(assets_src, assets_dst)
            log("  + assets/")
        else:
            log(f"Pasta assets nao encontrada na origem: {assets_src}", "WARN")

        # --- SCRIPTS DE INSTALAÇÃO ---
        scripts_src = self.builder_dir / "scripts"
        scripts_dst = self.staging_dir / "scripts"
        if scripts_src.exists():
            safe_copy_tree(scripts_src, scripts_dst)
            log("  + scripts/ (Para instalação de dependências)")
        else:
            log(f"Pasta scripts nao encontrada na origem: {scripts_src}", "WARN")

        # Templates
        templates_src = self.builder_dir / "templates"
        if templates_src.exists():
            settings_default = templates_src / "settings.default.json"
            if settings_default.exists():
                shutil.copy2(settings_default, self.staging_dir / "settings.json")
                log("  + settings.json (from template)")

            # Copiar arquivo de ordem E2E
            test_order_e2e = templates_src / "test_order_e2e.json"
            if test_order_e2e.exists():
                shutil.copy2(test_order_e2e, self.staging_dir / "test_order_e2e.json")
                log("  + test_order_e2e.json (from template)")

    def stage_qa_dev(self):
        """Copia artefatos do Projeto QA Dev para staging."""
        log(f"Importando artefatos de {self.qa_dev_dir}...", "STEP")

        if not self.qa_dev_dir.exists():
            log(f"Diretorio QA Dev nao encontrado: {self.qa_dev_dir}", "ERROR")
            return False

        # Core files
        whitelist_files = ["config.py", "conftest.py", "framework.py", "test_data.py", "pytest.ini", "requirements.txt"]
        whitelist_files.extend(self.whitelist.get("core_files", []))
        whitelist_files = list(set(whitelist_files))

        for filename in whitelist_files:
            src = self.qa_dev_dir / filename
            if src.exists():
                shutil.copy2(src, self.staging_dir / filename)
                log(f"  + {filename}")
            else:
                log(f"  - {filename} (nao encontrado na origem)", "WARN")

        # Directories
        dirs_config = self.whitelist.get("directories", {
            "pages": {"pattern": "*", "required": True},
            "tests": {"pattern": "*", "required": True},
            "xmls": {"pattern": "*", "required": False}
        })

        for dir_name, config in dirs_config.items():
            src_dir = self.qa_dev_dir / dir_name
            dst_dir = self.staging_dir / dir_name

            if not src_dir.exists():
                if config.get("required", False):
                    log(f"  - {dir_name}/ (obrigatorio, nao encontrado)", "ERROR")
                continue

            dst_dir.mkdir(parents=True, exist_ok=True)
            pattern = config.get("pattern", "*")

            files_copied = 0
            for file in src_dir.rglob(pattern):
                if file.is_file() and not self._is_excluded(file):
                    rel_path = file.relative_to(src_dir)
                    target_file = dst_dir / rel_path
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, target_file)
                    files_copied += 1

            log(f"  + {dir_name}/ ({files_copied} arquivos)")

            init_file = dst_dir / "__init__.py"
            if not init_file.exists(): init_file.touch()

        return True

    def _is_excluded(self, file_path: Path) -> bool:
        """Verifica se arquivo deve ser excluido."""
        name = file_path.name
        if "__pycache__" in str(file_path) or name.endswith(".pyc"): return True
        for pattern in self.whitelist.get("exclude_patterns", []):
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]): return True
            elif pattern in str(file_path): return True
        return False

    def verify_build_environment(self) -> bool:
        """Verifica se pacotes criticos estao instalados no ambiente de build."""
        log("Verificando pacotes criticos no ambiente de build...", "STEP")

        critical_packages = [
            "pytest", "pluggy", "_pytest", "iniconfig",
            "pytest_html", "pytest_metadata", # Adicionado para corrigir o erro do relatorio
            "allure_pytest", "allure_commons",
            "appium", "selenium",
            "faker", "requests",  # Adicionado para novos testes (bordero, cliente, historico)
        ]

        missing = []
        for pkg in critical_packages:
            try:
                importlib.import_module(pkg)
            except ImportError:
                missing.append(pkg)

        if not missing:
            log("Todos os pacotes criticos encontrados no ambiente de build")
            return True

        log(f"Pacotes FALTANDO no ambiente de build: {', '.join(missing)}", "ERROR")
        log("PyInstaller NAO consegue embutir pacotes que nao estao instalados!", "WARN")

        # Tenta instalar automaticamente
        log("Tentando instalar pacotes automaticamente...", "STEP")

        # Prioridade: requirements_build.txt (mínimo para build) > requirements.txt do projeto
        build_req_file = Path(__file__).parent / "requirements_build.txt"
        project_req_file = self.qa_dev_dir / "requirements.txt"

        if build_req_file.exists():
            install_cmd = [sys.executable, "-m", "pip", "install", "-r", str(build_req_file), "--quiet"]
            log(f"Usando requirements_build.txt: {build_req_file}")
        elif project_req_file.exists():
            install_cmd = [sys.executable, "-m", "pip", "install", "-r", str(project_req_file), "--quiet"]
            log(f"Usando requirements.txt: {project_req_file}")
        else:
            fallback_packages = ["pytest", "pytest-html", "pytest-metadata", "allure-pytest", "pluggy", "iniconfig"]
            install_cmd = [sys.executable, "-m", "pip", "install"] + fallback_packages
            log("requirements_build.txt nao encontrado, usando lista minima hardcoded", "WARN")

        try:
            result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                log(f"pip install falhou:\n{result.stderr}", "ERROR")
                return False
            log("Instalacao via pip concluida")
        except Exception as e:
            log(f"Erro ao instalar pacotes: {e}", "ERROR")
            return False

        # Reverifica apos install
        still_missing = []
        for pkg in missing:
            try:
                importlib.import_module(pkg)
            except ImportError:
                still_missing.append(pkg)

        if still_missing:
            log(f"Pacotes AINDA faltando apos install: {', '.join(still_missing)}", "ERROR")
            log("Build ABORTADO - pytest nao sera incluido no EXE sem estes pacotes", "ERROR")
            return False

        log("Todos os pacotes criticos instalados com sucesso")
        return True

    def compile_pyinstaller(self, onefile: bool = True, noconsole: bool = True) -> bool:
        """Compila com PyInstaller."""
        log("Compilando com PyInstaller...", "STEP")

        main_script = self.staging_dir / "app_runner.py"
        if not main_script.exists():
            log("app_runner.py nao encontrado no staging", "ERROR")
            return False

        # Limpa diretório build_temp antes de rodar PyInstaller
        build_temp_dir = self.output_dir / "build_temp"
        if build_temp_dir.exists():
            log("Limpando build_temp de builds anteriores...")
            for attempt in range(3):
                try:
                    shutil.rmtree(build_temp_dir, onerror=handle_remove_readonly)
                    log("Diretório build_temp limpo")
                    break
                except PermissionError:
                    if attempt < 2:
                        log(f"Tentativa {attempt + 1}/3: Aguardando processos liberarem arquivos...", "WARN")
                        time.sleep(2)
                    else:
                        log("Não foi possível limpar build_temp completamente. Continuando...", "WARN")
                except Exception as e:
                    log(f"Aviso ao limpar build_temp: {e}", "WARN")
                    break

        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name", "QA_Dashboard",
            "--distpath", str(self.dist_dir),
            "--workpath", str(build_temp_dir),
            "--specpath", str(self.output_dir),
        ]

        if onefile: cmd.append("--onefile")
        if noconsole: cmd.append("--noconsole")

        icon_source_path = self.builder_dir / "assets" / "icon.ico"
        if icon_source_path.exists():
            cmd.extend(["--icon", str(icon_source_path)])
            log(f"Utilizando ícone da fonte: {icon_source_path}")
        else:
            log(f"AVISO: Ícone não encontrado na origem: {icon_source_path}", "WARN")

        # Adiciona dados extras
        data_dirs = ["pages", "tests", "assets", "xmls"]
        for data_dir in data_dirs:
            src = self.staging_dir / data_dir
            if src.exists(): cmd.extend(["--add-data", f"{src};{data_dir}"])

        for root_file in ["config.py", "test_data.py", "framework.py", "VERSION"]:
            src = self.staging_dir / root_file
            if src.exists(): cmd.extend(["--add-data", f"{src};."])

        settings_file = self.staging_dir / "settings.json"
        if settings_file.exists(): cmd.extend(["--add-data", f"{settings_file};."])

        hidden_imports = [
            "pytest", "pytest_html", "pytest_html.plugin", "pytest_metadata", # Adicionado pytest_metadata
            "allure", "allure_pytest", "allure_pytest.plugin", "allure_commons",
            "appium", "appium.webdriver", "appium.webdriver.common", "appium.webdriver.common.appiumby",
            "appium.options.common", "appium.options.android",
            "selenium", "selenium.webdriver",
            "tkinter", "PIL", "PIL._tkinter_finder",
            "_pytest", "_pytest.config", "_pytest.python", "_pytest.assertion",
            "_pytest.runner", "_pytest.fixtures", "_pytest.hookspec",
            "pluggy", "pluggy._hooks", "pluggy._manager",
            "py",
            "faker", "faker.providers", "faker.providers.person.pt_BR",  # Para testes de cliente
            "faker.providers.address.pt_BR", "faker.providers.company.pt_BR",
            "requests", "requests.adapters", "urllib3",  # Para API ViaCEP
        ]
        for imp in hidden_imports: cmd.extend(["--hidden-import", imp])

        # --collect-all garante que TODOS os submodulos, dados e binarios
        # dos pacotes sejam incluidos (hidden-import sozinho nao e suficiente)
        collect_all_packages = ["pytest", "_pytest", "pluggy", "pytest_html", "pytest_metadata", "allure_pytest", "allure_commons", "allure_combine", "appium", "selenium", "faker", "requests"]
        for pkg in collect_all_packages: cmd.extend(["--collect-all", pkg])

        cmd.append(str(main_script))

        try:
            result = subprocess.run(cmd, cwd=str(self.staging_dir), capture_output=True, text=True, timeout=600)
            if result.returncode != 0:
                log(f"PyInstaller falhou. Logs:\n{result.stderr}", "ERROR")
                with open(self.output_dir / "pyinstaller_error.log", "w") as f: f.write(result.stdout + "\n" + result.stderr)
                return False

            # Verifica warnings de modulos faltando
            warn_file = self.output_dir / "build_temp" / "QA_Dashboard" / "warn-QA_Dashboard.txt"
            if warn_file.exists():
                try:
                    warn_content = warn_file.read_text(encoding='utf-8', errors='ignore')
                    for module_name in ["pytest", "_pytest"]:
                        if f"missing module named {module_name}" in warn_content:
                            log(f"ATENCAO: PyInstaller reportou 'missing module named {module_name}' — "
                                f"pytest pode NAO estar incluido no EXE!", "WARN")
                except Exception:
                    pass

            exe_path = self.dist_dir / "QA_Dashboard.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                log(f"Executavel criado com sucesso: {exe_path} ({size_mb:.1f} MB)")
                return True
            else:
                log("Executavel nao foi gerado na pasta dist.", "ERROR")
                return False

        except Exception as e:
            log(f"Erro inesperado ao compilar: {e}", "ERROR")
            return False

    def create_installer_iss(self) -> Path:
        """Cria script Inno Setup apontando para o icone original."""
        log("Gerando script Inno Setup...", "STEP")

        setup_icon_path = self.builder_dir / "assets" / "icon.ico"
        setup_icon_line = f"SetupIconFile={setup_icon_path}" if setup_icon_path.exists() else ""

        iss_content = f"""
; Inno Setup Script for QA Dashboard
; Gerado automaticamente por builder_pro.py em {self.timestamp}

#define MyAppName "QA Dashboard"
#define MyAppVersion "{self.version}"
#define MyAppPublisher "QA Team"
#define MyAppExeName "QA_Dashboard.exe"
#define MyAppDate "{self.timestamp}"

[Setup]
AppId={{{{B8F3A4D2-1234-5678-9ABC-DEF012345678}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
OutputDir={self.installer_dir}
OutputBaseFilename=Instalador_QA_Dashboard_{{#MyAppDate}}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
PrivilegesRequired=admin
{setup_icon_line}

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar icone na Area de Trabalho"; GroupDescription: "Icones adicionais:"

[Files]
; Executável
Source: "{self.dist_dir}\\QA_Dashboard.exe"; DestDir: "{{app}}"; Flags: ignoreversion
; Configuração
Source: "{self.staging_dir}\\settings.json"; DestDir: "{{app}}"; Flags: ignoreversion onlyifdoesntexist
Source: "{self.staging_dir}\\test_order_e2e.json"; DestDir: "{{app}}"; Flags: ignoreversion onlyifdoesntexist
; Core files
Source: "{self.staging_dir}\\config.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.staging_dir}\\conftest.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.staging_dir}\\framework.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.staging_dir}\\test_data.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.staging_dir}\\requirements.txt"; DestDir: "{{app}}"; Flags: ignoreversion
; Pastas
Source: "{self.staging_dir}\\pages\\*"; DestDir: "{{app}}\\pages"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{self.staging_dir}\\tests\\*"; DestDir: "{{app}}\\tests"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{self.staging_dir}\\assets\\*"; DestDir: "{{app}}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
; Scripts de Instalação
Source: "{self.staging_dir}\\scripts\\*"; DestDir: "{{app}}\\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; IconFilename: "{{app}}\\assets\\icon.ico"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon; IconFilename: "{{app}}\\assets\\icon.ico"

[Run]
; --- DEPENDENCIAS (WINGET E BATCH) ---
Filename: "{{app}}\\scripts\\instalar_dependencias.bat"; Description: "Instalar Java JDK, Node.js e Appium"; Flags: postinstall skipifsilent unchecked shellexec
Filename: "{{app}}\\scripts\\instalar_android_sdk.bat"; Description: "Instalar Android SDK (ADB e Tools)"; Flags: postinstall skipifsilent unchecked shellexec
Filename: "{{app}}\\scripts\\instalar_allure.bat"; Description: "Instalar Allure Report (Via Winget)"; Flags: postinstall skipifsilent unchecked shellexec
Filename: "{{app}}\\scripts\\verificar_ambiente.bat"; Description: "Verificar Ambiente Completo"; Flags: postinstall skipifsilent unchecked shellexec

; Iniciar o App
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "Iniciar {{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[Code]
// Cria arquivo .first_run para indicar primeira execução
// Isso evita popup de erro quando PATH ainda não foi atualizado
procedure CurStepChanged(CurStep: TSetupStep);
var
  MarkerFile: String;
begin
  if CurStep = ssPostInstall then
  begin
    MarkerFile := ExpandConstant('{{app}}\\.first_run');
    SaveStringToFile(MarkerFile, 'This file indicates first run after installation.' + #13#10 + 'It will be automatically deleted after first launch.' + #13#10, False);
  end;
end;
"""

        iss_path = self.output_dir / "qa_dashboard_installer.iss"
        with open(iss_path, 'w', encoding='utf-8') as f:
            f.write(iss_content)

        return iss_path

    def build_installer(self, iss_path: Path) -> bool:
        """Compila instalador com Inno Setup, procurando em todos os drives."""
        log("Compilando instalador com Inno Setup...", "STEP")

        # 1. Verifica se está no PATH (melhor cenário)
        iscc_exe = shutil.which("ISCC.exe")

        # 2. Se não estiver no PATH, varre TODOS os drives (C a Z)
        if not iscc_exe:
            # Lista de pastas comuns do Inno Setup
            common_folders = [
                "Inno Setup 6",
                "Inno Setup 5",
                r"Program Files (x86)\Inno Setup 6",
                r"Program Files\Inno Setup 6",
                r"Program Files (x86)\Inno Setup 5",
                r"Program Files\Inno Setup 5",
                r"Programs\Inno Setup 6" # Caso esteja em pasta Programs na raiz
            ]

            # Detecta drives disponíveis (C:, D:, E:, etc.)
            drives = [f"{d}:\\" for d in "CDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
            
            # Procura pelo ISCC.exe
            for drive in drives:
                for folder in common_folders:
                    candidate = os.path.join(drive, folder, "ISCC.exe")
                    if os.path.exists(candidate):
                        iscc_exe = candidate
                        break
                if iscc_exe: break

        # 3. Fallback: Procura pelo Compil32.exe (como o usuário pediu) em todos os drives
        if not iscc_exe:
            log("ISCC.exe não encontrado diretamente. Procurando via Compil32.exe...", "INFO")
            for drive in drives:
                for folder in common_folders:
                    candidate_compil32 = os.path.join(drive, folder, "Compil32.exe")
                    if os.path.exists(candidate_compil32):
                        # Se achou o Compil32, o ISCC deve estar ao lado
                        candidate_iscc = os.path.join(os.path.dirname(candidate_compil32), "ISCC.exe")
                        if os.path.exists(candidate_iscc):
                            iscc_exe = candidate_iscc
                            log(f"Inno Setup encontrado via Compil32 em: {drive}", "INFO")
                            break
                if iscc_exe: break

        if not iscc_exe:
            # --- MODO MANUAL ATIVADO ---
            log("Inno Setup (ISCC.exe ou Compil32.exe) não encontrado em nenhum drive.", "WARN")
            log(f"O script .iss foi gerado em: {iss_path}", "INFO")
            log("Abra este arquivo e clique em 'Compile' manualmente.", "INFO")
            return False

        log(f"Compilador encontrado: {iscc_exe}", "INFO")

        try:
            result = subprocess.run([iscc_exe, str(iss_path)], capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                log(f"Inno Setup falhou:\n{result.stderr}", "ERROR")
                return False

            installer = self.installer_dir / f"Instalador_QA_Dashboard_{self.timestamp}.exe"
            if installer.exists():
                size_mb = installer.stat().st_size / (1024 * 1024)
                log(f"Instalador criado com sucesso: {installer} ({size_mb:.1f} MB)")
                return True

        except Exception as e:
            log(f"Erro ao compilar instalador: {e}", "ERROR")

        return False

    def run(self, skip_installer: bool = False) -> bool:
        """Executa pipeline completo."""
        print(f"\n{'='*60}\n{Colors.BOLD}Builder Pro - QA Dashboard v{self.version}{Colors.RESET}\n{'='*60}\n")
        self.clean_python_cache()  # LIMPA CACHE PRIMEIRO
        self.clean()
        self.stage_runner()
        if not self.stage_qa_dev(): return False
        if not self.verify_build_environment(): return False
        if not self.compile_pyinstaller(): return False
        if not skip_installer:
            iss_path = self.create_installer_iss()
            self.build_installer(iss_path)
        print(f"\n{'='*60}")
        log("BUILD CONCLUÍDO", "STEP")
        print(f"Versão:       {self.version}")
        print(f"EXE Final:    {self.dist_dir / 'QA_Dashboard.exe'}")
        if not skip_installer: print(f"Instalador:   {self.installer_dir}")
        print(f"{'='*60}\n")
        return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qa-dev", required=True)
    parser.add_argument("--builder-dir", default=None)
    parser.add_argument("--no-installer", action="store_true")
    args = parser.parse_args()

    builder_dir = Path(args.builder_dir) if args.builder_dir else Path(__file__).parent.parent
    qa_dev_dir = Path(args.qa_dev)

    builder = BuilderPro(builder_dir, qa_dev_dir)
    sys.exit(0 if builder.run(skip_installer=args.no_installer) else 1)

if __name__ == "__main__":
    main()