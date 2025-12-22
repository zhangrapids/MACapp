"""
medical_parsers.py - Parse all types of medical records
Includes: vital signs, medications, immunizations, problems, procedures, imaging
"""
import re
from datetime import datetime

def parse_vital_signs(text):
    """Parse vital signs from Kaiser medical record"""
    results = {}
    
    vital_signs_section = re.search(r'Last Filed Vital Signs.*?(?=Results|Immunizations|$)', text, re.DOTALL)
    if not vital_signs_section:
        return results
    
    vital_text = vital_signs_section.group(0)
    
    # Blood Pressure
    bp_match = re.search(r'Blood Pressure\s+(\d+/\d+)\s+(\d{2}/\d{2}/\d{4})', vital_text)
    if bp_match:
        value, date = bp_match.groups()
        results['Blood Pressure'] = [{
            'Date': date,
            'Value': value,
            'Unit': 'mmHg',
            'Reference Range': '90-120/60-80',
            'Status': 'Normal',
            'Type': 'Vital Sign'
        }]
    
    # Pulse
    pulse_match = re.search(r'Pulse\s+(\d+)\s+(\d{2}/\d{2}/\d{4})', vital_text)
    if pulse_match:
        value, date = pulse_match.groups()
        results['Pulse'] = [{
            'Date': date,
            'Value': value,
            'Unit': 'bpm',
            'Reference Range': '60-100',
            'Status': 'Normal',
            'Type': 'Vital Sign'
        }]
    
    # Temperature
    temp_match = re.search(r'Temperature\s+([\d.]+)\s*°C\s*\(([\d.]+)\s*°F\)\s+(\d{2}/\d{2}/\d{4})', vital_text)
    if temp_match:
        temp_c, temp_f, date = temp_match.groups()
        results['Temperature'] = [{
            'Date': date,
            'Value': temp_f,
            'Unit': '°F',
            'Reference Range': '97.0-99.0',
            'Status': 'Normal',
            'Type': 'Vital Sign'
        }]
    
    # Weight
    weight_match = re.search(r'Weight\s+([\d.]+)\s*kg\s*\(([\d.]+)\s*lb.*?\)\s+(\d{2}/\d{2}/\d{4})', vital_text)
    if weight_match:
        weight_kg, weight_lb, date = weight_match.groups()
        results['Weight'] = [{
            'Date': date,
            'Value': weight_lb,
            'Unit': 'lb',
            'Reference Range': 'N/A',
            'Status': 'Normal',
            'Type': 'Vital Sign'
        }]
    
    # Height
    height_match = re.search(r'Height\s+([\d.]+)\s*cm\s*\(([\d\'\" .]+)\)\s+(\d{2}/\d{2}/\d{4})', vital_text)
    if height_match:
        height_cm, height_ft, date = height_match.groups()
        results['Height'] = [{
            'Date': date,
            'Value': height_cm,
            'Unit': 'cm',
            'Reference Range': 'N/A',
            'Status': 'Normal',
            'Type': 'Vital Sign'
        }]
    
    # BMI
    bmi_match = re.search(r'Body Mass Index\s+([\d.]+)\s+(\d{2}/\d{2}/\d{4})', vital_text)
    if bmi_match:
        value, date = bmi_match.groups()
        results['BMI'] = [{
            'Date': date,
            'Value': value,
            'Unit': '',
            'Reference Range': '18.5-24.9',
            'Status': 'Normal',
            'Type': 'Vital Sign'
        }]
    
    return results


def parse_medications(text):
    """Parse medications from Kaiser medical record"""
    results = {}
    
    # Active Medications (skip for now as they don't have dates/values)
    # Ended Medications
    ended_section = re.search(r'Ended Medications(.*?)(?=Active Problems|Immunizations|$)', text, re.DOTALL)
    if ended_section:
        med_text = ended_section.group(1)
        # Pattern: "MEDICATION_NAME (Started DATE) (Expired)"
        med_pattern = r'([A-Z][A-Za-z\s-]+(?:\([A-Z]+\))?)\s+.*?\(Started\s+(\d{1,2}/\d{1,2}/\d{4})\)'
        
        for match in re.finditer(med_pattern, med_text):
            med_name = match.group(1).strip()
            start_date = match.group(2)
            
            if 'Medications' not in results:
                results['Medications'] = []
            
            results['Medications'].append({
                'Date': start_date,
                'Value': med_name,
                'Unit': '',
                'Reference Range': '',
                'Status': 'Ended',
                'Type': 'Medication'
            })
    
    return results


