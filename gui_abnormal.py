"""
GUI Abnormal Tests Manager
Handles detection and display of abnormal test results
"""
import tkinter as tk


class AbnormalTestsManager:
    """Manages abnormal test detection and button creation"""
    
    def __init__(self, parent_frame, button_bg, text_color, all_tests, test_names):
        self.parent_frame = parent_frame
        self.button_bg = button_bg
        self.text_color = text_color
        self.all_tests = all_tests
        self.test_names = test_names
        
        self.abnormal_tests = []
        self.abnormal_blood_tests = []
        self.abnormal_other_tests = []
        
        # Blood test keywords for categorization
        self.blood_test_keywords = [
            'wbc', 'rbc', 'hemoglobin', 'hematocrit', 'platelet',
            'glucose', 'cholesterol', 'triglyceride', 'hdl', 'ldl',
            'sodium', 'potassium', 'chloride', 'calcium', 'magnesium',
            'creatinine', 'bun', 'alt', 'ast', 'alkaline phosphatase',
            'bilirubin', 'albumin', 'protein', 'globulin',
            'neutrophil', 'lymphocyte', 'monocyte', 'eosinophil', 'basophil',
            'mcv', 'mch', 'mchc', 'rdw', 'mpv',
            'tsh', 'vitamin', 'iron', 'ferritin', 'b12', 'folate',
            'psa', 'a1c', 'hemoglobin a1c', 'egfr', 'inr'
        ]
        
        # Non-blood test keywords (imaging, procedures)
        self.non_blood_keywords = [
            'fluoro', 'xr', 'x-ray', 'colon', 'air', 'imaging', 'scan',
            'colonoscopy', 'endoscopy', 'biopsy', 'procedure'
        ]
    
    def is_abnormal_value(self, entry):
        """Check if a test entry has abnormal values"""
        if not isinstance(entry, dict):
            return False
        
        # Check Status field
        status = entry.get('Status', '').upper()
        if any(keyword in status for keyword in ['ABNORMAL', 'HIGH', 'LOW', 'OUT OF RANGE', 'CRITICAL']):
            return True
        
        # Check Flag field
        flag = entry.get('Flag', '').upper()
        if any(keyword in flag for keyword in ['ABNORMAL', 'HIGH', 'LOW', 'H', 'L', 'CRITICAL']):
            return True
        
        # Check if value is outside reference range
        try:
            value = entry.get('Value', '')
            ref_range = entry.get('Reference Range', '')
            
            if value and ref_range and '-' in ref_range:
                # Try to parse numeric value and range
                value_num = float(str(value).split()[0])
                range_parts = ref_range.split('-')
                if len(range_parts) == 2:
                    low = float(range_parts[0].strip())
                    high = float(range_parts[1].strip().split()[0])
                    if value_num < low or value_num > high:
                        return True
        except (ValueError, AttributeError, IndexError):
            pass
        
        return False
    
    def find_abnormal_tests(self):
        """Find all tests with abnormal results"""
        self.abnormal_tests = []
        self.abnormal_blood_tests = []
        self.abnormal_other_tests = []
        
        print(f"\n=== ABNORMAL TEST DETECTION ===")
        print(f"Checking {len(self.test_names)} tests...")
        
        # Find tests with abnormal values
        for test_name in self.test_names:
            test_data = self.all_tests[test_name]
            has_abnormal = False
            
            for entry in test_data:
                if self.is_abnormal_value(entry):
                    has_abnormal = True
                    break
            
            if has_abnormal:
                self.abnormal_tests.append(test_name)
                print(f"✓ Found abnormal: {test_name}")
                
                # Check if it's a non-blood test first (imaging, procedures)
                test_lower = test_name.lower()
                if any(keyword in test_lower for keyword in self.non_blood_keywords):
                    self.abnormal_other_tests.append(test_name)
                    print(f"  → Categorized as OTHER TEST (imaging/procedure)")
                # Then check if it's a blood test
                elif any(keyword in test_lower for keyword in self.blood_test_keywords):
                    self.abnormal_blood_tests.append(test_name)
                    print(f"  → Categorized as BLOOD TEST")
                else:
                    self.abnormal_other_tests.append(test_name)
                    print(f"  → Categorized as OTHER TEST")
        
        print(f"\n=== SUMMARY ===")
        print(f"Total abnormal tests: {len(self.abnormal_tests)}")
        print(f"Blood tests: {len(self.abnormal_blood_tests)}")
        print(f"Other tests: {len(self.abnormal_other_tests)}")
        print(f"Blood tests list: {self.abnormal_blood_tests}")
        print(f"Other tests list: {self.abnormal_other_tests}")
        print(f"================\n")
        
        return self.abnormal_tests
    
    def create_buttons(self, click_callback):
        """Create individual buttons for each abnormal test"""
        # Clear existing buttons
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        print(f"\n=== CREATING BUTTONS ===")
        print(f"Blood tests to create: {len(self.abnormal_blood_tests)}")
        print(f"Other tests to create: {len(self.abnormal_other_tests)}")
        
        if not self.abnormal_blood_tests and not self.abnormal_other_tests:
            # No abnormal tests
            label = tk.Label(
                self.parent_frame,
                text="🎉 Great news!\n\nNo abnormal results found.\n\nAll your test results\nare within normal range!",
                bg="white",
                fg="green",
                font=("Arial", 11, "bold"),
                justify=tk.CENTER
            )
            label.pack(pady=30, padx=20)
            print("No abnormal tests - showing success message")
            return
        
        # Blood tests section
        if self.abnormal_blood_tests:
            print(f"\nCreating Blood Tests section with {len(self.abnormal_blood_tests)} buttons...")
            
            blood_label = tk.Label(
                self.parent_frame,
                text="🩸 Blood Tests",
                bg="white",
                fg=self.text_color,
                font=("Arial", 11, "bold"),
                anchor="w"
            )
            blood_label.pack(fill=tk.X, pady=(10, 8), padx=10)
            
            # Create container frame for buttons with wrapping
            blood_container = tk.Frame(self.parent_frame, bg="white")
            blood_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
            
            # Optimize button arrangement for blood tests
            self._create_optimized_button_layout(
                sorted(self.abnormal_blood_tests), 
                click_callback, 
                blood_container
            )
        
        # Other tests section
        if self.abnormal_other_tests:
            print(f"\nCreating Other Tests section with {len(self.abnormal_other_tests)} buttons...")
            
            other_label = tk.Label(
                self.parent_frame,
                text="📋 Other Tests",
                bg="white",
                fg=self.text_color,
                font=("Arial", 11, "bold"),
                anchor="w"
            )
            other_label.pack(fill=tk.X, pady=(20, 8), padx=10)
            
            # Create container frame for buttons with wrapping
            other_container = tk.Frame(self.parent_frame, bg="white")
            other_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
            
            # Optimize button arrangement for other tests
            self._create_optimized_button_layout(
                sorted(self.abnormal_other_tests), 
                click_callback, 
                other_container
            )
        
        print(f"=== BUTTONS CREATED ===\n")
    
    def _create_test_button(self, test_name, click_callback):
        """Create a single test button with hover effects"""
        btn = tk.Button(
            self.parent_frame,
            text=f"📊 {test_name}",
            command=lambda: click_callback(test_name),
            bg=self.button_bg,
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            cursor="hand2",
            anchor="w",
            padx=15,
            pady=10,
            activebackground="#1976D2",
            activeforeground="white",
            bd=2
        )
        btn.pack(fill=tk.X, pady=4, padx=10)
        
        # Add hover effect
        def on_enter(e):
            btn.config(bg="#1976D2")
        
        def on_leave(e):
            btn.config(bg=self.button_bg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def _create_test_button_in_row(self, test_name, click_callback, container):
        """Create a button that arranges in rows (left to right, wrapping when needed)"""
        # Shorten test name to first two words if more than two words
        display_name = self._shorten_test_name(test_name)
        
        btn = tk.Button(
            container,
            text=f"📊 {display_name}",
            command=lambda: click_callback(test_name),
            bg=self.button_bg,
            fg="white",
            font=("Arial", 9, "bold"),
            relief=tk.RAISED,
            cursor="hand2",
            padx=12,
            pady=6,
            activebackground="#1976D2",
            activeforeground="white",
            bd=2
        )
        btn.pack(side=tk.LEFT, padx=3, pady=3)
        
        # Add hover effect
        def on_enter(e):
            btn.config(bg="#1976D2")
        
        def on_leave(e):
            btn.config(bg=self.button_bg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def _shorten_test_name(self, test_name):
        """Shorten test name to first two words if more than two words"""
        words = test_name.split()
        if len(words) > 2:
            return ' '.join(words[:2])
        return test_name
    
    def _create_optimized_button_layout(self, test_names, click_callback, container):
        """Create optimized button layout that maximizes first row usage"""
        max_row_width = 800
        
        # Calculate width for each test name
        test_widths = []
        for test_name in test_names:
            display_name = self._shorten_test_name(test_name)
            estimated_width = len(display_name) * 9 + 50
            test_widths.append((test_name, display_name, estimated_width))
        
        # Sort by width (shortest first) to pack efficiently
        test_widths.sort(key=lambda x: x[2])
        
        # Greedy bin packing: fill rows optimally
        rows = []
        current_row = []
        current_width = 0
        
        for test_name, display_name, width in test_widths:
            if current_width + width <= max_row_width or len(current_row) == 0:
                current_row.append((test_name, display_name, width))
                current_width += width
            else:
                # Current row is full, start new row
                rows.append(current_row)
                current_row = [(test_name, display_name, width)]
                current_width = width
        
        # Add last row
        if current_row:
            rows.append(current_row)
        
        # Create buttons in optimized order
        print(f"  Optimized into {len(rows)} rows:")
        for row_idx, row in enumerate(rows, 1):
            row_frame = tk.Frame(container, bg="white")
            row_frame.pack(fill=tk.X, pady=2)
            
            row_total_width = sum(item[2] for item in row)
            print(f"    Row {row_idx}: {len(row)} buttons, total width ~{row_total_width}px")
            
            for test_name, display_name, width in row:
                self._create_test_button_in_row(test_name, click_callback, row_frame)
    
    def get_abnormal_count(self):
        """Get count of abnormal tests"""
        return len(self.abnormal_tests)