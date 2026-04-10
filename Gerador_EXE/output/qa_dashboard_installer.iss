
; Inno Setup Script for QA Dashboard
; Gerado automaticamente por builder_pro.py em 2026_04_10

#define MyAppName "QA Dashboard"
#define MyAppVersion "2.0.107"
#define MyAppPublisher "QA Team"
#define MyAppExeName "QA_Dashboard.exe"
#define MyAppDate "2026_04_10"

[Setup]
AppId={{B8F3A4D2-1234-5678-9ABC-DEF012345678}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=E:\PDV_AUTOMACAO\Gerador_EXE\output\installer
OutputBaseFilename=Instalador_QA_Dashboard_{#MyAppDate}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
PrivilegesRequired=admin
SetupIconFile=E:\PDV_AUTOMACAO\Gerador_EXE\assets\icon.ico

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar icone na Area de Trabalho"; GroupDescription: "Icones adicionais:"

[Files]
; Executável
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\dist\QA_Dashboard.exe"; DestDir: "{app}"; Flags: ignoreversion
; Configuração
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\settings.json"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\test_order_e2e.json"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
; Core files
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\config.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\conftest.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\framework.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\test_data.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
; Pastas
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\pages\*"; DestDir: "{app}\pages"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\tests\*"; DestDir: "{app}\tests"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
; Scripts de Instalação
Source: "E:\PDV_AUTOMACAO\Gerador_EXE\output\staging\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\assets\icon.ico"

[Run]
; --- DEPENDENCIAS (WINGET E BATCH) ---
Filename: "{app}\scripts\instalar_dependencias.bat"; Description: "Instalar Java JDK, Node.js e Appium"; Flags: postinstall skipifsilent unchecked shellexec
Filename: "{app}\scripts\instalar_android_sdk.bat"; Description: "Instalar Android SDK (ADB e Tools)"; Flags: postinstall skipifsilent unchecked shellexec
Filename: "{app}\scripts\instalar_allure.bat"; Description: "Instalar Allure Report (Via Winget)"; Flags: postinstall skipifsilent unchecked shellexec
Filename: "{app}\scripts\verificar_ambiente.bat"; Description: "Verificar Ambiente Completo"; Flags: postinstall skipifsilent unchecked shellexec

; Iniciar o App
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
// Cria arquivo .first_run para indicar primeira execução
// Isso evita popup de erro quando PATH ainda não foi atualizado
procedure CurStepChanged(CurStep: TSetupStep);
var
  MarkerFile: String;
begin
  if CurStep = ssPostInstall then
  begin
    MarkerFile := ExpandConstant('{app}\.first_run');
    SaveStringToFile(MarkerFile, 'This file indicates first run after installation.' + #13#10 + 'It will be automatically deleted after first launch.' + #13#10, False);
  end;
end;
