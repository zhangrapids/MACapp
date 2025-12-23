"""
Medical RAG GUI - Main Application Class (Modular)
Contains the core application logic and UI coordination
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loader import load_all_tests
from matcher import find_test
from medical_formatter import format_results, format_abnormal_tests
from visualizer import can_visualize
from config import RESULTS_FOLDER, DEBUG_MODE
from gui_widgets import create_header, create_status_bar
from gui_chart import ChartManager
from gui_results import ResultsManager
from gui_abnormal import AbnormalTestsManager
from pdf_converter import convert_pdfs_to_json, check_pdf_support, install_pdf_library
from pathlib import Path

class MedicalRAGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Health Assistant")
        self.root.geometry("1600x900")
        self.root.minsize(1200, 700)
        
        # Set colors
        self.bg_color = "#f0f0f0"
        self.accent_color = "#2196F3"
        self.text_color = "#333333"
        self.button_bg = "#2196F3"  # Blue for abnormal test buttons
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize data
        self.all_tests = {}
        self.test_names = []
        self.data_folder = None  # Will be set by user
        
        # Create managers (will be initialized after widgets)
        self.chart_manager = None
        self.results_manager = None
        self.abnormal_manager = None
        
        # Create UI
        self.create_widgets()
        
        # Prompt user to select data folder
        self.select_data_folder()
    
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Header - Full width
        create_header(self.root, self.accent_color, "Medical Health Assistant")
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left column (2/3 width) - Abnormal Records and Chart
        left_column = tk.Frame(main_frame, bg=self.bg_color)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Configure row weights to control proportions (1:2 ratio = 1/3 : 2/3)
        left_column.grid_rowconfigure(0, weight=1, minsize=250)  # Abnormal panel - 1/3, min 250px
        left_column.grid_rowconfigure(1, weight=2, minsize=500)  # Chart panel - 2/3, min 500px
        left_column.grid_columnconfigure(0, weight=1)
        
        # Abnormal Records section (top)
        abnormal_frame = tk.LabelFrame(
            left_column,
            text="⚠️ Abnormal Records",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=15
        )
        abnormal_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        # Scrollable frame for abnormal test buttons
        abnormal_canvas = tk.Canvas(abnormal_frame, bg="white", highlightthickness=0)
        abnormal_scrollbar = tk.Scrollbar(abnormal_frame, orient="vertical", command=abnormal_canvas.yview)
        self.abnormal_buttons_frame = tk.Frame(abnormal_canvas, bg="white")
        
        self.abnormal_buttons_frame.bind(
            "<Configure>",
            lambda e: abnormal_canvas.configure(scrollregion=abnormal_canvas.bbox("all"))
        )
        
        abnormal_canvas.create_window((0, 0), window=self.abnormal_buttons_frame, anchor="nw")
        abnormal_canvas.configure(yscrollcommand=abnormal_scrollbar.set)
        
        abnormal_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        abnormal_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bar Graph section (bottom)
        self.chart_frame = tk.LabelFrame(
            left_column,
            text="📊 Trend Visualization",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=15
        )
        self.chart_frame.grid(row=1, column=0, sticky="nsew")
        
        # Right column (1/3 width) - Chat with Assistant
        right_column = tk.Frame(main_frame, bg=self.bg_color)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_column.config(width=500)
        
        # Chat section
        self.create_chat_section(right_column)
        
        # Answers section
        self.create_answers_section(right_column)
        
        # Initialize managers
        self.results_manager = ResultsManager(self.results_text)
        self.chart_manager = ChartManager(self.chart_frame, self.accent_color)
        
        # Status bar
        self.status_label = create_status_bar(self.root, self.text_color)
    
    def create_chat_section(self, parent):
        """Create the chat input section"""
        chat_frame = tk.LabelFrame(
            parent,
            text="💬 Chat with Assistant",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=15
        )
        chat_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input question area
        tk.Label(
            chat_frame,
            text="Ask me about your health records:",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=(0, 5))
        
        input_frame = tk.Frame(chat_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            input_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            relief=tk.FLAT,
            bg="white",
            fg=self.text_color
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.search_entry.bind('<Return>', lambda e: self.search())
        
        # Placeholder text
        placeholder = "e.g., glucose, WBC, blood pressure..."
        self.search_entry.insert(0, placeholder)
        self.search_entry.config(fg='gray')
        
        def on_focus_in(event):
            if self.search_entry.get() == placeholder:
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg=self.text_color)
        
        def on_focus_out(event):
            if self.search_entry.get() == "":
                self.search_entry.insert(0, placeholder)
                self.search_entry.config(fg='gray')
        
        self.search_entry.bind('<FocusIn>', on_focus_in)
        self.search_entry.bind('<FocusOut>', on_focus_out)
        
        ask_btn = tk.Button(
            input_frame,
            text="🔍 Ask",
            command=self.search,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20
        )
        ask_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Quick category buttons
        tk.Label(
            chat_frame,
            text="Quick categories:",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 9, "italic")
        ).pack(anchor=tk.W, pady=(5, 5))
        
        btn_frame = tk.Frame(chat_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X)
        
        buttons = [
            ("📁 Change Folder", self.select_data_folder),
            ("📋 All Records", self.list_all_tests),
            ("🩸 Blood Tests", self.show_blood_tests),
            ("💉 Immunization", lambda: self.quick_search("immunization")),
            ("🩺 Vital Signs", lambda: self.quick_search("blood pressure weight height temperature pulse")),
            ("🏥 Procedures", lambda: self.quick_search("colonoscopy endoscopy biopsy surgery screening")),
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                bg="white",
                fg=self.text_color,
                font=("Arial", 9, "bold"),
                relief=tk.FLAT,
                cursor="hand2",
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def create_answers_section(self, parent):
        """Create the answers display section"""
        answers_frame = tk.LabelFrame(
            parent,
            text="Answers",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=15,
            pady=15
        )
        answers_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(
            answers_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="white",
            fg=self.text_color,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.tag_configure("abnormal", foreground="red", font=("Consolas", 10, "bold"))
    
    def select_data_folder(self):
        """Let user select the folder containing medical records (PDFs or JSON)"""
        self.update_status("Please select your medical records folder...")
        
        # Show folder selection dialog
        folder = filedialog.askdirectory(
            title="Select Folder Containing Medical Records (PDF files)",
            initialdir=os.path.expanduser("~"),
        )
        
        if folder:
            folder_path = Path(folder)
            self.update_status(f"Selected folder: {folder}")
            
            # Check if folder contains PDFs - ONLY count .pdf files
            pdf_files = [f for f in folder_path.glob("*") if f.suffix.lower() == ".pdf"]
            
            if pdf_files:
                # Found PDFs - offer to convert them
                response = messagebox.askyesno(
                    "PDF Files Detected",
                    f"Found {len(pdf_files)} PDF file(s) in the selected folder.\n\n"
                    "Would you like to convert them to JSON format?\n\n"
                    "Converted files will be saved in a 'txt_json' subfolder."
                )
                
                if response:
                    self.convert_and_load_pdfs(str(folder_path))
                else:
                    # User declined - check if txt_json subfolder already exists
                    txt_json_folder = folder_path / "txt_json"
                    if txt_json_folder.exists():
                        self.data_folder = str(txt_json_folder)
                        self.load_data()
                    else:
                        messagebox.showinfo(
                            "Convert PDFs First",
                            "Please convert your PDF files first to use the app.\n\n"
                            "Click 'Yes' when prompted to convert PDFs."
                        )
                        self.show_no_folder_message()
            else:
                # No PDFs - check if this IS the txt_json folder or if it contains one
                txt_json_folder = folder_path / "txt_json"
                
                # Check if current folder has JSON files
                json_files = list(folder_path.glob("*.json"))
                
                if json_files:
                    # Current folder has JSON files - use it
                    self.data_folder = str(folder_path)
                    self.load_data()
                elif txt_json_folder.exists():
                    # txt_json subfolder exists - use it
                    self.data_folder = str(txt_json_folder)
                    self.load_data()
                else:
                    messagebox.showinfo(
                        "No Data Found",
                        "This folder doesn't contain:\n"
                        "• PDF files to convert\n"
                        "• JSON files to load\n"
                        "• A 'txt_json' subfolder\n\n"
                        "Please select a folder containing PDF medical records."
                    )
                    self.show_no_folder_message()
        else:
            # User cancelled - ask if they want to try default folder
            if os.path.exists(RESULTS_FOLDER):
                response = messagebox.askyesno(
                    "Use Default Folder?",
                    f"Would you like to use the default folder?\n\n{RESULTS_FOLDER}"
                )
                if response:
                    self.data_folder = RESULTS_FOLDER
                    self.load_data()
                else:
                    self.show_no_folder_message()
            else:
                self.show_no_folder_message()
    
    def convert_and_load_pdfs(self, pdf_folder):
        """Convert PDFs to JSON and load the results"""
        
        # Check if PDF support is available
        has_support, library = check_pdf_support()
        
        if not has_support:
            # Offer to install PDF library
            response = messagebox.askyesno(
                "PDF Library Required",
                "PDF conversion requires an additional library.\n\n"
                "Would you like to install it now?\n\n"
                "This will install 'pdfplumber' (takes ~30 seconds)"
            )
            
            if response:
                self.update_status("Installing PDF library...")
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "📦 Installing PDF conversion library...\n")
                self.results_text.insert(tk.END, "This may take a moment...\n\n")
                self.root.update()
                
                if install_pdf_library():
                    messagebox.showinfo("Success", "PDF library installed successfully!")
                else:
                    messagebox.showerror(
                        "Installation Failed",
                        "Could not install PDF library.\n\n"
                        "Please install manually:\n"
                        "pip install pdfplumber"
                    )
                    self.show_no_folder_message()
                    return
            else:
                self.show_no_folder_message()
                return
        
        # Convert PDFs
        self.update_status("Converting PDF files...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔄 Converting PDF files to JSON...\n\n")
        self.root.update()
        
        try:
            # Create txt_json subfolder inside the PDF folder
            output_folder = Path(pdf_folder) / "txt_json"
            
            # Convert PDFs
            num_converted, output_path, errors = convert_pdfs_to_json(pdf_folder, output_folder)
            
            # Show results
            result_msg = f"✅ Conversion Complete!\n\n"
            result_msg += f"Converted {num_converted} PDF file(s)\n"
            result_msg += f"Output folder: {output_path}\n\n"
            
            if errors:
                result_msg += f"⚠️ Warnings ({len(errors)}):\n"
                for error in errors[:5]:  # Show first 5 errors
                    result_msg += f"  • {error}\n"
                if len(errors) > 5:
                    result_msg += f"  • ... and {len(errors) - 5} more\n"
            
            messagebox.showinfo("Conversion Complete", result_msg)
            
            # Now load from the txt_json subfolder
            self.data_folder = str(output_path)
            self.load_data()
            
        except Exception as e:
            messagebox.showerror(
                "Conversion Error",
                f"Error converting PDFs:\n\n{str(e)}"
            )
            self.show_no_folder_message()
    
    def show_no_folder_message(self):
        """Show message when no folder is selected"""
        msg = """
