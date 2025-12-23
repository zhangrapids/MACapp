"""
Trial Expiration System - Add this to your main application file
This creates a 100-day trial period from first installation
"""

import os
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

class TrialManager:
    """Manages trial period and expiration"""
    
    TRIAL_DAYS = 100
    
    def __init__(self):
        """Initialize trial manager"""
        # Store trial data in user's AppData folder (harder to find and delete)
        if sys.platform == 'win32':
            appdata = os.getenv('APPDATA')
            self.trial_file = os.path.join(appdata, 'MedicalHealthAssistant', '.trial_info')
        else:
            home = Path.home()
            self.trial_file = home / '.medical_health_assistant' / '.trial_info'
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.trial_file), exist_ok=True)
        
    def _obfuscate(self, data):
        """Simple obfuscation to make trial file less obvious"""
        import base64
        json_str = json.dumps(data)
        encoded = base64.b64encode(json_str.encode()).decode()
        # Add some random-looking prefix/suffix
        return f"MHAV1_{encoded}_END"
    
    def _deobfuscate(self, data):
        """Reverse the obfuscation"""
        import base64
        try:
            # Remove prefix/suffix
            if data.startswith("MHAV1_") and data.endswith("_END"):
                encoded = data[6:-4]
                decoded = base64.b64decode(encoded.encode()).decode()
                return json.loads(decoded)
        except:
            pass
        return None
    
    def get_trial_info(self):
        """Get trial information"""
        if os.path.exists(self.trial_file):
            try:
                with open(self.trial_file, 'r') as f:
                    obfuscated = f.read()
                    data = self._deobfuscate(obfuscated)
                    if data:
                        return data
            except:
                pass
        
        # First run - create trial info
        return self._create_trial()
    
    def _create_trial(self):
        """Create trial information on first run"""
        trial_data = {
            'first_run': datetime.now().isoformat(),
            'trial_days': self.TRIAL_DAYS,
            'version': '1.0.0'
        }
        
        try:
            with open(self.trial_file, 'w') as f:
                f.write(self._obfuscate(trial_data))
            # Make file hidden on Windows
            if sys.platform == 'win32':
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(self.trial_file, 0x02)
        except:
            pass
        
        return trial_data
    
    def check_trial(self):
        """
        Check if trial is still valid
        Returns: (is_valid, days_remaining, message)
        """
        trial_info = self.get_trial_info()
        
        try:
            first_run = datetime.fromisoformat(trial_info['first_run'])
            trial_days = trial_info['trial_days']
            
            now = datetime.now()
            days_used = (now - first_run).days
            days_remaining = trial_days - days_used
            
            if days_remaining <= 0:
                return False, 0, "Trial period has expired"
            elif days_remaining <= 10:
                return True, days_remaining, f"Warning: Only {days_remaining} days remaining in trial"
            else:
                return True, days_remaining, f"Trial: {days_remaining} days remaining"
                
        except Exception as e:
            # If there's any error reading trial info, treat as expired
            return False, 0, "Trial information corrupted"
    
    def show_expiration_dialog(self, days_remaining=0):
        """Show trial expiration dialog"""
        root = tk.Tk()
        root.withdraw()
        
        if days_remaining <= 0:
            messagebox.showerror(
                "Trial Expired",
                "Your 100-day trial period has expired.\n\n"
                "Thank you for using Medical Health Assistant!\n\n"
                "To continue using this software, please contact:\n"
                "Email: your.email@company.com\n"
                "Website: https://yourwebsite.com\n\n"
                "The application will now close."
            )
        else:
            messagebox.showwarning(
                "Trial Period Ending Soon",
                f"You have {days_remaining} days remaining in your trial period.\n\n"
                "To continue using this software after the trial expires, please contact:\n"
                "Email: your.email@company.com\n"
                "Website: https://yourwebsite.com"
            )
        
        root.destroy()
    
    def show_trial_info_menubar(self, days_remaining):
        """Returns text to display in application menu/status bar"""
        if days_remaining <= 10:
            return f"⚠️ Trial: {days_remaining} days left"
        else:
            return f"Trial: {days_remaining} days left"


def check_trial_and_start_app():
    """
    Call this function at the start of your application
    Returns True if app should continue, False if trial expired
    """
    trial_manager = TrialManager()
    is_valid, days_remaining, message = trial_manager.check_trial()
    
    if not is_valid:
        # Trial expired - show message and exit
        trial_manager.show_expiration_dialog(days_remaining)
        return False
    
    # Trial still valid
    if days_remaining <= 10:
        # Show warning for last 10 days
        trial_manager.show_expiration_dialog(days_remaining)
    
    print(f"Trial Status: {message}")
    return True


# ============================================================
# INTEGRATION INSTRUCTIONS
# ============================================================

"""
HOW TO INTEGRATE INTO YOUR APPLICATION:

1. Add this file to your project (e.g., save as 'trial_manager.py')

2. In your main application file (e.g., medical_health_assistant.py), 
   add at the very beginning of the main() function:

   from trial_manager import check_trial_and_start_app, TrialManager
   
   def main():
       # Check trial before starting app
       if not check_trial_and_start_app():
           sys.exit(0)  # Exit if trial expired
       
       # Rest of your application code...
       root = tk.Tk()
       app = MedicalHealthAssistant(root)
       root.mainloop()

3. (Optional) Add trial status to your UI:
   
   In your application's __init__ method:
   
   def __init__(self, root):
       self.trial_manager = TrialManager()
       is_valid, days_remaining, message = self.trial_manager.check_trial()
       
       # Add to status bar or menu
       trial_label = tk.Label(root, 
                             text=self.trial_manager.show_trial_info_menubar(days_remaining),
                             fg='red' if days_remaining <= 10 else 'gray')
       trial_label.pack(side='right')

4. Update your setup.py to include the trial_manager.py file:
   
   In the build_exe_options dictionary, add to 'include_files':
   'trial_manager.py'

5. IMPORTANT: After making these changes, rebuild your application:
   
   python setup.py build
"""


# ============================================================
# TESTING THE TRIAL SYSTEM
# ============================================================

def test_trial_system():
    """Test function to verify trial system works"""
    print("=" * 60)
    print("Testing Trial System")
    print("=" * 60)
    
    trial_manager = TrialManager()
    is_valid, days_remaining, message = trial_manager.check_trial()
    
    print(f"Trial Valid: {is_valid}")
    print(f"Days Remaining: {days_remaining}")
    print(f"Message: {message}")
    print(f"Trial file location: {trial_manager.trial_file}")
    
    if os.path.exists(trial_manager.trial_file):
        print(f"Trial file exists: YES")
        trial_info = trial_manager.get_trial_info()
        print(f"First run date: {trial_info['first_run']}")
        print(f"Trial period: {trial_info['trial_days']} days")
    else:
        print(f"Trial file exists: NO (will be created on first run)")
    
    print("=" * 60)


if __name__ == "__main__":
    # Run test when script is executed directly
    test_trial_system()