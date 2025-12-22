"""
Medical RAG GUI - Main Entry Point
Run this file to start the application

IMPORTANT: Make sure these files are in the same folder:
- medical_rag_gui.py (this file)
- gui_app.py
- gui_widgets.py
- gui_chart.py
- gui_results.py
- loader.py
- matcher.py
- formatter.py
- visualizer.py
- config.py
"""
import tkinter as tk
import sys
import os
#from trial_manager import check_trial_and_start_app, TrialManager

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui_app import MedicalRAGApp
except ImportError as e:
    print(f"ERROR: Could not import required modules: {e}")
    print("\nMake sure all these files are in the same folder:")
    print("- gui_app.py")
    print("- gui_widgets.py")
    print("- gui_chart.py")
    print("- gui_results.py")
    sys.exit(1)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = MedicalRAGApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()