No folder selected.

To use Medical Health Assistant:
1. Click the "📁 Change Folder" button
2. Select the folder containing your medical records
   - PDF files (will be converted automatically)
   - JSON files (from LabCorp or Kaiser Permanente)

📄 PDF Conversion:
   • Select a folder with PDF files
   • App will convert them to JSON automatically
   • Converted files saved in 'txt_json' subfolder

🔒 Your data stays private - all processing happens on your computer!
"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, msg)
        self.update_status("No folder selected - click '📁 Change Folder' to begin")
    
    def load_data(self):
        """Load medical data from selected folder"""
        if not self.data_folder:
            self.show_no_folder_message()
            return
            
        self.update_status(f"Loading records from {self.data_folder}...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔄 Loading your health data...\n\n")
        self.root.update()
        
        try:
            self.all_tests = load_all_tests(self.data_folder, DEBUG_MODE)
            self.test_names = sorted(self.all_tests.keys())
            
            total_entries = sum(len(v) for v in self.all_tests.values())
            
            # Initialize abnormal tests manager
            self.abnormal_manager = AbnormalTestsManager(
                self.abnormal_buttons_frame,
                self.button_bg,
                self.text_color,
                self.all_tests,
                self.test_names
            )
            
            # Find abnormal tests and create buttons
            self.abnormal_manager.find_abnormal_tests()
            self.abnormal_manager.create_buttons(self.show_abnormal_test)
            
            abnormal_count = self.abnormal_manager.get_abnormal_count()
            
            welcome_msg = f"""
{'='*60}
👋 Hello! I'm Your Health Records Assistant
{'='*60}

Great news! I've successfully loaded your medical records.

📂 Data Folder: {self.data_folder}

📊 Here's what I found:
   • {len(self.test_names)} different types of health records
   • {total_entries} total test results and medical entries
   • {abnormal_count} tests with abnormal results

🤔 What would you like to know today?

You can ask me about:
   💉 "glucose" or "blood sugar" - See your glucose levels
   🩸 "WBC" or "white blood cells" - Check your blood counts  
   💊 "cholesterol" - Review your lipid panel
   💓 "blood pressure" - View your vital signs
   🏥 "colonoscopy" or "procedures" - See medical procedures
   💉 "immunizations" - Check your vaccination history

👉 Check the Abnormal Records panel on the left for quick access!

💡 Tip: Click "📁 Change Folder" to load data from a different folder

Just type what you're curious about and I'll find it for you. 😊

{'='*60}
            """
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, welcome_msg)
            self.update_status(f"✓ Ready! {len(self.test_names)} health records loaded from {os.path.basename(self.data_folder)}")
            
        except Exception as e:
            error_msg = f"😟 Oops! I had trouble loading your health data.\n\n"
            error_msg += f"Error details: {e}\n\n"
            error_msg += f"Folder: {self.data_folder}\n\n"
            error_msg += "Please make sure your folder contains valid JSON files.\n\n"
            error_msg += "Click '📁 Change Folder' to select a different folder."
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, error_msg)
            self.update_status("❌ Error loading health data")
            messagebox.showerror("Loading Error", f"I couldn't load your health records.\n\n{e}\n\nPlease select a different folder.")
    
    def show_abnormal_test(self, test_name):
        """Show specific abnormal test details and chart"""
        self.update_status(f"📊 Showing {test_name}...")
        
        # Show chart first
        if can_visualize(self.all_tests[test_name]):
            self.chart_manager.show_chart(test_name, self.all_tests[test_name])
        
        # Show results in text area
        self.results_text.delete(1.0, tk.END)
        header = f"{'='*60}\n"
        header += f"⚠️ {test_name} - Abnormal Results\n"
        header += f"{'='*60}\n\n"
        
        self.results_text.insert(tk.END, header)
        self.results_manager.insert_colored_results(self.all_tests[test_name])
        
        footer = f"\n\n{'='*60}\n"
        footer += f"💡 Understanding Your Results:\n"
        footer += f"{'='*60}\n"
        footer += f"   • Red values indicate results outside the normal range\n"
        footer += f"   • Green lines in the chart show normal range boundaries\n"
        footer += f"   • Trends help you see changes over time\n"
        footer += f"\n⚕️  Please discuss these results with your healthcare provider\n"
        self.results_text.insert(tk.END, footer)
        
        self.update_status(f"✓ Displaying {test_name} results and chart")
    
    def search(self):
        """Perform search"""
        query = self.search_var.get().strip()
        placeholder = "e.g., glucose, WBC, blood pressure..."
        
        if not query or query == placeholder:
            messagebox.showwarning("Hey there!", "Please tell me what you'd like to search for! 😊")
            return
        
        self.update_status(f"🔍 Looking up '{query}' for you...")
        self.results_text.delete(1.0, tk.END)
        self.chart_manager.hide()
        
        if not self.test_names:
            self.results_text.insert(tk.END, "Hmm, I don't have any health records loaded yet. Please check your data folder.")
            return
        
        matches = find_test(query, self.test_names)
        
        if matches:
            if len(matches) == 1:
                self.show_single_match(matches[0])
            else:
                self.show_multiple_matches(matches, query)
        else:
            self.show_no_matches(query)
    
    def show_single_match(self, test_name):
        """Display results for a single matching test"""
        header = f"{'='*60}\n"
        header += f"📋 Here are your {test_name} results:\n"
        header += f"{'='*60}\n\n"
        
        self.results_text.insert(tk.END, header)
        self.results_manager.insert_colored_results(self.all_tests[test_name])
        
        footer = f"\n💡 Tip: Red values indicate results outside the normal range.\n"
        footer += f"     Green lines in the chart show the normal range boundaries.\n"
        self.results_text.insert(tk.END, footer)
        
        self.update_status(f"✓ Found your {test_name} results!")
        
        if can_visualize(self.all_tests[test_name]):
            self.chart_manager.show_chart(test_name, self.all_tests[test_name])
    
    def show_multiple_matches(self, matches, query):
        """Display results for multiple matching tests"""
        result = f"{'='*60}\n"
        result += f"🎯 Great! I found {len(matches)} matching records for '{query}':\n"
        result += f"{'='*60}\n\n"
        
        for test_name in sorted(matches):
            result += f"{'='*50}\n"
            result += f"📊 {test_name}\n"
            result += f"{'='*50}\n"
            result += format_results(self.all_tests[test_name])
            result += "\n\n"
        
        result += f"\n💡 Tip: Try searching for a specific test name to see the trend chart!\n"
        
        self.results_text.insert(tk.END, result)
        self.update_status(f"✓ Found {len(matches)} matches for you!")
    
    def show_no_matches(self, query):
        """Display message when no matches are found"""
        result = f"🤔 Hmm, I couldn't find any records matching '{query}'.\n\n"
        result += "Here's what you can try:\n"
        result += "• Double-check the spelling\n"
        result += "• Try a different keyword (e.g., 'glucose' instead of 'sugar')\n"
        result += "• Click '📋 All Records' to see everything I have\n"
        result += "• Use the quick action buttons above for common searches\n\n"
        result += "I'm here to help - just ask me anything! 😊\n"
        self.results_text.insert(tk.END, result)
        self.update_status(f"❌ No matches found for '{query}'")
    
    def list_all_tests(self):
        """List all available tests"""
        self.update_status("📋 Gathering all your health records...")
        self.results_text.delete(1.0, tk.END)
        self.chart_manager.hide()
        
        result = f"{'='*60}\n"
        result += f"📚 Your Complete Health Records ({len(self.test_names)} types)\n"
        result += f"{'='*60}\n\n"
        result += "Here's everything I have for you:\n\n"
        
        for i, name in enumerate(self.test_names, 1):
            count = len(self.all_tests[name])
            result += f"{i:3d}. 📊 {name} ({count} entries)\n"
        
        result += f"\n💡 Click on any test name above, or just type it in the search box!\n"
        result += f"    For example: Type 'glucose' or 'WBC' to see those results.\n"
        
        self.results_text.insert(tk.END, result)
        self.update_status(f"✓ Showing all {len(self.test_names)} record types")
    
    def show_blood_tests(self):
        """Show blood test results only"""
        self.update_status("🩸 Finding your blood test results...")
        self.results_text.delete(1.0, tk.END)
        self.chart_manager.hide()
        
        blood_tests = []
        for test_name in self.test_names:
            test_lower = test_name.lower()
            
            # First check if it's NOT a blood test (exclude imaging/procedures)
            is_non_blood = any(keyword in test_lower for keyword in self.abnormal_manager.non_blood_keywords)
            
            # Then check if it IS a blood test
            is_blood = any(keyword in test_lower for keyword in self.abnormal_manager.blood_test_keywords)
            
            # Only add if it's a blood test AND not an imaging/procedure test
            if is_blood and not is_non_blood:
                blood_tests.append(test_name)
        
        if blood_tests:
            result = f"{'='*60}\n"
            result += f"🩸 Your Blood Test Results ({len(blood_tests)} types)\n"
            result += f"{'='*60}\n\n"
            result += "Here are all your blood tests:\n\n"
            
            for i, name in enumerate(sorted(blood_tests), 1):
                count = len(self.all_tests[name])
                result += f"{i:3d}. 💉 {name} ({count} entries)\n"
            
            result += f"\n💡 Want to see details? Just search for any test name above!\n"
            result += f"    For example: Type 'glucose' to see your blood sugar trends.\n"
            
            self.results_text.insert(tk.END, result)
            self.update_status(f"✓ Found {len(blood_tests)} blood tests for you!")
        else:
            result = "🤔 Hmm, I couldn't find any blood test records.\n\n"
            result += "Try clicking '📋 All Records' to see what's available!\n"
            self.results_text.insert(tk.END, result)
            self.update_status("❌ No blood tests found")
    
    def quick_search(self, query):
        """Quick search with predefined query"""
        keywords = query.split()
        
        if len(keywords) > 1:
            self.multi_keyword_search(keywords, query)
        else:
            self.search_var.set(query)
            self.search()
    
    def multi_keyword_search(self, keywords, original_query):
        """Search for multiple keywords"""
        self.update_status(f"🔍 Searching for records matching: {original_query}")
        self.results_text.delete(1.0, tk.END)
        self.chart_manager.hide()
        
        all_matches = set()
        for keyword in keywords:
            matches = find_test(keyword, self.test_names)
            if matches:
                all_matches.update(matches)
        
        if all_matches:
            result = f"{'='*60}\n"
            result += f"🎯 Found {len(all_matches)} records matching your search:\n"
            result += f"{'='*60}\n\n"
            
            for test_name in sorted(all_matches):
                result += f"{'='*50}\n"
                result += f"📊 {test_name}\n"
                result += f"{'='*50}\n"
                result += format_results(self.all_tests[test_name])
                result += "\n\n"
            
            result += f"\n💡 Tip: Search for a specific test name to see the trend chart!\n"
            
            self.results_text.insert(tk.END, result)
            self.update_status(f"✓ Found {len(all_matches)} matching records!")
        else:
            result = f"🤔 Hmm, I couldn't find any records matching: {original_query}\n\n"
            result += "Here's what I searched for:\n"
            for keyword in keywords:
                result += f"  • {keyword}\n"
            result += "\nTry:\n"
            result += "• Click '📋 All Records' to see what's available\n"
            result += "• Search for a specific test name\n"
            self.results_text.insert(tk.END, result)
            self.update_status(f"❌ No matches found")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update()