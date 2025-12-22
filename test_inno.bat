@echo off
SETLOCAL EnableDelayedExpansion
echo Testing Inno Setup call...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo Found it
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss
    echo Exit code: %ERRORLEVEL%
)
pause