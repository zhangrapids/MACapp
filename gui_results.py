"""
Medical RAG GUI - Results Display Management
Handles formatting and displaying results with color coding
"""


class ResultsManager:
    """Manages results display with color coding for abnormal values"""
    
    def __init__(self, results_text_widget):
        self.results_text = results_text_widget
    
    def insert_colored_results(self, test_results):
        """Insert results with red/bold formatting for abnormal values"""
        # Process each test entry
        for entry in test_results:
            if not isinstance(entry, dict):
                continue
            
            # Check if this entry is abnormal
            status = entry.get('Status', '')
            is_abnormal = 'Abnormal' in status or 'HIGH' in status or 'LOW' in status or 'Out of Range' in status
            
            # Choose tag based on status
            tag = 'abnormal' if is_abnormal else None
            
            # Build the entry text
            entry_text = ""
            if 'Date' in entry:
                entry_text += f"Date: {entry['Date']}\n"
            if 'Value' in entry:
                entry_text += f"Value: {entry['Value']}"
                if 'Unit' in entry:
                    entry_text += f" {entry['Unit']}"
                entry_text += "\n"
            if 'Reference Range' in entry:
                entry_text += f"Reference Range: {entry['Reference Range']}\n"
            if 'Status' in entry:
                entry_text += f"Status: {entry['Status']}\n"
            
            # Add any other fields
            for key, value in entry.items():
                if key not in ['Date', 'Value', 'Unit', 'Reference Range', 'Status']:
                    entry_text += f"{key}: {value}\n"
            
            entry_text += "-" * 50 + "\n"
            
            # Insert with appropriate tag
            if tag:
                self.results_text.insert('end', entry_text, tag)
            else:
                self.results_text.insert('end', entry_text)