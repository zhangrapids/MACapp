"""
parsers.py - Lab report parsers for different formats
"""
import re

def parse_labcorp_tests(text, debug_mode=False):
    """Parse LabCorp test format"""
    results = {}
    
    # Find test date
    date_match = re.search(r'Date Collected:\s*(\d{1,2}/\d{1,2}/\d{4})', text)
    if not date_match:
        date_match = re.search(r'Collected:\s*(\d{2}/\d{2}/\d{4})', text)
    
    if not date_match:
        if debug_mode:
            print("    [DEBUG] No date found in LabCorp format")
        return results
    
    test_date = date_match.group(1)
    
    # Parse test result lines
    # Format 1 (with previous): "WBC 01 3.9 3.2 10/18/2024 x10E3/uL 3.4-10.8"
    # Format 2 (no previous):   "Glucose 01 100 High mg/dL 70-99"
    
    lines = text.split('\n')
    test_count = 0
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and headers
        if not line or 'Current Result' in line or 'Reference Interval' in line:
            continue
        
        # Try matching with previous result first
        match = re.match(
            r'^([A-Za-z][A-Za-z\s,()/-]+?)\s+01\s+([\d.<>]+)\s+(?:(Low|High|Critical)\s+)?([\d.<>]+)?\s+(\d{1,2}/\d{1,2}/\d{4})?\s+([a-zA-Z0-9/*%]+)?\s+([\d.<>-]+)?',
            line
        )
        
        # If no match, try simpler pattern without previous result
        if not match:
            match = re.match(
                r'^([A-Za-z][A-Za-z\s,()/-]+?)\s+01\s+([\d.<>]+)\s+(?:(Low|High|Critical)\s+)?([a-zA-Z0-9/*%]+)?\s+([\d.<>-]+)?',
                line
            )
            
            if match:
                test_name = match.group(1).strip()
                value = match.group(2).strip()
                flag = match.group(3) if match.group(3) else None
                unit = match.group(4).strip() if match.group(4) else ''
                ref_range = match.group(5).strip() if match.group(5) else ''
        else:
            test_name = match.group(1).strip()
            value = match.group(2).strip()
            flag = match.group(3) if match.group(3) else None
            unit = match.group(6).strip() if match.group(6) else ''
            ref_range = match.group(7).strip() if match.group(7) else ''
        
        if match:
            # Determine status
            status = _determine_status(value, ref_range, flag)
            
            if test_name not in results:
                results[test_name] = []
            
            results[test_name].append({
                'Date': test_date,
                'Value': value,
                'Unit': unit,
                'Reference Range': ref_range,
                'Status': status
            })
            test_count += 1
    
    if debug_mode and test_count > 0:
        print(f"    [DEBUG] Parsed {test_count} test results")
    
    return results


def parse_kaiser_tests(text, debug_mode=False):
    """Parse Kaiser lab test format"""
    results = {}
    
    # Pattern: "TEST PANEL - Final result (DATE)"
    panel_pattern = r'([A-Z][A-Z\s,()/-]+?)\s*-\s*Final result\s*\((\d{2}/\d{2}/\d{4})'
    
    for panel_match in re.finditer(panel_pattern, text):
        test_date = panel_match.group(2)
        start_pos = panel_match.end()
        
        # Extract table content after the header
        next_section = text[start_pos:start_pos+4000]
        
        # Find component lines: "TEST_NAME VALUE REF_RANGE UNIT"
        for line in next_section.split('\n'):
            line = line.strip()
            
            # Skip headers and empty lines
            if not line or 'Component' in line or 'Analysis' in line or 'Test Method' in line:
                continue
            
            # Stop at next panel or section
            if 'Final result' in line or 'Specimen' in line or 'Comment:' in line:
                break
            
            # Match: "WBC'S AUTO 4.2 3.5 - 11.0 10*3/uL"
            match = re.match(
                r'^([A-Z][A-Z\s,()\'/-]+?)\s+([\d.]+)\s+([\d.\s-]+)\s*([a-zA-Z0-9/*%]+)?',
                line
            )
            
            if match:
                test_name = match.group(1).strip()
                value = match.group(2).strip()
                ref_range = match.group(3).strip()
                unit = match.group(4).strip() if match.group(4) else ''
                
                # Determine status
                status = _determine_status(value, ref_range)
                
                if test_name not in results:
                    results[test_name] = []
                
                results[test_name].append({
                    'Date': test_date,
                    'Value': value,
                    'Unit': unit,
                    'Reference Range': ref_range,
                    'Status': status
                })
    
    return results


def _determine_status(value, ref_range, flag=None):
    """Determine if test result is normal, low, or high"""
    status = 'Normal'
    
    # Check flag first
    if flag:
        if flag == 'Low':
            return 'Low'
        elif flag == 'High':
            return 'High'
        elif flag == 'Critical':
            return 'Critical'
    
    # Check against reference range
    if ref_range and value:
        try:
            val = float(value.replace('<', '').replace('>', ''))
            if '-' in ref_range:
                parts = ref_range.split('-')
                if len(parts) == 2:
                    low = float(parts[0].strip().replace('<', '').replace('>', ''))
                    high = float(parts[1].strip().replace('<', '').replace('>', ''))
                    if val < low:
                        status = 'Low'
                    elif val > high:
                        status = 'High'
            elif '>' in ref_range:
                threshold = float(ref_range.replace('>', '').strip())
                if val <= threshold:
                    status = 'Low'
        except:
            pass
    
    return status