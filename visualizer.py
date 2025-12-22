"""
visualizer.py - Create visualizations for medical test results
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import tkinter as tk

def can_visualize(results):
    """Check if results can be visualized (numeric values)"""
    if not results or len(results) < 2:
        return False
    
    # Check if we have numeric values
    try:
        for r in results[:3]:  # Check first 3 entries
            float(r['Value'])
        return True
    except (ValueError, TypeError, KeyError):
        return False


def create_trend_chart(parent_frame, results, test_name):
    """Create a bar chart showing test trends over time"""
    
    # Clear existing widgets in frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Sort by date
    sorted_results = sorted(
        results,
        key=lambda x: datetime.strptime(x['Date'], "%m/%d/%Y")
    )
    
    # Extract data
    dates = []
    values = []
    colors = []
    
    for r in sorted_results:
        try:
            dates.append(r['Date'])
            values.append(float(r['Value']))
            
            # Color based on status
            if r['Status'] == 'High':
                colors.append('#ff6b6b')  # Red
            elif r['Status'] == 'Low':
                colors.append('#ffd93d')  # Yellow
            else:
                colors.append('#6bcf7f')  # Green
        except (ValueError, TypeError):
            continue
    
    if not values:
        no_data_label = tk.Label(
            parent_frame,
            text="No numeric data available for visualization",
            font=("Arial", 10),
            fg="#666666"
        )
        no_data_label.pack(pady=20)
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 3), facecolor='white')
    
    # Create bar chart
    bars = ax.bar(range(len(values)), values, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # Customize
    ax.set_xlabel('Date', fontsize=10, fontweight='bold')
    ax.set_ylabel('Value', fontsize=10, fontweight='bold')
    ax.set_title(f'{test_name} - Trend Over Time', fontsize=12, fontweight='bold', pad=15)
    
    # Set x-axis labels
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=8)
    
    # Add reference range if available
    if sorted_results[0].get('Reference Range'):
        ref_range = sorted_results[0]['Reference Range']
        try:
            if '-' in ref_range:
                parts = ref_range.split('-')
                low = float(parts[0].strip())
                high = float(parts[1].strip())
                
                # Add horizontal lines for reference range
                ax.axhline(y=low, color='blue', linestyle='--', linewidth=1, alpha=0.5, label=f'Low: {low}')
                ax.axhline(y=high, color='blue', linestyle='--', linewidth=1, alpha=0.5, label=f'High: {high}')
                
                # Shade reference range
                ax.fill_between(range(len(values)), low, high, alpha=0.1, color='blue')
        except:
            pass
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}',
                ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Grid
    ax.grid(True, alpha=0.3, axis='y', linestyle=':', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Legend
    if ax.get_legend_handles_labels()[0]:
        ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    
    # Tight layout
    plt.tight_layout()
    
    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    return canvas