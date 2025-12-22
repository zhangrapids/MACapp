# Medical Health Assistant - User Guide

## 📋 Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Using the Application](#using-the-application)
4. [Features](#features)
5. [Data Privacy](#data-privacy)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Option 1: Installer (Recommended)
1. **Download** `MedicalHealthAssistantSetup.exe`
2. **Double-click** the installer
3. **Follow** the installation wizard
4. **Choose** whether to create a desktop icon
5. **Click Finish** to launch the application

### Option 2: Portable Version
1. **Download** `MedicalHealthAssistant_Portable_v1.0.0.zip`
2. **Extract** the ZIP file to any folder
3. **Double-click** `Run Medical Health Assistant.bat`
   - Or navigate to `app` folder and run `MedicalHealthAssistant.exe`

---

## Getting Started

### First Launch
When you first launch the application:
1. The app will look for medical records in the `results` folder
2. Sample data may be included for demonstration
3. You'll see a welcome screen with instructions

### Adding Your Medical Records
1. **Locate your data folder:**
   - Installer: `C:\Program Files\Medical Health Assistant\results`
   - Portable: `[Extract Location]\app\results`

2. **Copy your JSON files:**
   - Place your medical record JSON files in the `results` folder
   - Supported formats: LabCorp, Kaiser Permanente JSON exports

3. **Restart the application** to load new data

---

## Using the Application

### Main Interface

The application has three main sections:

#### 1. **Abnormal Records Panel (Left Top)**
- Shows all test results outside normal ranges
- Organized into:
  - 🩸 **Blood Tests**: Lab values like glucose, cholesterol, WBC
  - 📋 **Other Tests**: Imaging, procedures, vital signs
- **Click any button** to view details and trends

#### 2. **Trend Visualization (Left Bottom)**
- Displays charts when you select a test
- Shows:
  - Values over time (line graph)
  - Normal range (green shaded area)
  - Abnormal values highlighted in red
  - Reference ranges

#### 3. **Chat Assistant (Right Side)**
- **Search box**: Type any test name or keyword
- **Quick categories**: One-click access to common searches
  - 📋 All Records
  - 🩸 Blood Tests
  - 💉 Immunization
  - 🩺 Vital Signs
  - 🏥 Procedures
- **Results area**: Shows detailed information

---

## Features

### 🔍 Search Functionality
**Examples:**
```
glucose          → Find glucose test results
WBC             → White blood cell counts
cholesterol     → Lipid panel results
blood pressure  → Vital signs
```

### 📊 Trend Analysis
- **Automatic charting** for numeric values
- **Color coding:**
  - 🔴 Red: Abnormal values
  - 🟢 Green: Normal range boundaries
  - 🔵 Blue: Your values over time

### ⚠️ Abnormal Detection
The app automatically identifies:
- Values outside reference ranges
- Tests flagged as HIGH or LOW
- Critical results

### 💬 Natural Language
Ask questions naturally:
- "Show me my glucose"
- "What are my blood tests?"
- "Find immunizations"

---

## Data Privacy

### Your Data Stays Private
✅ **Local Storage Only**
- All data stays on your computer
- No cloud uploads
- No internet connection required

✅ **No Data Collection**
- We don't collect personal information
- No analytics or tracking
- No third-party sharing

✅ **Your Responsibility**
- Back up your data regularly
- Secure your computer
- Don't share your device login

### Security Recommendations
1. **Encrypt your computer** (Windows BitLocker)
2. **Use strong passwords**
3. **Keep your system updated**
4. **Regular backups** to external drive

---

## Troubleshooting

### Application Won't Start
**Problem:** Double-clicking does nothing
**Solutions:**
1. Right-click → "Run as Administrator"
2. Check Windows Defender hasn't blocked it
3. Verify Windows 10 or later
4. Reinstall the application

### No Data Appears
**Problem:** App shows "No records loaded"
**Solutions:**
1. Verify JSON files are in the `results` folder
2. Check file format (should be valid JSON)
3. Look for error messages in the status bar
4. Try the sample data first

### Charts Not Displaying
**Problem:** Charts don't appear for test results
**Solutions:**
1. Ensure test has numeric values
2. Check if multiple data points exist
3. Verify reference ranges are included
4. Some tests (text-only) won't chart

### Search Returns No Results
**Problem:** Search doesn't find known tests
**Solutions:**
1. Check spelling
2. Try different keywords (e.g., "glucose" vs "sugar")
3. Click "📋 All Records" to see available tests
4. Use partial names (e.g., "chol" for cholesterol)

### Abnormal Test Buttons Overflow
**Problem:** Buttons extend beyond panel
**Solutions:**
1. This should auto-wrap to multiple rows
2. Resize the window wider
3. If persists, report as a bug

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Submit search |
| Ctrl+A | Select all text |
| Ctrl+C | Copy selected text |
| Mouse Wheel | Scroll results |

---

## System Requirements

### Minimum
- **OS:** Windows 10 (64-bit)
- **RAM:** 4 GB
- **Disk:** 200 MB free space
- **Display:** 1280x720 resolution

### Recommended
- **OS:** Windows 11 (64-bit)
- **RAM:** 8 GB or more
- **Disk:** 500 MB free space
- **Display:** 1920x1080 or higher

---

## Getting Help

### Support Options
1. **Check this guide** for common issues
2. **Email:** support@yourcompany.com
3. **Website:** https://yourwebsite.com/support
4. **Include:**
   - Windows version
   - Error messages
   - Screenshots
   - Steps to reproduce

---

## Version History

### Version 1.0.0 (2024)
- Initial release
- Medical record viewing
- Trend visualization
- Abnormal test detection
- Search functionality

---

## Legal

### Medical Disclaimer
⚠️ **Important:** This software is for informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

**Always:**
- Consult qualified healthcare professionals
- Follow your doctor's recommendations
- Discuss abnormal results with your physician
- Seek emergency care when needed

### License
This software is provided under the End User License Agreement included with installation.

---

## Tips for Best Results

1. **Regular Updates:** Check for app updates quarterly
2. **Data Organization:** Keep records in chronological order
3. **Backup Strategy:** Copy `results` folder monthly
4. **Note Taking:** Keep a health journal alongside the app
5. **Doctor Visits:** Bring printed reports from the app

---

**Thank you for using Medical Health Assistant!**

*Empowering you to understand your health data.*