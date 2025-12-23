# Medical Health Assistant - Quick Start Guide

## 🚀 Getting Started in 3 Easy Steps

### Step 1: Install the Application
1. Double-click `MedicalHealthAssistantSetup.exe`
2. Follow the installation wizard
3. Check "Create desktop icon" (recommended)
4. Click "Finish"

### Step 2: Launch the Application
- Double-click the **Medical Health Assistant** icon on your desktop
- Or find it in your Start Menu

### Step 3: Select Your Medical Records Folder
When the app opens, you'll be asked to select a folder:

#### Option A: You Have PDF Files
1. Select the folder containing your medical record PDFs
2. Click "Yes" when asked to convert PDFs
3. Wait for conversion (creates `txt_json` subfolder)
4. Your data is now loaded and ready!

#### Option B: You Have JSON Files
1. Select the folder containing JSON files
2. Data loads immediately
3. Start exploring!

---

## 📄 PDF File Support

### What PDFs Work?
- ✅ Lab test results from LabCorp, Quest, etc.
- ✅ Medical reports from hospitals
- ✅ Blood test results
- ✅ Any text-based medical PDF

### What Happens During Conversion?
1. **Extracts text** from each PDF
2. **Creates two files** for each PDF:
   - `.txt` file - plain text version
   - `.json` file - structured data
3. **Saves in `txt_json` subfolder** - original PDFs untouched
4. **Loads JSON files** - ready for analysis

### Note About Scanned PDFs
⚠️ **Scanned/Image PDFs**: If your PDFs are scanned images (not searchable text), they may not convert properly. For best results, use PDFs where you can select and copy text.

---

## 🔍 Using the Application

### Search for Specific Tests
In the search box, type:
- `glucose` - Find glucose test results
- `cholesterol` - See cholesterol levels
- `WBC` - White blood cell counts
- `blood pressure` - Vital signs

### Quick Access Buttons
- **📁 Change Folder** - Load data from different folder
- **📋 All Records** - See everything
- **🩸 Blood Tests** - View all blood tests
- **💉 Immunization** - Vaccination records
- **🩺 Vital Signs** - BP, weight, temp, etc.
- **🏥 Procedures** - Medical procedures

### Abnormal Records Panel (Left Side)
- See tests outside normal ranges
- Click any button to view details
- Charts show trends over time

---

## 📂 Folder Structure Example

```
My Medical Records/
├── LabCorp_2023.pdf        ← Your original PDFs
├── Quest_2024.pdf
└── txt_json/               ← Created by app
    ├── LabCorp_2023.txt
    ├── LabCorp_2023.json
    ├── Quest_2024.txt
    └── Quest_2024.json     ← App reads these
```

---

## 💡 Tips & Tricks

### 1. Organize Your Files
Keep all medical records from one person in one folder:
```
Mom's Records/
Dad's Records/
My Records/
```

### 2. Regular Updates
- Add new PDFs to your folder
- Click "📁 Change Folder"
- Select the same folder
- New files will be converted

### 3. Backup Your Data
- Copy your folder regularly
- Include both PDFs and txt_json subfolder
- Store on external drive or cloud

### 4. Multiple Family Members
- Create separate folders for each person
- Switch between folders using "📁 Change Folder"

---

## ❓ Common Questions

### Q: Do I need internet?
**A:** No! Everything runs on your computer. Your data stays private.

### Q: Where is my data stored?
**A:** In the folder you selected. Original files never modified.

### Q: Can I delete the PDFs after conversion?
**A:** Yes, but keep them as backup. The app only needs the JSON files.

### Q: What if conversion fails?
**A:** 
- Check if PDFs are text-based (not scanned images)
- Try opening the PDF - can you select/copy text?
- If scanned, you may need OCR software first

### Q: Can I use both PDFs and JSON files?
**A:** Yes! Put them in the same folder. App will handle both.

### Q: How do I update to new version?
**A:** 
1. Uninstall old version
2. Install new version
3. Your data folders are untouched

---

## 🆘 Need Help?

### App Won't Start
1. Right-click icon → "Run as Administrator"
2. Check Windows Defender hasn't blocked it
3. Reinstall the application

### PDFs Won't Convert
1. App will offer to install PDF library
2. Click "Yes" to auto-install
3. Or install manually: Open Command Prompt
   ```
   pip install pdfplumber
   ```

### No Data Shows
1. Verify folder has PDF or JSON files
2. Check txt_json subfolder was created
3. Look for error messages in app

### Charts Don't Appear
- Charts only show for numeric test results
- Need multiple data points to show trends
- Some tests (text-only) won't have charts

---

## 🔒 Privacy & Security

### Your Data is Safe
- ✅ Stored only on your computer
- ✅ No internet connection needed
- ✅ No cloud uploads
- ✅ No data sharing
- ✅ You control everything

### Recommendations
1. **Encrypt your computer** (Windows BitLocker)
2. **Use strong password** for your account
3. **Regular backups** to external drive
4. **Don't share your device** with untrusted users

---

## ⚕️ Medical Disclaimer

**Important**: This software is for informational purposes only.

- ❌ Not a substitute for medical advice
- ❌ Not for diagnosis or treatment
- ✅ Always consult healthcare professionals
- ✅ Discuss abnormal results with your doctor

---

## 📞 Support

- **Email**: support@yourcompany.com
- **Website**: https://yourwebsite.com
- **User Guide**: See full documentation

---

**Enjoy using Medical Health Assistant!**

*Making your health data clear and accessible.*