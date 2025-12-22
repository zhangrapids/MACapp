@echo off
REM Build script for Medical Health Assistant
REM Creates standalone Windows installer and portable version
SETLOCAL EnableDelayedExpansion

echo.
echo ============================================
echo   Medical Health Assistant - Build Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.13 from python.org
    echo.
    pause
    exit /b 1
)

echo [Step 1/6] Checking Python installation...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   Found Python %PYTHON_VERSION%

echo.
echo [Step 2/6] Installing/updating required packages...
pip install --upgrade cx_Freeze matplotlib numpy Pillow pdfplumber --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install required packages
    echo.
    pause
    exit /b 1
)
echo   All packages installed successfully

echo.
echo [Step 3/6] Cleaning previous builds...
if exist "build" (
    rmdir /s /q "build"
    echo   Removed old build directory
)
if exist "dist" (
    rmdir /s /q "dist"
    echo   Removed old dist directory
)
if exist "Output" (
    rmdir /s /q "Output"
    echo   Removed old Output directory
)
if exist "MedicalHealthAssistant_Portable" (
    rmdir /s /q "MedicalHealthAssistant_Portable"
    echo   Removed old portable directory
)

echo.
echo [Step 4/6] Building executable with cx_Freeze...
python setup.py build
if errorlevel 1 (
    echo [ERROR] Build failed!
    echo Check the error messages above.
    echo.
    pause
    exit /b 1
)
echo   Executable built successfully

REM Find the actual build directory
for /d %%d in (build\exe.win-amd64-*) do set BUILD_DIR=%%d

if not exist "%BUILD_DIR%\MedicalHealthAssistant.exe" (
    echo [ERROR] MedicalHealthAssistant.exe not found in build directory
    echo.
    pause
    exit /b 1
)

echo   Build directory: %BUILD_DIR%

echo.
echo [Step 5/6] Creating Windows installer with Inno Setup...

if exist "C:\Program Files ^(x86^)\Inno Setup 6\ISCC.exe" (
    echo   Found Inno Setup at: C:\Program Files ^(x86^)\Inno Setup 6\ISCC.exe
    "C:\Program Files ^(x86^)\Inno Setup 6\ISCC.exe" installer_script.iss
    if errorlevel 1 (
        echo [WARNING] Installer creation failed
        echo   Check the error messages above
    ) else (
        echo   Installer created successfully!
        if exist "Output\MedicalHealthAssistant_Setup_v1.0.0.exe" (
            for %%A in ("Output\MedicalHealthAssistant_Setup_v1.0.0.exe") do set INSTALLER_SIZE=%%~zA
            set /a INSTALLER_SIZE_MB=!INSTALLER_SIZE! / 1048576
            echo   Installer size: !INSTALLER_SIZE_MB! MB
        )
    )
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    echo   Found Inno Setup at: C:\Program Files\Inno Setup 6\ISCC.exe
    "C:\Program Files\Inno Setup 6\ISCC.exe" installer_script.iss
    if errorlevel 1 (
        echo [WARNING] Installer creation failed
        echo   Check the error messages above
    ) else (
        echo   Installer created successfully!
        if exist "Output\MedicalHealthAssistant_Setup_v1.0.0.exe" (
            for %%A in ("Output\MedicalHealthAssistant_Setup_v1.0.0.exe") do set INSTALLER_SIZE=%%~zA
            set /a INSTALLER_SIZE_MB=!INSTALLER_SIZE! / 1048576
            echo   Installer size: !INSTALLER_SIZE_MB! MB
        )
    )
) else if exist "C:\Program Files ^(x86^)\Inno Setup 5\ISCC.exe" (
    echo   Found Inno Setup at: C:\Program Files ^(x86^)\Inno Setup 5\ISCC.exe
    "C:\Program Files ^(x86^)\Inno Setup 5\ISCC.exe" installer_script.iss
    if errorlevel 1 (
        echo [WARNING] Installer creation failed
        echo   Check the error messages above
    ) else (
        echo   Installer created successfully!
        if exist "Output\MedicalHealthAssistant_Setup_v1.0.0.exe" (
            for %%A in ("Output\MedicalHealthAssistant_Setup_v1.0.0.exe") do set INSTALLER_SIZE=%%~zA
            set /a INSTALLER_SIZE_MB=!INSTALLER_SIZE! / 1048576
            echo   Installer size: !INSTALLER_SIZE_MB! MB
        )
    )
) else (
    echo [WARNING] Inno Setup not found!
    echo   Searched locations:
    echo     - C:\Program Files ^(x86^)\Inno Setup 6\ISCC.exe
    echo     - C:\Program Files\Inno Setup 6\ISCC.exe
    echo     - C:\Program Files ^(x86^)\Inno Setup 5\ISCC.exe
    echo.
    echo   Download from: https://jrsoftware.org/isdl.php
    echo   Skipping installer creation...
    echo   You can still use the portable version or run from build directory.
)

echo.
echo [Step 6/6] Creating portable ZIP package...
python create_portable.py
if errorlevel 1 (
    echo [WARNING] Portable package creation failed
) else (
    echo   Portable package created successfully!
    if exist "MedicalHealthAssistant_Portable_v1.0.0.zip" (
        for %%A in ("MedicalHealthAssistant_Portable_v1.0.0.zip") do set ZIP_SIZE=%%~zA
        set /a ZIP_SIZE_MB=!ZIP_SIZE! / 1048576
        echo   ZIP size: !ZIP_SIZE_MB! MB
    )
)

echo.
echo ============================================
echo   Build Complete!
echo ============================================
echo.

REM Check what was created
set CREATED_FILES=0

if exist "Output\MedicalHealthAssistant_Setup_v1.0.0.exe" (
    echo [✓] Windows Installer:
    echo     Output\MedicalHealthAssistant_Setup_v1.0.0.exe
    set /a CREATED_FILES+=1
)

if exist "MedicalHealthAssistant_Portable_v1.0.0.zip" (
    echo [✓] Portable Package:
    echo     MedicalHealthAssistant_Portable_v1.0.0.zip
    set /a CREATED_FILES+=1
)

if exist "%BUILD_DIR%\MedicalHealthAssistant.exe" (
    echo [✓] Development Build:
    echo     %BUILD_DIR%\MedicalHealthAssistant.exe
    set /a CREATED_FILES+=1
)

echo.
echo Files created: %CREATED_FILES%
echo.

if %CREATED_FILES% GEQ 1 (
    echo Next Steps:
    echo   1. Test the executable: %BUILD_DIR%\MedicalHealthAssistant.exe
    if exist "Output\MedicalHealthAssistant_Setup_v1.0.0.exe" (
        echo   2. Test the installer on a clean Windows VM
        echo   3. Distribute: Output\MedicalHealthAssistant_Setup_v1.0.0.exe
    )
    if exist "MedicalHealthAssistant_Portable_v1.0.0.zip" (
        echo   4. Distribute portable: MedicalHealthAssistant_Portable_v1.0.0.zip
    )
    echo.
    echo For commercial distribution:
    echo   - Consider code signing the installer
    echo   - Update version numbers in setup.py and installer_script.iss
    echo   - Test on multiple Windows versions
    echo.
) else (
    echo [ERROR] No distribution files were created!
    echo Please check the error messages above.
    echo.
)

echo Press any key to exit...
pause >nul
