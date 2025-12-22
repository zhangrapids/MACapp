; Medical Health Assistant Installer Script
; Requires Inno Setup 6 (free): https://jrsoftware.org/isdl.php

#define MyAppName "Medical Health Assistant"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Company Name"
#define MyAppURL "https://yourwebsite.com"
#define MyAppExeName "MedicalHealthAssistant.exe"

[Setup]
; Basic Information
AppId={{12345678-1234-1234-1234-123456789ABC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=README.md
OutputDir=Output
OutputBaseFilename=MedicalHealthAssistant_Setup_v{#MyAppVersion}
SetupIconFile=app_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
; Fixed: Changed from x64 to x64compatible (recommended for most cases)
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
; Removed deprecated quicklaunchicon task (Vista/Server 2008 no longer supported)

[Files]
Source: "build\exe.win-amd64-3.13\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\exe.win-amd64-3.13\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[UninstallDelete]
Type: filesandordirs; Name: "{app}\results"
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Medical Health Assistant will be installed on your computer.' + #13#10 + #13#10 +
         'This application helps you manage and analyze your medical records.' + #13#10 + #13#10 +
         'Click Next to continue.', mbInformation, MB_OK);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create results folder if it doesn't exist
    if not DirExists(ExpandConstant('{app}\results')) then
      CreateDir(ExpandConstant('{app}\results'));
  end;
end;