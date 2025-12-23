"""
PDF Converter Module
Converts medical record PDFs to text and JSON format
"""
import os
import json
from pathlib import Path


def convert_pdfs_to_json(pdf_folder, output_folder=None):
    """
    Convert all PDF files in a folder to text and JSON
    
    Args:
        pdf_folder: Path to folder containing PDF files
        output_folder: Path to output folder (default: pdf_folder/txt_json)
    
    Returns:
        tuple: (num_converted, output_folder_path, errors)
    """
    pdf_folder = Path(pdf_folder)
    
    # Create output folder if not specified
    if output_folder is None:
        output_folder = pdf_folder / "txt_json"
    else:
        output_folder = Path(output_folder)
    
    output_folder.mkdir(exist_ok=True)
    
    # Find all PDF files
    pdf_files = list(pdf_folder.glob("*.pdf")) + list(pdf_folder.glob("*.PDF"))
    
    if not pdf_files:
        return 0, output_folder, ["No PDF files found in the selected folder"]
    
    converted_count = 0
    errors = []
    
    # Try different PDF libraries
    converter = _get_pdf_converter()
    
    if not converter:
        return 0, output_folder, ["No PDF library available. Please install: pip install PyPDF2 pdfplumber"]
    
    for pdf_file in pdf_files:
        try:
            # Extract text from PDF
            text = converter(pdf_file)
            
            if not text or len(text.strip()) < 10:
                errors.append(f"{pdf_file.name}: Could not extract text (file may be scanned/image-based)")
                continue
            
            # Save as text file
            txt_file = output_folder / f"{pdf_file.stem}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # Parse and save as JSON
            json_data = _parse_medical_text_to_json(text, pdf_file.stem)
            json_file = output_folder / f"{pdf_file.stem}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2)
            
            converted_count += 1
            
        except Exception as e:
            errors.append(f"{pdf_file.name}: {str(e)}")
    
    return converted_count, output_folder, errors


def _get_pdf_converter():
    """Get the best available PDF converter"""
    
    # Try pdfplumber first (best quality)
    try:
        import pdfplumber
        
        def convert_with_pdfplumber(pdf_path):
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            return text
        
        return convert_with_pdfplumber
    except ImportError:
        pass
    
    # Try PyPDF2 as fallback
    try:
        from PyPDF2 import PdfReader
        
        def convert_with_pypdf2(pdf_path):
            text = ""
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            return text
        
        return convert_with_pypdf2
    except ImportError:
        pass
    
    return None


def _parse_medical_text_to_json(text, filename):
    """
    Parse medical record text into JSON format
    This is a basic parser - can be enhanced based on specific formats
    """
    
    # Basic structure
    json_data = {
        "source_file": filename,
        "raw_text": text,
        "tests": [],
        "metadata": {
            "conversion_method": "automated_pdf_extraction"
        }
    }
    
    # Try to extract test results (basic pattern matching)
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # Look for patterns like "Test Name: Value Unit Range"
        # This is a simple parser - enhance based on your PDF formats
        
        # Common lab test patterns
        if any(keyword in line.lower() for keyword in ['glucose', 'cholesterol', 'hemoglobin', 'wbc', 'rbc']):
            # Try to parse test information
            test_entry = {
                "Test": line,
                "Value": "",
                "Unit": "",
                "Reference Range": "",
                "Status": "",
                "Date": "",
                "raw_line": line
            }
            json_data["tests"].append(test_entry)
    
    return json_data


def install_pdf_library():
    """
    Install PDF processing library
    Returns True if successful
    """
    import subprocess
    import sys
    
    try:
        # Try to install pdfplumber (recommended)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber", "--quiet"])
        return True
    except:
        try:
            # Fallback to PyPDF2
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2", "--quiet"])
            return True
        except:
            return False


def check_pdf_support():
    """Check if PDF conversion is supported"""
    try:
        import pdfplumber
        return True, "pdfplumber"
    except ImportError:
        pass
    
    try:
        from PyPDF2 import PdfReader
        return True, "PyPDF2"
    except ImportError:
        pass
    
    return False, None