def parse_immunizations(text):
    """Parse immunizations from Kaiser medical record"""
    results = {}
    
    imm_section = re.search(r'Immunizations(.*?)(?=Social History|$)', text, re.DOTALL)
    if not imm_section:
        return results
    
    imm_text = imm_section.group(1)
    
    # Pattern: "VACCINE_NAME (Given DATE, DATE, ...)"
    imm_pattern = r'([A-Z][A-Za-z0-9\s,()/-]+?)\s+\(Given\s+([\d/,\s]+)\)'
    
    for match in re.finditer(imm_pattern, imm_text):
        vaccine_name = match.group(1).strip()
        dates_str = match.group(2)
        
        # Parse multiple dates
        dates = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', dates_str)
        
        if 'Immunizations' not in results:
            results['Immunizations'] = []
        
        for date in dates:
            results['Immunizations'].append({
                'Date': date,
                'Value': vaccine_name,
                'Unit': '',
                'Reference Range': '',
                'Status': 'Completed',
                'Type': 'Immunization'
            })
    
    return results


def parse_problems(text):
    """Parse active and resolved problems"""
    results = {}
    
    # Active Problems
    active_section = re.search(r'Active Problems(.*?)(?=Resolved Problems|Immunizations|$)', text, re.DOTALL)
    if active_section:
        prob_text = active_section.group(1)
        # Pattern: "PROBLEM Noted_Date MM/DD/YYYY"
        prob_pattern = r'([A-Z][A-Z\s,()/-]+?)\s+(\d{2}/\d{2}/\d{4})'
        
        for match in re.finditer(prob_pattern, prob_text):
            problem_name = match.group(1).strip()
            noted_date = match.group(2)
            
            if 'Active Problems' not in results:
                results['Active Problems'] = []
            
            results['Active Problems'].append({
                'Date': noted_date,
                'Value': problem_name,
                'Unit': '',
                'Reference Range': '',
                'Status': 'Active',
                'Type': 'Problem'
            })
    
    # Resolved Problems
    resolved_section = re.search(r'Resolved Problems(.*?)(?=Immunizations|$)', text, re.DOTALL)
    if resolved_section:
        prob_text = resolved_section.group(1)
        prob_pattern = r'([A-Z][A-Z\s,()/-]+?)\s+(\d{2}/\d{2}/\d{4})\s+.*?(\d{2}/\d{2}/\d{4})'
        
        for match in re.finditer(prob_pattern, prob_text):
            problem_name = match.group(1).strip()
            noted_date = match.group(2)
            resolved_date = match.group(3)
            
            if 'Resolved Problems' not in results:
                results['Resolved Problems'] = []
            
            results['Resolved Problems'].append({
                'Date': resolved_date,
                'Value': f"{problem_name} (noted {noted_date})",
                'Unit': '',
                'Reference Range': '',
                'Status': 'Resolved',
                'Type': 'Problem'
            })
    
    return results


