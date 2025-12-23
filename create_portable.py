"""
Create a portable package that can be distributed as a ZIP file
Version: 1.0.0
"""
import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_portable_package():
    """Create a professional portable package of the application"""
    
    print("\n" + "="*60)
    print("Creating Portable Package")
    print("="*60 + "\n")
    
    # Configuration
    VERSION = "1.0.0"
    APP_NAME = "Medical Health Assistant"
    
    # Find the build directory
    build_dirs = list(Path("build").glob("exe.win-amd64-*"))
    if not build_dirs:
        print("❌ ERROR: Build directory not found.")
        print("   Run 'python setup.py build' first.")
        return False
    
    build_dir = build_dirs[0]
    print(f"📂 Found build directory: {build_dir}")
    
    # Check if main executable exists
    if not (build_dir / "MedicalHealthAssistant.exe").exists():
        print("❌ ERROR: MedicalHealthAssistant.exe not found in build directory.")
        return False
    
    portable_dir = Path("MedicalHealthAssistant_Portable")
    
    # Clean up old portable directory
    if portable_dir.exists():
        print("🧹 Cleaning old portable directory...")
        shutil.rmtree(portable_dir)
    
    # Create portable directory structure
    portable_dir.mkdir()
    app_dir = portable_dir / "app"
    
    # Copy all files from build
    print("📦 Copying application files...")
    shutil.copytree(build_dir, app_dir, dirs_exist_ok=True)
    
    # Create necessary directories
    print("📁 Creating data directories...")
    results_dir = app_dir / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Copy documentation files
    print("📄 Copying documentation...")
    docs_to_copy = ["README.md", "LICENSE.txt", "USER_GUIDE.md", "QUICK_START.md"]
    for doc in docs_to_copy:
        if Path(doc).exists():
            shutil.copy(doc, portable_dir)
            print(f"   ✓ {doc}")
    
    # Copy sample data if exists
    if Path("results").exists() and any(Path("results").glob("*.json")):
        print("📊 Copying sample data...")
        sample_dir = app_dir / "results" / "samples"
        sample_dir.mkdir(exist_ok=True)
        for file in Path("results").glob("*.json"):
            shutil.copy(file, sample_dir)
            print(f"   ✓ {file.name}")
    
    # Create comprehensive README for portable version
    readme_content = f"""
╔═══════════════════════════════════════════════════════════════╗
║         {APP_NAME} - Portable Version v{VERSION}           ║
╚═══════════════════════════════════════════════════════════════╝

QUICK START
───────────────────────────────────────────────────────────────
1. Double-click "Run Medical Health Assistant.bat" to launch
   OR
   Navigate to app\ folder and run MedicalHealthAssistant.exe

2. Select your medical records folder when prompted

3. Start analyzing your health data!


FEATURES
───────────────────────────────────────────────────────────────
✓ Convert PDF medical records to structured data
✓ View and search all your test results
✓ Visualize health trends over time
✓ Identify abnormal test results instantly
✓ Easy-to-use conversational interface
✓ Works completely offline


SYSTEM REQUIREMENTS
───────────────────────────────────────────────────────────────
• Windows 10 or later (64-bit)
• 4 GB RAM minimum (8 GB recommended)
• 500 MB free disk space
• No installation required
• No internet connection needed


USAGE
───────────────────────────────────────────────────────────────
This portable version requires NO INSTALLATION. Simply:

1. Extract the ZIP file to any location:
   - USB drive for portability
   - Network drive for shared access
   - Local hard drive for personal use

2. Run the application:
   - Use "Run Medical Health Assistant.bat" (easiest)
   - Or run app\MedicalHealthAssistant.exe directly

3. Your medical records:
   - Place PDF files in any folder
   - App will convert them automatically
   - All data stays on your computer


FOLDER STRUCTURE
───────────────────────────────────────────────────────────────
MedicalHealthAssistant_Portable/
├── app/                          # Application files
│   ├── MedicalHealthAssistant.exe   # Main application
│   ├── lib/                         # Required libraries
│   └── results/                     # Default data folder
│       └── samples/                 # Sample data (if included)
├── Run Medical Health Assistant.bat # Easy launcher
├── README.txt                       # This file
├── LICENSE.txt                      # License information
├── USER_GUIDE.md                    # Detailed guide
└── QUICK_START.md                   # Quick tutorial


DATA PRIVACY & SECURITY
───────────────────────────────────────────────────────────────
✓ All processing happens locally on YOUR computer
✓ No data is uploaded to the cloud
✓ No internet connection required or used
✓ No tracking or analytics
✓ Your medical data never leaves your machine

This ensures complete privacy and HIPAA compliance.


TROUBLESHOOTING
───────────────────────────────────────────────────────────────
Problem: "Windows protected your PC" warning
Solution: Click "More info" → "Run anyway"
         (This is normal for unsigned applications)

Problem: Application won't start
Solution: Make sure you extracted ALL files from the ZIP
         Some antivirus software may block it - add exception

Problem: Can't find my data
Solution: Use "📁 Change Folder" button in the app
         Select the folder containing your PDF files

Problem: PDF conversion fails
Solution: Make sure PDFs are text-based (not scanned images)
         Check that files aren't password-protected


GETTING HELP
───────────────────────────────────────────────────────────────
📧 Email: support@yourcompany.com
🌐 Website: https://yourwebsite.com
📖 Full Documentation: See USER_GUIDE.md


VERSION INFORMATION
───────────────────────────────────────────────────────────────
Version: {VERSION}
Built: {datetime.now().strftime("%Y-%m-%d")}
Platform: Windows 10/11 (64-bit)


LICENSE
───────────────────────────────────────────────────────────────
See LICENSE.txt for complete license information.

Copyright © 2025 Your Company Name. All rights reserved.


═══════════════════════════════════════════════════════════════
Thank you for using {APP_NAME}!
═══════════════════════════════════════════════════════════════
"""
    
    with open(portable_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create launcher batch file
    print("🚀 Creating launcher script...")
    run_script = """@echo off
REM Medical Health Assistant Launcher
REM This script launches the application from the portable package

echo.
echo ========================================
echo  Medical Health Assistant
echo ========================================
echo.
echo Starting application...
echo.

cd /d "%~dp0app"

REM Check if executable exists
if not exist "MedicalHealthAssistant.exe" (
    echo ERROR: Application executable not found!
    echo Make sure all files were extracted from the ZIP.
    echo.
    pause
    exit /b 1
)

REM Launch the application
start "" "MedicalHealthAssistant.exe"

REM Optional: Wait a moment to check if it started
timeout /t 2 /nobreak >nul

echo Application launched!
echo You can close this window.
echo.
"""
    
    with open(portable_dir / "Run Medical Health Assistant.bat", "w") as f:
        f.write(run_script)
    
    # Create debug launcher for troubleshooting
    debug_script = """@echo off
REM Debug launcher - shows console for error messages

echo.
echo ========================================
echo  Medical Health Assistant (Debug Mode)
echo ========================================
echo.

cd /d "%~dp0app"

if not exist "MedicalHealthAssistant_Debug.exe" (
    echo Debug executable not found, using regular version...
    MedicalHealthAssistant.exe
) else (
    echo Running in debug mode with console output...
    echo.
    MedicalHealthAssistant_Debug.exe
)

echo.
echo Application closed.
pause
"""
    
    with open(portable_dir / "Run (Debug Mode).bat", "w") as f:
        f.write(debug_script)
    
    # Create ZIP file
    print("🗜️  Creating ZIP archive...")
    zip_filename = f"MedicalHealthAssistant_Portable_v{VERSION}.zip"
    
    # Remove old ZIP if exists
    if Path(zip_filename).exists():
        Path(zip_filename).unlink()
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        for root, dirs, files in os.walk(portable_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(portable_dir.parent)
                zipf.write(file_path, arcname)
                file_count += 1
        
        print(f"   ✓ Compressed {file_count} files")
    
    # Get file size
    zip_size = Path(zip_filename).stat().st_size / (1024 * 1024)  # MB
    
    print("\n" + "="*60)
    print("✅ Portable Package Created Successfully!")
    print("="*60)
    print(f"\n📦 Package: {zip_filename}")
    print(f"💾 Size: {zip_size:.1f} MB")
    print(f"📁 Files: {file_count}")
    print(f"\n🎉 Ready for distribution!\n")
    
    print("Distribution Instructions:")
    print("─" * 60)
    print(f"1. Share {zip_filename} with users")
    print("2. Users extract to any location")
    print("3. Users run 'Run Medical Health Assistant.bat'")
    print("4. No installation needed!")
    print("\n" + "="*60 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = create_portable_package()
        if not success:
            print("\n❌ Portable package creation failed.")
            exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)