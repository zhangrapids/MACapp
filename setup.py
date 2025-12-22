"""
Setup script for Medical Health Assistant
Creates a standalone Windows executable with installer
"""
from cx_Freeze import setup, Executable
import sys
import os

# Dependencies
build_exe_options = {
    "packages": [
        "tkinter",
        "json",
        "datetime",
        "matplotlib",
        "numpy",
        "os",
        "sys",
        "re",
        "difflib",
        "pathlib",
        "subprocess",
        "PIL",  # Added Pillow/PIL
    ],
    "include_files": [
        "config.py",
        "loader.py",
        "matcher.py",
        "medical_formatter.py",
        "visualizer.py",
        "gui_widgets.py",
        "gui_chart.py",
        "gui_results.py",
        "gui_abnormal.py",
        "gui_app.py",
        "pdf_converter.py",
        "parsers.py",
        "medical_parsers.py",
        "normalizer.py",
        "formatter.py",
        "standard_questions.txt",
        "README.md",
    ] + (
        [("txt_json", "txt_json")] if os.path.exists("txt_json") else []
    ) + (
        [("test_pdfs", "test_pdfs")] if os.path.exists("test_pdfs") else []
    ),
    "excludes": [
        "scipy",
        "pandas",
    ],  # Removed PIL from excludes
    "optimize": 2,
    "include_msvcr": True,  # Include Visual C++ runtime
}

# Base for Windows GUI application (no console window)
base = None
if sys.platform == "win32":
    base = "gui"  # Changed from "Win32GUI" to "gui" for newer cx_Freeze versions

# Create two executables: one GUI (no console) and one console (for debugging)
executables = [
    # Main GUI version (no console)
    Executable(
        "medical_rag_gui.py",
        base=base,
        target_name="MedicalHealthAssistant.exe",
        icon="app_icon.ico" if os.path.exists("app_icon.ico") else None,
        shortcut_name="Medical Health Assistant",
        shortcut_dir="DesktopFolder",
    ),
    # Debug version (with console)
    Executable(
        "medical_rag_gui.py",
        base=None,  # Console version
        target_name="MedicalHealthAssistant_Debug.exe",
        icon="app_icon.ico" if os.path.exists("app_icon.ico") else None,
    )
]

setup(
    name="Medical Health Assistant",
    version="1.0.0",
    description="AI-Powered Medical Records Assistant",
    author="Your Name",
    options={"build_exe": build_exe_options},
    executables=executables
)