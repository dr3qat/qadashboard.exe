"""
dependency_scanner.py — Busca dependências (Node, Allure, Appium, ADB) no sistema.
Extraído de app_runner.py para isolar a responsabilidade de detecção de ferramentas.
"""
import os
import shutil
import subprocess
import sys


def _buscar_node_instalado():
    """Busca Node.js em múltiplos locais além do PATH."""
    # 1. Tenta no PATH primeiro
    node_path = shutil.which("node") or shutil.which("node.exe")
    if node_path and os.path.exists(node_path):
        return node_path

    # 2. Locais típicos de instalação do Node.js
    locais_node = [
        r"C:\Program Files\nodejs\node.exe",
        r"C:\Program Files (x86)\nodejs\node.exe",
        os.path.expandvars(r"%PROGRAMFILES%\nodejs\node.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\nodejs\node.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\node\node.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\node\node.exe"),
        # NVM for Windows
        os.path.expandvars(r"%NVM_HOME%\current\node.exe"),
        os.path.expandvars(r"%APPDATA%\nvm\current\node.exe"),
    ]

    # 3. Busca em pastas NVM (versões específicas)
    nvm_home = os.environ.get("NVM_HOME") or os.path.expandvars(r"%APPDATA%\nvm")
    if os.path.isdir(nvm_home):
        try:
            for item in os.listdir(nvm_home):
                nvm_node = os.path.join(nvm_home, item, "node.exe")
                if os.path.isfile(nvm_node):
                    locais_node.append(nvm_node)
        except:
            pass

    for local in locais_node:
        if local and os.path.isfile(local):
            return local

    return None


def _buscar_allure_instalado():
    """Busca Allure CLI em múltiplos locais além do PATH."""
    # 1. Tenta no PATH primeiro
    allure_path = shutil.which("allure") or shutil.which("allure.bat") or shutil.which("allure.cmd")
    if allure_path and os.path.exists(allure_path):
        return allure_path

    # 2. Locais típicos de instalação do Allure
    locais_allure = [
        # Scoop (muito comum no Windows)
        os.path.expandvars(r"%USERPROFILE%\scoop\shims\allure.cmd"),
        os.path.expandvars(r"%USERPROFILE%\scoop\apps\allure\current\bin\allure.bat"),
        # Chocolatey
        r"C:\ProgramData\chocolatey\bin\allure.bat",
        r"C:\ProgramData\chocolatey\lib\allure\tools\allure\bin\allure.bat",
        # Manual install comum
        r"C:\allure\bin\allure.bat",
        r"C:\tools\allure\bin\allure.bat",
        os.path.expandvars(r"%USERPROFILE%\allure\bin\allure.bat"),
        # Allure instalado via npm
        os.path.expandvars(r"%APPDATA%\npm\allure.cmd"),
        os.path.expandvars(r"%LOCALAPPDATA%\npm\allure.cmd"),
    ]

    # 3. Busca recursiva em pastas scoop
    scoop_apps = os.path.expandvars(r"%USERPROFILE%\scoop\apps")
    if os.path.isdir(scoop_apps):
        try:
            for item in os.listdir(scoop_apps):
                if "allure" in item.lower():
                    for subdir in ["current", "bin"]:
                        for ext in ["allure.bat", "allure.cmd", "allure"]:
                            p = os.path.join(scoop_apps, item, subdir, "bin", ext)
                            if os.path.isfile(p):
                                locais_allure.append(p)
                            p2 = os.path.join(scoop_apps, item, subdir, ext)
                            if os.path.isfile(p2):
                                locais_allure.append(p2)
        except:
            pass

    for local in locais_allure:
        if local and os.path.isfile(local):
            return local

    return None


def _buscar_appium_instalado():
    """Busca Appium em múltiplos locais além do PATH."""
    # 1. Tenta no PATH primeiro
    appium_path = shutil.which("appium.cmd") or shutil.which("appium") or shutil.which("appium.ps1")
    if appium_path and os.path.exists(appium_path):
        return appium_path

    # 2. Tenta usar npm para descobrir o local de instalação global
    try:
        result = subprocess.run(
            ["npm", "bin", "-g"],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        if result.returncode == 0:
            npm_bin = result.stdout.strip()
            for ext in ["appium.cmd", "appium.ps1", "appium"]:
                p = os.path.join(npm_bin, ext)
                if os.path.isfile(p):
                    return p
    except:
        pass

    # 3. Locais típicos onde npm instala globalmente
    locais_appium = [
        os.path.expandvars(r"%APPDATA%\npm\appium.cmd"),
        os.path.expandvars(r"%APPDATA%\npm\appium.ps1"),
        os.path.expandvars(r"%LOCALAPPDATA%\npm\appium.cmd"),
        r"C:\Program Files\nodejs\appium.cmd",
        r"C:\Program Files\nodejs\node_modules\appium\build\lib\main.js",
        os.path.expandvars(r"%APPDATA%\npm\node_modules\appium\build\lib\main.js"),
        os.path.expandvars(r"%LOCALAPPDATA%\npm\node_modules\appium\build\lib\main.js"),
        os.path.expandvars(r"%NVM_HOME%\current\appium.cmd"),
    ]

    # 4. Busca em node_modules do usuário
    npm_prefix_paths = [
        os.path.expandvars(r"%APPDATA%\npm"),
        os.path.expandvars(r"%LOCALAPPDATA%\npm"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\npm"),
    ]

    for npm_path in npm_prefix_paths:
        if os.path.isdir(npm_path):
            for ext in ["appium.cmd", "appium.ps1", "appium"]:
                p = os.path.join(npm_path, ext)
                if os.path.isfile(p):
                    locais_appium.append(p)

    for local in locais_appium:
        if local and os.path.isfile(local):
            return local

    return None


def _buscar_adb_instalado():
    """Busca ADB em múltiplos locais além do PATH."""
    # 1. Tenta no PATH primeiro
    adb_path = shutil.which("adb") or shutil.which("adb.exe")
    if adb_path and os.path.exists(adb_path):
        return adb_path

    # 2. Locais típicos do Android SDK
    locais_adb = [
        os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"),
        os.path.expandvars(r"%ANDROID_HOME%\platform-tools\adb.exe"),
        os.path.expandvars(r"%ANDROID_SDK_ROOT%\platform-tools\adb.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe"),
        r"C:\Android\sdk\platform-tools\adb.exe",
        r"C:\android-sdk\platform-tools\adb.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"),
    ]

    for local in locais_adb:
        if local and os.path.isfile(local):
            return local

    return None
