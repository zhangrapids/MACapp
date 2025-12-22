"""
loader.py - Load and parse JSON test result files
"""
import os
import json
from parsers import parse_labcorp_tests, parse_kaiser_tests
from medical_parsers import parse_all_medical_records
from normalizer import normalize_name

def load_all_tests(results_folder, debug_mode=False):
    """Load and parse all JSON files from the results folder"""
    all_results = {}
    
    if not os.path.exists(results_folder):
        print(f"ERROR: Folder '{results_folder}' not found!")
        return all_results
    
    json_files = [f for f in os.listdir(results_folder) if f.lower().endswith('.json')]
    
    if not json_files:
        print(f"ERROR: No JSON files found in '{results_folder}'")
        return all_results
    
    print(f"Loading {len(json_files)} file(s)...\n")
    
    for fname in json_files:
        try:
            with open(os.path.join(results_folder, fname), 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Try both 'full_text' and 'raw_text' keys
                text = data.get('full_text', '') or data.get('raw_text', '')
            
            if not text:
                print(f"⚠ {fname}: No text content found (missing 'full_text' or 'raw_text' key)")
                continue
            
            # Detect format and parse
            file_results = {}
            record_types = []
            
            # Check if it's LabCorp format
            if 'Laboratory Corporation of America' in text or 'LabCorp' in text or 'Date Collected:' in text:
                file_results = parse_labcorp_tests(text, debug_mode)
                if file_results:
                    record_types.append('Lab Tests')
            
            # Check if it's Kaiser format
            if 'Kaiser Permanente' in text or 'Final result' in text:
                # Parse lab tests
                lab_results = parse_kaiser_tests(text, debug_mode)
                file_results.update(lab_results)
                if lab_results:
                    record_types.append('Lab Tests')
                
                # Parse other medical records (vital signs, immunizations, etc.)
                medical_results = parse_all_medical_records(text)
                file_results.update(medical_results)
                if medical_results:
                    # Count types
                    types_found = set(r[0]['Type'] for r in medical_results.values() if r)
                    record_types.extend(types_found)
            
            if file_results:
                types_str = ', '.join(record_types) if record_types else 'Unknown'
                print(f"✓ {fname}: {len(file_results)} items ({types_str})")
                
                # Merge into all_results with normalization
                for test_name, entries in file_results.items():
                    # Don't normalize medical record types
                    if entries and entries[0].get('Type') in ['Vital Sign', 'Medication', 'Immunization', 'Problem', 'Procedure']:
                        normalized = test_name
                    else:
                        normalized = normalize_name(test_name)
                    
                    if normalized not in all_results:
                        all_results[normalized] = []
                    all_results[normalized].extend(entries)
                    if debug_mode:
                        print(f"  {test_name} -> {normalized}")
            else:
                print(f"⚠ {fname}: No records found")
                
        except Exception as e:
            print(f"✗ {fname}: Error - {e}")
            if debug_mode:
                import traceback
                traceback.print_exc()
    
    return all_results