def parse_procedures(text):
    """Parse procedures and imaging studies with full narratives"""
    results = {}
    
    # Pattern 1: "PROCEDURE_NAME - Final result (DATE)"
    # More restrictive - stop at newline or specific delimiters
    procedure_patterns = [
        r'(COLONOSCOPY[^\n-]*?)\s*-\s*Final result\s*\((\d{2}/\d{2}/\d{4})',
        r'(ULTRASOUND[^\n-]*?)\s*-\s*Final result\s*\((\d{2}/\d{2}/\d{4})',
        r'(OPTICAL COHERENCE[^\n-]*?)\s*-\s*Final result\s*\((\d{2}/\d{2}/\d{4})',
        r'(FLUORO[^\n-]*?)\s*-\s*Final result\s*\((\d{2}/\d{2}/\d{4})',
        r'(XR [^\n-]*?)\s*-\s*Final result\s*\((\d{2}/\d{2}/\d{4})',
        r'(SARS-COV-2[^\n-]*?)\s*-\s*Final result\s*\((\d{2}/\d{2}/\d{4})'
    ]
    
    for pattern in procedure_patterns:
        for match in re.finditer(pattern, text):
            procedure_name = match.group(1).strip()
            procedure_date = match.group(2)
            
            # Clean up procedure name - remove extra spaces and newlines
            procedure_name = ' '.join(procedure_name.split())
            
            # Extract full narrative/report
            start_pos = match.end()
            next_section = text[start_pos:start_pos+3000]
            
            # Get impression
            impression = "See full report"
            impression_match = re.search(r'(?:IMPRESSION:|Impressions)(.*?)(?=\n\n|Narrative|Authorizing|Performing)', next_section, re.DOTALL)
            if impression_match:
                impression = impression_match.group(1).strip()[:500]
            
            # Get full narrative
            narrative = ""
            narrative_match = re.search(r'Narrative(.*?)(?=Authorizing Provider|Performing|$)', next_section, re.DOTALL)
            if narrative_match:
                narrative = narrative_match.group(1).strip()[:1000]
            
            # Store under specific procedure name, not generic "Procedures"
            if procedure_name not in results:
                results[procedure_name] = []
            
            full_report = impression
            if narrative:
                full_report = f"{impression}\n\nNarrative: {narrative}"
            
            results[procedure_name].append({
                'Date': procedure_date,
                'Value': procedure_name,
                'Unit': '',
                'Reference Range': '',
                'Status': full_report,
                'Type': 'Procedure'
            })
    
    # Pattern 2: "PROCEDURE_NAME (DATE)" - without "Final result"
    # Stop at opening parenthesis or newline
    procedure_patterns_alt = [
        r'(COLONOSCOPY[^\n(]*?)\s*\((\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}\s+[AP]M\s+[A-Z]+)\)',
        r'(OPTICAL COHERENCE[^\n(]*?)\s*\((\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}\s+[AP]M\s+[A-Z]+)\)'
    ]
    
    for pattern in procedure_patterns_alt:
        for match in re.finditer(pattern, text):
            procedure_name = match.group(1).strip()
            date_time_str = match.group(2)
            
            # Clean up procedure name
            procedure_name = ' '.join(procedure_name.split())
            
            # Extract just the date
            date_match = re.search(r'(\d{2}/\d{2}/\d{4})', date_time_str)
            if date_match:
                procedure_date = date_match.group(1)
            else:
                continue
            
            # Extract findings/impression/narrative
            start_pos = match.end()
            next_section = text[start_pos:start_pos+4000]
            
            # Get findings
            findings = ""
            findings_match = re.search(r'FINDINGS:(.*?)(?=COMPLICATIONS:|IMPRESSION:|Narrative|Authorizing|$)', next_section, re.DOTALL)
            if findings_match:
                findings = findings_match.group(1).strip()[:800]
            
            # Get impression
            impression = ""
            impression_match = re.search(r'IMPRESSION:(.*?)(?=RECOMMENDATIONS:|Narrative|Authorizing|$)', next_section, re.DOTALL)
            if impression_match:
                impression = impression_match.group(1).strip()[:500]
            
            # Get recommendations
            recommendations = ""
            rec_match = re.search(r'RECOMMENDATIONS:(.*?)(?=Narrative|Authorizing|$)', next_section, re.DOTALL)
            if rec_match:
                recommendations = rec_match.group(1).strip()[:300]
            
            # Store under specific procedure name
            if procedure_name not in results:
                results[procedure_name] = []
            
            # Build full report
            full_report = []
            if findings:
                full_report.append(f"Findings: {findings}")
            if impression:
                full_report.append(f"Impression: {impression}")
            if recommendations:
                full_report.append(f"Recommendations: {recommendations}")
            
            report_text = "\n\n".join(full_report) if full_report else "See full report"
            
            results[procedure_name].append({
                'Date': procedure_date,
                'Value': procedure_name,
                'Unit': '',
                'Reference Range': '',
                'Status': report_text,
                'Type': 'Procedure'
            })
    
    return results


def parse_clinical_notes(text):
    """Parse clinical notes and procedure narratives"""
    results = {}
    
    # Look for procedure notes with detailed narratives
    note_pattern = r'Procedure Note\s+(.*?)\s+Procedure Note(.*?)(?=Authorizing Provider|Performing|$)'
    
    for match in re.finditer(note_pattern, text, re.DOTALL):
        provider_info = match.group(1).strip()
        note_content = match.group(2).strip()
        
        # Extract date from note
        date_match = re.search(r'(\d{2}/\d{2}/\d{4})', provider_info)
        if date_match:
            note_date = date_match.group(1)
            
            # Extract provider name
            provider_match = re.search(r'([A-Z][A-Z\s]+(?:MD|DO|PA))', provider_info)
            provider = provider_match.group(1) if provider_match else "Provider"
            
            if 'Clinical Notes' not in results:
                results['Clinical Notes'] = []
            
            # Clean up note content
            note_summary = note_content[:500] + "..." if len(note_content) > 500 else note_content
            
            results['Clinical Notes'].append({
                'Date': note_date,
                'Value': f"{provider} - Clinical Note",
                'Unit': '',
                'Reference Range': '',
                'Status': note_summary,
                'Type': 'Clinical Note'
            })
    
    return results


def parse_all_medical_records(text):
    """Parse all types of medical records from text"""
    all_results = {}
    
    # Parse each type
    vital_signs = parse_vital_signs(text)
    medications = parse_medications(text)
    immunizations = parse_immunizations(text)
    problems = parse_problems(text)
    procedures = parse_procedures(text)
    clinical_notes = parse_clinical_notes(text)
    
    # Merge all results
    all_results.update(vital_signs)
    all_results.update(medications)
    all_results.update(immunizations)
    all_results.update(problems)
    all_results.update(procedures)
    all_results.update(clinical_notes)
    
    return all_results