"""
Medical RAG GUI - UI Widget Creation Functions
Contains all the UI widget creation logic
"""
import tkinter as tk
from tkinter import scrolledtext


def create_header(root, accent_color, title="Medical Health Assistant"):
    """Create the header frame"""
    header_frame = tk.Frame(root, bg=accent_color, height=60)
    header_frame.pack(fill=tk.X, side=tk.TOP)
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text=f"🏥 {title}",
        font=("Arial", 20, "bold"),
        bg=accent_color,
        fg="white"
    )
    title_label.pack(pady=15)


def create_search_frame(parent, bg_color, text_color, accent_color, 
                       search_callback, list_all_callback, blood_tests_callback,
                       abnormal_callback, quick_search_callback):
    """Create the search frame with entry and buttons"""
    search_frame = tk.LabelFrame(
        parent,
        text="💬 Chat with Your Health Assistant",
        font=("Arial", 11, "bold"),
        bg=bg_color,
        fg=text_color,
        padx=10,
        pady=10
    )
    search_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Search entry label
    tk.Label(
        search_frame,
        text="Ask me anything about your health records:",
        bg=bg_color,
        fg=text_color,
        font=("Arial", 10)
    ).pack(anchor=tk.W, pady=(0, 5))
    
    # Search entry frame
    search_entry_frame = tk.Frame(search_frame, bg=bg_color)
    search_entry_frame.pack(fill=tk.X, pady=(0, 10))
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(
        search_entry_frame,
        textvariable=search_var,
        font=("Arial", 12),
        relief=tk.FLAT,
        bg="white",
        fg=text_color
    )
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
    search_entry.bind('<Return>', lambda e: search_callback())
    search_entry.insert(0, "e.g., glucose, WBC, blood pressure...")
    search_entry.config(fg='gray')
    
    def on_focus_in(event):
        if search_entry.get() == "e.g., glucose, WBC, blood pressure...":
            search_entry.delete(0, tk.END)
            search_entry.config(fg=text_color)
    
    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "e.g., glucose, WBC, blood pressure...")
            search_entry.config(fg='gray')
    
    search_entry.bind('<FocusIn>', on_focus_in)
    search_entry.bind('<FocusOut>', on_focus_out)
    
    search_btn = tk.Button(
        search_entry_frame,
        text="🔍 Ask",
        command=search_callback,
        bg=accent_color,
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        padx=20
    )
    search_btn.pack(side=tk.LEFT, padx=(5, 0))
    
    # Helper text
    tk.Label(
        search_frame,
        text="Or use these quick actions:",
        bg=bg_color,
        fg=text_color,
        font=("Arial", 9, "italic")
    ).pack(anchor=tk.W, pady=(5, 5))
    
    # Quick action buttons - First row
    btn_frame1 = tk.Frame(search_frame, bg=bg_color)
    btn_frame1.pack(fill=tk.X, pady=(0, 5))
    
    buttons1 = [
        ("📋 Show All Records", list_all_callback),
        ("🩸 Blood Tests", blood_tests_callback),
        ("⚠️ Abnormal Results", abnormal_callback),
    ]
    
    for text, command in buttons1:
        btn = tk.Button(
            btn_frame1,
            text=text,
            command=command,
            bg="white",
            fg=text_color,
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=5
        )
        btn.pack(side=tk.LEFT, padx=2)
    
    # Quick action buttons - Second row
    btn_frame2 = tk.Frame(search_frame, bg=bg_color)
    btn_frame2.pack(fill=tk.X)
    
    buttons2 = [
        ("💉 Immunizations", lambda: quick_search_callback("immunization")),
        ("🩺 Vital Signs", lambda: quick_search_callback("blood pressure weight height temperature pulse")),
        ("🏥 Procedures", lambda: quick_search_callback("colonoscopy endoscopy biopsy surgery screening")),
    ]
    
    for text, command in buttons2:
        btn = tk.Button(
            btn_frame2,
            text=text,
            command=command,
            bg="white",
            fg=text_color,
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=5
        )
        btn.pack(side=tk.LEFT, padx=2)
    
    return search_var


def create_results_frame(parent, bg_color, text_color):
    """Create the results display frame"""
    # Results display (left side of content)
    results_frame = tk.LabelFrame(
        parent,
        text="Results",
        font=("Arial", 11, "bold"),
        bg=bg_color,
        fg=text_color,
        padx=10,
        pady=10
    )
    results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    results_text = scrolledtext.ScrolledText(
        results_frame,
        wrap=tk.WORD,
        font=("Consolas", 10),
        bg="white",
        fg=text_color,
        relief=tk.FLAT,
        padx=10,
        pady=10
    )
    results_text.pack(fill=tk.BOTH, expand=True)
    
    # Configure text tags for red/bold abnormal values
    results_text.tag_configure("abnormal", foreground="red", font=("Consolas", 10, "bold"))
    
    # Chart frame (right side of content, initially hidden)
    chart_frame = tk.LabelFrame(
        parent,
        text="Trend Visualization",
        font=("Arial", 11, "bold"),
        bg=bg_color,
        fg=text_color,
        padx=10,
        pady=10
    )
    
    return results_text, chart_frame


def create_info_panel(parent, bg_color, text_color):
    """Create the info panel on the right"""
    right_frame = tk.Frame(parent, bg=bg_color, width=250)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
    right_frame.pack_propagate(False)
    
    # Statistics
    stats_frame = tk.LabelFrame(
        right_frame,
        text="Statistics",
        font=("Arial", 11, "bold"),
        bg=bg_color,
        fg=text_color,
        padx=10,
        pady=10
    )
    stats_frame.pack(fill=tk.X, pady=(0, 10))
    
    stats_label = tk.Label(
        stats_frame,
        text="Loading data...",
        bg=bg_color,
        fg=text_color,
        font=("Arial", 10),
        justify=tk.LEFT,
        anchor=tk.W
    )
    stats_label.pack(fill=tk.X)
    
    # Help
    help_frame = tk.LabelFrame(
        right_frame,
        text="Quick Help",
        font=("Arial", 11, "bold"),
        bg=bg_color,
        fg=text_color,
        padx=10,
        pady=10
    )
    help_frame.pack(fill=tk.BOTH, expand=True)
    
    help_text = """
💬 How to Chat with Me:

Just type naturally!

Examples:
• "glucose" or "blood sugar"
  → I'll show your glucose trends

• "WBC" or "white blood cells"
  → See your blood count results

• "cholesterol"
  → Review your lipid panel

• "blood pressure"
  → Check your vital signs

• "procedures" or "colonoscopy"
  → View medical procedures

🎯 Quick Tips:
- Just ask in plain language
- Use the buttons for instant results
- Red text = needs attention
- Green chart lines = normal range
- I'm here to help! 😊
    """
    
    help_label = tk.Label(
        help_frame,
        text=help_text.strip(),
        bg=bg_color,
        fg=text_color,
        font=("Arial", 9),
        justify=tk.LEFT,
        anchor=tk.NW
    )
    help_label.pack(fill=tk.BOTH, expand=True)
    
    return stats_label


def create_status_bar(root, text_color):
    """Create the status bar at the bottom"""
    status_frame = tk.Frame(root, bg="#e0e0e0", height=30)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    status_frame.pack_propagate(False)
    
    status_label = tk.Label(
        status_frame,
        text="Ready",
        bg="#e0e0e0",
        fg=text_color,
        font=("Arial", 9),
        anchor=tk.W
    )
    status_label.pack(fill=tk.BOTH, padx=10)
    
    return status_label