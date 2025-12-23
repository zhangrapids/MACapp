"""
Medical RAG GUI - Chart Management
Handles all chart creation and display logic
"""
import re
from datetime import datetime

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ChartManager:
    """Manages chart creation and display"""
    
    def __init__(self, chart_frame, accent_color):
        self.chart_frame = chart_frame
        self.accent_color = accent_color
    
    def hide(self):
        """Hide the chart frame"""
        self.chart_frame.pack_forget()
    
    def show_chart(self, test_name, results):
        """Display trend chart for numeric results"""
        try:
            # Clear any existing chart content
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            print(f"\n{'='*60}")
            print(f"CREATING CHART FOR: {test_name}")
            print(f"{'='*60}")
            
            # Extract data
            data_points = []
            normal_min = None
            normal_max = None
            
            # First pass - find normal range from first entry
            if len(results) > 0 and isinstance(results[0], dict):
                first_entry = results[0]
                print(f"First entry keys: {first_entry.keys()}")
                print(f"First entry: {first_entry}")
                
                # Check for 'Reference Range' field (capital R)
                if 'Reference Range' in first_entry:
                    range_str = str(first_entry['Reference Range'])
                    print(f"Found 'Reference Range': '{range_str}'")
                    match = re.search(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', range_str)
                    if match:
                        normal_min = float(match.group(1))
                        normal_max = float(match.group(2))
                        print(f"✓ Parsed range: {normal_min} to {normal_max}")
            
            # Extract values and dates
            for idx, entry in enumerate(results):
                if not isinstance(entry, dict):
                    continue
                
                # Find date
                date_str = entry.get('Date') or entry.get('date')
                # Find value  
                value_raw = entry.get('Value') or entry.get('value')
                
                if date_str and value_raw:
                    try:
                        # Parse date
                        date_obj = None
                        for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%Y/%m/%d']:
                            try:
                                date_obj = datetime.strptime(str(date_str), fmt)
                                break
                            except:
                                pass
                        
                        if date_obj:
                            # Parse value
                            value_str = str(value_raw).replace('<', '').replace('>', '').strip()
                            match = re.search(r'\d+\.?\d*', value_str)
                            if match:
                                value = float(match.group())
                                data_points.append((date_obj, value))
                    except:
                        pass
            
            print(f"Extracted {len(data_points)} data points")
            print(f"Normal range: {normal_min} - {normal_max}")
            
            if len(data_points) == 0:
                # Show message that no data available
                no_data_label = tk.Label(
                    self.chart_frame,
                    text="No numeric data available\nfor visualization",
                    font=("Arial", 11),
                    fg="gray",
                    bg="white"
                )
                no_data_label.pack(expand=True)
                print("No data points - skipping chart")
                return
            
            # Sort and reverse (recent first)
            data_points.sort(key=lambda x: x[0])
            data_points.reverse()
            
            dates = [dp[0] for dp in data_points]
            values = [dp[1] for dp in data_points]
            
            # Create figure - adjusted size for new layout
            fig = Figure(figsize=(6, 5), dpi=80)
            ax = fig.add_subplot(111)
            
            # Determine colors
            print("\nBar colors:")
            bar_colors = []
            for i, val in enumerate(values):
                is_abnormal = False
                if normal_min and val < normal_min:
                    is_abnormal = True
                    print(f"  Bar {i}: {val} < {normal_min} = ABNORMAL (RED)")
                elif normal_max and val > normal_max:
                    is_abnormal = True
                    print(f"  Bar {i}: {val} > {normal_max} = ABNORMAL (RED)")
                else:
                    print(f"  Bar {i}: {val} = normal (blue)")
                
                bar_colors.append('red' if is_abnormal else 'blue')
            
            # Plot bars
            positions = list(range(len(values)))
            for i, (pos, val, color) in enumerate(zip(positions, values, bar_colors)):
                if color == 'red':
                    ax.bar(pos, val, color='#FF0000', alpha=0.9, width=0.6, edgecolor='darkred', linewidth=2)
                else:
                    ax.bar(pos, val, color='#2196F3', alpha=0.7, width=0.6)
            
            # Add green reference lines
            if normal_min:
                ax.axhline(y=normal_min, color='lime', linestyle='--', linewidth=5, 
                          label=f'Min: {normal_min}', alpha=1.0, zorder=100)
                print(f"✓ Added green line at y={normal_min}")
            
            if normal_max:
                ax.axhline(y=normal_max, color='lime', linestyle='--', linewidth=5,
                          label=f'Max: {normal_max}', alpha=1.0, zorder=100)
                print(f"✓ Added green line at y={normal_max}")
            
            # Format
            date_labels = [d.strftime('%m/%d/%y') for d in dates]
            ax.set_xticks(positions)
            ax.set_xticklabels(date_labels, rotation=45, ha='right', fontsize=8)
            ax.set_ylabel('Value', fontsize=10, fontweight='bold')
            ax.set_xlabel('Date (Recent → Older)', fontsize=9, fontweight='bold')
            ax.set_title(f'{test_name}\nTrend', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            if normal_min or normal_max:
                ax.legend(loc='best', fontsize=8)
            
            # Add value labels
            for i, (val, color) in enumerate(zip(values, bar_colors)):
                text_color = 'red' if color == 'red' else 'black'
                weight = 'bold' if color == 'red' else 'normal'
                ax.text(i, val, f'{val:.0f}', ha='center', va='bottom', 
                       fontsize=7, color=text_color, fontweight=weight)
            
            fig.tight_layout()
            
            # Embed
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
            
            print("✓ Chart created successfully!\n")
            
        except Exception as e:
            print(f"✗ Chart error: {e}")
            import traceback
            traceback.print_exc()
            # Show error message
            error_label = tk.Label(
                self.chart_frame,
                text="Error creating chart\nSee console for details",
                font=("Arial", 10),
                fg="red",
                bg="white"
            )
            error_label.pack(expand=True)